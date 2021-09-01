from random  import randint
from random  import shuffle
from board   import Board
from board   import other_player
#from rich    import print
from time    import sleep
from _thread import start_new_thread

from enemies import PishTerminator
from enemies import SemiPish
from enemies import Terminator
from enemies import PishIdek
from enemies import TukeAI
from enemies import Windows
from enemies import Human
from enemies import Pear

DELAY = 0
RANDOM_START = True
ROUNDS = 1
MINIROUNDS = 2
PRINT = False
THREADS = 24
game_count = 0

def AIPlay(Class1, Class2, human: bool = False) -> int:
    global game_count
    #enemies = [TukeHeuristic("TukeAI"), TukeHeuristic("Obama Tuke")]
    enemies = [Class1(), Class2()]

    if PRINT:
        for enemy in enemies:
            enemy.PRINT = True

    shuffle(enemies)
    board   = Board(7, 6)
    board   .exits = False

    def Turn(enemy):
        if PRINT:
            print(enemy.name)
        x = enemy.Play(board)
        if PRINT:
            board.Print()
            print("=" + "=="*board.w + "\n")

        if DELAY != 0:
            sleep(DELAY)

        return x

    # random start
    if RANDOM_START:
        for _ in range(randint(2, 5) * 2):
            while True:
                move = randint(0, 6)
                if board.ValidMove(move):
                    board.Place(move)
                    break

    i = 0
    last_move = 0
    while not board.over:
        last_move = Turn(enemies[i % len(enemies)])
        i += 1

    game_count += 1

    if not board.draw:
        if human:
            #board.Print()
            print(f"last move: {last_move}")
        print(f"game over! enemy {board.player}, aka {enemies[other_player(board.player) - 1].name} won\n")
        return enemies[other_player(board.player) - 1].name
    else:
        print(f"draw!")
        return "Draw"

TOURNAMENT = True

if TOURNAMENT:
    win_board = {
        "Draw": 0
    }
    names = ["Tukeque", "Pishle", "Terminator", "Pishle's epic ai, aka Terminator", "borkthing", "Windows", "Pear"]
    for i in names:
        win_board[i] = 0

    classes = [Pear, Windows]

    finisheds = [False for _ in range(THREADS)]

    def thread(identifier: int, happy: bool):
        global win_board

        if len(classes) == 2:
            for _ in range(ROUNDS):
                win_board[AIPlay(classes[0], classes[1])] += 1
        else:
            for i in range(MINIROUNDS):
                for i in classes:
                    for j in classes:
                        win_board[AIPlay(i, j)] += 1

        finisheds[identifier] = True

        if happy:
            print(f"happyly exited ! {game_count}")
            print(finisheds)

    for i in range(THREADS):
        start_new_thread(thread, (i, True))

    while finisheds.count(False) != 0:
        pass

    print(win_board)
    print(game_count)
else:
    RANDOM_START = False

    PRINT = True
    import board
    board.BIG_EXITS   = True
    board.BIG_PRINTS = True
    AIPlay(Pear, Windows)
