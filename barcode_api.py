import requests

# function for getting barcode info from a barcode number

def error_thing(response):
    print(f"Status code: {response.status_code}")
    try:
        print(f"{response.json()['status_verbose']}")
    except:
        pass


def print_barcode_info(barcode):
    url = f"https://off:off@ie.openfoodfacts.org/api/v2/product/{barcode}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                packaging_info = data['product'].get('packaging')
                packagings_info = data['product'].get('packagings')
                print(packaging_info)
                print(packagings_info)
            except:
                error_thing(response)
        else:
            error_thing(response)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
