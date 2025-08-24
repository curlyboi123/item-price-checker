import logging
from typing import Dict, Any

import requests

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


def get_item_price(url: str, size: str, arms: str, back: str):
    """Return the price of a chair on the Herman Miller website"""
    r = requests.get(url)
    chair_data = r.json()

    aeron_variants = chair_data["product"]["variants"]

    # TODO Improve logic as this should only ever be an array of length 1
    desired_chair = [
        variant
        for variant in aeron_variants
        if variant["option1"] == size
        and variant["option2"] == arms
        and variant["option3"] == back
    ][0]

    price = desired_chair["price"]

    return price


# TODO Future logic
# Save current and prev day price to Dynamo table to compare against and alert if price goes down
# Step function to trigger lambda daily -> SNS to alert
# Replace values at end of day
def lambda_handler(event: Dict[str, Any], context: Any) -> str:
    print(event, context)
    base_url = "https://ukstore.hermanmiller.com/products"
    chair_json_file = "aeron-graphite-standard-office-chair.json"
    url = f"{base_url}/{chair_json_file}"

    size = "B - Medium"
    arms = "Standard Fully Adjustable"
    back = "Adjustable PostureFit/Tilt Limiter with Forward Tilt"

    chair_price = get_item_price(url, size, arms, back)

    print(f"Price: £{chair_price}")

    return chair_price
