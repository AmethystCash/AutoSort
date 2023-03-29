import requests

# v2, simplified, hopefully it works just as well as v1

def get_barcode_info(barcode):
    url = f"https://off:off@ie.openfoodfacts.org/api/v2/product/{barcode}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        packaging_info = data['product'].get('packaging')
        packagings_info = data['product'].get('packagings')
        return (packaging_info, packagings_info)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return None