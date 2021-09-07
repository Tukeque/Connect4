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
from enemies import Rebstome
from enemies import Rebstomer
from enemies import RandomHeuristic
from enemies import Rebstomer2Deep
from enemies import Rebstomer3Deep
from enemies import RebstomeLastLayerOptimized

DELAY = 0
RANDOM_START = True
ROUNDS = 3
MINIROUNDS = 10
PRINT = False
THREADS = 12
game_count = 0

def AIPlay(Class1, Class2, human: bool = False) -> int:
    global game_count
    #enemies = [TukeHeuristic("TukeAI"), TukeHeuristic("Obama Tuke")]
    enemies = [Class1(), Class2()]

    if PRINT:
        for enemy in enemies:
            enemy.PRINT = True

    shuffle(enemies)
    board = Board(7, 6)
    board.main = False

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
        for _ in range(randint(1, 5) * 2):
            while True:
                move = randint(0, 6)
                if board.ValidMove(move) != -1:
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
        print(f"game over! enemy {board.player}, aka {enemies[other_player(board.player) - 1].name} won")
        return enemies[other_player(board.player) - 1].name
    else:
        print(f"draw!")
        return "Draw"

TOURNAMENT = True

def make_index(class1, class2) -> str:
    dummy1 = class1()
    dummy2 = class2()
    return f"{dummy1.name} vs {dummy2.name}"

if TOURNAMENT:
    win_board = {
        "Draw": 0
    }
    names = ["RandoMan", "Tukeque", "Pishle", "Terminator", "Pishle's epic ai, aka Terminator", "borkthing", "Windows", "Pear", "Rebstome", "Rebstomer", "Rebstomer 3D", "Rebstomer 2D", "Rebstome Optimized"]
    for i in names:
        win_board[i] = 0

    #classes = [RandomHeuristic, Pear, Rebstome, Rebstomer, Terminator, Windows]
    classes = [RandomHeuristic, TukeAI, Rebstome, Rebstomer, Rebstomer3Deep, RebstomeLastLayerOptimized]
    #classes = [Rebstome, RebstomeLastLayerOptimized]

    if len(classes) == 2:
        win_board[make_index(classes[0], classes[1])] = 0
    else:
        for i in classes:
            for j in classes:
                #name = AIPlay(i, j)
                win_board[make_index(i, j)] = 0

    finisheds = [False for _ in range(THREADS)]

    def thread(identifier: int, happy: bool):
        global win_board

        if len(classes) == 2:
            for _ in range(ROUNDS):
                name = AIPlay(classes[0], classes[1])
                win_board[name] += 1
                win_board[make_index(classes[0], classes[1])] += [classes[0]().name, "Draw", classes[1]().name].index(name) - 1
        else:
            for i in range(MINIROUNDS):
                for i in classes:
                    for j in classes:
                        name = AIPlay(i, j)
                        win_board[name] += 1
                        win_board[make_index(i, j)] += [i().name, "Draw", j().name].index(name) - 1

        finisheds[identifier] = True

        if happy:
            print(f"happyly exited ! {game_count}")
            print(finisheds)

    for i in range(THREADS):
        start_new_thread(thread, (i, True))

    while finisheds.count(False) != 0:
        pass

    new_board = {}
    vs_board = {}
    for key in list(win_board.keys()):
        if key.count("vs") >= 1:
            vs_board[key] = win_board[key]
        else:
            if win_board[key] != 0:
                new_board[key] = win_board[key]
    #print(win_board)
    print(new_board)
    print(vs_board)
    #print(f"game count: {game_count}")
else:
    RANDOM_START = False

    PRINT = True
    AIPlay(RandomHeuristic, Rebstomer, True)
