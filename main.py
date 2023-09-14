#import libraries
import tkinter as tk
from tkinter import *
from tkinter.ttk import *

#init puzzle board
puzzle_board = [[None, None, None], [None, None, None], [None, None, None]]
empty_grid = {"x":0,"y":0}

#function for updating puzzle grid
def update_puzzle_board(number):
    # Implement the logic to update the GUI based on the current state of the puzzle
    #check if adjacent to empty grid
    
    #if adjacent swap, if not do nothing
    #check if solved already
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
            puzzle_board[i][j] = tk.Button(
                mainFrame, 
                text = initial[i][j], 
                command=lambda: update_puzzle_board(), 
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
            puzzle_board[i][j].number = initial[i][j]
            puzzle_board[i][j].x = i
            puzzle_board[i][j].y = j
            puzzle_board[i][j].grid(row=i, column=j, pady = 2, padx = 2)
        else:
            empty_grid["x"] = i
            empty_grid["y"] = j

print(empty_grid) 

root.mainloop()

