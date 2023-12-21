import sys
import math
import unittest


# Score points by scanning valuable fish faster than your opponent.

# A map is 10000 x 10000 u starting at 0 0
# A drone moves max 600 u per turn but sink by 300u if no motors
# A drone scans min 800u to 2000u around source
# A battery starts at 30 and drains by 5 for a high power scan put +1 for normal
# Drone has Id, x, y, and battery
# a number of fish is given
# the fish have id, colour, type, x, y, speed
# the details broadcast are id, colour and type

def log(message):
    print(message, file=sys.stderr, flush=True)


# drone, id, mine, x, y, battery
class drone:
    def __init__(self, id, mine, x, y, battery):
        self.id = id
        self.mine = mine
        self.x = x
        self.y = y
        self.battery = battery

    def drain_battery(self, total):
        self.battery -= total
        if self.battery < 0:
            self.battery = 0


class fish:
    def __init__(self, id, _type, colour):
        self.id = id
        self.colour = colour
        self._type = _type
        self.x = None
        self.y = None
        self.vx = None
        self.vy = None

    def update_location(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


def add_or_update(object_to_update, array):
    if object_to_update.id in [d.id for d in array]:
        if isinstance(object_to_update, drone):
            active_drone = [d for d in array if d.id == object_to_update.id][0]
            active_drone.x = object_to_update.x
            active_drone.y = object_to_update.y
            active_drone.battery = object_to_update.battery
        elif isinstance(object_to_update, fish):
            active_fish = [f for f in array if f.id == object_to_update.id][0]
            active_fish.update_location(object_to_update.x, object_to_update.y, object_to_update.vx,
                                        object_to_update.vy)
    else:
        array.append(object_to_update)

    return array


# tests
debug = False
if debug:
    class MyTest(unittest.TestCase):
        def test_drone_initialises(self):
            self.assertIsNotNone(drone(1, True, 0, 0, 30))

        def test_add_or_update(self):
            drone_array = []
            new_drone = drone(1, True, 0, 0, 30)
            drone_array = add_or_update(new_drone, drone_array)
            self.assertEqual(len(drone_array), 1)
            new_drone.drain_battery(10)
            drone_array = add_or_update(new_drone, drone_array)
            self.assertEqual(len(drone_array), 1)
            self.assertEqual(drone_array[0].battery, 20)

        def test_fishstocks(self):
            fish_array = []
            test_fish = fish(1, "fish", "red")
            add_or_update(test_fish, fish_array)
            self.assertEqual(len(fish_array), 1)
            test_fish.x = 0
            test_fish.y = 1
            test_fish.vx = 1
            test_fish.vy = 1
            add_or_update(test_fish, fish_array)
            self.assertEqual(len(fish_array), 1)
            self.assertEqual(fish_array[0].y, 1)


    if __name__ == '__main__':
        unittest.main()

# data containers
my_drones = []
enemy_drones = []
fish_array = []
my_scan_record = []

creature_count = int(input())
for i in range(creature_count):
    creature_id, color, _type = [int(j) for j in input().split()]
    fish_array = add_or_update(fish(creature_id, _type, color), fish_array)

# game loop
while True:
    my_score = int(input())
    foe_score = int(input())

    my_scan_record = []
    my_scan_count = int(input())
    for i in range(my_scan_count):
        creature_id = int(input())
        my_scan_record.append(creature_id)

    log(my_scan_record)

    foe_scan_count = int(input())
    for i in range(foe_scan_count):
        creature_id = int(input())

    my_drone_count = int(input())
    for i in range(my_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        add_or_update(drone(drone_id, True, drone_x, drone_y, battery), my_drones)

    foe_drone_count = int(input())
    for i in range(foe_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        add_or_update(drone(drone_id, False, drone_x, drone_y, battery), enemy_drones)

    drone_scan_count = int(input())
    for i in range(drone_scan_count):
        drone_id, creature_id = [int(j) for j in input().split()]
        log(f"drone{drone_id} sees {creature_id}")

    visible_creature_count = int(input())
    for i in range(visible_creature_count):
        creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]

    radar_blip_count = int(input())
    for i in range(radar_blip_count):
        inputs = input().split()
        drone_id = int(inputs[0])
        creature_id = int(inputs[1])
        radar = inputs[2]

    for i in range(my_drone_count):
        my_active_drone = my_drones[i]
        log(f"{my_active_drone.id} {my_active_drone.x}, {my_active_drone.y}, {my_active_drone.battery}")
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        # MOVE <x> <y> <light (1|0)> | WAIT <light (1|0)>

        print("WAIT 1")

