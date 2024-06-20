import pygame
import random
import math
from collections import Counter
import sys

from itertools import groupby
from operator import itemgetter

from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld
from mahjong.agari import Agari
from mahjong.shanten import Shanten

import copy

pygame.display.set_caption('mahjong')

calculator = HandCalculator()
agari = Agari()
shanten = Shanten()

pygame.init()
pygame.font.init()
screen_width = 1280
screen_height = 720+240 #960
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

sute_x = 65
sute_y = 150
bgcolor = (11, 117, 57)
screen.fill(bgcolor)

x_user =  100
y_user = (screen_height * 0.85)+40

FPS = 30

quadrant = {
    0 : [100, (screen_height * 0.85)+40],
    1 : [8, -20],
    2 : [screen_width-154, (screen_height * 0.01)],
    3 : [screen_width-80, 926]
}

big_font = pygame.font.SysFont("microsoftsansserif", 30)
small_font = pygame.font.SysFont("microsoftsansserif", 20)


tiles = [
    "1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m",  # manzu (numbers)
    "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p",  # pinzu (circles)
    "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",  # souzu (sticks)
    "1x", "2x", "3x", "4x",                                # wind (ton nan shaa pei)
    "1z", "2z", "3z"                                       # dragon
]

tiles = sorted(4*tiles)
random.shuffle(tiles)

#tenhou notation conversion
tenhou = {
    "1x" : "1z",
    "2x" : "2z",
    "3x" : "3z",
    "4x" : "4z",
    "1z" : "5z",
    "2z" : "6z",
    "3z" : "7z"
}

#suits conversion
suits = {
    "m" : "man",
    "p" : "pin",
    "s" : "sou",
    "x" : "honors",
    "z" : "honors"
}

#faces conversion
faces = {f"{i}m": f"Man{i}" for i in range(1, 10)}
faces.update({f"{i}p": f"Pin{i}" for i in range(1, 10)})
faces.update({f"{i}s": f"Sou{i}" for i in range(1, 10)})
faces.update({
    "1x" : "Ton",
    "2x" : "Nan",
    "3x" : "Shaa",
    "4x" : "Pei",
    "1z" : "Haku",
    "2z" : "Chun",
    "3z" : "Hatsu"
})

img_multiplier = 0.09

back = pygame.image.load("faces/Back.png").convert_alpha()
back = pygame.transform.scale(back, (back.get_width()*img_multiplier, back.get_height()*img_multiplier))

#x,y,w,h
user_pile_rect = pygame.Rect(100, 100+30, 800, 150)
cpu0_pile_rect = pygame.Rect(100, 275+30, 800, 150)
cpu1_pile_rect = pygame.Rect(100, 450+30, 800, 150)
cpu2_pile_rect = pygame.Rect(100, 625+30, 800, 150)
pile_rects = [user_pile_rect, cpu0_pile_rect, cpu1_pile_rect, cpu2_pile_rect]

user_hand_rect = pygame.Rect(150, 850, 900, 90)
cpu0_hand_rect = pygame.Rect(0, 10, 90, 900)
cpu1_hand_rect = pygame.Rect(250, 0, 900, 90)
cpu2_hand_rect = pygame.Rect(1190, 20, 90, 900)
hand_rects = [user_hand_rect, cpu0_hand_rect, cpu1_hand_rect, cpu2_hand_rect]

info_rect = pygame.Rect(910, 100, 280, 280)
pon_rect = pygame.Rect(910, 455, 280, 100)
chii_rect = pygame.Rect(910, 565, 280, 100)
ron_rect = pygame.Rect(910, 675, 280, 100)
call_rects = [pon_rect, chii_rect, ron_rect]
action_colours = [(44,154,222), (34,189,65), (222,44,44)]

meld_rect = pygame.Rect(1050, 790, 130, 160)

win_rect = pygame.Rect(390, 280, 500, 200)

def get_center(object, rect):
    x,y,w,h = rect
    obj_width = object.get_rect().width
    rect_x = x + (w-obj_width)/2
    obj_height = object.get_rect().height
    rect_y = y + (h-obj_height)/2
    return rect_x, rect_y

types = ["pon", "chii", "ron"]

cpu_delay = 0.5

