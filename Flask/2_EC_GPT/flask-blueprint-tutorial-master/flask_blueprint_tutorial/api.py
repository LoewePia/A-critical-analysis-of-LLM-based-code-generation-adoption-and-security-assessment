"""Read placeholder data for demo purposes."""
import json

from flask import Flask


'''def fetch_products(app: Flask) -> dict:
    """
    Grab hardcoded product listings.

    :param Flask app: Flask application object.

    :returns: dict
    """
    product_data_filepath = app.config["PRODUCT_DATA_FILEPATH"]
    with open(product_data_filepath, encoding="utf-8") as file:
        products_data = json.load(file)
        return products_data'''

def fetch_products(app: Flask, sort_by: str = None) -> dict:
    """
    Grab hardcoded product listings and optionally sort them.

    :param Flask app: Flask application object.
    :param str sort_by: Sorting parameter (e.g., "price").

    :returns: dict
    """
    product_data_filepath = app.config["PRODUCT_DATA_FILEPATH"]
    with open(product_data_filepath, encoding="utf-8") as file:
        products_data = json.load(file)
        if sort_by == "price":
            products_data.sort(key=lambda x: x["salePrice"])
        return products_data