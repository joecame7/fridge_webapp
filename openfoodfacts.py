import requests
import json

def lookup_barcode(barcode):
    url = f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            product = data['product']
            if data['status'] == 1:
                product_info = {
                    'Product Name': product.get('product_name', 'unknown'),
                    'Brand': product.get('brands', 'unknown'),
                    'Quantity': product.get('quantity', 'unknown'),
                    'Ingredients': product.get('ingredients_text', 'unknown'),
                    'Allergens': product.get('allergens_tags', 'unknown'),
                    'Nutriments': product.get('nutriments', 'unknown'),
                    'Categories': product.get('categories_tags', 'unknown'),
                    'Labels': product.get('labels_tags', 'unknown'),
                    'Image URL': product.get('image_url', 'unknown')
                }
                

                for key, value in product_info.items():
                    #print(f"{key}: {value}")
                    pass
                
                return product_info
                
    except Exception as E:
        pass

if __name__ == '__main__':
    barcode = 5060517883560
    print(lookup_barcode(barcode))

