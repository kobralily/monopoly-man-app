import random
import time
import json
import os

from operator import itemgetter

BOARD_MAP = [
    'Go',
    'Mediterranean Avenue (Brown 1)',
    'Community Chest 1',
    'Baltic Avenue (Brown 2)',
    'Income Tax',
    'Reading Railroad (Railroad 1)',
    'Oriental Avenue (Aqua 1)',
    'Chance 1',
    'Vermont Avenue (Aqua 2)',
    'Connecticut Avenue (Aqua 3)',
    'Jail',
    'St. Charles Place (Pink 1)',
    'Electric Company (Utility 1)',
    'States Avenue (Pink 2)',
    'Virginia Avenue (Pink 3)',
    'Pennsylvania Railroad (Railroad 2)',
    'St. James Place (Orange 1)',
    'Community Chest 2',
    'Tennessee Avenue (Orange 2)',
    'New York Avenue (Orange 3)',
    'Free Parking',
    'Kentucky Avenue (Red 1)',
    'Chance 3',
    'Indiana Avenue (Red 2)',
    'Illinois Avenue (Red 3)',
    'B & O Railroad (Railroad 3)',
    'Atlantic Avenue (Yellow 1)',
    'Ventnor Avenue (Yellow 2)',
    'Water Works (Utility 2)',
    'Marvin Gardens (Yellow 3)',
    'Go to Jail',
    'Pacific Avenue (Green 1)',
    'North Carolina Avenue (Green 2)',
    'Community Chest 3',
    'Pennsylvania Avenue (Green 3)',
    'Short Line (Railroad 4)',
    'Chance 4',
    'Park Place (Blue 1)',
    'Luxury Tax',
    'Boardwalk (Blue 2)'
]

jailed = False
rolls_while_in_jail = 0
consecutive_double_count = 0

PROPERTY_TILES = [1, 3, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 18, 19, 21, 23, 24, 25, 26, 27, 28, 29, 31, 32, 34, 35, 37, 39]

tile_occurrences_dictionary = dict()


# certain cards from the Chance tile will move the player to certain positions
def chance(pos):
    global jailed

    # 16 cards in the Chance chest, most will move the player to a certain tile
    cards = random.randint(1, 16)

    # Advance to Go
    if cards == 1:
        return 0

    # Advance to Illinois Ave
    elif cards == 2:
        return 24

    # Advance to St. Charles Place
    elif cards == 3:
        return 11

    # Advance token to nearest Utility
    elif cards == 4 and pos == 22:
        return 28
    elif cards == 4:
        return 12

    # Advance token to the nearest Railroad
    elif cards == 5 and pos == 36:
        return 5
    elif cards == 5 and pos == 7:
        return 15
    elif cards == 5:
        return 25

    # Go Back 3 Spaces
    elif cards == 8:
        return pos - 3

    # Go to Jail – Go directly to Jail
    elif cards == 9:
        jailed = True
        return 10

    # Take a trip to Reading Railroad
    elif cards == 12:
        return 5

    # Take a walk on the Boardwalk – Advance token to Boardwalk
    elif cards == 13:
        return 39

    # did not draw a card that moves the player
    return pos


# certain cards from the Community Chest tile
# will move the player to certain positions
def community(pos):
    global jailed

    # 17 cards in the Community Chest, 2 will move the player to a certain tile
    cards = random.randint(1, 17)

    # Advance to Go
    if cards == 1:
        return 0

    # Go to Jail – Go directly to jail
    elif cards == 6:
        jailed = True
        return 10

    # did not draw a card that moves the player
    return pos


# takes current position, returns new position
def roll(pos):
    global jailed
    global rolls_while_in_jail
    global consecutive_double_count

    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)

    # rolling a double will knock the player out of jail
    if die1 == die2:
        consecutive_double_count += 1
        jailed = False
        rolls_while_in_jail = 0
    else:
        consecutive_double_count = 0

    # rolling three times will knock a player out of jail
    if rolls_while_in_jail == 3:
        jailed = False
        rolls_while_in_jail = 0

    # skips to the next turn if in jail AND
    # hasn't rolled a double AND
    # hasn't rolled three times
    if jailed == True:
        rolls_while_in_jail += 1
        return 10

    # calculates the new position after jail is sorted out
    pos += (die1 + die2)

    # board is 40 tiles long, so pos must stay between 0 and 39.
    if pos >= 40:
        pos -= 40

    # rolling three doubles in a row will throw you in jail,
    # rather than the tile you rolled onto

    # landing on the "Go to Jail" tile will throw you in jail
    if consecutive_double_count == 3 or pos == 30:
        jailed = True
        consecutive_double_count = 0
        return 10

    # determines if on a Community Chest or Chance tile
    first_word_of_tile = BOARD_MAP[pos].split(" ")[0]

    if first_word_of_tile == 'Chance':
        return chance(pos)
    elif first_word_of_tile == 'Community':
        return community(pos)

    # all special cases dealt with, return simply pos + (die1 + die2)
    return pos


# tossed this in here for the create project
def get_rounded_time_seconds():
    return int(round(time.time() * 1000)) / 1000


def main(num):
    pos = 0

    if int(num) > 100000:
        num = '100000'

    num_rolls = num

    time_since_start = get_rounded_time_seconds()
    
    listrolls = []

    for x in range(0, int(num_rolls)):
        pos = roll(pos)
        listrolls.append(pos)
        if pos in PROPERTY_TILES:
            if BOARD_MAP[pos] in tile_occurrences_dictionary:
                tile_occurrences_dictionary[BOARD_MAP[pos]] += 1
            else:
                tile_occurrences_dictionary[BOARD_MAP[pos]] = 1

    list_of_dictionary_entries = tile_occurrences_dictionary.items()

    sorted_list_of_dictionary_entries = sorted(list_of_dictionary_entries, key=itemgetter(1), reverse=True)

#     for entry in sorted_list_of_dictionary_entries:
#         print(str(entry) + "\n")

    output = []
    for entry in sorted_list_of_dictionary_entries:
        this_entry_results = {}
        this_entry_results['name'] = entry[0]
        this_entry_results['num_rolls'] = entry[1]

        output.append(this_entry_results)
    
    with open("./results.json", "w") as f:
        json.dump(output, f, indent=4)

#     print("We completed " + str(num_rolls) + " rolls in "
#           + str(get_rounded_time_seconds() - time_since_start) + " seconds!")
    return listrolls

# if __name__ == "__main__":
#     main()
