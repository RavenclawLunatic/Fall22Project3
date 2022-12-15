import os
from item import Item
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.location = None
        self.items = []
        self.health = 50
        self.alive = True
    # goes in specified direction if possible, returns True
    # if not possible returns False
    def go_direction(self, direction):
        new_location = self.location.get_destination(direction.lower())
        if new_location is not None:
            self.location = new_location
            return True
        return False
    def pickup(self, item):
        self.items.append(item)
        item.loc = self
        self.location.remove_item(item)
    def drop(self, item):
        self.items.remove(item)
        item.put_in_room(self.location)
    def show_inventory(self):
        clear()
        print("You are currently carrying:")
        print()
        for i in self.items:
            print(i.name)
        print()
        input("Press enter to continue...")
    def get_item_by_name(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False
    def attack_monster(self, mon):
        clear()
        print("You are attacking " + mon.name)
        print()
        print("Your health is " + str(self.health) + ".")
        print(mon.name + "'s health is " + str(mon.health) + ".")
        print()
        if self.health > mon.health:
            self.health -= mon.health
            print("You win. Your health is now " + str(self.health) + ".")
            mon.die()
            print(mon.name + " has somehow dropped something, despite only existing in your head.")
            loot = random.random()
            if loot > .5:
                n = Item("Memory", "You not sure if this is a particularly helpful memory to have. But you have it anyway.")
            else:
                n = Item("Will to Live", "Oh, is that where that went? Well, you have it back now. Unfortunately, it can't fix everything on its own.")
            n.put_in_room(self.location)
        else:
            print("You lose.")
            self.alive = False
        print()
        input("Press enter to continue...")

