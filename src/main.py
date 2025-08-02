import re
import sys
import logging
from urllib.request import urlopen


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def get_item_price(url: str):
    """Return the price of an item on a website"""
    logger.info(f"Searching for item price on page: {url}")
    page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    return html


# TODO Refactor to query json https://ukstore.hermanmiller.com/products/aeron-graphite-standard-office-chair.json and extract details
# TODO Future logic
# Save current and prev day price to Dynamo table to compare against and alert if price goes down
# Step function to trigger lambda daily -> SNS to alert
# Replace values at end of day
def main():
    base_url = "https://ukstore.hermanmiller.com/products"

    chair_variants = [
        {
            "model": "aeron",
            "size": "medium",
            "arms": "standard_fully_adjustable",
            "back_support": "fixed_posturefit",
            "chair_id": "42502223036569"
        }
    ]

    chair_name = "aeron-graphite-standard-office-chair"
    model = "aeron"
    size = "medium"
    arms = "standard_fully_adjustable"
    back_support = "fixed_posturefit"

    matches = [chair for chair in chair_variants if
               chair["model"] == model and
               chair["size"] == size and
               chair["arms"] == arms and
               chair["back_support"] == back_support
    ]
    if matches:
        chair_variant = matches[0]["chair_id"]
    else:
        logger.critical("No ID found for chair details selected. Please try different values.")
        sys.exit()

    url = f"{base_url}/{chair_name}?variant={chair_variant}"

    response = get_item_price(url)


    # TODO Seperate this logic into own function
    # Search entire HTML content for section with price
    # Within this section grab exact part with price
    # Convert price into GBP
    # TODO Add error handling for not finding text in HTML
    start_index = response.find("<span id=\"addToCartText\">")
    end_index = start_index + response[start_index:].find("</span>")
    price_section = response[start_index:end_index]

    pattern = r'data-total-price="(\d+)"'

    match = re.search(pattern, price_section)
    if match:
        price = match.group(1)  # This returns just the number
    else:
        logger.critical("Item price not found.")
        sys.exit()


    gbp_price = int(price) / 100
    print(f"£{gbp_price}")


if __name__ == "__main__":
    main()
