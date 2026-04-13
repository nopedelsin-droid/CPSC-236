import random

def display_menu():
    print("COMMAND MENU")
    print("walk - Walk down the path")
    print("show - Show all items")
    print("drop - Drop an item")
    print("exit - Exit program")

def walk(inv, items):
    found = random.choice(items)
    print("While walking down a path, you see,",found)
    user = input("Do you want to grab it? (y/n): ")
    try:
        if user == "y":
            if len(inv) <=4:
                inv.append(found)
            else:
                print("Your hands are full")
    except:
        print("Invalid input, a goblin steals the item")
        
def drop(inv):
    user = int(input("Number: "))
    try:
        dropped_item = inv.pop(user-1)
    except:
        print("Invalid item Number.")
    else:
        print("Dropped ", dropped_item)

def show(inv):
    if len(inv) == 0:
        print("Your pockets are empty")
    x = 1
    for item in inv:
        print(f"{x}.  {item}")

try:
    with open("wizard_all_items.txt", "r") as file:
        all_items = file.read()
except FileNotFoundError:
    print("Could not find the items file.")
    done = True
else:
    done = False
finally:
    file.close()

all_items = all_items.split('\n')
print("The Wizard Inventory Program")
display_menu()
try:
    with open("wizard_inventory.txt", "r") as file:
        current_items = file.read()
        current_items = current_items.split('\n')
except FileNotFoundError:
    print("Could not find the inventory file!")
    print("Wizard is starting with no inventory.")
    current_items = []
finally:
    file.close()
    

while not done:
    
    x = input("Command: ")
    if x == "walk":
        walk(current_items, all_items)

    elif x == "show":
        show(current_items)

    elif x == "drop":
        drop(current_items)

    elif x == "exit":
        done = True
        with open("wizard_inventory.txt", "w") as file:
            for item in current_items:
                file.write(item)
                file.write("\n")
    else:
        print("Invalid Command")





    
    