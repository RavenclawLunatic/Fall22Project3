from room import Room
from player import Player
from item import Item
from monster import Monster
import os
import updater
import random

player = Player()

def create_world():
    a = Room("You are in your bedroom")
    b = Room("You are in the hall")
    c = Room("You are in the kitchen")
    d = Room("You are in the living room")
    e = Room("You are in the bathroom")
    Room.connect_rooms(a, "east", b, "west")
    Room.connect_rooms(c, "east", d, "west")
    Room.connect_rooms(a, "south", e, "north")
    Room.connect_rooms(b, "north", c, "south")
    rooms = [a, b, c, d, e]
    random.shuffle(rooms)
    i = Item("Stuffed bear", "You remember this bear from when you were little. It feels much smaller now that you've grown, but it's still comforting.", a)
    i.put_in_room(rooms[0])
    j = Item("Shampoo", "You don't even want to know when the last time you washed your hair was.", e)
    j.put_in_room(rooms[1])
    k = Item("Apple", "Why is there randomly an apple? You're not sure you remember buying one ever but it's here regardless. You might not want to eat it, you don't know how long it's been out.", c)
    k.put_in_room(rooms[2])
    l = Item("Shoe", "You lost the other one years ago, and now this one seems to just mock you.", b)
    l.put_in_room(rooms[3])
    m = Item("TV Remote", "It's the remote for the TV. Sometimes it gets a little picky about where it's pointed.", d)
    m.put_in_room(rooms[4])
    player.location = a
    Monster("Passive Ideation", 100, player.location, True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_situation():
    clear()
    print(player.location.desc)
    print()
    happen = False
    event = random.random()
    if happen == False and event <= .25: 
        print("You think you can kill that pesky ideation, at least for today. You have the strength to do so.")
        player.health += 110
        print()
        happen = True
    else:
        if player.location.has_monsters():
            print("This room contains the following monsters:")
            for m in player.location.monsters:
                print(m.name)
            print()
        if player.location.has_items():
            print("This room contains the following items:")
            for i in player.location.items:
                print(i.name)
            print()
        print("You can go in the following directions:")
        for e in player.location.exit_names():
            print(e)
        print()

def show_help():
    clear()
    print("go <direction> -- moves you in the given direction")
    print("inventory -- opens your inventory")
    print("pickup <item> -- picks up the item")
    print("quit -- quits the game")
    print()
    input("Press enter to continue...")

if __name__ == "__main__":
    create_world()
    playing = True
    print("You're tired.")
    print("You know there's stuff you need to do, but it feels so far away.")
    print("Instead, you'll just do some housework.")
    print("If you place everything in the right rooms, maybe it'll help.")
    print("You are too tired to fight anything. Your best bet is to ignore such things and hope they go away. It's always worked before...")
    print("Note: I am okay. I swear. I haven't been in that bad of a place in a while.")
    input("Press enter to continue...")
    count = 0
    success = False
    while playing and player.alive:
        if count == 5:
            success = True
            break
        print_situation()
        command_success = False
        time_passes = False
        while not command_success:
            command_success = True
            command = input("What now? ")
            if len(command) == 0:
                continue
            command_words = command.split()
            if len(command_words) == 0:
                continue
            match command_words[0].lower():
                case "go":   #cannot handle multi-word directions
                    okay = player.go_direction(command_words[1]) 
                    if okay:
                        time_passes = True
                    else:
                        print("You can't go that way.")
                        command_success = False
                case "pickup":  #can handle multi-word objects
                    target_name = command[7:] # everything after "pickup "
                    target = player.location.get_item_by_name(target_name)
                    if target != False:
                        if len(player.items) == 5:
                            print("You're already holding too much.")
                            command_success = False
                        else:
                            player.pickup(target)
                            if player.location == target.correct:
                                count -= 1
                    else:
                        print("No such item.")
                        command_success = False
                case "pic":
                    target_name = command[4:]
                    target = player.location.get_item_by_name(target_name)
                    if target != False:
                        if len(player.items) == 3:
                            print("You're already holding too much.")
                            command_success = False
                        else:
                            player.pickup(target)
                            if player.location == target.correct:
                                count -= 1
                    else:
                        print("No such item.")
                        command_success = False
                case "inventory":
                    player.show_inventory()
                case "inv":
                    player.show_inventory()
                case "help":
                    show_help()
                case "quit":
                    playing = False
                case "attack":
                    target_name = command[7:]
                    target = player.location.get_monster_by_name(target_name)
                    if target != False:
                        player.attack_monster(target)
                    else:
                        print("No such monster.")
                        command_success = False
                case "a":
                    target_name = command[2:]
                    target = player.location.get_monster_by_name(target_name)
                    if target != False:
                        player.attack_monster(target)
                    else:
                        print("No such monster.")
                        command_success = False
                case "inspect":
                    target_name = command[8:]
                    if player.get_item_by_name(target_name):
                        player.get_item_by_name(target_name).describe()
                    elif player.location.get_item_by_name(target_name):
                        player.location.get_item_by_name(target_name).describe()
                    else:
                        print("No items named that in your inventory")
                        command_success = False
                case "insp":
                    target_name = command[5:]
                    if player.get_item_by_name(target_name):
                        player.get_item_by_name(target_name).describe()
                    elif player.location.get_item_by_name(target_name):
                        player.location.get_item_by_name(target_name).describe()
                    else:
                        print("No items named that in your inventory")
                        command_success = False
                case "drop":
                    target_name = command[5:]
                    target = player.get_item_by_name(target_name)
                    if target:
                        player.drop(target)
                        if player.location == target.correct:
                            count += 1
                    else:
                        print("No items named that in your inventory")
                        command_success = False
                case "wait":
                    time_passes == True
                case other:
                    print("Not a valid command")
                    command_success = False
        if time_passes == True:
            updater.update_all(player)
    if not player.alive:
        print("Why didn't I just ignore it...")
    if success:
        print("All the things have been sorted, but now what?")
        print("You're not really sure. All you can really do is get up again tomorrow and do it all over again.")
        print("Maybe someday you'll feel like you have the mental capacity to do more than deal with basic housework.")



