##########################
###### DAILY SUDOKU ######
##########################

# The only rule is that each row, column, and 3x3 block must have the numbers 1 to 9 once.

import sys, datetime, win32print, win32ui, win32con
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout as grid, QPushButton as button, QHBoxLayout as hlay, QVBoxLayout as vlay, QFrame as line, QLabel as text
from PyQt5.QtCore import QObject
from PIL import ImageGrab, Image, ImageWin
from random import shuffle, seed, randint
from time import time
from math import floor
app = QApplication([])
window = QWidget()

class Buttons(QObject):
    def __init__(self, parent=None):
        global nums
        super().__init__(parent)
        self.buttons = []
        self.text = []
        self.score = 0
        self.nums = nums
        self.isscoreadded = False
    
    def add(self, button: button):
        self.buttons.append(button)
        button.clicked.connect(self.click)
    
    def click(self):
        global selected, selectedtext, puzzle, prefilled, solutionsudoku, solvetime, solvedtext, system, score, nums
        if not self.isscoreadded:
            system.insertWidget(0, score)
            self.isscoreadded = True
        if self.sender().geometry().height() == 70:
            row, col, rows, cols = puzzle.getItemPosition(puzzle.indexOf(self.sender()))
            if prefilled[row][col] == "no":
                if selected == "X":
                    self.sender().setText("")
                    sudoku[row][col] = 0
                    if sudoku[row][col] == solutionsudoku[row][col]:
                        self.nums -= 1
                        self.score = ((self.nums - nums) ** 6) // floor(time() - floor(float(solvetime.text())))
                        score.setText(f"Score: {self.score}")
                elif self.sender().text() == "":
                    self.sender().setText(str(selected))
                    sudoku[row][col] = int(selected)
                    if sudoku[row][col] == solutionsudoku[row][col]:
                        self.nums += 1
                        self.score = ((self.nums - nums) ** 6) // floor(time() - floor(float(solvetime.text())))
                        score.setText(f"Score: {self.score}")
                    if sudoku == solutionsudoku:
                        if time() - floor(float(solvetime.text())) >= 3600:
                            solvetime.setText(f"Time: {int((time() - floor(float(solvetime.text()))) // 3600)}h {int(((time() - floor(float(solvetime.text()))) // 60) % 60)}m {floor((time() - floor(float(solvetime.text()))) % 60)}s")
                        elif time() - floor(float(solvetime.text())) >= 60:
                            solvetime.setText(f"Time: {int((time() - floor(float(solvetime.text()))) // 60)}m {floor((time() - floor(float(solvetime.text()))) % 60)}s")
                        else:
                            solvetime.setText(f"Time: {floor(time() - floor(float(solvetime.text())))}s")
                        system.insertLayout(0, solvedtext)

        else:
            selected = str(self.sender().text())
            selectedtext.setText(f"Selected: {selected}")

def printPuzzle():
    screenshot = ImageGrab.grab(bbox=(window.x(), window.y(), window.width(), window.height()))
    screenshot.save("C:/Users/Bentley School/OneDrive - Liberty University/Documents/vscode/DailySudoku.png")
    image = Image.open("C:/Users/Bentley School/OneDrive - Liberty University/Documents/vscode/DailySudoku.png")
    printer = win32print.GetDefaultPrinter()
    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer)
    area = hdc.GetDeviceCaps(win32con.PHYSICALWIDTH), hdc.GetDeviceCaps(win32con.PHYSICALHEIGHT)
    size = hdc.GetDeviceCaps(win32con.HORZRES), hdc.GetDeviceCaps(win32con.VERTRES)
    image.thumbnail(area, Image.LANCZOS)
    hdc.StartDoc("C:/Users/Bentley School/OneDrive - Liberty University/Documents/vscode/DailySudoku.png")
    hdc.StartPage()
    dib = ImageWin.Dib(image)
    x1 = int((size[0] - area[0]) / 2)
    y1 = int((size[1] - area[1]) / 2)
    x2 = x1 + area[0]
    y2 = y1 + area[1]
    dib.draw(hdc.GetHandleOutput(), (x1, y1, x2, y2))
    hdc.EndPage()
    hdc.EndDoc()
    hdc.DeleteDC()

def clear(layout: vlay):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clear(item.layout())
        layout.deleteLater()

def isGridFull(sudoku: list):
    for i in range(81):
        if sudoku[i // 9][i % 9] == 0:
            return False
    return True

def solutionCountOfGrid(sudoku):
    global solutions
    for i in range(81):
        row = i // 9
        column = i % 9
        if sudoku[row][column] == 0:
            for value in range (1, 10):
                if value not in sudoku[row]:
                    if value not in (sudoku[0][column], sudoku[1][column], sudoku[2][column], sudoku[3][column], sudoku[4][column], sudoku[5][column], sudoku[6][column], sudoku[7][column], sudoku[8][column]):
                        square = []
                        if row < 3:
                            if column < 3:
                                square = [sudoku[i][0:3] for i in range(3)]
                            elif column < 6:
                                square = [sudoku[i][3:6] for i in range(3)]
                            else:  
                                square = [sudoku[i][6:9] for i in range(3)]
                        elif row < 6:
                            if column < 3:
                                square = [sudoku[i][0:3] for i in range(3, 6)]
                            elif column < 6:
                                square = [sudoku[i][3:6] for i in range(3, 6)]
                            else:  
                                square = [sudoku[i][6:9] for i in range(3, 6)]
                        else:
                            if column < 3:
                                square = [sudoku[i][0:3] for i in range(6, 9)]
                            elif column < 6:
                                square = [sudoku[i][3:6] for i in range(6, 9)]
                            else:  
                                square = [sudoku[i][6:9] for i in range(6, 9)]
            
                        if value not in (square[0] + square[1] + square[2]):
                            sudoku[row][column] = value
                            if isGridFull(sudoku):
                                solutions += 1
                                break
                            else:
                                if solutionCountOfGrid(sudoku):
                                    return True
            break
    sudoku[row][column] = 0 

def makeGrid(sudoku: list):
    og = sudoku
    global solutions
    for i in range(81):
        row = i // 9
        column = i % 9
        if sudoku[row][column] == 0:
            nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            shuffle(nums)
            for value in nums:
                if value not in sudoku[row]:
                    if value not in (sudoku[0][column], sudoku[1][column], sudoku[2][column], sudoku[3][column], sudoku[4][column], sudoku[5][column], sudoku[6][column], sudoku[7][column], sudoku[8][column]):
                        square = []
                        if row < 3:
                            if column < 3:
                                square = [sudoku[i][0:3] for i in range(0, 3)]
                            elif column < 6:
                                square = [sudoku[i][3:6] for i in range(0, 3)]
                            else:
                                square = [sudoku[i][6:9] for i in range(0, 3)]
                        elif row < 6:
                            if column < 3:
                                square = [sudoku[i][0:3] for i in range(3, 6)]
                            elif column < 6:
                                square = [sudoku[i][3:6] for i in range(3, 6)]
                            else:  
                                square = [sudoku[i][6:9] for i in range(3, 6)]
                        else:
                            if column < 3:
                                square = [sudoku[i][0:3] for i in range(6, 9)]
                            elif column < 6:
                                square = [sudoku[i][3:6] for i in range(6, 9)]
                            else:  
                                square = [sudoku[i][6:9] for i in range(6, 9)]
                        if value not in (square[0] + square[1] + square[2]):
                            sudoku[row][column] = value
                            if isGridFull(sudoku):
                                return sudoku
                            elif makeGrid(og):
                                return sudoku
            break
    sudoku[row][column] = 0

rows = 0
solutions = 0
sudoku = []
for _ in range(9):
    sudoku.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
seed(datetime.datetime.today().strftime('%m-%d-%Y'))
difficulty = [1, randint(2, 4), randint(5, 10), randint(11, 20), randint(21, 25)][randint(0, 4)]
sudoku = makeGrid(sudoku)
solutionsudoku = [[], [], [], [], [], [], [], [], []]
nums = 81
for r in range(9):
    for c in range(9):
        solutionsudoku[r].append(sudoku[r][c])
    print(solutionsudoku[r])
attempts = difficulty
while attempts > 0:
    row = randint(0, 8)
    column = randint(0, 8)
    while sudoku[row][column] == 0:
        row = randint(0, 8)
        column = randint(0, 8)
    value = sudoku[row][column]
    sudoku[row][column] = 0
    nums -= 1
    solutions = 0
    copy = sudoku
    solutionCountOfGrid(copy)
    if solutions != 1:
        sudoku[row][column] = value
        nums += 1
        print("Attempts:", attempts)
        attempts -= 1
prefilled = [[], [], [], [], [], [], [], [], []]
for r in range(9):
    for c in range(9):
        if sudoku[r][c] != 0:
            prefilled[r].append("yes")
        else:
            prefilled[r].append("no")
system = vlay()
score = text("Score: 0")
score.setStyleSheet("font-size: 24px;")
picker = hlay()
selected = 1
puzzle = grid()
buttons = Buttons()
for i in range(9):
    for j in range(9):
        square = button(None)
        square.setFixedSize(70, 70)
        textcolor = " color: #053296;" if prefilled[i][j] == "no" else ""
        if i < 3:
            if j < 3:
                square.setStyleSheet(f"font-size: 20pt; background-color: #ddd;{textcolor}")
            elif j < 6:
                square.setStyleSheet(f"font-size: 20pt; background-color: #fff;{textcolor}")
            else:
                square.setStyleSheet(f"font-size: 20pt; background-color: #ddd;{textcolor}")
        elif i < 6:
            if j < 3:
                square.setStyleSheet(f"font-size: 20pt; background-color: #fff;{textcolor}")
            elif j < 6:
                square.setStyleSheet(f"font-size: 20pt; background-color: #ddd;{textcolor}")
            else:
                square.setStyleSheet(f"font-size: 20pt; background-color: #fff;{textcolor}")
        else:
            if j < 3:
                square.setStyleSheet(f"font-size: 20pt; background-color: #ddd;{textcolor}")
            elif j < 6:
                square.setStyleSheet(f"font-size: 20pt; background-color: #fff;{textcolor}")
            else:
                square.setStyleSheet(f"font-size: 20pt; background-color: #ddd;{textcolor}")
        buttons.add(square)
        if sudoku[i][j] != 0:
            square.setText(str(sudoku[i][j]))
        puzzle.addWidget(square, i, j)
layout = hlay()
for i in range(9):
    frame = line()
    frame.resize(10, 630)
    layout.addWidget(frame)
puzzle.setContentsMargins(0, 0, 0, 50)
for i in range(10):
    if i < 9:
        square = button(str(i + 1))
    else:
        square = button("X")
    square.setFixedSize(60, 60)
    square.setStyleSheet("font-size: 17pt;")
    buttons.add(square)
    picker.addWidget(square)
system.addLayout(puzzle)
system.addLayout(layout)
selectedtext = text("Selected: 1", window)
selectedtext.setStyleSheet("font-size: 42px;")
printbutton = button("Print Puzzle")
printbutton.clicked.connect(printPuzzle)
solvedtext = vlay()
solved = text("You have solved the puzzle!")
solved.setStyleSheet("font-size: 96px;")
solvetime = text(str(time()))
solvetime.setStyleSheet("font-size: 42px;")
solvedtext.addWidget(solved)
solvedtext.addWidget(solvetime)
system.addWidget(selectedtext)
system.addLayout(picker)
system.addWidget(printbutton)
window.setGeometry(0, 0, 0, 0)
window.setLayout(system)
if difficulty < 2:
    window.setWindowTitle(f"Today's Puzzle: {datetime.datetime.today().strftime('%m-%d-%Y')} (Easy)")
elif difficulty < 5:
    window.setWindowTitle(f"Today's Puzzle: {datetime.datetime.today().strftime('%m-%d-%Y')} (Medium)")
elif difficulty < 11:
    window.setWindowTitle(f"Today's Puzzle: {datetime.datetime.today().strftime('%m-%d-%Y')} (Hard)")
elif difficulty < 21:
    window.setWindowTitle(f"Today's Puzzle: {datetime.datetime.today().strftime('%m-%d-%Y')} (Expert)")
else:
    window.setWindowTitle(f"Today's Puzzle: {datetime.datetime.today().strftime('%m-%d-%Y')} (Master)")
window.show()
sys.exit(app.exec())
