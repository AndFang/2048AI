import pyautogui
import webbrowser
import time
import random

# https://sleepycoder.github.io/2048/ai.js
class AI:
    def __init__(self):
        self.next = 0
        self.grid = [0 for i in range(16)]
        self.node = 0
        self.MAXDEPTH = 3
    
    def moveLeft(self, board):
        k = 0
        base = 0
        score = 0
        result = [0 for i in range(16)]

        for i in range(4, 17, 4):
            while (k < i):
                if (board[k] == 0):
                    k += 1
                    continue
                if (k + 1 < i and board[k] == board[k + 1]):
                    result[base] = board[k] * 2
                    base += 1
                    score += board[k] * 2
                    k += 2
                else:
                    result[base] = board[k]
                    base += 1
                    k += 1
            while (base < i):
                result[base] = 0
                base += 1

        return [result, score]

    def rotate(self, board):
        res = []
        for i in range(4):
            for j in range(4):
                res.append(board[12 + i - 4 * j])

        return res

    def estimate(self, board):
        dif = 0
        tot = 0

        for i in range(16):
            tot += board[i]
            if (i % 4 != 3):
                dif += abs(board[i] - board[i + 1])
            if (i < 12):
                dif += abs(board[i] - board[i + 4])
        
        return (tot * 4 - dif) * 2

    def search(self, board, depth):
        self.node += 1
        
        if (depth >= self.MAXDEPTH):
            return self.estimate(board)
        
        best = -1
        for i in range(4):
            res = self.moveLeft(board)
            nextBoard = res[0]
            same = True
            for j in range(16):
                if (nextBoard[j] != board[j]):
                    same = False
                    break

            if (not same):
                temp = 0
                empty = 0
                for j in range(16):
                    if (nextBoard[j] == 0):
                        nextBoard[j] = 2
                        empty += 1
                        temp += self.search(nextBoard, depth + 1) * 0.9
                        nextBoard[j] = 4
                        temp += self.search(nextBoard, depth + 1) * 0.1
                        nextBoard[j] = 0
                if (empty != 0):
                    temp = temp // empty
                else:
                    temp = -999999999
                if (res[1] + temp > best):
                    best = res[1] + temp
                    if (depth == 0):
                        self.next = i
            if (i != 3):
                board = self.rotate(board)

        return best
    
    def setTile(self, row, col, val):
        self.grid[row + col * 4] = val

    def startSearch(self, levels):
        self.node = 0
        self.MAXDEPTH = levels
        
        while (True):
            self.node = 0
            self.search(self.grid, 0)
            if (self.node >= 10000 or self.MAXDEPTH >= 8):
                break
            self.MAXDEPTH += 1

def smartAI(AIControl, box):
    # dimensions of game grid
    boxL = box.left
    boxT = box.top
    boxW = box.width
    boxH = box.height

    # constants for game
    nums = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    prev = []
    error = max(boxW, boxH) // 40
    x = max(boxW, boxH) // 41
    rows = [range(boxL + x - error, boxL + x + error + 1), range(boxL + 11 * x - error, boxL + 11 * x + error + 1), range(boxL + 21 * x - error, boxL + 21 * x + error + 1), range(boxL + 31 * x - error, boxL + 31 * x + error + 1)]
    cols = [range(boxT + x - error, boxT + x + error + 1), range(boxT + 11 * x - error, boxT + 11 * x + error + 1), range(boxT + 21 * x - error, boxT + 21 * x + error + 1), range(boxT + 31 * x - error, boxT + 31 * x + error + 1)]

    while (pyautogui.locateOnScreen('Images/gameover.png', confidence = 0.95) == None):
        AIControl.grid = [0 for i in range(16)]
        for n in nums:
            for pos in pyautogui.locateAllOnScreen('Images/{}.png'.format(n), region = (boxL, boxT, boxW, boxH), confidence = 0.95):
                x = -1
                y = -1
                for i in range(4):
                    if (pos.left in rows[i]):
                        x = i
                        break
                for i in range(4):
                    if (pos.top in cols[i]):
                        y = i
                        break
                AIControl.setTile(x, y, n)
        AIControl.startSearch(2)
        if (prev == AIControl.grid):
            AIControl.next = (AIControl.next + 2) % 4
        if (AIControl.next == 0):
            pyautogui.press('a')
        if (AIControl.next == 1):
            pyautogui.press('s')
        if (AIControl.next == 2):
            pyautogui.press('d')
        if (AIControl.next == 3):
            pyautogui.press('w')
        
        prev = AIControl.grid

def randomAI(AIControl, box):
    while (pyautogui.locateOnScreen('Images/gameover.png', confidence = 0.95) == None):
        # randomly picks a direction to move in
        AIControl.next = random.randint(0,4)
        if (AIControl.next == 0):
            pyautogui.press('w')
        if (AIControl.next == 1):
            pyautogui.press('d')
        if (AIControl.next == 2):
            pyautogui.press('s')
        if (AIControl.next == 3):
            pyautogui.press('a')

def main():
    AIControl = AI()

    # setting up 
    url = 'https://play2048.co/'
    webbrowser.open(url, new = 2)
    time.sleep(5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('-')
    pyautogui.press('-')
    pyautogui.keyUp('ctrl')

    # get placement of game box
    box = pyautogui.locateOnScreen('Images/boardnew.png', confidence = 0.5)

    # run algorithm choice
    start = time.time()
    smartAI(AIControl, box)
    # randomAI(AIControl, box)
    print(time.time() - start)

    # resetting to defaults
    pyautogui.keyDown('ctrl')
    pyautogui.press('+')
    pyautogui.press('+')
    pyautogui.keyUp('ctrl')

main()