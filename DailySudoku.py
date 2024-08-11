##########################
###### DAILY SUDOKU ######
##########################

import sys, datetime, platform
try:
    import win32print, win32ui, win32con
except ImportError:
    print("failed to import win32 libraries\nyou will not be able to print the Sudoku puzzles")
except ImportWarning:
    print("win32 libraries may not work\nyou may encounter some errors printing the Sudoku puzzles")
except Exception as e:
    print(f"some other error occurred: {e}")

from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout as grid, QPushButton as button, QHBoxLayout as hlay, QVBoxLayout as vlay, QFrame as line, QLabel as text, QMainWindow as main, QProgressBar as bar, QTextEdit as textarea, QCheckBox as cbox
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QFont
from PIL import ImageGrab, Image, ImageWin
from random import shuffle, seed, randint
from time import sleep, time
from math import floor
from pyautogui import alert

class Buttons(QObject):
    def __init__(self, parent=None):
        global nums, sudoku
        super().__init__(parent)
        self.buttons = []
        self.notes = []
        self.text = []
        self.score = 0
        self.notesEnabled = False
        self.mistakes = 1
        self.totalnums = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        for i in range(81):
            row = i // 9
            col = i % 9
            if sudoku[row][col] != 0:
                self.totalnums[sudoku[row][col]] += 1
        self.nums = nums
        self.isscoreadded = False
        self.numberFont = QFont()
        self.numberFont.setPointSize(30)
        self.numberFont.setWeight(100)
        self.noteFont = QFont()
        self.noteFont.setPointSize(1)
        self.numberFont.setFamily("Courier New, Consolas")
        self.noteFont.setFamily("8514oem, Courier, Consolas")
    
    def add(self, button: button):
        self.buttons.append(button)
        self.notes.append([0])
        button.setFont(self.numberFont)
        button.clicked.connect(self.click)

    def click(self):
        global selected, selectedtext, puzzle, prefilled, solutionsudoku, solvetime, solvedtext, system, score, nums, printbutton, difficulty
        if not self.isscoreadded:
            system2.insertWidget(0, score)
            system2.insertWidget(2, selectedtext)
            puzzle.setContentsMargins(0, 0, 0, 0)
            printbutton.deleteLater()
            self.isscoreadded = True
        if self.sender().geometry().height() == 70:
            row, col, rows, cols = puzzle.getItemPosition(puzzle.indexOf(self.sender()))
            if prefilled[row][col] == "no":
                if selected == "X":
                    try:   
                        self.totalnums[int(self.sender().text())] -= 1
                    except:
                        self.notes[9 * row + col] = [0]
                    self.sender().setText("")
                    if sudoku[row][col] == solutionsudoku[row][col]:
                        self.nums -= 1
                        self.score = floor((((self.nums - nums) * difficulty * 10 + self.nums ** 2) - floor(time() - floor(float(solvetime.text())))) / self.mistakes ** 2)
                        score.setText(f"Score: {self.score}")
                    sudoku[row][col] = 0
                elif selected != sudoku[row][col]:
                    if self.notesEnabled:
                        self.sender().setFont(self.noteFont)
                        if int(selected) in self.notes[9 * row + col]:
                            self.notes[9 * row + col].remove(int(selected))
                            if self.notes[9 * row + col] == [0]:
                                self.sender().setText("")
                            else:
                                self.sender().setText(self.notesGenerator(self.notes[9 * row + col]))
                        else:
                            if sudoku[row][col] == solutionsudoku[row][col]:
                                self.nums -= 1
                                self.score = floor((((self.nums - nums) * difficulty * 10 + self.nums ** 2) - floor(time() - floor(float(solvetime.text())))) / self.mistakes ** 2)
                                score.setText(f"Score: {self.score}")
                            self.notes[9 * row + col].append(int(selected))
                            self.sender().setText(self.notesGenerator(self.notes[9 * row + col]))
                        textcolor = " color: #555;"
                    else:
                        self.notes[9 * row + col] = [0]
                        if sudoku[row][col] != 0:
                            self.totalnums[int(self.sender().text())] -= 1
                        self.sender().setText(str(selected))
                        self.sender().setFont(self.numberFont)
                        self.totalnums[int(self.sender().text())] += 1
                        sudoku[row][col] = int(selected)
                        if sudoku[row][col] == solutionsudoku[row][col]:
                            textcolor = " color: #053296;"
                            self.nums += 1
                        else:
                            textcolor = " color: #f00;"
                            self.mistakes += 1
                        self.score = floor((((self.nums - nums) * difficulty * 10 + self.nums ** 2) - floor(time() - floor(float(solvetime.text())))) / self.mistakes ** 2)
                        score.setText(f"Score: {self.score}")
                        if sudoku == solutionsudoku:
                            if time() - floor(float(solvetime.text())) >= 3600:
                                solvetime.setText(f"Time: {int((time() - floor(float(solvetime.text()))) // 3600)}h {int(((time() - floor(float(solvetime.text()))) // 60) % 60)}m {floor((time() - floor(float(solvetime.text()))) % 60)}s")
                            elif time() - floor(float(solvetime.text())) >= 60:
                                solvetime.setText(f"Time: {int((time() - floor(float(solvetime.text()))) // 60)}m {floor((time() - floor(float(solvetime.text()))) % 60)}s")
                            else:
                                solvetime.setText(f"Time: {floor(time() - floor(float(solvetime.text())))}s")
                            system2.insertLayout(0, solvedtext)
                            window2.setWindowTitle("Puzzle solved!")
                for i in self.buttons:
                    if i.geometry().height() == 60 and i.text() != "X" and i .text() != "✏️":
                        if self.totalnums[int(i.text())] > 8:
                            i.setEnabled(False)
                        else:
                            i.setEnabled(True)
        else:
            if self.sender().text() != "✏️":
                selected = str(self.sender().text())
                if self.notesEnabled:
                    selectedtext.setText(f"Selected: {selected}, notes on")
                else:
                    selectedtext.setText(f"Selected: {selected}")
            else:
                if self.notesEnabled:
                    selectedtext.setText(selectedtext.text()[:11])
                    self.notesEnabled = False
                else:
                    selectedtext.setText(selectedtext.text() + ", notes on")
                    self.notesEnabled = True
        for i in range(81):
            row = i // 9
            col = i % 9
            if prefilled[row][col] == "yes":
                textcolor = " color: #000;"
            elif sudoku[row][col] == solutionsudoku[row][col]:
                textcolor = " color: #053296;"
            elif self.notes[i] != [0]:
                textcolor = " color: #555;"
            else:
                textcolor = " color: #F00;"
            if selected == "X":
                return
            if sudoku[row][col] == int(selected):
                if row < 3:
                    if col < 3:
                        self.buttons[i].setStyleSheet(f"background-color: #aaa;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #bbb;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #aaa;{textcolor}")
                elif row < 6:
                    if col < 3:
                        self.buttons[i].setStyleSheet(f"background-color: #bbb;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #aaa;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #bbb;{textcolor}")
                else:
                    if col < 3:
                        self.buttons[i].setStyleSheet(f"background-color: #aaa;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #bbb;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #aaa;{textcolor}")
            else:
                if row < 3:
                    if col < 3:
                        self.buttons[i].setStyleSheet(f"background-color: #ddd;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #fff;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #ddd;{textcolor}")
                elif row < 6:
                    if col < 3:
                        self.buttons[i].setStyleSheet(f"background-color: #fff;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #ddd;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #fff;{textcolor}")
                else:
                    if col < 3:
                        self.buttons[i].setStyleSheet(f"background-color: #ddd;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #fff;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #ddd;{textcolor}")
    
    def notesGenerator(self, notes: list):
        first, second, third = "|", "|", "|"
        if 1 in notes:
            first += "1"
        else:
            first += " "
        if 2 in notes:
            first += "2"
        else:
            first += " "
        if 3 in notes:
            first += "3"
        else:
            first += " "
        first += "|"
        if 4 in notes:
            second += "4"
        else:
            second += " "
        if 5 in notes:
            second += "5"
        else:
            second += " "
        if 6 in notes:
            second += "6"
        else:
            second += " "
        second += "|"
        if 7 in notes:
            third += "7"
        else:
            third += " "
        if 8 in notes:
            third += "8"
        else:
            third += " "
        if 9 in notes:
            third += "9"
        else:
            third += " "
        third += "|"
        return "\n".join([first, second, third])

class Music:
    def __init__(self):
        self.isrunning = False
    
    def start(self):
        try:
            self.isrunning = True
            while self.isrunning:
                import wave, pyaudio
                self.wf = wave.open("SudokuMusic.wav", "rb")
                self.p = pyaudio.PyAudio()
                self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                            channels = self.wf.getnchannels(),
                            rate = self.wf.getframerate(),
                            output = True)
                data = self.wf.readframes(48000)
                while data:
                    self.stream.write(data)
                    data = self.wf.readframes(48000)
                self.wf.close()
                self.stream.close()
                self.p.terminate()
        except:
            pass
    
    def stop(self):
        if self.isrunning:
            self.isrunning = False
            self.wf.close()
            self.stream.close()
            self.p.terminate()

def printPuzzle():
    global window2
    if platform.system() == "Windows":
        screenshot = ImageGrab.grab(bbox=(window2.x(), window2.y(), window2.width(), window2.height()))
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
    else:
        alert(f"This feature will only work on Windows, not {platform.system()}!")

def isGridFull(sudoku: list):
    for i in range(81):
        if sudoku[i // 9][i % 9] == 0:
            return False
    return True

def solutionCountOfGrid(sudoku):
    global solutions
    for i in range(81):
        if solutions > 1:
            break
        row = i // 9
        column = i % 9
        if sudoku[row][column] == 0:
            for value in range (1, 10):
                if solutions > 1:
                    break
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
                            if solutions > 1:
                                break
                            sudoku[row][column] = value
                            if isGridFull(sudoku):
                                solutions += 1
                                break
                            else:
                                if solutions > 1:
                                    break
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

def Sudoku(diff: str | None = None):
    global solutions, sudoku, difficulty, solutionsudoku, nums, attempts, stars, row, column, value, copy, prefilled, score, picker, selected, puzzle, buttons, square, textcolor, system2, selectedtext, printbutton, solvedtext, solvetime, window2, system3, mainwindow, progress, music, dailyprogress
    solutions = 0
    sudoku = []
    for _ in range(9):
        sudoku.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    sudoku = makeGrid(sudoku)
    solutionsudoku = [[], [], [], [], [], [], [], [], []]
    nums = 81
    for r in range(9):
        for c in range(9):
            solutionsudoku[r].append(sudoku[r][c])
        print(solutionsudoku[r]) # this is the line to comment if you don't want the solution
    attempts = difficulty
    total = attempts
    stars = round((round(attempts) - 38) / 43 * 5, 1)
    sleep(1)
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
        attempts -= 1
        try:
            progress.setValue(floor((1 - attempts / total) * 100))
        except:
            pass
        try:
            dailyprogress.setValue(floor((1 - attempts / total) * 100))
        except:
            pass
    prefilled = [[], [], [], [], [], [], [], [], []]
    for r in range(9):
        for c in range(9):
            if sudoku[r][c] != 0:
                prefilled[r].append("yes")
            else:
                prefilled[r].append("no")
    score = text("Score: 0")
    score.setStyleSheet("font-size: 24px;")
    picker = hlay()
    selected = 1
    puzzle = grid()
    puzzle.setColumnStretch(0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8, 1)
    puzzle.setContentsMargins(0, 0, 0, 100)
    buttons = Buttons()
    for i in range(9):
        for j in range(9):
            square = button(None)
            square.setFixedSize(70, 70)
            numberFont = QFont()
            numberFont.setPointSize(30)
            numberFont.setWeight(100)
            square.setFont(numberFont)
            textcolor = " color: #053296;" if prefilled[i][j] == "no" else ""
            if i < 3:
                if j < 3:
                    square.setStyleSheet(f"background-color: #ddd;{textcolor}")
                elif j < 6:
                    square.setStyleSheet(f"background-color: #fff;{textcolor}")
                else:
                    square.setStyleSheet(f"background-color: #ddd;{textcolor}")
            elif i < 6:
                if j < 3:
                    square.setStyleSheet(f"background-color: #fff;{textcolor}")
                elif j < 6:
                    square.setStyleSheet(f"background-color: #ddd;{textcolor}")
                else:
                    square.setStyleSheet(f"background-color: #fff;{textcolor}")
            else:
                if j < 3:
                    square.setStyleSheet(f"background-color: #ddd;{textcolor}")
                elif j < 6:
                    square.setStyleSheet(f"background-color: #fff;{textcolor}")
                else:
                    square.setStyleSheet(f"background-color: #ddd;{textcolor}")
            buttons.add(square)
            if sudoku[i][j] != 0:
                square.setText(str(sudoku[i][j]))
            puzzle.addWidget(square, i, j)
    for i in range(11):
        if i < 9:
            square = button(str(i + 1))
        elif i == 9:
            square = button("X")
        else:
            square = button("✏️")
        square.setFixedSize(60, 60)
        square.setStyleSheet("font-size: 17pt;")
        buttons.add(square)
        picker.addWidget(square)
    picker.addStretch(1)
    system2 = vlay()
    system2.addLayout(puzzle)
    selectedtext = text("Selected: 1")
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
    system2.addLayout(picker)
    system2.addWidget(printbutton)
    window2 = QWidget()
    window2.setLayout(system2)
    if diff in (None, False):
        window2.setWindowTitle(f"Today's Puzzle: {datetime.datetime.today().strftime('%m-%d-%Y')} ({stars + 1}★)")
    else:
        window2.setWindowTitle(f"{diff} ({stars + 1}★)")
    window2.windowTitleChanged.connect(music.stop)
    window2.setGeometry(0, 0, 0, 0)
    mainwindow.destroy()
    window2.show()

def SudokuInit(diff: str | None = None):
    global difficulty, music, canplaymusic, canplaymusic2, window2
    if diff:
        seed(time())
    music = Music()
    try:
        if canplaymusic.isChecked():
            Thread(target=music.start).start()
    except:
        if canplaymusic2.isChecked():
            Thread(target=music.start).start()
    Sudoku(diff)

def VeryEasy():
    global difficulty
    difficulty = 29
    SudokuInit("Very Easy Sudoku")

def Easy():
    global difficulty
    difficulty = randint(38, 46)
    SudokuInit("Easy Sudoku")
    
def Medium():
    global difficulty
    difficulty = randint(47, 54)
    SudokuInit("Medium Sudoku")
    
def Hard():
    global difficulty
    difficulty = randint(55, 63)
    SudokuInit("Hard Sudoku")
    
def Expert():
    global difficulty
    difficulty = randint(64, 71)
    SudokuInit("Expert Sudoku")
    
def Master():
    global difficulty
    difficulty = randint(72, 81)
    SudokuInit("Master Sudoku")

def CustomDifficulty():
    global mainwindow, system3, progress, canplaymusic, canplaymusic2
    window3 = QWidget()
    system3 = vlay()
    title = text("Custom Difficulty")
    title.setAlignment(Qt.Alignment(Qt.AlignCenter))
    title.setStyleSheet("font-size: 42px;")
    veryeasy = button("Very Easy")
    veryeasy.setStyleSheet("font-size: 24px; background-color: #0F9;")
    veryeasy.clicked.connect(VeryEasy)
    easy = button("Easy")
    easy.setStyleSheet("font-size: 24px; background-color: #0F0;")
    easy.clicked.connect(Easy)
    medium = button("Medium")
    medium.setStyleSheet("font-size: 24px; background-color: #FF0;")
    medium.clicked.connect(Medium)
    hard = button("Hard")
    hard.setStyleSheet("font-size: 24px; background-color: #F90;")
    hard.clicked.connect(Hard)
    expert = button("Expert")
    expert.setStyleSheet("font-size: 24px; background-color: #F00;")
    expert.clicked.connect(Expert)
    master = button("Master")
    master.setStyleSheet("font-size: 24px; background-color: #F09;")
    master.clicked.connect(Master)
    progress = bar()
    progress.setGeometry(0, 0, 150, 50)
    canplaymusic2 = cbox("Music")
    canplaymusic2.setChecked(canplaymusic.isChecked())
    system3.addWidget(veryeasy)
    system3.addWidget(easy)
    system3.addWidget(medium)
    system3.addWidget(hard)
    system3.addWidget(expert)
    system3.addWidget(master)
    system3.addWidget(progress)
    system3.addWidget(canplaymusic2)
    window3.setLayout(system3)
    mainwindow.setCentralWidget(window3)

def calculateChange():
    try:
        global freeplay, dailychallenge, skillpoints, stars
        freeplay.setEnabled(True)
        dailychallenge.setEnabled(True)
        minchange = round((((stars + 1) * 5) / (int(skillpoints.toPlainText()) / 1000 + 0.03)) - (int(skillpoints.toPlainText()) / 70))
        maxchange = round((((stars + 1) * 10) / (int(skillpoints.toPlainText()) / 1000 + 0.03)) - (int(skillpoints.toPlainText()) / 70))
        if minchange >= 0:
            minchange = f"+{minchange}"
        if maxchange >= 0:
            maxchange = f"+{maxchange}"
        dailychallenge.setText(f"Daily Challenge ({stars + 1}★) ({minchange} with hints — {maxchange} without hints)")
    except:
        pass

if __name__ == "__main__":
    app = QApplication([])
    mainwindow = main()
    window = QWidget()
    system = vlay()
    title = text("Daily Sudoku")
    title.setAlignment(Qt.Alignment(Qt.AlignCenter))
    title.setStyleSheet("font-size: 42px;")
    freeplay = button("Custom Difficulty")
    freeplay.setStyleSheet("font-size: 24px;")
    freeplay.setEnabled(False)
    seed(datetime.datetime.today().strftime('%m-%d-%Y'))
    difficulty = [randint(38, 46), randint(47, 54), randint(55, 63), randint(64, 71), randint(72, 81)][randint(0, 4)]
    stars = round((round(difficulty) - 38) / 43 * 5, 1)
    dailychallenge = button(f"Daily Challenge ({stars + 1}★)")
    dailychallenge.setStyleSheet("font-size: 24px;")
    dailychallenge.setEnabled(False)
    skillpoints = textarea("Enter skill points here to play Sudoku")
    skillpoints.textChanged.connect(calculateChange)
    canplaymusic = cbox("Music")
    canplaymusic.setChecked(True)
    dailyprogress = bar()
    system.addWidget(title)
    system.addWidget(freeplay)
    system.addWidget(dailychallenge)
    system.addWidget(skillpoints)
    system.addWidget(canplaymusic)
    system.addWidget(dailyprogress)
    freeplay.clicked.connect(CustomDifficulty)
    dailychallenge.clicked.connect(SudokuInit)
    mainwindow.setWindowTitle("Daily Sudoku")
    mainwindow.setGeometry(0, 0, 400, 250)
    window.setLayout(system)
    mainwindow.setCentralWidget(window)
    mainwindow.show()
    sys.exit(app.exec())
