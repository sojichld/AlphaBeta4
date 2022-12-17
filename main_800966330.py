# UNC Charlotte
# ITCS 5153 - Applied AI - Fall 2022
# Lab 3
# Adversarial Search / Game Playing
# This module implements …
# Student ID: 800966330

import pygame as pg
import sys
import random
import interface_800966330 as interface
import argparse

class playGame(object):
    def __init__(self, gameType):
        self.Screen = pg.display.get_surface()
        self.Clock = pg.time.Clock()
        self.firstPlayer = random.choice([True, False])
        self.State = interface.Interface((6, 7), self.firstPlayer, gameType)
        self.State.gen_playing_field()

    def event_loop(self):
        #Quit condition
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            #If a button is pressed, execute button command
            decision = self.State.get_event(event)
            if decision == "Exit":
                sys.exit()
            elif decision == "Restart":
                main()
            #display replay message if winning condition is true
            elif decision == "Won":
                self.State.restartMessage()
                pg.display.update()
                pg.time.wait(400)
        self.State.ai_event()

    def game_loop(self):
        #start core game loop
        while not self.State.dead:
            self.event_loop()

def main(args):
    print("New connect four game started!")
    pg.init()
    if args.ai == "d":
        gameType = "Default"
    elif args.ai == "m":
        gameType = "Minimax"
    elif args.ai == "a":
        gameType = "Alpha Beta Pruning"
    start = playGame(gameType)
    pg.display.update()
    while not start.State.dead:
        #Star preliminary game loop
        start.State.startMessage()
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.pos[1] >= 460 and event.pos[1] < 490:
                    return "Exit"
                if event.pos[1] >= 400 and event.pos[1] < 430 and event.pos[1]:
                    start.game_loop()
            


if __name__ == "__main__":
    #get arguments for game type
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--ai', help = 'Algorithm type: d = default, m = minimax, a = alpha beta pruning', type = str, required = True)
    args = parser.parse_args()
    main(args)