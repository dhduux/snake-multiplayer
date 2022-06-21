import re
from random import randint


player_snakes = [
    [(12, 6), (12, 7), (12, 8), (12, 9)],
    [(33, 6), (33, 7), (33, 8), (33, 9)],
    [(12, 18), (12, 17), (12, 16), (12, 15)],
    [(33, 18), (33, 17), (33, 16), (33, 15)]
]


def _convert_hex_to_rgb(hex_, default="rgb(255, 255, 255)"):
    """hex - #ffffff or #fff"""

    if hex_[0] == "#":
        hex_ = hex_[1:]
    
    if len(hex_) == 3:
        hex_ += hex_

    if len(hex_) != 6:
        return default

    # data converts
    dc = dict(zip(list("0123456789abcdef"), range(1, 17)))
    
    r = dc[hex_[0]] * dc[hex_[1]]
    g = dc[hex_[2]] * dc[hex_[3]]
    b = dc[hex_[4]] * dc[hex_[5]]

    return f"rgb({r}, {g}, {b})"


class Snake:
    def __init__(self, map_: str, chars: dict, data_chars: dict, player: int, name: str, color: str = "white", color_head: str = "white"):
        """
        colors:
        
        black
        white
        red
        blue
        yellow
        green
        magenta
        cyan
        rgb(r, g, b)
        #000000
        """

        self.__name = name
        self.__color = color
        self.__color_head = color_head

        self.__map = list(map(list, map_.split("\n")))[:-1]
        self.__chars = chars
        self.__data_chars = data_chars

        self.__snake = player_snakes[player-1]

        self.__is_live = True

    def get_map_info(self):
        info = f"""
        {"x".join(map(lambda i: str(i+1), self.map_size()))}
        snake length: {len(self.__snake)}
        status: {"live" if self.__is_live else "dead"}
        """
        return info

    def get_map_with_info(self):
        map_ = self.get_normal_map().split("\n")
        info = [i for i in self.get_map_info().split("\n") if i]
        info_lines = [" ".join([s.strip() for s in list(i)]) for i in zip(map_, info)]
        map_ = "\n".join(info_lines + map_[len(info_lines):])
        return map_

    def get_map_str(self) -> tuple:
        map_ = ""
        m_ = self.__map
        for line in m_:
            map_ += "".join(line) + "\n"
        map_ = map_[:-1]
        return map_

    def map_size(self):
        heigth = len(self.__map)
        width = len(self.__map[0])
        return (width, heigth)

    def update_snake(self):        
        map_ = self.get_map_str()
        chars = self.__chars
        snake = self.__snake

        if not snake:
            return None

        map_ = map_.replace(chars["head_up"], chars["void"])
        map_ = map_.replace(chars["head_down"], chars["void"])
        map_ = map_.replace(chars["head_left"], chars["void"])
        map_ = map_.replace(chars["head_right"], chars["void"])
        map_ = map_.replace(chars["snake"], chars["void"])

        m_ = []
        for m in map_.split("\n"):
            m_.append(list(m))
        map_ = m_

        x, y = snake[0]
        if y < snake[1][1]:
            map_[y][x] = chars["head_up"]
        elif y > snake[1][1]:
            map_[y][x] = chars["head_down"]
        elif x < snake[1][0]:
            map_[y][x] = chars["head_left"]
        elif x > snake[1][0]:
            map_[y][x] = chars["head_right"]
        for x, y in snake[1:]:
            map_[y][x] = chars["snake"]
        
        self.__map = map_
            
    
    def get_map(self) -> list:
        map_ = self.__map
        snake = self.__snake
        if snake:
            x, y = snake[0]
            if y < snake[1][1]:
                map_[y][x] = self.__chars["head_up"]
            elif y > snake[1][1]:
                map_[y][x] = self.__chars["head_down"]
            elif x < snake[1][0]:
                map_[y][x] = self.__chars["head_left"]
            elif x > snake[1][0]:
                map_[y][x] = self.__chars["head_right"]
            for x, y in snake[1:]:
                map_[y][x] = self.__chars["snake"]
        map_ = list(map(lambda x: "".join(x), map_))
        return map_

    def get_normal_map(self) -> str:
        color = {
            "snake": "\x1b[38;2;0;255;255m",
            "wall": "\x1b[48;2;255;255;255m",
            "food": "\x1b[38;2;0;100;255m",
            "bold": "\x1b[1m",
            "reset": "\x1b[0m"
        }

        chars = self.__data_chars

        map_ = ""
        m_ = self.__map
        for line in m_:
            map_ += "".join(line) + "\n"
        map_ = map_[:-1]
        
        map_ = map_.replace(chars["char_void"], chars["void"])
        map_ = map_.replace(chars["char_wall"], color["wall"] + chars["wall"] + color["reset"])
        map_ = map_.replace(chars["char_food"], color["food"] + chars["food"] + color["reset"])
        map_ = map_.replace(chars["char_snake"], color["snake"] + chars["snake"] + color["reset"])
        map_ = map_.replace(chars["char_head_up"], color["snake"] + color["bold"] + chars["head_up"] + color["reset"])
        map_ = map_.replace(chars["char_head_down"], color["snake"] + color["bold"] + chars["head_down"] + color["reset"])
        map_ = map_.replace(chars["char_head_left"], color["snake"] + color["bold"] + chars["head_left"] + color["reset"])
        map_ = map_.replace(chars["char_head_right"], color["snake"] + color["bold"] + chars["head_right"] + color["reset"])

        return map_

    def get_color(self, color: str):
        colors = {
            "white": "\x1b[38;2;255;255;255m",
            "black": "\x1b[38;2;0;0;0m",
            "red": "\x1b[38;2;255;0;0m",
            "blue": "\x1b[38;2;0;0;255m",
            "yellow": "\x1b[38;2;255;255;255m",
            "green": "\x1b[38;2;0;255;0m",
            "cyan": "\x1b[38;2;0;255;255m",
            "magenta": "\x1b[38;2;255;0;255m",
        }

        if color in colors.keys():
            return get(colors, color, None)
        if color[0] == "#" and len(color) in (4, 7):
            color = _convert_hex_to_rgb(color)
        color = color.replace(" ", "")
        m = re.findall(r"rgb\((\d{1,3}),(\d{1,3}),(\d{1,3})\)", color)
        if m:
            return f"\x1b[38;2;{m[1]};{m[2]};{m[3]}m"

    def get_data(self) -> bytes:
        #             name       color body       color_head
        return f"{self.__name},{self.__color},{self.__color_head}".encode("utf-8")

    def __str__(self):
        return f"{self.__name},{self.__color},{self.__color_head}"

    def iswall(self, x: int, y: int) -> bool:
        return self.__map[y][x] == self.__chars["wall"]

    def isfood(self, x: int, y: int) -> bool:
        return self.__map[y][x] == self.__chars["food"]

    def isvoid(self, x: int, y: int) -> bool:
        return self.__map[y][x] == self.__chars["void"]

    def issnake(self, x: int, y: int) -> bool:
        return self.__map[y][x] == self.__chars["snake"]

    def dead(self):
        for x, y in self.__snake:
            self.__map[y][x] = self.__chars["food"]
        self.__snake.clear()
        self.__is_live = False

    def move(self, side: str):
        if not self.__is_live:
            return None
        snake = self.__snake
        map_ = self.__map
        chars = self.__chars.copy()
        x, y = snake[0]
        width, heigth = self.map_size()
        
        match side:
            case "up":
                next_y = y - 1
                if next_y < 0:
                    next_y = heigth - 1
                if self.iswall(x, next_y) or self.issnake(x, next_y):
                    self.dead()
                elif snake[1][1] != next_y:
                    snake.insert(0, (x, next_y))
                    if not self.isfood(x, next_y):
                        snake.pop()
                    else:
                        food_x = randint(0, width-2)
                        food_y = randint(0, heigth-1)

                        while not self.isvoid(food_x, food_y):
                            food_x = randint(0, width-2)
                            food_y = randint(0, heigth-1)

                        map_[food_y][food_x] = chars["food"]
                        
                        map_[next_y][x] = chars["void"]
            case "down":
                next_y = y + 1
                if next_y > heigth-1:
                    next_y = 0
                if self.iswall(x, next_y) or self.issnake(x, next_y):
                    self.dead()
                elif snake[1][1] != next_y:
                    snake.insert(0, (x, next_y))
                    if not self.isfood(x, next_y):
                        snake.pop()
                    else:
                        food_x = randint(0, width-2)
                        food_y = randint(0, heigth-1)

                        while not self.isvoid(food_x, food_y):
                            food_x = randint(0, width-2)
                            food_y = randint(0, heigth-1)

                        map_[food_y][food_x] = chars["food"]
                        
                        map_[next_y][x] = chars["void"]
            case "left":
                next_x = x - 1
                if next_x < 0:
                    next_x = width - 1
                if self.iswall(next_x, y) or self.issnake(next_x, y):
                    self.dead()
                elif snake[1][0] != next_x:
                    snake.insert(0, (next_x, y))
                    if not self.isfood(next_x, y):
                        snake.pop()
                    else:
                        food_x = randint(0, width-2)
                        food_y = randint(0, heigth-1)

                        while not self.isvoid(food_x, food_y):
                            food_x = randint(0, width-2)
                            food_y = randint(0, heigth-1)

                        map_[food_y][food_x] = chars["food"]
                        
                        map_[y][next_x] = chars["void"]
            case "right":
                next_x = x + 1
                if next_x > width-1:
                    next_x = 0
                if self.iswall(next_x, y) or self.issnake(next_x, y):
                    self.dead()
                elif snake[1][0] != next_x:
                    snake.insert(0, (next_x, y))
                    if not self.isfood(next_x, y):
                        snake.pop()
                    else:
                        food_x = randint(0, width-2)
                        food_y = randint(0, heigth-1)

                        while not self.isvoid(food_x, food_y):
                            food_x = randint(0, width-2)
                            food_y = randint(0, heigth-1)

                        map_[food_y][food_x] = chars["food"]
                        
                        map_[y][next_x] = chars["void"]
        self.__map = map_
        self.__snake = snake
        self.update_snake()
