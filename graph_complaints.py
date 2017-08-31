"""
Author: Zach Morgan
Title: Graphing State Results
"""

from math import *
import turtle as t
from operator import itemgetter
from utilities import *
from state_complaints import *

def drawbar(height, width):
    """
    Purpose: Draw a bar used in the bar graph
    :param height: height dependent on the amount of complaints
    :param width: half the distance between each state name
    :return:
    """
    t.left(90)
    t.begin_fill()
    t.forward(height)
    t.right(90)
    t.forward(width)
    t.right(90)
    t.forward(height)
    t.end_fill()
    t.left(90)

def draw_state_graph(statemap):
    """
    Purpose: utilizes all utility functions and draws the graph
    :param statemap: dictionary of complaints mapped to belonging state
    :return: NONE
    """
    t.hideturtle()
    infolst = []
    for state in statemap:
        infolst.append((state, len(statemap[state])))
    infolst.sort(key=itemgetter(1))
    max_complaints = infolst[-1][1]
    if max_complaints >= 50000:
        y_max = ceil(max_complaints / 10000) * 10000
    if max_complaints >= 10000 and max_complaints < 50000:
        y_max = ceil(max_complaints / 1000) * 1000
    if max_complaints >= 1000 and max_complaints < 10000:
        y_max = ceil(max_complaints / 100) * 100
    elif max_complaints <= 1000:
        y_max = ceil(max_complaints / 10) * 10
    x_dis, y_int, infolst = draw_axis(statemap, y_max)
    t.up()
    t.goto(-325,-325)
    width = x_dis / 2
    int_pixel = y_int / 35
    for info in infolst:
        t.forward(x_dis)
        drawbar(info[1] / int_pixel , width)
        t.back(width)


def draw_int(inter, y_max):
    """
    Purpose: draws the pegs on the y - axis and the number on each one
    :param inter: value that the y axis steps by
    :param y_max: max value of y
    :return: none
    """
    for num in range(y_max, -1, -inter):
       if num == 0:
           break
       t.left(90)
       t.forward(35)
       t.right(90)
       t.write(str(num), font = ("Arial", 8, "normal"))
       t.left(90)
       t.back(35)
       t.right(90)
       t.back(35)

def draw_axis(statemap, y_max):
    """
    Purpose: draws the axis and the labels on the axis
    :param statemap
    :param y_max: Value of the state with the highest amount of complaints
    :return: x_dis: float number that represents the distance between the start of each bar line, or state name
    y_int: number that represents what the intervals on the y axis
    infolst: alphabetically sorted statemap
    """
    infolst = []
    for state in statemap:
        if len(statemap[state]) == 0:
            continue
        infolst.append((state, len(statemap[state])))
    infolst.sort(key=itemgetter(0))
    y_int = y_max // 20
    x_dis = 700 / len(infolst)
    t.up()
    t.back(325)
    t.right(90)
    t.forward(325)
    t.left(90)
    t.down()
    t.forward(700 + x_dis)
    t.back(700 + x_dis)
    t.left(90)
    t.forward(700)
    draw_int(y_int, y_max)
    counter = 0
    t.right(90)
    for state in infolst:
        counter += 1
        t.up()
        t.forward(x_dis)
        t.right(90)
        t.forward(15)
        t.left(180)
        t.write(state[0], font = ("Arial", 8, "normal"))
        t.right(90)
        if counter == 4:
            t.left(90)
            t.forward(60)
            t.right(90)
            counter = 0
    return x_dis, y_int, infolst

def main():
    entries = read_complaint_data("data/" + input("Enter Consumer Complaints file:"))
    statemap = make_state_map(entries)
    t.speed(0)
    draw_state_graph(statemap)
    print("Please close the canvas to quit.")
    t.done()

if __name__ == "__main__":
    main()



