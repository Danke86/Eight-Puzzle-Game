#import libraries
import tkinter as tk
from tkinter import *
from tkinter.ttk import *

#init puzzle board
puzzle_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
empty_grid = {"x":0,"y":0}

solved = False

#function for updating puzzle grid
def update_puzzle_board(button):
    print("Pressed: " + button.number + " Button")
    print("Location X: {}, Location Y: {}".format(button.x, button.y) )
    # Implement the logic to update the GUI based on the current state of the puzzle
    #if solved already change the solvability label to solved
    if isSolved():
        print("SOLVED!")
    else:
        #check if adjacent to empty grid
        #if adjacent swap, if not do nothing
        if (abs(button.x - empty_grid['x'])+ abs(button.y -  empty_grid['y'])) <= 1:
            #swap
            # print("adjacent")
            
            puzzle_board[empty_grid['x']][empty_grid['y']] = button
            puzzle_board[button.x][button.y] = 0
            tempx = empty_grid['x']
            tempy = empty_grid['y']
            empty_grid['x'] = button.x
            empty_grid['y'] = button.y
            button.x = tempx
            button.y = tempy

            
            buildGrid()
            checkSolved()
            
#check if solved already
def isSolved():
    solved_state = [[1,2,3], [4,5,6], [7,8,0]]
    current_state = [[puzzle_board[i][j] if puzzle_board[i][j] == 0 else int(puzzle_board[i][j].number) for j in range(3)] for i in range (3)]
    print(current_state)
    return current_state == solved_state

def buildGrid():
    for i in range(3):
        for j in range(3):
            if puzzle_board[i][j]:
                b = puzzle_board[i][j]
                b.grid(row=i, column=j, pady=2, padx=2)
                
def checkSolved():
    pass

#read puzzle.in
f = open("puzzle.in", "r")
lines = f.readlines()
initial = []

for line in lines:
    initial.append(line.rstrip("\n").split())
    
print(initial)

#create window
root = tk.Tk()
root.title("Eight-Puzzle Game")
root.geometry('330x350')
root.resizable(0,0) 

#colors
color1 = '#020f12'
color2 = '#05d7ff'
color3 = '#65e7ff'
color4 = 'BLACK'

#create main frame
mainFrame = tk.Frame(root, bg=color1)
mainFrame.pack(fill=tk.BOTH, expand=True)
mainFrame.columnconfigure(0, weight=1)
mainFrame.columnconfigure(1, weight=1)
mainFrame.columnconfigure(2, weight=1)
mainFrame.rowconfigure(0, weight=1)
mainFrame.rowconfigure(1, weight=1)
mainFrame.rowconfigure(2, weight=1)

#checks is solvable
is_solvable = False
if is_solvable:
    solvtext = ""
    solvability_label = tk.Label(
        mainFrame, 
        text="Puzzle is solvable",
        relief="flat",
        background=color1,
        fg="WHITE",
        font=('Arial',10,'bold')
        )
else:
    solvability_label = tk.Label(
        mainFrame, 
        text="Puzzle is not solvable",
        relief="flat",
        fg="WHITE",
        background=color1,
        font=('Arial',10,'bold')
        )
solvability_label.grid(row=4, columnspan=3)

#create grid
for i in range(3):
    for j in range(3):
        if initial[i][j] != '0':
            p = puzzle_board[i][j] = tk.Button(
                mainFrame,
                text = initial[i][j], 
                # command=lambda: update_puzzle_board(), 
                relief="solid",
                background=color2,
                foreground=color4,
                activebackground=color3,
                highlightthickness=2,
                highlightcolor='WHITE',
                height=10,
                width=10,
                border=3,
                font=('Arial',30,'bold')
                )
            p.config(command = lambda button=p: update_puzzle_board(button) )
            puzzle_board[i][j].number = initial[i][j]
            puzzle_board[i][j].x = i
            puzzle_board[i][j].y = j
            puzzle_board[i][j].grid(row=i, column=j, pady = 2, padx = 2)
        else:
            empty_grid["x"] = i
            empty_grid["y"] = j

# print(puzzle_board)
# print(empty_grid) 

root.mainloop()

