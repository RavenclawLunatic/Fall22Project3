updates = []

def update_all(player):
    for u in updates:
        u.update(player)

def register(thing):
    updates.append(thing)

def deregister(thing):
    updates.remove(thing)