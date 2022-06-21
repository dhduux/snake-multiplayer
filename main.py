import json
import sys
import os

import socket


with open("config.json") as file:
    config = json.load(file)

def set_level(level, game="./game"):
    with open(f"{config['levels_dir']}/{level}") as f:
        with open("./game", "w") as fg:
            fg.write(f.read())

chars = {
    'char_void': '0',
    'char_wall': '1',
    'char_food': 'f',
    'char_head_up': '^',
    'char_head_down': '.',
    'char_head_left': '<',
    'char_head_right': '>',
    'char_snake': 's',
    'void': ' ',
    'wall': ' ',
    'food': '⬤',
    'head_up': 'ᐃ',         #'ᐱ',
    'head_down': 'ᐁ',       #'ᐯ',
    'head_left': 'ᐊ',
    'head_right': 'ᐅ',
    'snake': '■'             #'█'
}

color = {
    "snake": "\x1b[38;2;0;255;255m",
    "wall": "\x1b[48;2;255;255;255m",
    "food": "\x1b[38;2;0;100;255m",
    "bold": "\x1b[1m",
    "reset": "\x1b[0m"
}

def draw_map(level="./game"):
    with open(level) as f:
        file = f.read()
    file = file.replace(chars["char_void"], chars["void"])
    file = file.replace(chars["char_wall"], color["wall"] + chars["wall"] + color["reset"])
    file = file.replace(chars["char_food"], color["food"] + chars["food"] + color["reset"])
    file = file.replace(chars["char_snake"], color["snake"] + chars["snake"] + color["reset"])
    file = file.replace(chars["char_head_up"], color["snake"] + color["bold"] + chars["head_up"] + color["reset"])
    file = file.replace(chars["char_head_down"], color["snake"] + color["bold"] + chars["head_down"] + color["reset"])
    file = file.replace(chars["char_head_left"], color["snake"] + color["bold"] + chars["head_left"] + color["reset"])
    file = file.replace(chars["char_head_right"], color["snake"] + color["bold"] + chars["head_right"] + color["reset"])

    print(file, end="")

data_chars = {
    "void": chars["char_void"],
    "wall": chars["char_wall"],
    "food": chars["char_food"],
    "snake": chars["char_snake"],
    "head_up": chars["char_head_up"],
    "head_down": chars["char_head_down"],
    "head_left": chars["char_head_left"],
    "head_right": chars["char_head_right"],
}

ip = sys.argv[1]  # "localhost:13572"
players = 2
address = (ip[:ip.find(":")], int(ip[ip.find(":")+1:]))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(address)
sock.listen(players)

try:
    client, client_addres = sock.accept()

    p = 512
    with open("./game") as f:
        f.seek(0)
        data = f.read(p).encode("utf-8")
        while data:
            client.send(data)
            data = f.read(p).encode("utf-8")
        client.send(json.dumps(data_chars).encode("utf-8"))
        client.send(b"|||")
        client.send(json.dumps(color).encode("utf-8"))
        client.send(b"&&&")
        client.send(json.dumps(chars).encode("utf-8"))
        client.send(b"end")
finally:
    client.close()
