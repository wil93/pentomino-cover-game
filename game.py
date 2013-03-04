# 

from Tkinter import Tk, Canvas, ALL

class Game:
    margin = 10
    cellSize = 35
    pentPadding = 5
    # it's better if: cellSize % (dashBlack + dashWhite) == 0
    dashBlack, dashWhite = 3, 2
    colors = {
        'idle'      : 'white',
        'free'      : 'yellow',
        'busy'      : '#F3C0BB',
        'pentomino' : '#D8B042',
        'pent_edit' : '#CB1222'
    }
    possibleRotations = 4
    numPieces = 5
    pos = (
        ((2,0),  (1,0),  (0,0), (0,1),  (0,2)),
        ((-2,0), (-1,0), (0,0), (0,1),  (0,2)),
        ((-2,0), (-1,0), (0,0), (0,-1), (0,-2)),
        ((2,0),  (1,0),  (0,0), (0,-1), (0,-2))
    )
    info = (
        (
            ((1 << 0) | (0 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7)),
            ((1 << 0) | (0 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (0 << 6) | (1 << 7)),
            ((1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (0 << 4) | (1 << 5) | (0 << 6) | (1 << 7)),
            ((1 << 0) | (1 << 1) | (1 << 2) | (0 << 3) | (0 << 4) | (1 << 5) | (1 << 6) | (1 << 7)),
            ((1 << 0) | (1 << 1) | (1 << 2) | (0 << 3) | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7))
        ),
        (
            ((1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (0 << 6) | (1 << 7)),
            ((1 << 0) | (0 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (0 << 6) | (1 << 7)),
            ((1 << 0) | (0 << 1) | (1 << 2) | (1 << 3) | (0 << 4) | (1 << 5) | (1 << 6) | (1 << 7)),
            ((1 << 0) | (1 << 1) | (1 << 2) | (0 << 3) | (0 << 4) | (1 << 5) | (1 << 6) | (1 << 7)),
            ((1 << 0) | (1 << 1) | (1 << 2) | (0 << 3) | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7))
        ),
        (
            ((1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (0 << 6) | (1 << 7)),
            ((1 << 0) | (0 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (0 << 6) | (1 << 7)),
            ((1 << 0) | (0 << 1) | (1 << 2) | (0 << 3) | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7)),
            ((1 << 0) | (1 << 1) | (1 << 2) | (0 << 3) | (0 << 4) | (1 << 5) | (1 << 6) | (1 << 7)),
            ((1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (0 << 4) | (1 << 5) | (1 << 6) | (1 << 7))
        ),
        (
            ((1 << 0) | (0 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7)),
            ((1 << 0) | (0 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (0 << 6) | (1 << 7)),
            ((1 << 0) | (1 << 1) | (1 << 2) | (0 << 3) | (1 << 4) | (1 << 5) | (0 << 6) | (1 << 7)),
            ((1 << 0) | (1 << 1) | (1 << 2) | (0 << 3) | (0 << 4) | (1 << 5) | (1 << 6) | (1 << 7)),
            ((1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (0 << 4) | (1 << 5) | (1 << 6) | (1 << 7))
        )
    )
    
    def __init__(self, num_rows, num_cols, window_title, best_possible):
        self.rows = num_rows
        self.cols = num_cols
        self.expectedBest = best_possible
        # create the root and the canvas
        root = Tk()
        root.title(window_title)
        # local function to unbind events
        self.unbind = root.unbind
        # local function to change title
        self.updateTitle = root.title
        # local function to change cursor
        self.updateCursor = lambda x: root.config(cursor=x)
        # local function to start game
        self.start = root.mainloop
        # get screen width and height
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        self.canvasWidth = 2 * self.margin + self.cols * self.cellSize
        self.canvasHeight = 2 * self.margin + self.rows * self.cellSize
        self.canvas = Canvas(root, width=self.canvasWidth, height=self.canvasHeight)
        self.canvas.pack()
        # calculate position x, y
        x = (ws - self.canvasWidth) / 2
        y = (hs - self.canvasHeight) / 2
        root.geometry('%dx%d+%d+%d' % (self.canvasWidth, self.canvasHeight, x, y))
        root.resizable(width=0, height=0)
        self.init()
        # set up events
        root.bind("<Motion>", self.mouseOver)
        root.bind("<Leave>", self.mouseOut)
        root.bind("<Button-1>", self.mouseClick)
        root.bind('<Button-4>', self.rollWheel)
        root.bind('<Button-5>', self.rollWheel)
        root.bind("<Key>", self.keyPressed)

    def gameOver(self):
        self.correctPending()
        self.unbind("<Motion>")
        self.unbind("<Leave>")
        self.unbind("<Button-1>")
        self.unbind("<Button-4>")
        self.unbind("<Button-5>")
        self.unbind("<Key>")

    def refreshScore(self):
        self.updateTitle(str(self.onBoard) + " / " + str(self.expectedBest))

    def checkAvailable(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols and not self.gridBusy[x][y]

    def checkFree(self, x, y):
        for i in xrange(self.numPieces):
            if not self.checkAvailable(
                x + self.pos[self.rotation][i][0],
                y + self.pos[self.rotation][i][1]
                ):
                return self.colors['busy']
        return self.colors['free']

    def doPaint(self, x, y, color, pattern=""):
        for i in xrange(self.numPieces):
            if 0 <= x + self.pos[self.rotation][i][0] < self.rows and \
                0 <= y + self.pos[self.rotation][i][1] < self.cols:
                for item in self.gridBG[ x + self.pos[self.rotation][i][0] ][ y + self.pos[self.rotation][i][1] ][0]:
                    self.canvas.itemconfigure(item, fill=color, stipple=pattern)

    def correctPending(self):
        if self.lastPainted:
            self.doPaint(self.lastPainted[0], self.lastPainted[1], self.colors['idle'], "gray75")
            self.lastPainted = None

    def paintBackground(self, x, y, color):
        self.correctPending()
        self.lastPainted = (x, y)
        self.doPaint(x, y, color)

    def mouseOut(self, event):
        if self.editMode and self.lastChanged:
            self.changeColor(self.lastChanged, self.colors['pentomino'])
            return
        self.correctPending()
        self.lastPosition = None

    def mouseOver(self, event):
        if self.editMode:
            self.setEditCursor(event)
            return
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        if self.lastPosition == (x, y):
            return # I've already drawn this
        if not ( 0 <= x < self.rows and 0 <= y < self.cols ):
            return # not on the grid
        self.lastPosition = (x, y)
        self.paintBackground(x, y, self.checkFree(x, y))

    def goBackInTime(self):
        if (len(self.history) == 0):
            return
        notBusy, notVisible = self.history.pop()
        for cell in notVisible:
            for item in cell[0] + cell[1]:
                self.canvas.delete(item)
        for x, y in notBusy:
            self.gridBusy[x][y] = 0
        self.onBoard -= 1
        self.refreshScore()

    def setBusy(self, x, y):
        changes = []
        for i in xrange(self.numPieces):
            changes.append((x + self.pos[self.rotation][i][0], y + self.pos[self.rotation][i][1]))
            self.gridBusy[ changes[-1][0] ][ changes[-1][1] ] = self.onBoard
        self.correctPending()
        return changes

    def addPentomino(self, x, y):
        changes = []
        for i in xrange(self.numPieces):
            changes.append(self.drawCell(
                x + self.pos[self.rotation][i][0], y + self.pos[self.rotation][i][1],
                self.colors['pentomino'], self.info[self.rotation][i]
            ))
        return changes

    def mouseClick(self, event):
        if self.editMode:
            self.applyEditing(event)
            self.clearEditCursor(event)
            return
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        if self.checkFree(x, y) == self.colors['busy']:
            return # clicked busy position
        self.onBoard += 1
        self.refreshScore()
        self.history.append((
            self.setBusy(x, y),
            self.addPentomino(x, y)
        ))
        if self.onBoard == self.expectedBest:
            self.gameOver()

    def doRotation(self, delta):
        self.correctPending()
        self.rotation = (self.rotation + delta) % self.possibleRotations

    def rollWheel(self, event):
        if event.num == 4:
            self.doRotation( -1 ) # CCW rotation
        elif event.num == 5:
            self.doRotation( +1 ) # CW rotation
        else:
            return
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        self.paintBackground(x, y, self.checkFree(x, y))
    
    def applyEditing(self, event):
        self.lastChanged = None
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        if not (0 <= x < self.rows and 0 <= y < self.cols):
            return
        if not self.gridBusy[x][y]:
            return
        assert len(self.history) >= self.gridBusy[x][y]
        for busy, items in self.history[self.gridBusy[x][y] : ]:
            for i, j in busy:
                self.gridBusy[i][j] -= 1
        notBusy, notVisible = self.history.pop(self.gridBusy[x][y] - 1)
        for cell in notVisible:
            for item in cell[0] + cell[1]:
                self.canvas.delete(item)
        for i, j in notBusy:
            self.gridBusy[i][j] = 0
        self.onBoard -= 1
        self.refreshScore()
    
    def clearEditCursor(self, event):
        self.editMode = False
        self.updateCursor("arrow")
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        self.paintBackground(x, y, self.checkFree(x, y))
    
    def changeColor(self, pentNumber, color):
        if not pentNumber:
            return
        assert(len(self.history) >= pentNumber)
        for cell in self.history[pentNumber - 1][1]:
            for item in cell[0]:
                self.canvas.itemconfigure(item, fill=color)
    
    def setEditCursor(self, event):
        self.changeColor(self.lastChanged, self.colors['pentomino'])
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        if not (0 <= x < self.rows and 0 <= y < self.cols):
            return
        if not self.gridBusy[x][y]:
            return
        assert len(self.history) >= self.gridBusy[x][y]
        self.lastChanged = self.gridBusy[x][y]
        self.changeColor(self.lastChanged, self.colors['pent_edit'])

    def keyPressed(self, event):
        if event.char == "r":
            self.init()
            return
        elif event.char == ' ':
            if self.editMode:
                self.changeColor(self.lastChanged, self.colors['pentomino'])
                self.clearEditCursor(event)
                return
            self.correctPending()
            self.editMode = True
            self.updateCursor("X_cursor")
            self.setEditCursor(event)
            return
        elif event.keysym == "BackSpace":
            self.goBackInTime()
        elif event.keysym == "Right":
            self.doRotation( +1 ) # CW rotation
        elif event.keysym == "Left":
            self.doRotation( -1 ) # CCW rotation
        else:
            return
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        self.paintBackground(x, y, self.checkFree(x, y))

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.gridBG = []
        self.gridBusy = []
        for row in range(self.rows):
            self.gridBG.append([])
            self.gridBusy.append([])
            for col in range(self.cols):
                self.gridBG[row].append(self.drawCell(row, col, self.colors['idle'], bgPattern="gray75"))
                self.gridBusy[row].append(0)
        for row in range(self.rows + 1):
            self.canvas.create_line(
                self.margin,
                self.margin + row * self.cellSize,
                self.margin + self.cols * self.cellSize,
                self.margin + row * self.cellSize,
                dash=(self.dashBlack, self.dashWhite)
            )
        for col in range(self.cols + 1):
            self.canvas.create_line(
                self.margin + col * self.cellSize,
                self.margin,
                self.margin + col * self.cellSize,
                self.margin + self.rows * self.cellSize,
                dash=(self.dashBlack, self.dashWhite)
            )

    def drawCell(self, x, y, bgColor, openSection=0, borderColor="", bgPattern=""):
        left = self.margin + y * self.cellSize
        right = left + self.cellSize
        top = self.margin + x * self.cellSize
        bottom = top + self.cellSize
        adjustValue = self.cellSize - self.pentPadding
        # sections tuple = ([rectangles], [lines])
        sections = ([], [])
        # main section
        sections[0].append(self.canvas.create_rectangle(
            left + self.pentPadding,
            top + self.pentPadding,
            1 + right - self.pentPadding,
            1 + bottom - self.pentPadding,
            fill=bgColor, outline=borderColor, stipple=bgPattern
        ))
        # border sections
        if not openSection & (1 << 0):
            sections[0].append(self.canvas.create_rectangle(
                left,
                top,
                1 + right - adjustValue,
                1 + bottom - adjustValue,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if not openSection & (1 << 1):
            sections[0].append(self.canvas.create_rectangle(
                left + self.pentPadding,
                top,
                1 + right - self.pentPadding,
                1 + bottom - adjustValue,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if not openSection & (1 << 2):
            sections[0].append(self.canvas.create_rectangle(
                left + adjustValue,
                top,
                1 + right,
                1 + bottom - adjustValue,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if not openSection & (1 << 3):
            sections[0].append(self.canvas.create_rectangle(
                left,
                top + self.pentPadding,
                1 + right - adjustValue,
                1 + bottom - self.pentPadding,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if not openSection & (1 << 4):
            sections[0].append(self.canvas.create_rectangle(
                left + adjustValue,
                top + self.pentPadding,
                1 + right,
                1 + bottom - self.pentPadding,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if not openSection & (1 << 5):
            sections[0].append(self.canvas.create_rectangle(
                left,
                top + adjustValue,
                1 + right - adjustValue,
                1 + bottom,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if not openSection & (1 << 6):
            sections[0].append(self.canvas.create_rectangle(
                left + self.pentPadding,
                top + adjustValue,
                1 + right - self.pentPadding,
                1 + bottom,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if not openSection & (1 << 7):
            sections[0].append(self.canvas.create_rectangle(
                left + adjustValue,
                top + adjustValue,
                1 + right,
                1 + bottom,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        # main section's borders
        if openSection & (1 << 1):
            sections[1].append(self.canvas.create_line(
                left + self.pentPadding,
                top + self.pentPadding,
                1 + right - self.pentPadding,
                bottom - adjustValue
            ))
        if openSection & (1 << 3):
            sections[1].append(self.canvas.create_line(
                left + self.pentPadding,
                top + self.pentPadding,
                right - adjustValue,
                1 + bottom - self.pentPadding
            ))
        if openSection & (1 << 4):
            sections[1].append(self.canvas.create_line(
                left + adjustValue,
                top + self.pentPadding,
                right - self.pentPadding,
                1 + bottom - self.pentPadding
            ))
        if openSection & (1 << 6):
            sections[1].append(self.canvas.create_line(
                left + self.pentPadding,
                top + adjustValue,
                1 + right - self.pentPadding,
                bottom - self.pentPadding
            ))
        # border sections' borders
        if (not openSection & (1 << 1)) and (openSection & (1 << 0)):
            sections[1].append(self.canvas.create_line(
                left + self.pentPadding,
                top,
                right - adjustValue,
                1 + bottom - adjustValue
            ))
        if (not openSection & (1 << 1)) and (openSection & (1 << 2)):
            sections[1].append(self.canvas.create_line(
                left + adjustValue,
                top,
                right - self.pentPadding,
                1 + bottom - adjustValue
            ))
        if (not openSection & (1 << 4)) and (openSection & (1 << 2)):
            sections[1].append(self.canvas.create_line(
                left + adjustValue,
                top + self.pentPadding,
                1 + right,
                bottom - adjustValue
            ))
        if (not openSection & (1 << 4)) and (openSection & (1 << 7)):
            sections[1].append(self.canvas.create_line(
                left + adjustValue,
                top + adjustValue,
                1 + right,
                bottom - self.pentPadding
            ))
        if (not openSection & (1 << 6)) and (openSection & (1 << 7)):
            sections[1].append(self.canvas.create_line(
                left + adjustValue,
                top + adjustValue,
                right - self.pentPadding,
                1 + bottom
            ))
        if (not openSection & (1 << 6)) and (openSection & (1 << 5)):
            sections[1].append(self.canvas.create_line(
                left + self.pentPadding,
                top + adjustValue,
                right - adjustValue,
                1 + bottom
            ))
        if (not openSection & (1 << 3)) and (openSection & (1 << 5)):
            sections[1].append(self.canvas.create_line(
                left,
                top + adjustValue,
                1 + right - adjustValue,
                bottom - self.pentPadding
            ))
        if (not openSection & (1 << 3)) and (openSection & (1 << 0)):
            sections[1].append(self.canvas.create_line(
                left,
                top + self.pentPadding,
                1 + right - adjustValue,
                bottom - adjustValue
            ))
        return sections

    def init(self):
        self.onBoard = 0
        self.rotation = 0
        self.lastPosition = None
        self.lastPainted = None
        self.lastChanged = None
        self.editMode = False
        self.history = []
        self.redrawAll()

if __name__ == '__main__':
    game = Game(8, 8, "0 / 12", 12)
    game.start()
