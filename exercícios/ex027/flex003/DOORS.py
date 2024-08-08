import random
import time
import threading

currentRoom = 0
hidden = False

RUSH = False
RUSH_CHANCE = 70

ROOMS = [
    [
        [True, True],
        ["A simple room.", 2],
        ["Has 3 closets and 4 plants in each corner.", 3],
        ["The walls are white, and the floor is made of carpet", 2]
    ],
    [
        [False, True],
        ["A long hallway room.", 2],
        ["There are no closets or beds here.", 3],
        ["The walls are white, and the floor is made of carpet", 2],
        ["There are a lot of windows here.", 2]
    ],
    [
        [True, True],
        ["An 'L' shaped rooms", 2],
        ["There are only one closet here.", 3],
        ["The walls are white, and the floor is made of blue carpet", 2],
        ["Nothing special. ", 2]
    ]
]

canPass = False
DEAD = False
deathCause = ""

def readRoom(room):
    for line in room:
        if room.index(line) > 0:
            text = line[0]
            delay = line[1]

            print(text)
            input()

def rush_timer():
    time.sleep(3.5)
    print("\nRush is near. HIDE!")
    time.sleep(1.5)

    if not hidden:
        print("\nRush has murdered you.")
        deathCause = "Rush"
        DEAD = True
    else:
        print("\nRush hasen't found you.")
    


while not DEAD:
    print(f"current room: {currentRoom}")
    currentRoomIndex = random.randint(0, len(ROOMS)-1)
    readRoom(ROOMS[currentRoomIndex])

    rushChance = random.randint(0, 100)
    if (rushChance > 100 - RUSH_CHANCE):
        print("Lights flickered. Take care.")
        threading.Thread(target=rush_timer).start()

    while not canPass and not DED:
        inputs = input("Action: ")

        if "hide" in inputs:
            if not hidden:
                if ROOMS[currentRoomIndex][0][0]:
                    print(f"You have hided.")
                    hidden = True
                else:
                    print(f"There is no hiding spots here.")
            else:
                print("You are alredy hidden. Type 'exit spot' for gettin' out.")
        
        if "exit " in inputs:
            if hidden:
                print(f"You have exit your hiding spot.")
                hidden = False
            else:
                print("You aren't hidden. ")

        if not hidden:
            if inputs == "next":
                canPass = True
        else:
            print("You are hidden. Type 'exit (spot)' for gettin' out.")
        
        
    
    currentRoom += 1
    canPass = False

print("YOU DIED!")
time.sleep(2)
print(f"You died to {deathCause}.")