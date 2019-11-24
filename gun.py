from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, g, x=40, y=450):
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 2
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30
        self.game = g

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        if self.y <= 500:
            self.vy -= 1.1
            self.y -= self.vy
            self.x += self.vx
            self.vx *= 0.99
            self.set_coords()
        if self.x > 780:
            self.vx = -self.vx / 2
            self.x = 779
        if self.y > 500:
            self.vy = -self.vy / 2
            self.vx = self.vx / 2
            self.y = 499
        if self.live < 0:
            self.game.balls.pop(self.game.balls.index(self))
            canv.delete(self.id)
        else:
            self.live -= 0.25
        if self.vx ** 2 + self.vy ** 2 < 1:
            self.vy = 0
            self.vx = 0

    def hittest(self, obj):
        if abs(obj.x - self.x) <= (self.r + obj.r) and abs(obj.y - self.y) <= (self.r + obj.r):
            return True
        else:
            return False


class gun():
    def __init__(self, g):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7)
        self.game = g

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        self.game.bullet += 1
        new_ball = ball(self.game)
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        self.game.balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=''):
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self, points=0):
        self.id = canv.create_oval(0, 0, 0, 0)
        self.points = points
        self.new_target()

    def live(self):
        self.points = 0
        self.live = 1

    def new_target(self):
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)


class game:
    def __init__(self):
        self.balls = []
        self.bullet = 0
        self.target1 = target()
        self.g1 = gun(self)
        self.points = 0
        self.id_points = canv.create_text(30, 30, text=self.points, font='40')

    def new_game(self, event=''):
        screen1 = canv.create_text(400, 300, text='', font='28')
        self.target1.new_target()
        self.balls = []
        self.bullet = 0
        canv.bind('<Button-1>', self.g1.fire2_start)
        canv.bind('<ButtonRelease-1>', self.g1.fire2_end)
        canv.bind('<Motion>', self.g1.targetting)
        self.target1.live = 1
        while self.target1.live or self.balls:
            for b in self.balls:
                b.move()
                if b.hittest(self.target1) and self.target1.live:
                    self.target1.live = 0
                    self.hit()
                    canv.bind('<Button-1>', '')
                    canv.bind('<ButtonRelease-1>', '')
                    canv.itemconfig(screen1, text='Вы уничтожили цель за ' + str(self.bullet) + ' выстрелов')

            canv.update()
            time.sleep(0.03)
            self.g1.targetting()
            self.g1.power_up()
        canv.itemconfig(screen1, text='')
        root.after(500, self.new_game)

    def hit(self, points=1):
        canv.coords(self.target1.id, -10, -10, -10, -10)
        self.points += points
        canv.itemconfig(self.id_points, text=self.points)


games = game()
games.new_game()
tk.mainloop()
