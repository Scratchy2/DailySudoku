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

from PyQt5.QtWidgets import QApplication, QWidget as win, QGridLayout as grid, QPushButton as button, QHBoxLayout as hlay, QVBoxLayout as vlay, QLabel as text, QMainWindow as main, QProgressBar as bar, QTextEdit as textarea, QCheckBox as cbox
from PyQt5.QtCore import QObject, Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
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
        self.numberFont.setWeight(1000)
        self.noteFont = QFont()
        self.noteFont.setPointSize(1)
        self.numberFont.setFamily("Courier New, Consolas")
        self.noteFont.setFamily("8514oem, Courier, Consolas")
    
    def quit(self):
        global window2, music
        window2.close()
        music.stop()

    def add(self, button: button):
        self.buttons.append(button)
        self.notes.append([0])
        button.setFont(self.numberFont)
        button.clicked.connect(self.click)

    def click(self):
        global selected, selectedtext, puzzle, prefilled, solutionsudoku, solvetime, solvedtext, system, score, nums, printbutton, difficulty
        if not self.isscoreadded:
            close = button("Quit Puzzle")
            close.setFixedHeight(35)
            close.setStyleSheet("background-color: #333; border-radius: 5px;")
            close.clicked.connect(self.quit)
            system2.insertWidget(0, score)
            system2.insertWidget(2, selectedtext)
            system2.addWidget(close)
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
                        self.mistakes += 1
                        score.setText(f"Score: {self.score}")
                    sudoku[row][col] = 0
                elif selected != sudoku[row][col]:
                    if (self.notesEnabled) and (sudoku[row][col] == 0):
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
                                self.mistakes += 1
                                score.setText(f"Score: {self.score}")
                            self.notes[9 * row + col].append(int(selected))
                            self.sender().setText(self.notesGenerator(self.notes[9 * row + col]))
                        textcolor = " color: #555;"
                    elif not self.notesEnabled:
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
                        score.setText(f"Score: {self.score}")
                        if sudoku == solutionsudoku:
                            if time() - floor(float(solvetime.text())) >= 3600:
                                minutes, seconds = divmod(time() - float(solvetime.text()), 60)
                                hours = minutes // 60
                                minutes %= 60
                                solvetime.setText(f"Time: {floor(hours)}h {floor(minutes)}m {floor(seconds)}s")
                            elif time() - floor(float(solvetime.text())) >= 60:
                                minutes, seconds = divmod(time() - floor(float(solvetime.text())), 60)
                                solvetime.setText(f"Time: {floor(minutes)}m {floor(seconds)}s")
                            else:
                                solvetime.setText(f"Time: {floor(time() - float(solvetime.text()))}s")
                            system2.insertLayout(0, solvedtext)
                            window2.setWindowTitle("Puzzle solved!")
                try:
                    self.score = floor((((self.nums - nums) * difficulty * 10 + self.nums ** 2) - floor(time() - floor(float(solvetime.text())))) / self.mistakes ** 2)
                except ValueError:
                    pass
                idx = 1
                for i in self.buttons:
                    if i.geometry().height() == 60 and i.text() != "X" and i .text() != "✏️":
                        if self.totalnums[idx] > 8:
                            i.setEnabled(False)
                            i.setText("▯")
                        else:
                            i.setEnabled(True)
                            i.setText(str(idx))
                        idx += 1
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
                        self.buttons[i].setStyleSheet(f"background-color: #888; border-radius: 3px;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #999; border-radius: 3px;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #888; border-radius: 3px;{textcolor}")
                elif row < 6:
                    if col < 3:
                        self.buttons[i].setStyleSheet(f"background-color: #999; border-radius: 3px;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #888; border-radius: 3px;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #999; border-radius: 3px;{textcolor}")
                else:
                    if col < 3:
                        self.buttons[i].setStyleSheet(f"background-color: #888; border-radius: 3px;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #999; border-radius: 3px;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #888; border-radius: 3px;{textcolor}")
            else:
                if row < 3:
                    if col < 3:
                        self.buttons[i].setStyleSheet(f"background-color: #ddd; border-radius: 3px;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #fff; border-radius: 3px;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #ddd; border-radius: 3px;{textcolor}")
                elif row < 6:
                    if col < 3:
                        self.buttons[i].setStyleSheet(f"background-color: #fff; border-radius: 3px;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #ddd; border-radius: 3px;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #fff; border-radius: 3px;{textcolor}")
                else:
                    if col < 3:
                        self.buttons[i].setStyleSheet(f"background-color: #ddd; border-radius: 3px;{textcolor}")
                    elif col < 6:
                        self.buttons[i].setStyleSheet(f"background-color: #fff; border-radius: 3px;{textcolor}")
                    else:
                        self.buttons[i].setStyleSheet(f"background-color: #ddd; border-radius: 3px;{textcolor}")
    
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
        self.isrunning = None
        self.player = QMediaPlayer()
        self.player.stateChanged.connect(self.stateChanged)
        self.player.error.connect(self.error)
        self.player.mediaStatusChanged.connect(self.isAudioLoaded)

    def start(self):
        self.isrunning = True
        self.player.setMedia(QMediaContent(QUrl("https://github.com/Scratchy2/DailySudoku/raw/main/SudokuMusic.wav")))
        self.player.play()
    
    def stop(self):
        self.isrunning = False
        self.player.stop()
    
    def stateChanged(self, state):
        if state == QMediaPlayer.StoppedState and self.isrunning:
            self.player.play()
    
    def error(self):
        print(f"Failed to play audio: {self.player.errorString()}")
        if self.isrunning:
            sleep(0.1)
            self.start()

    def isAudioLoaded(self, status):
        if status == QMediaPlayer.LoadedMedia and self.isrunning:
            self.player.play()

def printPuzzle(pr: str):
    if platform.system() == "Windows":
        try:
            image = Image.open("DailySudoku.png")
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(pr)
            area = hdc.GetDeviceCaps(win32con.PHYSICALWIDTH), hdc.GetDeviceCaps(win32con.PHYSICALHEIGHT)
            size = hdc.GetDeviceCaps(win32con.HORZRES), hdc.GetDeviceCaps(win32con.VERTRES)
            image.thumbnail(area, Image.LANCZOS)
            hdc.StartDoc("DailySudoku.png")
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
        except Exception as e:
            print("Error printing:", e)
            return "error printing"
    else:
        alert(f"This feature will only work on Windows, not {platform.system()}! It's because of win32 libraries.")

def choosePrinter():
    global window2, choose
    if platform.system() == "Windows":
        screenshot = ImageGrab.grab(bbox=(window2.x(), window2.y(), window2.width(), window2.height()))
        screenshot.save("DailySudoku.png")
        printers = []
        for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
            printers.append(printer[2])
        choose = win()
        chooselayout = vlay()
        titlec = text("Choose Printer")
        titlec.setAlignment(Qt.AlignCenter)
        titlec.setStyleSheet("font-size: 42px;")
        chooselayout.addWidget(titlec)
        titled = text("Clicking a button will print the puzzle on that printer once.")
        titled.setStyleSheet("font-size: 15px;")
        chooselayout.addWidget(titled)
        idx = 0
        for p in printers:
            exec(f'printer{idx} = button("{p}")')
            exec(f'printer{idx}.setStyleSheet("border-radius: 5px; background-color: #333;")')
            exec(f'printer{idx}.setFixedHeight(35)')
            exec(f'printer{idx}.clicked.connect(lambda: printPuzzle("{p}"))')
            exec(f"chooselayout.addWidget(printer{idx})")
            idx += 1
        cancel = button("Close Printing")
        cancel.setStyleSheet("border-radius: 5px; background-color: #333;")
        cancel.setFixedHeight(35)
        cancel.clicked.connect(choose.close)
        chooselayout.addWidget(cancel)
        choose.setLayout(chooselayout)
        choose.setWindowTitle("Printing Puzzle")
        choose.setStyleSheet("background-color: black; color: white;")
        choose.setGeometry(0, 0, 500, 500)
        choose.show()
        window2.setStyleSheet("background-color: black; color: white;")
    else:
        alert(f"This feature will only work on Windows, not {platform.system()}! It's because of win32 libraries.")

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
    global solutions, sudoku, difficulty, solutionsudoku, nums, attempts, stars, row, column, value, copy, prefilled, score, picker, selected, puzzle, buttons, square, textcolor, system2, selectedtext, printbutton, solvedtext, solvetime, window2, system3, mainwindow, progress, music, dailyprogress, app
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
        # print(solutionsudoku[r]) # this is the line to comment if you don't want the solution
    attempts = difficulty
    total = attempts
    stars = round((round(difficulty) - 38) / 43 * 5, 1)
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
            textcolor = " color: #053296;" if prefilled[i][j] == "no" else " color: #000000;"
            if i < 3:
                if j < 3:
                    square.setStyleSheet(f"background-color: #ddd; border-radius: 3px;{textcolor}")
                elif j < 6:
                    square.setStyleSheet(f"background-color: #fff; border-radius: 3px;{textcolor}")
                else:
                    square.setStyleSheet(f"background-color: #ddd; border-radius: 3px;{textcolor}")
            elif i < 6:
                if j < 3:
                    square.setStyleSheet(f"background-color: #fff; border-radius: 3px;{textcolor}")
                elif j < 6:
                    square.setStyleSheet(f"background-color: #ddd; border-radius: 3px;{textcolor}")
                else:
                    square.setStyleSheet(f"background-color: #fff; border-radius: 3px;{textcolor}")
            else:
                if j < 3:
                    square.setStyleSheet(f"background-color: #ddd; border-radius: 3px;{textcolor}")
                elif j < 6:
                    square.setStyleSheet(f"background-color: #fff; border-radius: 3px;{textcolor}")
                else:
                    square.setStyleSheet(f"background-color: #ddd; border-radius: 3px;{textcolor}")
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
        square.setStyleSheet("font-size: 17pt; border-radius: 5px; background-color: #333; color: white;")
        buttons.add(square)
        picker.addWidget(square)
    picker.addStretch(1)
    system2 = vlay()
    system2.addLayout(puzzle)
    selectedtext = text("Selected: 1")
    selectedtext.setStyleSheet("font-size: 30px;")
    printbutton = button("Print Puzzle")
    printbutton.setFixedHeight(35)
    printbutton.pressed.connect(lambda: window2.setStyleSheet("color: black;"))
    printbutton.setStyleSheet("background-color: #333; border-radius: 5px;")
    printbutton.released.connect(choosePrinter)
    solvedtext = vlay()
    solved = text("You have solved the puzzle!")
    solved.setStyleSheet("font-size: 42px;")
    solvetime = text(str(time()))
    solvetime.setStyleSheet("font-size: 42px;")
    solvedtext.addWidget(solved)
    solvedtext.addWidget(solvetime)
    system2.addLayout(picker)
    system2.addWidget(printbutton)
    window2 = win()
    window2.setLayout(system2)
    if diff in (None, False):
        window2.setWindowTitle(f"DailySudoku Puzzle #{(datetime.datetime.today() - datetime.datetime(2024, 7, 3)).days}: {datetime.datetime.today().strftime('%m-%d-%Y')} ({stars + 1}★)")
    else:
        window2.setWindowTitle(f"{diff} ({stars + 1}★)")
    window2.windowTitleChanged.connect(music.stop)
    app.aboutToQuit.connect(music.stop)
    window2.setGeometry(0, 0, 0, 0)
    mainwindow.close()
    window2.setStyleSheet("background-color: black; color: white;")
    window2.show()

def SudokuInit(diff: str | None = None):
    global difficulty, music, canplaymusic, canplaymusic2, window2
    music = Music()
    try:
        if canplaymusic.isChecked():
            music.start()
    except:
        if canplaymusic2.isChecked():
            music.start()
    Sudoku(diff)

def VeryEasy():
    global difficulty
    seed(time())
    difficulty = 29
    SudokuInit("Very Easy Sudoku")

def Easy():
    global difficulty
    seed(time())
    difficulty = randint(38, 46)
    SudokuInit("Easy Sudoku")
    
def Medium():
    global difficulty
    seed(time())
    difficulty = randint(47, 54)
    SudokuInit("Medium Sudoku")
    
def Hard():
    global difficulty
    seed(time())
    difficulty = randint(55, 63)
    SudokuInit("Hard Sudoku")
    
def Expert():
    global difficulty
    seed(time())
    difficulty = randint(64, 71)
    SudokuInit("Expert Sudoku")
    
def Master():
    global difficulty
    seed(time())
    difficulty = randint(72, 81)
    SudokuInit("Master Sudoku")

def CustomDifficulty():
    global mainwindow, system3, progress, canplaymusic, canplaymusic2, skillpoints, veryeasy, easy, medium, hard, expert, master
    window3 = win()
    system3 = vlay()
    title = text("Custom Difficulty")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 42px;")
    veryeasy = button("Very Easy")
    veryeasy.setStyleSheet("font-size: 20px; background-color: #0F9; border-radius: 5px; color: black;")
    veryeasy.clicked.connect(VeryEasy)
    easy = button("Easy")
    easy.setStyleSheet("font-size: 20px; background-color: #0F0; border-radius: 5px; color: black;")
    easy.clicked.connect(Easy)
    medium = button("Medium")
    medium.setStyleSheet("font-size: 20px; background-color: #FF0; border-radius: 5px; color: black;")
    medium.clicked.connect(Medium)
    hard = button("Hard")
    hard.setStyleSheet("font-size: 20px; background-color: #F90; border-radius: 5px; color: black;")
    hard.clicked.connect(Hard)
    expert = button("Expert")
    expert.setStyleSheet("font-size: 20px; background-color: #F00; border-radius: 5px; color: black;")
    expert.clicked.connect(Expert)
    master = button("Master")
    master.setStyleSheet("font-size: 20px; background-color: #F09; border-radius: 5px; color: black;")
    master.clicked.connect(Master)
    progress = bar()
    progress.setStyleSheet("border-radius: 5px; background-color: #333;")
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
    calculateChange(True)
    mainwindow.setCentralWidget(window3)

def calculateChange(custom: bool=False):
    try:
        global freeplay, dailychallenge, skillpoints, stars, change, veryeasy, easy, medium, hard, expert, master
        freeplay.setEnabled(True)
        freeplay.setText("Custom Difficulty")
        dailychallenge.setEnabled(True)
        dailychallenge.setText(f"Daily Challenge ({stars + 1}★)")
        factor = int(skillpoints.toPlainText()) / 1000 + 0.03
        penalty = int(skillpoints.toPlainText()) / 70
        minchange = "{:+}".format(round((((stars + 1) * 3) / factor) - penalty))
        maxchange = "{:+}".format(round((((stars + 1) * 10) / factor) - penalty))
        failchange = round(0 - penalty)
        if custom:
            minchangev = "{:+}".format(round(((0 * 3) / factor) - penalty))
            maxchangev = "{:+}".format(round(((0 * 10) / factor) - penalty))
            minchangee = "{:+}".format(round(((1.1 * 3) / factor) - penalty))
            maxchangee = "{:+}".format(round(((1.1 * 10) / factor) - penalty))
            minchangem = "{:+}".format(round(((2.2 * 3) / factor) - penalty))
            maxchangem = "{:+}".format(round(((2.2 * 10) / factor) - penalty))
            minchangeh = "{:+}".format(round(((3.3 * 3) / factor) - penalty))
            maxchangeh = "{:+}".format(round(((3.3 * 10) / factor) - penalty))
            minchangex = "{:+}".format(round(((4.5 * 3) / factor) - penalty))
            maxchangex = "{:+}".format(round(((4.5 * 10) / factor) - penalty))
            minchangea = "{:+}".format(round(((5.8 * 3) / factor) - penalty))
            maxchangea = "{:+}".format(round(((5.8 * 10) / factor) - penalty))
            veryeasy.setText(f"Very Easy\nWin without hints — {maxchangev}\nWin with hints — {minchangev}\nLoss: {failchange}")
            easy.setText(f"Easy\nWin without hints — {maxchangee}\nWin with hints — {minchangee}\nLoss: {failchange}")
            medium.setText(f"Medium\nWin without hints — {maxchangem}\nWin with hints — {minchangem}\nLoss: {failchange}")
            hard.setText(f"Hard\nWin without hints — {maxchangeh}\nWin with hints — {minchangeh}\nLoss: {failchange}")
            expert.setText(f"Expert\nWin without hints — {maxchangex}\nWin with hints — {minchangex}\nLoss: {failchange}")
            master.setText(f"Master\nWin without hints — {maxchangea}\nWin with hints — {minchangea}\nLoss: {failchange}")
        else:
            change.setText(f"Skill Points changes (Daily Challenge):\n{maxchange} if won\n{minchange} if won with hints\n{failchange} if failed\n\nWrite these down or screenshot them!")
    except:
        pass

if __name__ == "__main__":
    app = QApplication([])
    mainwindow = main()
    window = win()
    system = vlay()
    title = text("Daily Sudoku v3.3")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 42px;")
    freeplay = button("Enter skill points first")
    freeplay.setStyleSheet("font-size: 24px; border-radius: 5px; background-color: #333;")
    freeplay.setEnabled(False)
    seed(datetime.datetime.today().strftime('%m-%d-%Y'))
    difficulty = [randint(38, 46), randint(47, 54), randint(55, 63), randint(64, 71), randint(72, 81)][randint(0, 4)]
    stars = round((round(difficulty) - 38) / 43 * 5, 1)
    dailychallenge = button("Enter skill points first")
    dailychallenge.setStyleSheet("font-size: 24px; border-radius: 5px; background-color: #333;")
    dailychallenge.setEnabled(False)
    skillpoints = textarea("Enter skill points here to play Sudoku. Leave blank if you don't wish to be rated.")
    skillpoints.setStyleSheet("border-radius: 5px; background-color: #333;")
    skillpoints.textChanged.connect(calculateChange)
    canplaymusic = cbox("Music")
    canplaymusic.setChecked(True)
    dailyprogress = bar()
    dailyprogress.setStyleSheet("border-radius: 5px; background-color: #333;")
    change = text("Skill Points changes:\n(?) if won\n(?) if won with hints\n(?) if failed")
    system.addWidget(title)
    system.addWidget(freeplay)
    system.addWidget(dailychallenge)
    system.addWidget(skillpoints)
    system.addWidget(canplaymusic)
    system.addWidget(dailyprogress)
    system.addWidget(change)
    freeplay.clicked.connect(CustomDifficulty)
    dailychallenge.clicked.connect(SudokuInit)
    mainwindow.setWindowTitle("Daily Sudoku")
    mainwindow.setGeometry(0, 0, 400, 250)
    window.setLayout(system)
    mainwindow.setCentralWidget(window)
    mainwindow.setStyleSheet("background-color: black; color: white;")
    mainwindow.show()
    sys.exit(app.exec())
