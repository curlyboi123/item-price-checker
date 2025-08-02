import requests


def get_item_price(url: str):
    """Return the price of an item on a website"""
    print(url)
    r = requests.get(url)
    print(r.status_code)
    content = r.text
    return content


def main():
    base_url = "https://ukstore.hermanmiller.com/products"
    chair_name = "aeron-graphite-standard-office-chair"
    chair_variant = "42502223036569" # Herman Miller Aeron - Medium - Fully Leather Adjustable

    url = f"{base_url}/{chair_name}?variant={chair_variant}"

    response = get_item_price(url)
    print(response)
    print(type(response))

    x = response.find("Add to Basket")
    print(x)


if __name__ == "__main__":
    main()
