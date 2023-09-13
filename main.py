#import libraries
import tkinter as tk
from tkinter import *
from tkinter.ttk import *

#function for updating puzzle grid
def update_puzzle_board():
    # Implement the logic to update the GUI based on the current state of the puzzle
    #check if adjacent 
    
    #if adjacent swap, if not do nothing
    #check if solved already
    pass


#read puzzle.in
f = open("puzzle.in", "r")
lines = f.readlines()
initial = []

for line in lines:
    # print(line.rstrip("\n").split())
    initial.append(line.rstrip("\n").split())
    
print(initial)

#create window
root = tk.Tk()
root.title("Eight-Puzzle Game")
root.geometry('330x350')
root.resizable(0,0) 

#checks is solvable
is_solvable = False
if is_solvable:
    solvability_label = tk.Label(root, text="Puzzle is solvable")
else:
    solvability_label = tk.Label(root, text="Puzzle is not solvable")
solvability_label.grid(row=4, columnspan=3)

#create grid
empty_grid = {"x":0,"y":0}
puzzle_board = [[None, None, None], [None, None, None], [None, None, None]]
for i in range(3):
    for j in range(3):
        if initial[i][j] != '0':
            img = tk.PhotoImage(file="./images/" + initial[i][j] +".png")
            puzzle_board[i][j] = tk.Button(root, image=img, command=update_puzzle_board, relief="solid")
            puzzle_board[i][j].image = img
            puzzle_board[i][j].number = initial[i][j]
            puzzle_board[i][j]. = 
            puzzle_board[i][j].grid(row=i, column=j, pady = 2, padx = 2)
        else:
            empty_grid["x"] = i
            empty_grid["y"] = j

print(empty_grid) 

root.mainloop()

