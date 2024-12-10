from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
from datetime import datetime, timedelta, timezone


def save_key_and_cert(directory, filename, private_key, cert=None):
    """Save private key and certificate to files."""
    os.makedirs(directory, exist_ok=True)

    # Save private key
    with open(os.path.join(directory, f"{filename}.key"), "wb") as key_file:
        key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Save certificate if provided
    if cert:
        with open(os.path.join(directory, f"{filename}.crt"), "wb") as cert_file:
            cert_file.write(cert.public_bytes(serialization.Encoding.PEM))


def create_ca():
    """Creates a CA private key and self-signed certificate."""
    print("Creating CA private key and self-signed certificate...")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)

    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Organization"),
            x509.NameAttribute(NameOID.COMMON_NAME, "RootCA"),
        ]
    )

    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=3650))  # 10 years
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(private_key, hashes.SHA256())
    )

    save_key_and_cert("ca", "ca", private_key, certificate)


def issue_user_key_and_cert(username):
    """Issue a private key and certificate for a user."""
    print(f"Issuing private key and certificate for user: {username}...")
    
    user_dir = f"users/{username}"
    os.makedirs(user_dir, exist_ok=True)
    
    # Generate user's private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key_path = os.path.join(user_dir, f"{username}.key")
    with open(private_key_path, "wb") as key_file:
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Create CSR for the user
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Organization"),
        x509.NameAttribute(NameOID.COMMON_NAME, username),
    ])
    csr = x509.CertificateSigningRequestBuilder().subject_name(subject).sign(private_key, hashes.SHA256())
    
    # Load CA private key and certificate
    with open("ca/ca.key", "rb") as key_file:
        ca_private_key = serialization.load_pem_private_key(key_file.read(), password=None)
    with open("ca/ca.crt", "rb") as cert_file:
        ca_cert = x509.load_pem_x509_certificate(cert_file.read())
    
    # Create user certificate
    user_cert = x509.CertificateBuilder() \
        .subject_name(csr.subject) \
        .issuer_name(ca_cert.subject) \
        .public_key(csr.public_key()) \
        .serial_number(x509.random_serial_number()) \
        .not_valid_before(datetime.now(timezone.utc)) \
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=365)) \
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True) \
        .sign(private_key=ca_private_key, algorithm=hashes.SHA256())
    
    # Save user's certificate
    user_cert_path = os.path.join(user_dir, f"{username}.crt")
    with open(user_cert_path, "wb") as cert_file:
        cert_file.write(user_cert.public_bytes(serialization.Encoding.PEM))
    
    print(f"User certificate issued and saved to {user_cert_path}.")


def revoke_user_cert(username):
    """Revoke a user's certificate and update the CRL."""
    print(f"Revoking certificate for user: {username}...")
    
    # Load CA private key and certificate
    with open("ca/ca.key", "rb") as key_file:
        ca_private_key = serialization.load_pem_private_key(key_file.read(), password=None)
    with open("ca/ca.crt", "rb") as cert_file:
        ca_cert = x509.load_pem_x509_certificate(cert_file.read())
    
    # Load the user's certificate
    user_cert_path = f"users/{username}/{username}.crt"
    if not os.path.exists(user_cert_path):
        print(f"Error: Certificate for user '{username}' does not exist.")
        return
    
    with open(user_cert_path, "rb") as user_cert_file:
        user_cert = x509.load_pem_x509_certificate(user_cert_file.read())

    # Create or update the CRL
    crl_path = "ca/crl/crl.pem"
    if os.path.exists(crl_path):
        # Load existing CRL
        with open(crl_path, "rb") as crl_file:
            crl = x509.load_pem_x509_crl(crl_file.read())
    else:
        # Create a new CRL
        crl = x509.CertificateRevocationListBuilder()
        crl = crl.issuer_name(ca_cert.subject)
        crl = crl.last_update(datetime.now(timezone.utc))
        crl = crl.next_update(datetime.now(timezone.utc) + timedelta(days=7))  # CRL valid for 7 days

    # Add the revoked certificate
    crl = crl.add_revoked_certificate(
        x509.RevokedCertificateBuilder()
        .serial_number(user_cert.serial_number)
        .revocation_date(datetime.now(timezone.utc))
        .build()
    )

    # Sign and save the updated CRL
    crl = crl.sign(private_key=ca_private_key, algorithm=hashes.SHA256())
    os.makedirs("ca/crl", exist_ok=True)
    with open(crl_path, "wb") as crl_file:
        crl_file.write(crl.public_bytes(serialization.Encoding.PEM))
    
    print(f"Certificate for user '{username}' revoked and CRL updated.")



if __name__ == "__main__":
    print("=== Internal PKI Setup ===")
    if not os.path.exists("ca/ca.key"):
        create_ca()

    while True:
        print("\nOptions:")
        print("1. Issue a user key and certificate")
        print("2. Revoke a user certificate")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            user = input("Enter username: ")
            issue_user_key_and_cert(user)
        elif choice == "2":
            user = input("Enter username to revoke: ")
            revoke_user_cert(user)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")
