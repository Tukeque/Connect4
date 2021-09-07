from rich import print

CHARACTERS = ["[white]. ", "[blue]X ", "[red]O "]

def other_player(player: int):
    return {
        1: 2,
        2: 1
    }[player]

class Board:
    over  = False
    main  = False
    draw  = False

    def Generate(self):
        self.board = []
        for _ in range(self.w):
            self.board.append([0] * self.h)

    def ValidMove(self, i) -> int:
        last_empty_index = -1

        for y in range(self.h):
            if self.board[i][y] != 0: break
            last_empty_index = y

        return last_empty_index

    def Place(self, i):
        possibles: list[bool] = []
        for j in range(7):
            possibles.append(self.ValidMove(j) != -1)

        if possibles.count(True) >= 1:
            last_empty_index = self.ValidMove(i)

            if last_empty_index != -1:
                self.board[i][last_empty_index] = self.player   # place
                self.over = self.CheckWin(self.player)          # update win bool
                self.player = other_player(self.player)         # change player
            else:
                if self.main:
                    print("cant place move")
        else:
            if self.main:
                print("its a draw!")
                self.Print()
                exit()

            self.over = True
            self.draw = True

    def Remove(self, i):
        last_empty_index = -1

        for y in range(self.h):
            last_empty_index = y
            if self.board[i][y] != 0: break
        
        self.board[i][last_empty_index] = 0 # overwrite
        self.player = other_player(self.player)  # change player

    def __init__(self, w: int, h: int, main: bool = False):
        self.w = w
        self.h = h
        self.player = 1
        self.Generate()
        self.main = main

    def CheckRelative(self, x: int, y: int, xvec: int, yvec: int, player: bool, N: int):
        #N = 4 # this is big brain yes dynamic
        count = 0
        for _ in range(N):
            if x >= self.w or y >= self.h or x < 0 or y < 0:
                return False
            if self.board[x][y] == player:
                count += 1
            x += xvec
            y += yvec
            
        if count >= N:
            return True

    def CheckRelativeNotOther(self, x: int, y: int, xvec: int, yvec: int, player: bool, N: int):
        #N = 4 # this is big brain yes dynamic
        count = 0
        for _ in range(N):
            if x >= self.w or y >= self.h or x < 0 or y < 0:
                return False
            if self.board[x][y] != other_player(player):
                count += 1
            x += xvec
            y += yvec
            
        if count >= N:
            return True
    
    def CheckVariable(self, N: int, player: int) -> int:
        count = 0

        for x in range(self.w):
            for y in range(self.h):
                coords = [[1, 0], [0, 1], [1, 1], [1, -1]]
                
                for coord in coords:
                    if self.CheckRelative(x, y, coord[0], coord[1], player, N):
                        count += 1
        return count

    def CheckWin(self, player: int, N: int = 4) -> bool:
        n = self.CheckVariable(N, player)   # big brain

        if n >= 1:
            if self.main:
                self.Print()
                print(CHARACTERS[self.player] + "[green] won!")
                exit()
            return True
        return False

    def CheckPossibleWins(self, player: int, N: int = 4) -> bool:
        count = 0

        for x in range(self.w):
            for y in range(self.h):
                coords = [[1, 0], [0, 1], [1, 1], [1, -1]]
                
                for coord in coords:
                    if self.CheckRelativeNotOther(x, y, coord[0], coord[1], player, N):
                        count += 1
        return count

    def Print(self):
        for y in range(self.h):
            row_string = " "
            for x in range(self.w):
                row_string += CHARACTERS[self.board[x][y]]
            print(row_string)

        bottom = "[blue]-"
        for i in range(self.w):
            bottom += f"{i}-" # ye
        print(bottom)