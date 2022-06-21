from sys import argv
import json
import socket

from textual.app import App

from snake import Snake


ip = argv[1]  # "localhost:13573"
address = (ip[:ip.find(":")], int(ip[ip.find(":")+1:]))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(address)

p = 512
try:
    file = ""
    data = ""
    while data != "end":
        data = server.recv(p).decode("utf-8")
        if "end" in data:
            file += data[:data.find("end")]
            break
        file += data
finally:
    server.close()
if file[-1] == "\n":
    file = file[:-1]
jsons = file[file.find("{"):]
chars = json.loads(jsons[:jsons.find("|||")])
colors = json.loads(jsons[jsons.find("|||")+3:jsons.find("&&&")])
data_chars = json.loads(jsons[jsons.find("&&&")+3:])
file = file[:file.find("{")]
# print(file, chars, colors, data_chars, sep="\n")

s = Snake(file, chars, data_chars, 1, "pl1")
s.get_map()

class Play(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.side = "up"

    async def on_mount(self):
        self.set_interval(0.2, self.draw_map)

    async def on_load(self):
        await self.bind("q", "quit")
        await self.bind("up", "move('up')")
        await self.bind("down", "move('down')")
        await self.bind("left", "move('left')")
        await self.bind("right", "move('right')")

    async def action_move(self, side):
        if side not in ("up", "down", "left", "right"):
            return None

        match side:
            case "up":
                if self.side != "down":
                    self.side = side
            case "down":
                if self.side != "up":
                    self.side = side
            case "left":
                if self.side != "right":
                    self.side = side
            case "right":
                if self.side != "left":
                    self.side = side

    def draw_map(self):
        self.refresh()
        s.move(self.side)
        map_ = s.get_map_with_info()
        print(map_)
        

Play.run()

# s.get_map()
# 
# s.move("up")
# s.move("up")
# s.move("up")
# s.move("up")
# s.move("right")
# s.move("right")
# s.move("down")
# s.move("right")
# s.move("right")
# s.move("right")
# s.move("right")
# s.move("right")
# s.move("right")
# s.move("up")
# s.move("up")
# s.move("up")

# print(s.get_normal_map(), sep="\n")
# print(data_chars)
