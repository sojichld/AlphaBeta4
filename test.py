# UNC Charlotte
# ITCS 5153 - Applied AI - Fall 2022
# Lab 3
# Adversarial Search / Game Playing
# This module implements …
# Student ID: 800966330

import numpy as np
import pygame
import sys
import math
import random

#Initialize game matrix
def makeGame():
    return np.zeros((MATRIX[0],MATRIX[1]))


#Add the puck to the game board.
def placePuck(game, row, well, puck):
    game[row][well] = puck


#Contralateral flip.
def reveal(game):
    return np.flip(game, 0)

#Check final well.
def isOpen(game, well):
    return game[MATRIX[0]-1][well] == 0

#Fall to the last open row.
def gravity(game, well):
    for i in range(MATRIX[0]):
        if game[i][well] == 0:
            return i

def win(game, puck):
    for j in range(MATRIX[1]-3):
        for i in range(MATRIX[0]):
            if game[i][j] == puck and game[i][j+1] == puck and game[i][j+2] == puck and game[i][j+3] == puck:
                return True
    for j in range(MATRIX[1]):
        for i in range(MATRIX[0]-3):
            if game[i][j] == puck and game[i+1][j] == puck and game[i+2][j] == puck and game[i+3][j] == puck:
                return True
    for j in range(MATRIX[1]-3):
        for i in range(MATRIX[0]-3):
            if game[i][j] == puck and game[i+1][j+1] == puck and game[i+2][j+2] == puck and game[i+3][j+3] == puck:
                return True
    for j in range(MATRIX[1] - 3):
        for i in range(3, MATRIX[0]):
            if game[i][j] == puck and game[i-1][j+1] == puck and game[i-2][j+2] == puck and game[i-3][j+3] == puck:
                return True

def evaluate(percept, puck):
    value = 0
    if puck == player[1]:
        enemyPuck == player[2]
    else:
        enemyPuck = player[1]
    for i in range(4, 1, -1):
        if percept.count(puck) == i and percept.count(player[0]) == 4 - i:
            value += 5 ** i
            break
    for i in range(4, 1, -1):
        if percept.count(enemyPuck) == i and percept.count(player[0]) == 4 - i:
            value -= 4 ** i
            break
    return value

#visualize board
def heuristic(game, puck):
    value = 0
    stack = [int(u) for u in list(game[:, MATRIX[1]//2])]
    percept = stack.count(puck)
    value += 6*percept
    for r in range(MATRIX[0]):
        rows = [int(x) for x in list(game[r,:])]
        for l in range(MATRIX[1]-3):
            percept = rows[l:l + 4]
            value += evaluate(percept, puck)
    for c in range(MATRIX[1]):
        wells = [int(x) for x in list(game[:,c])]
        for l in range(MATRIX[0]-3):
            percept = wells[l:l + 4]
            value += evaluate(percept, puck)
    for r in range(MATRIX[0] - 3):
        for c in range(MATRIX[1] -3):
            percept = [game[r+i][c+i] for i in range(4)]
            value += evaluate(percept, puck)
    for r in range(MATRIX[0] - 3):
        for c in range(MATRIX[1] -3):
            percept = [game[r+3-i][c+i] for i in range(4)]
            value += evaluate(percept, puck)
    return value

def isTerminal(game):
    return win(game, player[1]) or win(game, player[2]) or len(considerMoves(game)) == 0
        
def minmax(game, depth, playerMax):
    moves = considerMoves(game)
    terminal = isTerminal(game)
    if depth == 0 or terminal:
        if terminal:
            if win(game, player[2]):
                return (None, math.inf)
            elif win(game, player[1]):
                return (None, -math.inf)
            else:
                return (None, 0)
        else:
            return (None, heuristic(game, player[2]))
    if playerMax:
        value = -math.inf
        choice = random.choice(moves)
        for i in moves:
            row = gravity(game, i)
            mind_game = game.copy()
            placePuck(mind_game, row, i, player[2])
            nextValue = minmax(mind_game, depth - 1, False)[1]
            if nextValue > value:
                value = nextValue
                choice = i
        return choice, value
    else:
        value = math.inf
        choice = random.choice(moves)
        for j in moves:
            row = gravity(game, j)
            mind_game = game.copy()
            placePuck(mind_game, row, j, player[1])
            nextValue = minmax(mind_game, depth - 1, True)[1]
            if nextValue < value:
                value = nextValue
                choice = j
        return choice, value

def alphabetaprune(game, depth, alpha, beta, playerMax):
    moves = considerMoves(game)
    terminal = isTerminal(game)
    if depth == 0 or terminal:
        if terminal:
            if win(game, player[2]):
                return (None, math.inf)
            elif win(game, player[1]):
                return (None, -math.inf)
            else:
                return (None, 0)
        else:
            return (None, heuristic(game, player[2]))
    if playerMax:
        value = -math.inf
        choice = random.choice(moves)
        for i in moves:
            row = gravity(game, i)
            mind_game = game.copy()
            placePuck(mind_game, row, i, player[2])
            nextValue = alphabetaprune(mind_game, depth - 1, alpha, beta, False)[1]
            if nextValue > value:
                value = nextValue
                choice = i
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return choice, value
    else:
        value = math.inf
        choice = random.choice(moves)
        for j in moves:
            row = gravity(game, j)
            mind_game = game.copy()
            placePuck(mind_game, row, j, player[1])
            nextValue = alphabetaprune(mind_game, depth - 1, alpha, beta, True)[1]
            if nextValue < value:
                value = nextValue
                choice = j
            beta = min(beta, value)
            if alpha >= beta:
                break
        return choice, value


def considerMoves(game):
    posibilities = []
    for j in range(MATRIX[1]):
        if isOpen(game, j):
            posibilities.append(j)
    print(posibilities)
    return posibilities

def action(game, puck):
    highestVal = -math.inf
    posibilities = considerMoves(game)
    choice = random.choice(posibilities)
    for p in posibilities:
        row = gravity(game, p)
        mindGame = game.copy()
        placePuck(mindGame, row, p, puck)
        value = heuristic(mindGame, puck)
        if value > highestVal:
            highestVal = value
            choice = p
    #print(posibilities)
    #print(highestVal)
    return choice


def generatePlayingField(game):
    for i in range(MATRIX[0]):
        for j in range(MATRIX[1]):
            pygame.draw.rect(screen, (100, 130, 255), (j*boardSegment, i*boardSegment + boardSegment, boardSegment, boardSegment))
            if game[i, j] == player[0]:
                pygame.draw.circle(screen, (0, 0, 0), (int(j * boardSegment + boardSegment/2), int(i * boardSegment + boardSegment + boardSegment/2)), r )
            if game[i, j] == player[1]:
                pygame.draw.circle(screen, (150, 0, 0), (int(j * boardSegment + boardSegment/2), int(i * boardSegment + boardSegment + boardSegment/2)), r )
            elif game[i, j] == player[2]:
                pygame.draw.circle(screen, (200, 200, 0), (int(j * boardSegment + boardSegment/2), int(i * boardSegment + boardSegment + boardSegment/2)), r )
            pygame.display.update()





MATRIX = [6, 7]
dead = False
playerTurn = random.choice([True, False])
game = makeGame()
#print(reveal(game))

pygame.init()
player = [0, 1, 2]
boardSegment = 80
width = MATRIX[1] * boardSegment
height = (MATRIX[0]+1) * boardSegment

size = (width, height)
r = int(boardSegment / 2 - 5)

screen = pygame.display.set_mode(size)
generatePlayingField(game)
pygame.display.update()

font = pygame.font.SysFont("calibri", 50)

#Run
while not dead:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            if playerTurn == True:
                pygame.draw.rect(screen, (0, 0, 0), (0,0, width, boardSegment))
                place = event.pos[0]
                for p in range(MATRIX[1]):
                    if place <= boardSegment*p + boardSegment:
                        place = boardSegment*p + boardSegment/2
                        break
                point1 = (place - 20, 30)
                point2 = (place + 20 , 30)
                point3 = (place, 50)
                pygame.draw.polygon(screen, (150, 0, 0), (point1, point2, point3))
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if playerTurn == True:
                place = event.pos[0] 
                well = int(math.floor(place/boardSegment))
                if isOpen(game, well):
                    row = gravity(game, well)
                    placePuck(game, row, well, player[1])
                    if win(game, player[1]):
                        label = font.render("Player 1 wins!!", 1, (100, 130, 255))
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        generatePlayingField(game)
                        pygame.time.wait(1800)
                        dead = True
                playerTurn = not playerTurn
                generatePlayingField(game)
                #print(reveal(game))

    if playerTurn == False and not dead:
        #well = action(game, player[2])
        #well, value = minmax(game, 3, True)
        well, value = alphabetaprune(game, 5, -math.inf, math.inf, True)
        place = (boardSegment * well)
        for p in range(MATRIX[1]):
            if place < boardSegment * p + boardSegment:
                place = boardSegment * p + boardSegment/2
                break
        point1 = (place - 20, 30)
        point2 = (place + 20 , 30)
        point3 = (place, 50)
        for l in range(0,3):
            pygame.draw.rect(screen, (0, 0, 0), (0,0, width, boardSegment))
            pygame.display.update()
            pygame.time.wait(300)
            pygame.draw.polygon(screen, (200, 200, 0), (point1, point2, point3))
            pygame.display.update()
            pygame.time.wait(300)
        if isOpen(game, well):
            pygame.time.wait(400)
            row = gravity(game, well)
            placePuck(game, row, well, player[2])
            pygame.display.update()
            pygame.time.wait(400)
            if win(game, player[2]):
                label = font.render("Player 2 wins!!", 1, (100, 130, 255))
                screen.blit(label, (40, 10))
                pygame.display.update()
                generatePlayingField(game)
                pygame.time.wait(1800)
                dead = True
        playerTurn = not playerTurn
        generatePlayingField(game)
        #print(reveal(game))

