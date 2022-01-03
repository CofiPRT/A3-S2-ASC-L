"""
Module to load recipes from a set of files
"""

import os
from typing import Iterable, Dict

RECIPES_FOLDER = "recipes"
ASSUMED_EXTENSION = ".txt"

PRODUCT = str
RESOURCE = str
QUANTITY = int
MESSAGE = str


def print_import_failure(product, info=None):
    """
    Notify the user about an import failure, along with optional info
    """
    message = "Could not import product '%s'" % product

    if info is not None:
        message += ": " + info

    print(message)


def to_ingredient(line):
    """
    Splits a line into a resource and its quantity, as found in the recipe files
    """
    details = line.split("=")
    return details[0], int(details[1])


def load(products: Iterable[PRODUCT]) -> Dict[PRODUCT, Dict[RESOURCE, QUANTITY]]:
    """
    Loads and returns the recipes for the given products
    """
    result = {}

    for product in products:
        # make sure the file exists
        file_name = os.path.join(RECIPES_FOLDER, product + ASSUMED_EXTENSION)

        if not os.path.exists(file_name):
            print_import_failure(product, "File '%s' not found!" % file_name)
            continue

        # attempt to open the file
        try:
            input_file = open(file_name, "r")
        except OSError:
            print_import_failure(product, "File '%s' could not be opened!" % file_name)
            continue

        # make sure the product ID corresponds to the file name
        product_id = input_file.readline().strip()

        if product_id != product:
            message = "File '%s' contains invalid product ID '%s'" % (file_name, product_id)
            print_import_failure(product, message)
            continue

        # add a new recipe
        result[product] = dict(to_ingredient(line) for line in input_file)

        print("Successfully imported product '%s'" % product)

    return result
