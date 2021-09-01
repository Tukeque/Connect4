from random  import randint
from random  import shuffle
from board   import Board
from board   import other_player
#from rich    import print
from time    import sleep
from _thread import start_new_thread

from enemies import TukeAI
from enemies import SemiPish
from enemies import PishNo2Row

DELAY = 0
RANDOM_START = True
ROUNDS = 10
PRINT = False
THREADS = 48
game_count = 0

def AIPlay(Class1, Class2) -> int:
    global game_count
    #enemies = [TukeHeuristic("TukeAI"), TukeHeuristic("Obama Tuke")]
    enemies = [Class1(), Class2()]
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
        #board.Print()
        #print(f"last move: {last_move}")
        print(f"game over! enemy {board.player}, aka {enemies[other_player(board.player) - 1].name} won\n")
        return enemies[other_player(board.player) - 1].name
    else:
        print(f"draw!")
        return "Draw"

win_board = {
    "Draw": 0
}
names = ["Tukeque", "Pishle", "Pishle's Back", "Pishle Without Rows"]
for i in names:
    win_board[i] = 0

classes = [TukeAI, SemiPish, PishNo2Row]

finisheds = [False for _ in range(THREADS)]

def thread(identifier: int, happy: bool):
    global win_board

    #for _ in range(ROUNDS):
    #    win_board[AIPlay()] += 1

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
