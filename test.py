from textual.app import App


class My(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.side = "up"

    async def on_mount(self):
        self.set_interval(0.2, self.print_text)

    async def on_load(self, event):
        await self.bind("q", "quit")
        await self.bind("up", "move('up')")
        await self.bind("down", "move('down')")
        await self.bind("left", "move('left')")
        await self.bind("right", "move('right')")

    async def action_move(self, side):
        if side in ("up", "down", "left", "right"):
            self.side = side

    def print_text(self):
        self.refresh()
        print(self.side)

My.run()
