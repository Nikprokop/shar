# coding: utf-8
from tkinter import *
from random import randrange as rnd, choice
import time

root = Tk()
root.geometry('800x600')

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

colors = ['red', 'orange', 'yellow', 'green', 'blue']

k = 0


class ball():
    def __init__(self):
        self.x = rnd(100, 700)
        self.y = rnd(100, 500)
        self.r = rnd(30, 50)
        self.vx = rnd(-7, 7)
        self.vy = rnd(-7, 7)
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def remove(self):
        self.move_ball()
        root.after(30, self.remove)

    def move_ball(self):
        canv.move(self.id, self.vx, self.vy)
        self.x += self.vx
        self.y += self.vy
        if (self.x + self.r) >= 800 or (self.x - self.r) <= 0:
            self.vx = -self.vx
        if (self.y + self.r) >= 600 or (self.y - self.r) <= 0:
            self.vy = -self.vy


def click(event):
    global k
    for i in range(len(balls)):
        if ((event.x - balls[i].x) ** 2 + (event.y - balls[i].y) ** 2 <= balls[i].r ** 2):
            canv.delete(balls[i].id)
            k = k + 1
            print(k)

balls = []

for i in range(10):
    balls.append(i)
for i in range(10):
    balls[i] = ball()
    balls[i].remove()

canv.bind('<Button-1>', click)

mainloop()
