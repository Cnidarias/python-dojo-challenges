import json
import time
import requests
from bs4 import BeautifulSoup


def get_listings(location='london', property_type='houses', page=1):
    url = f"https://www.zoopla.co.uk/for-sale/houses/{location}/?identifier={location}&property_type={property_type}&search_source=home&radius=0&pn={page}"
    requests_result = requests.get(url)
    if requests_result.status_code != 200:
        raise RuntimeError("Could not successfully fetch", url)
    content = requests_result.text
    soup = BeautifulSoup(content, 'html.parser')
    container_listings = soup.select('#content > ul > li')
    results = []
    for listing in container_listings:
        text_price_element = listing.select('.text-price')
        if len(text_price_element) < 1:
            continue
        price_string = ''.join(c for c in text_price_element[0].get_text() if c.isdigit())
        if len(price_string) <= 0:
            continue
        price = int(price_string)
        results.append({"price": price})
    return results


if __name__ == '__main__':
    all_results = []
    max_page = 10
    for i in range(1, max_page, 1):
        page_result = get_listings(page=i)
        all_results.extend(page_result)
        print(f"{i}/{max_page - 1}")
        # wait some time so we don't hammer the server with requests!
        time.sleep(1)

    with open("result.json", "w") as f:
        json.dump(all_results, f, indent=4)
