import tkinter as tk
from tkinter import messagebox, scrolledtext
import random

# Tabelele utilizate în DES
PC_1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC_2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def permute(key, table):
    return ''.join(key[i - 1] for i in table)

def left_shift(key_half, shifts):
    return key_half[shifts:] + key_half[:shifts]

def generate_round_key(K, round_number):
    """Generează cheia de rundă pentru o rundă dată."""
    result_steps = []

    # Pas 1: Permutarea PC-1
    permuted_key = permute(K, PC_1)
    result_steps.append(f"Cheia după PC-1: {permuted_key}")
    
    # Pas 2: Împărțirea în două jumătăți
    C, D = permuted_key[:28], permuted_key[28:]
    result_steps.append(f"C0: {C}, D0: {D}")
    
    # Pas 3: Shiftare ciclică pentru runda curentă
    for i in range(round_number):
        shifts = SHIFT_TABLE[i]
        C, D = left_shift(C, shifts), left_shift(D, shifts)
        result_steps.append(f"Shiftare rundă {i + 1}: C = {C}, D = {D}")
    
    # Pas 4: Permutarea PC-2 pentru cheia de rundă
    combined_key = C + D
    round_key = permute(combined_key, PC_2)
    result_steps.append(f"Cheia de rundă K{round_number}: {round_key}")
    return round_key, result_steps

# Funcția pentru GUI
def calculate_key():
    try:
        K = key_entry.get().strip()
        if len(K) != 64 or not all(c in '01' for c in K):
            messagebox.showerror("Eroare", "Cheia trebuie să aibă 64 de biți în format binar.")
            return

        round_number = int(round_entry.get())
        if round_number < 1 or round_number > 16:
            messagebox.showerror("Eroare", "Numărul rundei trebuie să fie între 1 și 16.")
            return

        round_key, steps = generate_round_key(K, round_number)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "\n".join(steps) + f"\n\nCheia de rundă finală (K{round_number}): {round_key}")
    except ValueError:
        messagebox.showerror("Eroare", "Introduceți o rundă validă (număr între 1 și 16).")

def generate_random_key():
    random_key = ''.join(random.choice('01') for _ in range(64))
    key_entry.delete(0, tk.END)
    key_entry.insert(0, random_key)

# Crearea ferestrei principale
root = tk.Tk()
root.title("Algoritm DES: Generare Cheie de Rundă")
root.geometry("600x500")

# Elemente GUI
tk.Label(root, text="Cheia inițială (64 biți în format binar):").pack(pady=5)
key_entry = tk.Entry(root, width=64)
key_entry.pack(pady=5)

tk.Button(root, text="Generează cheie aleatorie", command=generate_random_key).pack(pady=5)

tk.Label(root, text="Numărul rundei (1-16):").pack(pady=5)
round_entry = tk.Entry(root, width=5)
round_entry.pack(pady=5)

tk.Button(root, text="Calculează cheia de rundă", command=calculate_key).pack(pady=10)

result_text = scrolledtext.ScrolledText(root, width=70, height=20)
result_text.pack(pady=10)

# Start GUI
root.mainloop()
