import minesweeper

msTest = minesweeper.Minesweeper()

print(msTest.print())

ai = minesweeper.MinesweeperAI()



cell = (3,3)

nearby = msTest.nearby_mines(cell)

ai.add_knowledge(cell,nearby)

#print(ai.knowledge)
