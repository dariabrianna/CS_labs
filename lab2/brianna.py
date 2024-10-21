import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

def scrape_products():
    try:
        response = requests.get('https://999.md/ro/list/transport/cars') ## GET REQUEST-UL
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser') ## HTML PARSER-UL

        products = []
        total_euro = 0
        total_mdl = 0

        product_elements = soup.find_all('li', class_='ads-list-photo-item', limit=10)  

        for product in product_elements:
            name = product.find('div', class_='ads-list-photo-item-title').get_text(strip=True) # Extragerea datelor automobilelor
            relative_url = product.find('a', class_='js-item-ad')['href']
            price_text = product.find('span', class_='ads-list-photo-item-price-wrapper').get_text(strip=True)

            # Construct the full URL for each product page
            full_url = f"https://999.md{relative_url}"

            # Verifica daca  price text is "Negociabil"
            if "Negociabil" in price_text:
                print(f'Skipping product "{name}" because the price is negotiable.')
                continue  # Skip this product

            price_cleaned = price_text.replace('€', '').replace('\xa0', '').replace(' ', '')

            if price_cleaned:
                price_euros = float(price_cleaned)

                # Filter out products based on price
                if 10000 <= price_euros <= 20000:
                    price_mdl = price_euros * 18.9

                    # Add to total sum
                    total_euro += price_euros
                    total_mdl += price_mdl

                    # Get current UTC timestamp
                    timestamp_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

                    product_response = requests.get(full_url)
                    product_soup = BeautifulSoup(product_response.text, 'html.parser')

                    # Extract the views information
                    views_div = product_soup.find('div', class_='adPage__aside__stats__views not-marketplace')
                    views = views_div.get_text(strip=True) if views_div else 'No views info'

                    products.append({
                        'name': name,
                        'url': full_url,
                        'price_euros': price_text.strip().replace('\xa0', '').replace(' ', ''),  
                        'price_mdl': round(price_mdl, 0),  
                        'timestamp': timestamp_utc,  # UTC timestamp
                        'views': views  # Views information from the product page
                    })

        products.append({
            'Sum_euro': round(total_euro, 2), 
            'Sum_mdl': round(total_mdl, 2)    
        })
        print(products, len(products))

    except requests.exceptions.RequestException as e:
        print('Error:', e)

scrape_products()
