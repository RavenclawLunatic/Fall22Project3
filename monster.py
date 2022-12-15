import random
import updater

class Monster:
    def __init__(self, name, health, room, follower):
        self.name = name
        self.health = health
        self.room = room
        self.follower = follower
        room.add_monster(self)
        updater.register(self)
    def update(self, player):
        if self.follower:
            self.move_to(player.location)
        elif random.random() < .5:
            self.move_to(self.room.random_neighbor())
    def move_to(self, room):
        self.room.remove_monster(self)
        self.room = room
        room.add_monster(self)
    def die(self):
        self.room.remove_monster(self)
        updater.deregister(self)
