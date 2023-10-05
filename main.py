#import libraries
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import copy
import sys

sys.setrecursionlimit(100000)

#init puzzle board
initial = []
puzzle_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
empty_grid = {"x":0,"y":0}
previous_action = None
loaded = False

# for the solution
move_list = []
current_move_index = 0

class pState:
    def __init__(self, pboard, emptyX, emptyY, prevaction, parent, g=0, h=0, f=0):
        self.pboard = pboard
        self.emptyX = emptyX
        self.emptyY = emptyY
        self.prevaction = prevaction
        self.parent = parent
        self.g = g
        self.h = h
        self.f = f

class Solution:
    def __init__(self, state, moves, cost):
        self.state = state
        self.moves = moves
        self.cost = cost

#brute force solver function
def Action(s):
    possibleActions = []
    emptyX = s.emptyX
    emptyY = s.emptyY

    # up, right, down, left
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for dx, dy in moves:
        new_x = emptyX + dx
        new_y = emptyY + dy
        
        # Check if the new position is within bounds
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            # Add the action corresponding to the move
            # action = (new_x, new_y)

            if (dx == -1 and dy == 0):
                action = "U"
            elif (dx == 0 and dy == 1):
                action = "R"
            elif (dx == 1 and dy == 0):
                action = "D"
            elif (dx == 0 and dy == -1):
                action = "L"
            else:
                action = "N/A"
            possibleActions.append(action)
    # print("pboard:{} emptyX:{} emptyY:{} prev:{} parent:{}".format(s.pboard,s.emptyX,s.emptyY,s.prevaction,s.parent))
    # print(possibleActions)
    # possibleActions.reverse()
    return possibleActions

def Result(s,a):
    newState = copy.deepcopy(s)

    pBoard = newState.pboard
    emptyX = newState.emptyX
    emptyY = newState.emptyY

    if a == "U":
        new_emptyX = emptyX - 1
        new_emptyY = emptyY
    elif a == "R":
        new_emptyX = emptyX
        new_emptyY = emptyY + 1
    elif a == "D":
        new_emptyX = emptyX + 1
        new_emptyY = emptyY
    elif a == "L":
        new_emptyX = emptyX 
        new_emptyY = emptyY - 1
    else:
        print("Invalid move")
        return s
    
    #swap
    pBoard[emptyX][emptyY] = pBoard[new_emptyX][new_emptyY]
    pBoard[new_emptyX][new_emptyY] = 0

    newState.emptyX = new_emptyX
    newState.emptyY = new_emptyY
    newState.prevaction = a
    newState.parent = s

    # newState.g = PathCostToFrom(initialS, newState)
    # newState.h = Manhattan(newState)
    # newState.f = newState.g + newState.h
    # print("pboard:{} emptyX:{} emptyY:{} prev:{} parent:{}".format(newState.pboard,newState.emptyX,newState.emptyY,newState.prevaction,newState.parent))

    return newState

def GoalTest(s):
    solved_state = [[1,2,3], [4,5,6], [7,8,0]]
    if (solved_state == s.pboard):
        print("solution found")
    return solved_state == s.pboard

def PathCost(path):
    return len(path)

def BFSearch(s):
    frontier = [s]
    visited = set()
    while frontier:
        cState = frontier.pop(0)
        visited.add(str(cState.pboard))  # Add the current state to the visited set
        if GoalTest(cState):
            print("Explored States: {}".format(len(visited)))
            return cState
        else:
            for a in Action(cState):
                nState = Result(cState, a)
                if str(nState.pboard) not in visited and not isInFrontier(nState,frontier):
                # if str(nState.pboard) not in visited and all(str(x.pboard) != str(nState.pboard) for x in frontier):
                    frontier.append(nState)
        print("States explored: {}".format(len(visited)))

def DFSearch(s):
    frontier = [s]
    visited = set()
    while frontier:
        cState = frontier.pop()
        visited.add(str(cState.pboard))  # Add the current state to the visited set
        if GoalTest(cState):
            print("Explored States: {}".format(len(visited)))
            return cState
        else:
            for a in Action(cState):
                nState = Result(cState, a)
                if str(nState.pboard) not in visited and not isInFrontier(nState,frontier):
                    frontier.append(nState)
        print("States explored: {}".format(len(visited)))

def PathCostToFrom(initialS, final):
    pathcost = 0
    currentpointer = final
    if (currentpointer.parent == None):
        return 0
    while (initialS is not currentpointer):
        pathcost = pathcost + 1
        currentpointer = currentpointer.parent
    return pathcost

def Manhattan(pb):
    #goal: [[1,2,3],[4,5,6],[7,8,0]]
    goal = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    total = 0
    for x in range(9):
        for i in range (3):
            for j in range (3):
                #find where x is 
                if pb[i][j] == x and x != 0:
                    total = total + (abs(i - goal[x-1][0]) + abs(j - goal[x-1][1])) 
    return total

def removeMinF(frontier):
    lowest = min(frontier, key=lambda state: state.f)
    frontier.remove(lowest)
    return lowest

def findDuplicate(state, frontier):
    for x in frontier:
        if state.pboard == x.pboard:
            return x

def isInFrontier(state, frontier):
    for x in frontier:
        if state.pboard == x.pboard:
            return True
    return False

def AStar(s):
    frontier = [s]
    visited = set()
    while frontier:
        bestState = removeMinF(frontier)
        visited.add(str(bestState.pboard))
        if GoalTest(bestState):
            print("Explored States: {}".format(len(visited)))
            return bestState
        else:
            for a in Action(bestState):
                nState = Result(bestState, a)
                nState.g = PathCostToFrom(s, nState)
                nState.h = Manhattan(nState.pboard)
                nState.f = nState.g + nState.h
                print("g:{} h:{} f:{}".format(nState.g, nState.h, nState.f))
                if (str(nState.pboard) not in visited and not isInFrontier(nState,frontier)) or (isInFrontier(nState,frontier) and nState.g < findDuplicate(nState,frontier).g):
                    nState.parent = bestState
                    frontier.append(nState)
        print("States explored: {}".format(len(visited)))

def solvePuzzle(s,choice):
    initstate = s.pboard
    inv_count = getInvCount([j for sub in initstate for j in sub])
    if (inv_count % 2 == 0): #solvable
        # pathCost = 0
        move_list = []
        if choice == "BFS":
            solution = BFSearch(s)
            print("pboard:{} emptyX:{} emptyY:{} prev:{} parent:{}".format(solution.pboard,solution.emptyX,solution.emptyY,solution.prevaction,solution.parent))
            
        elif choice == "DFS":
            solution = DFSearch(s)
            print("pboard:{} emptyX:{} emptyY:{} prev:{} parent:{}".format(solution.pboard,solution.emptyX,solution.emptyY,solution.prevaction,solution.parent))
        
        elif choice == "A*":
            solution = AStar(s)
            print("pboard:{} emptyX:{} emptyY:{} prev:{} parent:{}".format(solution.pboard,solution.emptyX,solution.emptyY,solution.prevaction,solution.parent))
        
        currentpointer = solution
        while (s is not currentpointer):
            move_list.append(currentpointer.prevaction)
            # pathCost = pathCost + 1
            currentpointer = currentpointer.parent

        #reverse path to get the move list
        move_list.reverse()
        print(move_list)
        #path cost
        pathcost = PathCost(move_list)
        print("Path cost: {}".format(pathcost))

        #puzzle.out
        maxHorizontal = 50
        with open("puzzle.out", "w") as file:
            charcount = 0
            for x in move_list:
                if charcount + 1 > maxHorizontal:
                    file.write("\n")
                    charcount = 0
                file.write("{} ".format(x))
                charcount += 2
        
        #return solution
        solutionObject = Solution(solution, move_list, pathcost)
        return solutionObject

    else:
        print("Not Solvable")

def handleSolve():
    global move_list
    #disable user input
    disableUserSolve()
    solveButton.config(state=tk.DISABLED)

    choice = clicked.get()
    currPboard = [[puzzle_board[i][j] if puzzle_board[i][j] == 0 else int(puzzle_board[i][j].number) for j in range(3)] for i in range (3)]
    currstate = pState(currPboard, empty_grid["x"], empty_grid["y"], previous_action, None, 0, Manhattan(currPboard), Manhattan(currPboard))

    if choice == "BFS":
        solution = solvePuzzle(currstate,"BFS")
    elif choice == "DFS":
        solution = solvePuzzle(currstate,"DFS")
    elif choice == "A*":
        solution = solvePuzzle(currstate,"A*")
    else:
        print("Error: not an option")

    #update solution text display
    for x in solution.moves:
        solText.insert(tk.END, "{} ".format(x))

    #do the next next solution thingy
    move_list = solution.moves
    pathcostText.config(text="Path Cost: {}".format(PathCost(move_list)))
    dropdown.config(state=tk.DISABLED)
    solveButton.config(state=tk.NORMAL, text="Next", command= movePuzzle)

def movePuzzle():
    global current_move_index
    global move_list

    if current_move_index < len(move_list):
        # Update the button state and text
        solveButton.config(state=tk.NORMAL, text="Next")

        current_move = move_list[current_move_index]
        print("move:{} index:{}".format(current_move, current_move_index))
        current_move_index += 1

        updatePuzzleOnMove(current_move)

        if current_move_index == len(move_list):
            solveButton.config(state=tk.DISABLED, text="Solved!")
        # else:
        #     # Schedule the next move after a button press
        #     root.after(1000,movePuzzle)
            

def updatePuzzleOnMove(a):
    if a == "U":
        new_emptyX = empty_grid["x"] - 1
        new_emptyY = empty_grid["y"] 
    elif a == "R":
        new_emptyX = empty_grid["x"] 
        new_emptyY = empty_grid["y"]  + 1
    elif a == "D":
        new_emptyX = empty_grid["x"]  + 1
        new_emptyY = empty_grid["y"] 
    elif a == "L":
        new_emptyX = empty_grid["x"]  
        new_emptyY = empty_grid["y"]  - 1
    else:
        print("Invalid move")

    puzzle_board[empty_grid["x"]][empty_grid["y"]] = puzzle_board[new_emptyX][new_emptyY]
    puzzle_board[new_emptyX][new_emptyY] = 0

    empty_grid["x"] = new_emptyX
    empty_grid["y"] = new_emptyY

    buildGrid()
    checkSolved()


#function for updating puzzle grid
def update_puzzle_board(button):
    print("Pressed number: " + button.number )
    print("Location X: {}, Location Y: {}".format(button.x, button.y) )
    # Implement the logic to update the GUI based on the current state of the puzzle
    #if solved already change the solvability label to solved
    
    if isSolved():
        checkSolved()
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
        
        currPboard = [[puzzle_board[i][j] if puzzle_board[i][j] == 0 else int(puzzle_board[i][j].number) for j in range(3)] for i in range (3)]
        currstate = pState(currPboard, empty_grid["x"], empty_grid["y"], previous_action, None)
        # currstate = {"pboard": currPboard, "emptyX": empty_grid["x"], "emptyY": empty_grid["y"], "prevaction": previous_action}
        Action(currstate)
        # Result(currstate, "U")

        buildGrid()
        checkSolved()

def disableUserSolve():
    for i in range(3):
        for j in range(3):
            if puzzle_board[i][j] != 0:
                puzzle_board[i][j].config(state = tk.DISABLED)
            
            
#check if solved already
def isSolved():
    solved_state = [[1,2,3], [4,5,6], [7,8,0]]
    current_state = [[puzzle_board[i][j] if puzzle_board[i][j] == 0 else int(puzzle_board[i][j].number) for j in range(3)] for i in range (3)]
    # print(current_state)
    return current_state == solved_state

def buildGrid():
    for i in range(3):
        for j in range(3):
            if puzzle_board[i][j]:
                b = puzzle_board[i][j]
                b.grid(row=i, column=j, pady=2, padx=2)
                
def checkSolved():
    if isSolved():
        solvability_label.config(text="Puzzle is solved!")
        disableUserSolve()
        print("SOLVED!")
        
        
def isSolvable(puzzle):
    initstate = [[puzzle[i][j] if puzzle[i][j] == 0 else int(puzzle[i][j].number) for j in range(3)] for i in range (3)]
    inv_count = getInvCount([j for sub in initstate for j in sub])
    return (inv_count % 2 == 0)

def getInvCount(arr):
    inv_count = 0
    empty_value = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if int(arr[j]) != empty_value and int(arr[i]) != empty_value and int(arr[i]) > int(arr[j]):
                inv_count += 1
    return inv_count

def open_file_dialog():
    global loaded
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Input files", "*.in"), ("All files", "*.*")])

    if file_path:
        loaded = True
        read_file(file_path)
    else:
        pass

def read_file(filepath="puzzle.in"):
    global initial, puzzle_board, loaded, move_list, current_move_index

    initial.clear()
    #reset
    if loaded:
        for i in range(3):
            for j in range(3):
                if puzzle_board[i][j] != 0:
                    puzzle_board[i][j].destroy()
    puzzle_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    f = open(filepath, "r")
    lines = f.readlines()

    for line in lines:
        initial.append(line.rstrip("\n").split())
    
    print(initial)
    f.close()

    for i in range(3):
        for j in range(3):
            if initial[i][j] != '0':
                p = puzzle_board[i][j] = tk.Button(
                    mainFrame,
                    text = initial[i][j], 
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
                puzzle_board[i][j] = 0
                empty_grid["x"] = i
                empty_grid["y"] = j

    
    dropdown.config(state = tk.NORMAL)
    solveButton.config(state = tk.NORMAL, text="Solve", command=handleSolve)
    pathcostText.config(text="Path Cost:")
    notloaded_label.config(text="")
    solText.delete(1.0, tk.END)

    move_list = []
    current_move_index = 0

    if isSolvable(puzzle_board):
        solvability_label.config(text="Puzzle is solvable")
    else:
        solvability_label.config(text="Puzzle is not solvable")

    loaded = True

    print(initial)
    print(puzzle_board)
    print(empty_grid["x"])
    print(empty_grid["y"])

    buildGrid()
    checkSolved()

#create window
root = tk.Tk()
root.title("Eight-Puzzle Game")
root.geometry('400x580')
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

#solvability label
solvability_label = tk.Label(
        mainFrame, 
        text="No puzzle loaded",
        relief="flat",
        fg="WHITE",
        background=color1,
        font=('Arial',10,'bold')
        )
solvability_label.grid(row=4, columnspan=3)

solutionFrame = tk.Frame(mainFrame, bg=color1)
solutionFrame.grid(row=5, columnspan=3)

#options dropdown
options = ["BFS", "BFS", "DFS", "A*"]
clicked = StringVar()
clicked.set(options[0]) 

dropdown = OptionMenu(solutionFrame, clicked, *options)
dropdown.pack(side=tk.LEFT, padx=10)

solveButton = Button(solutionFrame , text = "Solve" , command = handleSolve)
if not isSolvable(puzzle_board):
    solveButton.config(state = tk.DISABLED)
solveButton.pack(side=tk.LEFT, padx=10)

#solution text
solutionTextFrame = tk.Frame(mainFrame, bg=color1)
solutionTextFrame.grid(row=6, columnspan=4)
solText = Text(solutionTextFrame, height=5, width=40)
solText.pack(pady=10)

#pathcost text
pathcostFrame = tk.Frame(mainFrame, bg=color1)
pathcostFrame.grid(row=7, columnspan=4)
pathcostText = tk.Label(
        pathcostFrame, 
        text="Path Cost: ",
        relief="flat",
        fg="WHITE",
        background=color1,
        font=('Arial',10,'bold')
        )
pathcostText.pack(pady=2)

#open puzzle.in files
openfileFrame = tk.Frame(mainFrame, bg=color1)
openfileFrame.grid(row=8, columnspan=4)

open_button = tk.Button(openfileFrame, text="Open File", command=open_file_dialog)
open_button.pack(side=tk.LEFT, pady=5)

#displays possible actions
currPboard = [[puzzle_board[i][j] if puzzle_board[i][j] == 0 else int(puzzle_board[i][j].number) for j in range(3)] for i in range (3)]
currstate = pState(currPboard, empty_grid["x"], empty_grid["y"], previous_action, None, 0, Manhattan(currPboard), Manhattan(currPboard))
Action(currstate)

#read puzzle.in
if loaded:
    read_file()
else:
    solveButton.config(state = tk.DISABLED)
    notloaded_label = tk.Label(
        mainFrame, 
        text="File not yet Loaded",
        relief="flat",
        background=color1,
        fg="WHITE",
        font=('Arial',10,'bold')
        )
    notloaded_label.grid(row=1, columnspan=3)

root.mainloop()

