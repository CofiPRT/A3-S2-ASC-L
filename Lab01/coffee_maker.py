"""
A command-line controlled coffee maker.
"""

import load_recipes

MODEL_NAME = "M1939-52K"

# Commands
EXIT = "exit"
LIST_COFFEES = "list"
MAKE_COFFEE = "make"
HELP = "help"
REFILL = "refill"
RESOURCE_STATUS = "status"
COMMANDS = {EXIT, LIST_COFFEES, MAKE_COFFEE, REFILL, RESOURCE_STATUS, HELP}


# Coffee types
ESPRESSO = "espresso"
AMERICANO = "americano"
CAPPUCCINO = "cappuccino"
RECIPES = load_recipes.load({ESPRESSO, AMERICANO, CAPPUCCINO})

# Resources
WATER = "water"
COFFEE = "coffee"
MILK = "milk"
RESOURCES = {WATER: 100, COFFEE: 100, MILK: 100}


def print_robot(message):
    """
    "print" function wrapper which prefixes the model's name to the message
    """
    print("[%s] %s" % (MODEL_NAME, message))


def input_robot(message):
    """
    "input" function which prefixes the model's name to the message
    """
    return input("[%s - INPUT] %s" % (MODEL_NAME, message))


def print_welcome_message():
    """
    Print a message to greet the user
    """
    print_robot("I am the advanced %s coffee maker!" % MODEL_NAME)


def print_help_suggestion():
    """
    Suggest the "help" function to the user
    """
    print_robot("For a list of commands, type '" + HELP + "'")


def print_goodbye_message():
    """
    Farewell to the user
    """
    print_robot("Thank you for using the advanced %s coffee maker. Goodbye!" % MODEL_NAME)


def exit_delegate():
    """
    Delegate for the "exit" command
    """
    print_robot("Exit command issued")


def list_coffees_delegate():
    """
    Delegate for the "list" command
    """
    print_robot("Available products: " + ", ".join(RECIPES.keys()))


def make_coffee_delegate():
    """
    Delegate for the "make" command
    """
    product = input_robot("Please select a product: ")

    # make sure this product is on the menu
    if product not in RECIPES.keys():
        print_robot("%s is not a valid product!" % product)
        list_coffees_delegate()
        return

    # make sure we have all the ingredients
    for resource, quantity in RECIPES[product].items():
        if resource not in RESOURCES.keys():
            message = "%s needs %s. We don't even use %s. Contact the administrator!"
            print_robot(message % (product, resource, resource))
            return

        if RESOURCES[resource] < quantity:
            message = "Insufficient %s. Current: %d, Required: %d"
            print_robot(message % (resource, RESOURCES[resource], quantity))
            return

    # we have all the ingredients, consume them
    for resource, quantity in RECIPES[product].items():
        RESOURCES[resource] = RESOURCES[resource] - quantity

    print_robot("Beep-boop! Here's your %s. Enjoy!" % product)


def refill_delegate():
    """
    Delegate for the "refill" command
    """
    message = "PLease select the resource to refill. Type 'all' to refill everything: "
    resource = input_robot(message)

    # make sure the resource is valid
    if resource not in RESOURCES.keys() and resource != "all":
        print_robot("%s is not a valid resource!" % resource)
        return

    # according to user input, choose the resources to be replenished
    resources_to_refill = RESOURCES.keys() if resource == "all" else {resource}

    for resource in resources_to_refill:
        RESOURCES[resource] = 100

    message = "Vrrrr! The following resources have been replenished: "
    message += ", ".join(resources_to_refill)
    print_robot(message)


def resource_status_delegate():
    """
    Delegate for the "status" command
    """
    print_robot("Available resources:")

    # simply iterate over the current available resources
    for resource, quantity in RESOURCES.items():
        print_robot("\t%s: %s" % (resource, quantity))


def help_delegate():
    """
    Delegate for the "help" command
    """
    print_robot("List of available commands: " + ", ".join(COMMANDS))


COMMAND_DELEGATES = {
    EXIT: exit_delegate,
    LIST_COFFEES: list_coffees_delegate,
    MAKE_COFFEE: make_coffee_delegate,
    REFILL: refill_delegate,
    RESOURCE_STATUS: resource_status_delegate,
    HELP: help_delegate
}


def main():
    """
    Main function to execute when this module is directly called
    """
    print_welcome_message()
    print_help_suggestion()

    while True:
        command = input_robot("Command: ")

        if command not in COMMANDS:
            print_robot("%s is not a valid command!" % command)
            help_delegate()
            continue

        # call the command's delegate
        COMMAND_DELEGATES[command]()

        if command == EXIT:
            break

    print_goodbye_message()


if __name__ == "__main__":
    main()
