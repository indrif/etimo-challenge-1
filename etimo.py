import requests
import json
import pprint
from time import sleep

KEY = "blacksabbath"
URL = "http://192.168.0.72:8080/api"

pp = pprint.PrettyPrinter(indent=4)

def get():
    r = requests.get(URL)
    return r.json()

def go(s):
    # print("go", s)
    obj = {
    "playerKey": KEY,
    "direction": s
    }
    r = requests.post(
        URL,
        headers={
        "Content-Type": "application/json",
        }, data=json.dumps(obj))

def get_dist(px, py, cx, cy):
    mx = cx - px
    my = cy - py
    return mx, my

def get_player(players):
    for i in players:
        if i["color"] == "red":
            return i
    return None

def go_like(mx, my):
    if mx < 0:
        # Left
        for i in range(abs(mx)):
            go("left")
    elif mx > 0:
        # Right
        for i in range(abs(mx)):
            go("right")
    if my < 0:
        # Up
        for i in range(abs(my)):
            go("up")
    elif my > 0:
        # Down
        for i in range(abs(my)):
            go("down")

def go_home(current_x, current_y):
    mx, my = get_dist(current_x, current_y, 0, 0)
    go_like(mx, my)


def next_iteration():
    m = get()
    player = get_player(m["players"])
    px = player["x"]
    py = player["y"]
    current_coins = player["coins"]
    # print("Iteration: px=", px, "py=", py, "current_coins=", current_coins)
    if current_coins == 5:
        go_home(px, py)
    else:
        coins = m["coins"]
        for coin in coins:
            mx, my = get_dist(px, py, coin["x"], coin["y"])
            coin["mx"] = mx
            coin["my"] = my
            coin["dist"] = abs(mx) + abs(my)

        coins = sorted(coins, key=lambda x: x["dist"])

        index = 1
        max_coins = 5 - current_coins
        coin = coins[0]
        mx, my = get_dist(px, py, coin["x"], coin["y"])
        # print("  => ", mx, my)
        go_like(mx, my)
        index += 1

while True:
    next_iteration()

