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
        if self.y <= 550:
            self.vy -= 1.1
            self.y -= self.vy
            self.x += self.vx
            self.vx *= 0.99
            self.set_coords()
        if self.x > 780:
            self.vx = -self.vx / 2
            self.x = 779
        if self.y > 550:
            self.vy = -self.vy / 2
            self.vx = self.vx / 2
            self.y = 549
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
        self.x = rnd(100, 700)
        self.y = rnd(100, 500)
        self.r = rnd(20, 50)
        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)
        self.id = canv.create_oval(0, 0, 0, 0)
        self.points = points
        self.new_target()

    def live(self):
        self.points = 0
        self.live = 1

    def new_target(self):
        x = self.x = rnd(100, 700)
        y = self.y = rnd(100, 500)
        r = self.r = rnd(20, 50)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def move_target(self):
        canv.move(self.id, self.vx, self.vy)
        self.x += self.vx
        self.y += self.vy
        if (self.x + self.r) >= 800 or (self.x - self.r) <= 0:
            self.vx = -self.vx
        if (self.y + self.r) >= 600 or (self.y - self.r) <= 0:
            self.vy = -self.vy


class game:
    def __init__(self):
        self.balls = []
        self.bullet = 0
        self.tnumbers = rnd(2, 5)
        self.targets = []
        self.g1 = gun(self)
        self.goon = 1
        self.points = 0
        self.id_points = canv.create_text(30, 30, text=self.points, font='40')

    def new_game(self, event=''):
        screen1 = canv.create_text(400, 300, text='', font='28')
        self.tnumbers = rnd(2, 5)
        self.targets = [target() for _ in range(self.tnumbers)]
        for i in range(self.tnumbers):
            self.targets[i].new_target()
            self.targets[i].live = 1
        self.balls = []
        self.bullet = 0
        canv.bind('<Button-1>', self.g1.fire2_start)
        canv.bind('<ButtonRelease-1>', self.g1.fire2_end)
        canv.bind('<Motion>', self.g1.targetting)
        self.goon = 1
        while self.goon or self.balls:
            for a in self.targets:
                a.move_target()
            for b in self.balls:
                b.move()
                for i in self.targets:
                    if b.hittest(i) and i.live:
                        i.live = 0
                        self.hit(i)
                        self.livecheck()
                        if self.goon == 0:
                            if (self.bullet % 10 == 1):
                                canv.itemconfig(screen1, text='Вы уничтожили цель за ' + str(self.bullet) + ' выстрел')
                            elif ((self.bullet % 10 >= 2) and (self.bullet % 10 <= 4)):
                                canv.itemconfig(screen1, text='Вы уничтожили цель за ' + str(self.bullet) + ' выстрела')
                            else:
                                canv.itemconfig(screen1,
                                                text='Вы уничтожили цель за ' + str(self.bullet) + ' выстрелов')
                            canv.update()
            canv.update()
            time.sleep(0.03)
            self.g1.targetting()
            self.g1.power_up()
        else:
            canv.delete(screen1)
        canv.delete(self.targets)
        root.after(500, self.new_game)

    def livecheck(self):
        self.k = 0
        for i in range(self.tnumbers):
            if (self.targets[i].live == 0):
                self.k += 1
        if (self.k == self.tnumbers):
            self.goon = 0
        else:
            self.goon = 1

    def hit(self, i, points=1):
        canv.coords(i.id, -10, -10, -10, -10)
        self.points += points
        canv.itemconfig(self.id_points, text=self.points)


games = game()
games.new_game()
tk.mainloop()
