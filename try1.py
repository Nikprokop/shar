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


def new_ball():
    global x, y, r, ball, dx, dy
    canv.delete(ALL)
    x = rnd(100, 700)
    y = rnd(100, 500)
    r = rnd(30, 50)
    dx = rnd(-7, 7)
    dy = rnd(-7, 7)
    ball = canv.create_oval(x - r, y - r, x + r, y + r, fill=choice(colors), width=0)
    root.after(4000, new_ball)
    return ball;



def click(event):
    global k
    if ((event.x - x) ** 2 + (event.y - y) ** 2 <= r ** 2):
        canv.delete(ALL)
        k = k + 1
        print(k)


def move_ball():
    global ball, dx, dy, x, y
    canv.move(ball, dx, dy)
    x = x + dx
    y = y + dy
    if (x + r) >= 800 or (x - r) <= 0:
        dx = -dx
    if (y + r) >= 600 or (y - r) <= 0:
        dy = -dy
    return x, y


def main():
    move_ball()
    root.after(30, main)


new_ball()
main()

canv.bind('<Button-1>', click)
mainloop()
