# UNC Charlotte
# ITCS 5153 - Applied AI - Fall 2022
# Lab 3
# Adversarial Search / Game Playing
# This module implements …
# Student ID: 800966330

import math
import random


class Algorithm(object):
    def __init__(self,  matrix, player, ai_type = "Alpha Beta Pruning"):
        self.matrix = matrix
        self.player = player
        self.type = ai_type
        self.AI = ai_type
        self.nodeCount = 0

    def get_move(self, game):
        #get the type of ai opponent and return the given move choice
        if self.AI == "Alpha Beta Pruning":
            well, value = self.alpha_beta_prune(game, 4, -math.inf, math.inf, True)
        elif self.AI == "Minimax":
            well, value = self.minmax(game, 4, True)
        else:
            well = self.action(game, self.player[2])
        return well

    def is_open(self, game, well):
        #check if matrix position is viable
        return game[self.matrix[0]-1][well] == 0

    def gravity(self, game, well):
        #get the lowest row position in the given well
        for i in range(self.matrix[0]):
            if game[i][well] == 0:
                return i
    def place_puck(self, game, row, well, puck):
        #place the puck in the game model
        game[row][well] = puck

    def win(self, game, puck):
        #check diagonal, and vertical positions and if a player has won, return
        for j in range(self.matrix[1]-3):
            for i in range(self.matrix[0]):
                if game[i][j] == puck and game[i][j+1] == puck and game[i][j+2] == puck and game[i][j+3] == puck:
                    return True
        for j in range(self.matrix[1]):
            for i in range(self.matrix[0]-3):
                if game[i][j] == puck and game[i+1][j] == puck and game[i+2][j] == puck and game[i+3][j] == puck:
                    return True
        for j in range(self.matrix[1]-3):
            for i in range(self.matrix[0]-3):
                if game[i][j] == puck and game[i+1][j+1] == puck and game[i+2][j+2] == puck and game[i+3][j+3] == puck:
                    return True
        for j in range(self.matrix[1] - 3):
            for i in range(3, self.matrix[0]):
                if game[i][j] == puck and game[i-1][j+1] == puck and game[i-2][j+2] == puck and game[i-3][j+3] == puck:
                    return True

    def evaluate(self, percept, puck):
        #evaluate the total value of a particular game state, return the value
        self.nodeCount += 1
        value = 0
        if puck == self.player[1]:
            enemyPuck == self.player[2]
        else:
            enemyPuck = self.player[1]
        for i in range(4, 1, -1):
            if percept.count(puck) == i and percept.count(self.player[0]) == 4 - i:
                value += 5 ** i
                break
        for i in range(4, 1, -1):
            if percept.count(enemyPuck) == i and percept.count(self.player[0]) == 4 - i:
                value -= 3 ** i
                break
        return value

#visualize board
    def heuristic(self, game, puck):
        # retrieve the various game states in the board per turn and evaluate them
        value = 0
        stack = [int(u) for u in list(game[:, self.matrix[1]//2])]
        percept = stack.count(puck)
        value += 6*percept
        for r in range(self.matrix[0]):
            rows = [int(x) for x in list(game[r,:])]
            for l in range(self.matrix[1]-3):
                percept = rows[l:l + 4]
                value += self.evaluate(percept, puck)
        for c in range(self.matrix[1]):
            wells = [int(x) for x in list(game[:,c])]
            for l in range(self.matrix[0]-3):
                percept = wells[l:l + 4]
                value += self.evaluate(percept, puck)
        for r in range(self.matrix[0] - 3):
            for c in range(self.matrix[1] -3):
                percept = [game[r+i][c+i] for i in range(4)]
                value += self.evaluate(percept, puck)
        for r in range(self.matrix[0] - 3):
            for c in range(self.matrix[1] -3):
                percept = [game[r+3-i][c+i] for i in range(4)]
                value += self.evaluate(percept, puck)
        return value

    def isTerminal(self, game):
        #if a node is terminal return winning conditions
        return self.win(game, self.player[1]) or self.win(game, self.player[2]) or len(self.consider_moves(game)) == 0
        
    def minmax(self, game,  depth, playerMax):
        #minimax implementation
        moves = self.consider_moves(game)
        terminal = self.isTerminal(game)
        if depth == 0 or terminal:
            if terminal:
                if self.win(game, self.player[2]):
                    return (None, math.inf)
                elif self.win(game, self.player[1]):
                    return (None, -math.inf)
                else:
                    return (None, 0)
            else:
                return (None, self.heuristic(game, self.player[2]))
        if playerMax:
            value = -math.inf
            choice = random.choice(moves)
            for i in moves:
                row = self.gravity(game, i)
                mind_game = game.copy()
                self.place_puck(mind_game, row, i, self.player[2])
                nextValue = self.minmax(mind_game, depth - 1, False)[1]
                if nextValue > value:
                    value = nextValue
                    choice = i
            return choice, value
        else:
            value = math.inf
            choice = random.choice(moves)
            for j in moves:
                row = self.gravity(game, j)
                mind_game = game.copy()
                self.place_puck(mind_game, row, j, self.player[1])
                nextValue = self.minmax(mind_game, depth - 1, True)[1]
                if nextValue < value:
                    value = nextValue
                    choice = j
            return choice, value

    def alpha_beta_prune(self, game, depth, alpha, beta, playerMax):
        #alpha beta pruning implementation
        moves = self.consider_moves(game)
        terminal = self.isTerminal(game)
        if depth == 0 or terminal:
            if terminal:
                if self.win(game, self.player[2]):
                    return (None, math.inf)
                elif self.win(game, self.player[1]):
                    return (None, -math.inf)
                else:
                    return (None, 0)
            else:
                return (None, self.heuristic(game, self.player[2]))
        if playerMax:
            value = -math.inf
            choice = random.choice(moves)
            for i in moves:
                row = self.gravity(game, i)
                mind_game = game.copy()
                self.place_puck(mind_game, row, i, self.player[2])
                nextValue = self.alpha_beta_prune(mind_game, depth - 1, alpha, beta, False)[1]
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
                row = self.gravity(game, j)
                mind_game = game.copy()
                self.place_puck(mind_game, row, j, self.player[1])
                nextValue = self.alpha_beta_prune(mind_game, depth - 1, alpha, beta, True)[1]
                if nextValue < value:
                    value = nextValue
                    choice = j
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return choice, value

    def consider_moves(self, game):
        #get viable moves
        posibilities = []
        for j in range(self.matrix[1]):
            if self.is_open(game, j):
                posibilities.append(j)
        return posibilities

    def action(self, game, puck):
        #general general heuristic method implementation
        highestVal = -math.inf
        posibilities = self.consider_moves(game)
        choice = random.choice(posibilities)
        for p in posibilities:
            row = self.gravity(game, p)
            mind_game = game.copy()
            self.place_puck(mind_game, row, p, puck)
            value = self.heuristic(mind_game, puck)
            if value > highestVal:
                highestVal = value
                choice = p
        return choice

