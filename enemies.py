from copy   import deepcopy as copy
from random import randint
from board  import Board, other_player
from board  import CHARACTERS
from rich   import print
import gc

class Enemy:
    name = ""

    def __init__(self, name: str = "Obama's Big Chungus Pet"):
        self.name = name

    def Heuristic(self, board: Board) -> int: # evaluate positions and choose best move
        return 0

    def Play(self, board: Board):
        move: int = self.Heuristic(board)
        board.Place(move)
        return move

class RandomHeuristic(Enemy):
    def Heuristic(self, board: Board) -> int:
        while True:
            x = randint(0, 6)
            if board.ValidMove(x) != -1:
                return x

class Heuristic3(Enemy):
    def Heuristic(self, board: Board) -> int:
        return 0 # overwriting our own heuristic
#^ repeat for however many heuristics

class Human(Enemy):
    def Heuristic(self, board: Board) -> int:
        while True:
            x = int(input("human pls choose: ")) # kek
            if x in range(board.w) and board.ValidMove(x) != -1:
                return x
            else:
                print("pls choose a valid move fuckin idiot")

class MinMax(Enemy):
    WIN_BONUS = 20
    DEPTH = 4
    PRINT = False

    def Score(self, move: int, board: Board) -> tuple[int, bool]:
        score = 0

        return (score, False)

    def Evaluate(self, move: int, board: Board, depth: int, mult: int) -> tuple[int, bool]:
        score, won = self.Score(move, board)

        if won:
            return (score * mult, True)
            
        score *= mult

        if depth != 0: # generate child evaluators
            score += self.MinMax(board, depth - 1, -mult)[1]

        return (score, False)

    def MinMax(self, board: Board, depth: int, mult: int, big: bool = False) -> tuple[int, int]: # returns (min/max  move, score)
        boards = {}

        for i in range(7):
            if board.ValidMove(i) != -1:
                boards[i] = {
                    "board": copy(board)
                }
                boards[i]["board"].child = True
                boards[i]["board"].Place(i)
                #boards[i]["score"] = 1
                boards[i]["score"] = self.Evaluate(i, boards[i]["board"], depth, mult)

                if boards[i]["score"][1]:
                    return (i, boards[i]["score"][0])

        keys = list(boards.keys())
        if len(keys) == 0: return (0, 0)

        best = keys[0]
        for key in keys:
            del boards[key]['board']

            if mult == 1:
                if boards[best]["score"][0] < boards[key]["score"][0]:
                    best = key
            elif mult == -1:
                if boards[best]["score"][0] > boards[key]["score"][0]:
                    best = key

        gc.collect() # i need my ram

        if big:
            if self.PRINT:
                print(f"[yellow]scores: {[boards[score]['score'][0] for score in boards]}")

        return (best, boards[best]['score'][0])

    def Heuristic(self, board: Board) -> int:
        
        result = self.MinMax(board, self.DEPTH - 1, 1, True)
        move = result[0]
        if self.PRINT:
            print(f"best score: {result[1]}")

        return move

class TukeAI(MinMax):
    WIN_BONUS = 15
    PIECE_BELOW_BONUS = 2

    def __init__(self):
        self.name = "Tukeque"

    def Score(self, move: int, board: Board) -> tuple[int, bool]: # (score, win)
        score = 0

        if board.CheckWin(other_player(board.player)):
            score += self.WIN_BONUS
            return (score, True)
        
        if move <= 3:
            score += move
        else: # score > 3
            score += 6 - move

        column = board.board[move]
        piece_below = 0
        for i in range(5):
            if column[5 - i] != CHARACTERS[0]:
                if 5 - i >= 1:
                    piece_below = column[5 - i - 1]
                break

        if piece_below != 0:
            if piece_below == board.player:
                score += self.PIECE_BELOW_BONUS
        
        return (score, False)

class SemiPish(MinMax):
    WIN_BONUS         = 15
    PIECE_BELOW_BONUS = 1
    ROW2_BONUS        = 0.5
    ROW3_BONUS        = 1
    VERTICAL_BONUS    = 1

    def __init__(self):
        self.name = "Pishle"

    def Score(self, move: int, board: Board) -> tuple[int, bool]:
        score = 0

        # wins
        if board.CheckWin(other_player(board.player)):
            score += self.WIN_BONUS
            return (score, True)
        
        # center bias
        if move <= 3:
            score += move
        else: # score > 3
            score += 6 - move

        # piece below bonus
        column = board.board[move]
        piece_below = 0
        last_piece  = -1
        for i in range(5):
            if column[5 - i] != CHARACTERS[0]:
                last_piece = 5 - i
                if 5 - i >= 1:
                    piece_below = column[5 - i - 1]
                break

        if piece_below != 0:
            if piece_below == board.player:
                score += self.PIECE_BELOW_BONUS
        
        # 2 in a row
        row2 = board.CheckVariable(2, True)
        if row2 != 0:
            score += row2 * self.ROW2_BONUS
    
        # 3 in a row
        row3 = board.CheckVariable(3, True)
        if row3 != 0:
            score += row3 * self.ROW3_BONUS

        # vertical win space check
        if last_piece != -1:
            if last_piece <= 1:
                score += self.VERTICAL_BONUS

        return (score, False)

class Terminator(MinMax):
    WIN_BONUS         = 15
    PIECE_BELOW_BONUS = 1
    ROW3_BONUS        = 1
    VERTICAL_BONUS    = 1

    def __init__(self):
        self.name = "Terminator"

    def Score(self, move: int, board: Board) -> tuple[int, bool]:
        score = 0

        # wins
        if board.CheckWin(other_player(board.player)):
            score += self.WIN_BONUS
            return (score, True)
        
        # center bias
        if move <= 3:
            score += move
        else: # score > 3
            score += 6 - move

        # piece below bonus
        column = board.board[move]
        piece_below = 0
        last_piece  = -1
        for i in range(5):
            if column[5 - i] != CHARACTERS[0]:
                last_piece = 5 - i
                if 5 - i >= 1:
                    piece_below = column[5 - i - 1]
                break

        if piece_below != 0:
            if piece_below == board.player:
                score += self.PIECE_BELOW_BONUS
    
        # 3 in a row
        row3 = board.CheckVariable(3, True)
        if row3 != 0:
            score += row3 * self.ROW3_BONUS

        # vertical win space check
        if last_piece != -1:
            if last_piece <= 1:
                score += self.VERTICAL_BONUS

        return (score, False)

import math

class PishTerminator(MinMax):
    def __init__(self):
        self.name = "Pishle's epic ai, aka Terminator"

    def Score(self, move: int, board: Board) -> tuple[int, bool]:
        # wins
        if board.CheckWin(other_player(board.player)):
            return (math.inf, True)
    
        def gen_quads():
            for r in range(6):
                for c in range(4):
                    yield True, (r, c), (r, c + 1), (r, c + 2), (r, c + 3)
            for r in range(3):
                for c in range(7):
                    yield False, (r, c), (r + 1, c), (r + 2, c), (r + 3, c)
            for r in range(3):
                for c in range(4):
                    yield (True, (r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3))
                    yield (True, (r + 3, c), (r + 2, c + 1), (r + 1, c + 2), (r, c + 3))

        score = 0
        for over, *pts in gen_quads():
            pieces = [board.board[c][r] for r, c in pts]
            p1 = 0
            for p in pieces:
                if p == 1:
                    p1 += 1
                    
            p2 = 0
            for p in pieces:
                if p == -1:
                    p2 += 1

            assert 0 <= p1 <= 3
            assert 0 <= p2 <= 3

            if p1 == p2 == 0:
                pass
            elif p2 == 0:
                if p1 == 2:
                    score += 1
                elif p1 == 3:
                    if over:
                        score += 3           
            elif p1 == 0:
                if p2 == 2:
                    score -= 1
                elif p2 == 3:
                    if over:
                        score -= 3
        return (score, False)

class PishIdek(MinMax):
    def __init__(self):
        self.name = "borkthing"

    def Score(self, move: int, board: Board) -> tuple[int, bool]:
        # wins
        if board.CheckWin(other_player(board.player)):
            return (math.inf, True)
    
        def gen_quads():
            for r in range(6):
                for c in range(4):
                    yield True, (r, c), (r, c + 1), (r, c + 2), (r, c + 3)
            for r in range(3):
                for c in range(7):
                    yield False, (r, c), (r + 1, c), (r + 2, c), (r + 3, c)
            for r in range(3):
                for c in range(4):
                    yield True, (r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3)
                    yield True, (r + 3, c), (r + 2, c + 1), (r + 1, c + 2), (r, c + 3)

        score = 0
        for over, *pts in gen_quads():
            pieces = [board.board[c][r] for r, c in pts]
            p1 = 0
            for p in pieces:
                if p == 1:
                    p1 += 1
                    
            p2 = 0
            for p in pieces:
                if p == -1:
                    p2 += 1

            assert 0 <= p1 <= 3
            assert 0 <= p2 <= 3

            if p1 == p2 == 0:
                pass
            elif p2 == 0:
                score += 1         
            elif p1 == 0:
                score -= 1
        return (score, False)

class Windows(MinMax):
    WIN_BONUS         = 255
    PIECE_BELOW_BONUS = 1
    ROW3_BONUS        = 1
    VERTICAL_BONUS    = 1
    WINCOUNT_BONUS    = 1

    def __init__(self):
        self.name = "Windows"

    def Score(self, move: int, board: Board) -> tuple[int, bool]:
        score = 0

        # wins
        if board.CheckWin(other_player(board.player)):
            score += self.WIN_BONUS
            return (score, True)
        
        # center bias
        if move <= 3:
            score += move
        else: # score > 3
            score += 6 - move

        # piece below bonus
        column = board.board[move]
        piece_below = 0
        last_piece  = -1
        for i in range(5):
            if column[5 - i] != CHARACTERS[0]:
                last_piece = 5 - i
                if 5 - i >= 1:
                    piece_below = column[5 - i - 1]
                break

        if piece_below != 0:
            if piece_below == board.player:
                score += self.PIECE_BELOW_BONUS
    
        # 3 in a row
        row3 = board.CheckVariable(3, True)
        if row3 != 0:
            score += row3 * self.ROW3_BONUS

        # possible wins
        winCount = board.CheckPossibleWins(other_player(board.player))
        if winCount != 0:
            score += winCount * self.WINCOUNT_BONUS

        # vertical win space check
        if last_piece != -1:
            if last_piece <= 1:
                score += self.VERTICAL_BONUS

        return (score, False)

class Pear(MinMax):
    WIN_BONUS         = 255
    PIECE_BELOW_BONUS = 1
    ROW3_BONUS        = 1
    WINCOUNT_BONUS    = 1

    def __init__(self):
        self.name = "Pear"

    def Score(self, move: int, board: Board) -> tuple[int, bool]:
        score = 0

        # wins
        if board.CheckWin(other_player(board.player)):
            score += self.WIN_BONUS
            return (score, True)
        
        # center bias
        if move <= 3:
            score += move
        else: # score > 3
            score += 6 - move

        # piece below bonus
        column = board.board[move]
        piece_below = 0
        last_piece  = -1
        for i in range(5):
            if column[5 - i] != CHARACTERS[0]:
                last_piece = 5 - i
                if 5 - i >= 1:
                    piece_below = column[5 - i - 1]
                break

        if piece_below != 0:
            if piece_below == board.player:
                score += self.PIECE_BELOW_BONUS
    
        # 3 in a row
        row3 = board.CheckVariable(3, True)
        if row3 != 0:
            score += row3 * self.ROW3_BONUS

        # possible wins
        winCount = board.CheckPossibleWins(other_player(board.player))
        if winCount != 0:
            score += winCount * self.WINCOUNT_BONUS

        return (score, False)
