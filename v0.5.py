'''
Created on Aug 5, 2014

@author: Yves.Rosius
'''
import os

with open("inventory.txt", "r") as inventory_file:
    inventory = eval(inventory_file.read())


def splash_screen():
    """ASCII art fun"""
    print " _    _                                   _   _                  "
    print "| |  | |                                 | | | |                 "
    print "| |  | | ___  __ _ _ __    __ _ _ __   __| | | |_ ___  __ _ _ __ "
    print "| |/\| |/ _ \/ _` | '__|  / _` | '_ \ / _` | | __/ _ \/ _` | '__|"
    print "\  /\  /  __/ (_| | |    | (_| | | | | (_| | | ||  __/ (_| | |   "
    print " \/  \/ \___|\__,_|_|     \__,_|_| |_|\__,_|  \__\___|\__,_|_|   \n"


def clear_screen():
    """Clears console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    """Start menu for user"""
    # List of tuples. (function name, description for user, keyword arguments)
    menu_list = [(view_parts, "View all parts.", {'equipped': False}),
                 (view_parts, "View all equipped parts.", {'equipped': True}),
                 (add_part, "Add a part.", {}),
                 (remove_part, "Remove a part.", {}),
                 (edit_part, "Edit a part.", {}),
                 (equip_part, "Equip a part.", {}),
                 (add_ride, "Add a ride.", {})]

    clear_screen()
    for description in menu_list:
        print menu_list.index(description), description[1]

    choice = raw_input("\nPlease make a choice.")
    clear_screen()
    try:
        function, description, kwargs = menu_list[int(choice)]
        function(**kwargs)
    except (ValueError, IndexError):
        print "Please select correct number to make a choice."


def view_parts(equipped):
    """View parts in your inventory. Display equipped or all parts."""
    for part_type in inventory:
        print part_type
        for part_name in inventory[part_type]:
            if inventory[part_type][part_name][3] == True or equipped == False:
                print "\t", part_name
                print "\t\t", inventory[part_type][part_name]


def choose_part(type_or_name, type_choice):
    """Return value chosen by user."""
    clear_screen()
    if type_or_name == "type":
        temp_list = inventory.keys()
    elif type_or_name == "name":
        temp_list = inventory[type_choice].keys()

    for index, item in enumerate(temp_list):
        print index, item

    choice = raw_input("\nPlease make a choice.")
    while type(choice) != int:
        try:
            choice = int(choice)
        except ValueError:
            choice = raw_input("Please select correct number to make a choice.")
    return temp_list[choice]
    clear_screen()


def add_part():
    """Add a new part to your inventory."""
    type_choice = choose_part("type", 0)

    name_choice = raw_input("What is the name of the part?")
    weight = raw_input("What is the weight of the part?")
    price = raw_input("What is the price of the part?")

    inventory[str(type_choice)] = {str(name_choice) : [weight,
                                                       price,
                                                       0,
                                                       False]}


def remove_part():
    """Remove a part from your inventory."""
    type_choice = choose_part("type", 0)
    if inventory[type_choice] == {}:
        print "There are no items of this type."
    else:
        name_choice = choose_part("name", type_choice)

        del inventory[type_choice][name_choice]


def edit_part():
    """Change properties of a specific part."""
    type_choice = choose_part("type", 0)
    if inventory[type_choice] == {}:
        print "There are no items of this type."
    else:
        name_choice = choose_part("name", type_choice)

        print "0 weight"
        print "1 price"
        edit_choice = int(raw_input("What property do you want to edit?"))
        if edit_choice == 0 or edit_choice == 1:
            new_value = raw_input("Please give the new value for the property.")
            inventory[type_choice][name_choice][edit_choice] = new_value
        else:
            print "Please select correct number to make a choice."
            edit_part()


def equip_part():
    """Equip one part, unequip all other parts of that part type."""
    type_choice = choose_part("type", 0)
    if inventory[type_choice] == {}:
        print "There are no items of this type."
    else:
        name_choice = choose_part("name", type_choice)

        for part_name in inventory[type_choice]:
            inventory[type_choice][part_name][3] = False

        inventory[type_choice][name_choice][3] = True
        print "Your part has been equipped."


def add_ride():
    """Adds miles to properties of all equipped parts."""
    distance = int(raw_input("How many miles do you want to add?"))

    for part_type in inventory:
        for part_name in inventory[part_type]:
            if inventory[part_type][part_name][3]:
                inventory[part_type][part_name][2] += distance


splash_screen()
while 1:
    proceed = raw_input("\nPress any key to continue. Q to quit.")
    if proceed.lower() == "q":
        clear_screen()
        with open("inventory.txt", "w") as inventory_file:
            inventory_file.write(str(inventory))
            print "Bye"
            exit()
    else:
        menu()
