# UNC Charlotte
# ITCS 5153 - Applied AI - Fall 2022
# Lab 3
# Adversarial Search / Game Playing
# This module implements …
# Student ID: 800966330
import time as ti
import numpy as np
import pygame as pg
import math
import alg_800966330 as alg

class Interface(object):
    def __init__(self, matrix, playerTurn, gameType):
        #Board dimensions
        self.matrix = matrix
        self.game = np.zeros((self.matrix[0], self.matrix[1]))
        #Fonts
        self.fonts = [pg.font.SysFont("calibri", 50), pg.font.SysFont("calibri", 40), pg.font.SysFont("calibri", 30), pg.font.SysFont("calibri", 20), pg.font.SysFont("calibri", 10)]
        #Board parameters
        self.boardSegment = 80
        self.width = self.matrix[1] * self.boardSegment
        self.height = (self.matrix[0]+1) * self.boardSegment
        self.size = (self.width * 1.286, self.height)
        self.radius = int(self.boardSegment / 2 - 5)
        self.screen = pg.display.set_mode(self.size)
        self.dead = False
        self.playerTurn = playerTurn
        #player types
        self.player = [0, 1, 2]
        #Initialize algorithm type
        self.alg = alg.Algorithm(matrix, self.player, gameType)
        #Runtime for algorithm
        self.runTime = 0
        #Winner state
        self.winner = False

    def reveal(self):
        #flip the board for gravity simulation
        return np.flip(self.game, 0)

    def gen_playing_field(self):
        #Generate the board
        pg.draw.rect(self.screen, (0, 0, 0), (self.width, 0 , self.width * 0.286, self.boardSegment))
        #Update the board with metrics by blacking out old values
        pg.draw.rect(self.screen, (0, 0, 0), (self.width, 175 , self.width * 0.286, 15))
        pg.draw.rect(self.screen, (0, 0, 0), (self.width, 235 , self.width * 0.286, 15))
        pg.draw.rect(self.screen, (0, 0, 0), (self.width, 400 , self.width * 0.286, 15))
        #Create sidebar and buttons
        algTypeLabel = self.fonts[3].render("Algorithm:", 1, (100, 130, 255))
        runTimeLabel = self.fonts[3].render("Run Time (s):", 1, (100, 130, 255))
        startTxt = self.fonts[3].render("Start", 1, (100, 130, 255))
        restartTxt = self.fonts[3].render("Restart", 1, (100, 130, 255))
        exitTxt = self.fonts[3].render("Exit", 1, (100, 130, 255))
        runTimeTxt = self.fonts[3].render(str(round((self.runTime), 2)), 1, (100, 130, 255))
        nodeLabel = self.fonts[3].render("Nodes :", 1, (100, 130, 255))
        nodeTxt = self.fonts[3].render(str(self.alg.nodeCount), 1, (100, 130, 255))
        if self.alg.type == "Alpha Beta Pruning":
            algType1 = self.fonts[3].render("Alpha Beta", 1, (100, 130, 255))
            algType2 = self.fonts[3].render("Pruning", 1, (100, 130, 255))
            self.screen.blit(algType1, (590, 105))
            self.screen.blit(algType2, (590, 125))
        else:
            algType = self.fonts[3].render(self.alg.type, 1, (100, 130, 255))
            algTypeLabel = self.fonts[3].render("Algorithm:", 1, (100, 130, 255))
            self.screen.blit(algType, (590, 105))
        self.screen.blit(algTypeLabel, (590, 85))
        self.screen.blit(runTimeLabel, (590, 155))
        self.screen.blit(runTimeTxt, (590, 175))
        self.screen.blit(nodeLabel, (590, 215))
        self.screen.blit(nodeTxt, (590, 235))
        self.screen.blit(startTxt, (590, 400))
        self.screen.blit(restartTxt, (590, 430))
        self.screen.blit(exitTxt, (590, 460))
        #Create individual wells and assign colors to pieces
        if self.playerTurn == True:
            turnText = self.fonts[3].render("Player Turn", 1, (150, 0, 0))
            self.screen.blit(turnText, (600, 40))
        for i in range(self.matrix[0]):
            for j in range(self.matrix[1]):
                #Wells and Board Creation
                pg.draw.rect(self.screen, (100, 130, 255), (j*self.boardSegment, i*self.boardSegment + self.boardSegment, self.boardSegment, self.boardSegment))
                pg.draw.circle(self.screen, (0, 0, 0), (int(j * self.boardSegment + self.boardSegment/2), int(i * self.boardSegment + self.boardSegment + self.boardSegment/2)), self.radius )
        for i in range(self.matrix[0]):
            for j in range(self.matrix[1]):
                #Add new pieces and track current pieces
                if self.game[i, j] == self.player[1]:
                    pg.draw.circle(self.screen, (150, 0, 0), (int(j * self.boardSegment + self.boardSegment/2), self.height - int(i * self.boardSegment + self.boardSegment/2)), self.radius )
                elif self.game[i, j] == self.player[2]:
                    pg.draw.circle(self.screen, (200, 200, 0), (int(j * self.boardSegment + self.boardSegment/2), self.height - int(i * self.boardSegment + self.boardSegment/2)), self.radius )
        pg.display.update()

    def draw_cursor(self, event):
        #Draw cursor whereever the player moves it, while remaining within the well.
        pg.draw.rect(self.screen, (0, 0, 0), (0,0, self.width, self.boardSegment))
        if event.pos[0] >= 560:
            place = 560
        else: 
            place = event.pos[0]
        for p in range(self.matrix[1]):
            if place <= self.boardSegment*p + self.boardSegment:
                place = self.boardSegment*p + self.boardSegment/2
                break
        #Create triangle shape
        point1 = (place - 20, 30)
        point2 = (place + 20 , 30)
        point3 = (place, 50)
        pg.draw.polygon(self.screen, (150, 0, 0), (point1, point2, point3))
        pg.display.update()

    def playerMove(self, event):
        #Handle player click event.
        place = event.pos[0] 
        well = int(math.floor(place/self.boardSegment))
        if self.alg.is_open(self.game, well):
            row = self.alg.gravity(self.game, well)
            self.alg.place_puck(self.game, row, well, self.player[1])
            if self.alg.win(self.game, self.player[1]):
                #Print the winner of the match
                label = self.fonts[0].render("Player 1 wins!!", 1, (100, 130, 255))
                self.screen.blit(label, (40, 10))
                pg.display.update()
                self.gen_playing_field()
                #Wait for realistic feel.
                pg.time.wait(1800)
                self.winner = True
        self.playerTurn = not self.playerTurn
        self.gen_playing_field()

    def startMessage(self):
            label = self.fonts[0].render("Press Start to Begin!", 1, (100, 130, 255))
            self.screen.blit(label, (40, 10))

    def restartMessage(self):
            label = self.fonts[0].render("Press Restart to Continue!", 1, (100, 130, 255))
            self.screen.blit(label, (40, 10))

    def ai_turn(self):
        self.alg.nodeCount = 0
        start = ti.perf_counter()
        pg.draw.rect(self.screen, (0, 0, 0), (self.width, 0 , self.width * 0.286, self.boardSegment))
        turnText = self.fonts[3].render("Opponent Turn", 1, (200, 200, 0))
        self.screen.blit(turnText, (580, 40))
        well = self.alg.get_move(self.game) 
        place = (self.boardSegment * well)
        for p in range(self.matrix[1]):
            if place < self.boardSegment * p + self.boardSegment:
                place = self.boardSegment * p + self.boardSegment/2
                break
        #Draw pulsing indicator
        point1 = (place - 20, 30)
        point2 = (place + 20 , 30)
        point3 = (place, 50)
        for l in range(0,3):
            pg.draw.rect(self.screen, (0, 0, 0), (0,0, self.width, self.boardSegment))
            pg.display.update()
            #Pusling behavior
            pg.time.wait(300)
            pg.draw.polygon(self.screen, (200, 200, 0), (point1, point2, point3))
            pg.display.update()
            pg.time.wait(300)
        if self.alg.is_open(self.game, well):
            pg.time.wait(400)
            row = self.alg.gravity(self.game, well)
            self.alg.place_puck(self.game, row, well, self.player[2])
            pg.display.update()
            pg.time.wait(400)
            if self.alg.win(self.game, self.player[2]):
                #Print the winner of the match
                label = self.fonts[0].render("Player 2 wins!!", 1, (100, 130, 255))
                self.screen.blit(label, (40, 10))
                pg.display.update()
                self.gen_playing_field()
                pg.time.wait(1800)
                self.winner = True
        self.playerTurn = not self.playerTurn
        #update time running for algorithm
        self.runTime = ti.perf_counter() - start
        self.gen_playing_field()

    def get_event(self, event):
        #Main event loop, reaact to mouse imputs
        if event.type == pg.MOUSEMOTION:
            if self.playerTurn == True:
                self.draw_cursor(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            #Initiate button clicks
                if event.pos[1] >= 460 and event.pos[1] < 490:
                    return "Exit"
                elif event.pos[1] >= 430 and event.pos[1] < 460 :
                    return "Restart"
                elif self.winner == True:
                    #if win, pause game and send information to main method
                    return "Won" 
                elif self.playerTurn == True:
                    self.playerMove(event)

    def ai_event(self):
        #Run ai turn
        if self.playerTurn == False and not self.dead:
            self.ai_turn()