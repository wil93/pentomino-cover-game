#!/usr/bin/python2

# "Pentomino covering game"
# William Di Luigi

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
    """For each rotation of the polyomino, it should be specified the
    "offset" from the center (0, 0) for every piece. The offset is a
    tuple (dx, dy). The center (0, 0) should appear somewhere in the
    list as well as other pieces. The order of pieces doesn't matter
    """
    pos = (
        ((2, 0),  (1, 0),  (0, 0), (0, 1),  (0, 2)),
        ((-2, 0), (-1, 0), (0, 0), (0, 1),  (0, 2)),
        ((-2, 0), (-1, 0), (0, 0), (0, -1), (0, -2)),
        ((2, 0),  (1, 0),  (0, 0), (0, -1), (0, -2))
    )
    """For each rotation and for each piece of the polyomino it should
    be specified a bitmask to instruct the program on how to draw that
    piece. Each piece of polyomino will be splitted in 9 subrectangles,
    according to the scheme:
        .___.___________.___.
        |   |           |   |
        | 0 |     1     | 2 |
        |___|___________|___|
        |   |           |   |
        |   |           |   |
        | 3 |           | 4 |
        |   |           |   |
        |___|___________|___|
        |   |           |   |
        | 5 |     6     | 7 |
        |___|___________|___|

    The middle rectangle will always be full.
    If you want the i-th rectangle to be full, then the i-th bit of the
    bitmask should be set. For example if you want to draw a CROSS piece
    then you will need to have 1-th, 3-th, 4-th and 6-th bits set: so
    the bitmask of the CROSS piece is (2**1)+(2**3)+(2**4)+(2**6)=90.
    For readability it's better to set explicitly every bit of the mask,
    like the pentomino's shape encoded in the "info" array, for example
    """
    info = (
        (
            ((0 << 0) | (1 << 1) | (0 << 2) | (0 << 3) | (0 << 4) | (0 << 5) | (0 << 6) | (0 << 7)),
            ((0 << 0) | (1 << 1) | (0 << 2) | (0 << 3) | (0 << 4) | (0 << 5) | (1 << 6) | (0 << 7)),
            ((0 << 0) | (0 << 1) | (0 << 2) | (0 << 3) | (1 << 4) | (0 << 5) | (1 << 6) | (0 << 7)),
            ((0 << 0) | (0 << 1) | (0 << 2) | (1 << 3) | (1 << 4) | (0 << 5) | (0 << 6) | (0 << 7)),
            ((0 << 0) | (0 << 1) | (0 << 2) | (1 << 3) | (0 << 4) | (0 << 5) | (0 << 6) | (0 << 7))
        ),
        (
            ((0 << 0) | (0 << 1) | (0 << 2) | (0 << 3) | (0 << 4) | (0 << 5) | (1 << 6) | (0 << 7)),
            ((0 << 0) | (1 << 1) | (0 << 2) | (0 << 3) | (0 << 4) | (0 << 5) | (1 << 6) | (0 << 7)),
            ((0 << 0) | (1 << 1) | (0 << 2) | (0 << 3) | (1 << 4) | (0 << 5) | (0 << 6) | (0 << 7)),
            ((0 << 0) | (0 << 1) | (0 << 2) | (1 << 3) | (1 << 4) | (0 << 5) | (0 << 6) | (0 << 7)),
            ((0 << 0) | (0 << 1) | (0 << 2) | (1 << 3) | (0 << 4) | (0 << 5) | (0 << 6) | (0 << 7))
        ),
        (
            ((0 << 0) | (0 << 1) | (0 << 2) | (0 << 3) | (0 << 4) | (0 << 5) | (1 << 6) | (0 << 7)),
            ((0 << 0) | (1 << 1) | (0 << 2) | (0 << 3) | (0 << 4) | (0 << 5) | (1 << 6) | (0 << 7)),
            ((0 << 0) | (1 << 1) | (0 << 2) | (1 << 3) | (0 << 4) | (0 << 5) | (0 << 6) | (0 << 7)),
            ((0 << 0) | (0 << 1) | (0 << 2) | (1 << 3) | (1 << 4) | (0 << 5) | (0 << 6) | (0 << 7)),
            ((0 << 0) | (0 << 1) | (0 << 2) | (0 << 3) | (1 << 4) | (0 << 5) | (0 << 6) | (0 << 7))
        ),
        (
            ((0 << 0) | (1 << 1) | (0 << 2) | (0 << 3) | (0 << 4) | (0 << 5) | (0 << 6) | (0 << 7)),
            ((0 << 0) | (1 << 1) | (0 << 2) | (0 << 3) | (0 << 4) | (0 << 5) | (1 << 6) | (0 << 7)),
            ((0 << 0) | (0 << 1) | (0 << 2) | (1 << 3) | (0 << 4) | (0 << 5) | (1 << 6) | (0 << 7)),
            ((0 << 0) | (0 << 1) | (0 << 2) | (1 << 3) | (1 << 4) | (0 << 5) | (0 << 6) | (0 << 7)),
            ((0 << 0) | (0 << 1) | (0 << 2) | (0 << 3) | (1 << 4) | (0 << 5) | (0 << 6) | (0 << 7))
        )
    )

    def __init__(self, num_rows, num_cols, best_possible):
        self.rows = num_rows
        self.cols = num_cols
        self.expectedBest = best_possible
        # create the root and the canvas
        root = Tk()
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
        root.bind("<Button-4>", self.rollWheel)
        root.bind("<Button-5>", self.rollWheel)
        root.bind("<MouseWheel>", self.rollWheelDelta)
        root.bind("<Key>", self.keyPressed)

    def gameOver(self):
        """Game over: clears background, unbinds events so the user can
        enjoy his result, updates title: "You won"
        """
        self.correctPending()
        self.updateTitle("You won !!")
        self.unbind("<Motion>")
        self.unbind("<Leave>")
        self.unbind("<Button-1>")
        self.unbind("<Button-4>")
        self.unbind("<Button-5>")
        self.unbind("<Key>")

    def refreshScore(self):
        """Visually updates the score reached by the user: actually it
        just changes the window title :P
        """
        self.updateTitle(str(self.onBoard) + " / " + str(self.expectedBest))

    def checkAvailable(self, x, y):
        """Checks if the cell at (x, y) is on the board AND is not busy
        """
        return 0 <= x < self.rows and 0 <= y < self.cols and not self.gridBusy[x][y]

    def checkFree(self, x, y):
        """Checks whether the position (x, y) is available or not.
        Returns the color to use for the background ('busy' or 'free')
        """
        for i in xrange(self.numPieces):
            new_x = x + self.pos[self.rotation][i][0]
            new_y = y + self.pos[self.rotation][i][1]
            if not self.checkAvailable(new_x, new_y):
                return self.colors['busy']
        return self.colors['free']

    def doPaint(self, x, y, color, pattern=""):
        """Does the actual painting: it paints with the specified color
        and pattern the background at (x, y). If a pattern isn't
        specified it won't be used
        """
        for i in xrange(self.numPieces):
            new_x = x + self.pos[self.rotation][i][0]
            new_y = y + self.pos[self.rotation][i][1]
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                for item in self.gridBG[new_x][new_y][0]:
                    self.canvas.itemconfigure(item, fill=color, stipple=pattern)

    def correctPending(self):
        """Restores to the normal state the last painted background
        """
        if self.lastPainted:
            self.doPaint(self.lastPainted[0], self.lastPainted[1], self.colors['idle'], "gray75")
            self.lastPainted = None

    def paintBackground(self, x, y, color):
        """Updates background to visually indicate whether the position
        (x, y) is available or not
        """
        self.correctPending()
        self.lastPainted = (x, y)
        self.doPaint(x, y, color)

    def mouseOut(self, event):
        """Catch mouseout in order to clean the last background painted
        when the cursor leaves the grid
        """
        if self.editMode and self.lastChanged:
            self.changeColor(self.lastChanged, self.colors['pentomino'])
            return
        self.correctPending()
        self.lastPosition = None

    def mouseOver(self, event):
        """Catch mouseover to paint the background accordingly to the
        availability of the pentomino space under the cursor
        """
        if self.editMode:
            self.setEditCursor(event)
            return
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        if self.lastPosition == (x, y):
            return  # I've already drawn this
        if not (0 <= x < self.rows and 0 <= y < self.cols):
            return  # not on the grid
        self.lastPosition = (x, y)
        self.paintBackground(x, y, self.checkFree(x, y))

    def mouseClick(self, event):
        """Catch mouse click to confirm the insertion or removal (if in
        Edit mode) of a pentomino on the cell under the mouse pointer
        """
        if self.editMode:
            self.applyEditing(event)
            self.clearEditCursor(event)
            return
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        if self.checkFree(x, y) == self.colors['busy']:
            return  # clicked busy position
        self.onBoard += 1
        self.refreshScore()
        self.history.append((
            self.setBusy(x, y),
            self.addPentomino(x, y)
        ))
        if self.onBoard == self.expectedBest:
            self.gameOver()

    def goBackInTime(self):
        """Removes the most recently inserted pentomino
        """
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
        """Sets as "busy" the cells occupied by a pentomino centered at
        (x, y) rotated as the current rotation stored in self.rotation
        """
        changes = []
        for i in xrange(self.numPieces):
            new_x = x + self.pos[self.rotation][i][0]
            new_y = y + self.pos[self.rotation][i][1]
            changes.append((new_x, new_y))
            self.gridBusy[new_x][new_y] = self.onBoard
        self.correctPending()
        return changes

    def addPentomino(self, x, y):
        """Adds a new pentomino with its center in the position (x, y)
        of the grid and returns the list of changes done. Each element
        of the list returned is a cell (that is the list of IDs of the
        new drawn items)
        """
        changes = []
        for i in xrange(self.numPieces):
            new_x = x + self.pos[self.rotation][i][0]
            new_y = y + self.pos[self.rotation][i][1]
            changes.append(self.drawCell(
                new_x, new_y, self.colors['pentomino'], self.info[self.rotation][i]
            ))
        return changes

    def doRotation(self, delta):
        """Sets the current rotation value to be rotated delta times by
        90 degrees CW. If delta is negative the rotation is CCW
        """
        self.correctPending()
        self.rotation = (self.rotation + delta) % self.possibleRotations

    def rollWheel(self, event):
        """Catch mousewheel scrolling to change the rotation
        """
        if event.num == 4:
            self.doRotation(-1)  # CCW rotation
        elif event.num == 5:
            self.doRotation(+1)  # CW rotation
        else:
            return
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        self.paintBackground(x, y, self.checkFree(x, y))

    def rollWheelDelta(self, event):
        """Catch mousewheel scrolling to change the rotation: this is
        a version for newer mice (I think) because I had to add it to
        make the rotation work properly with a newer mouse. It would be
        nice to merge this routine with self.rollWheel()
        """
        if event.delta < 0:
            self.doRotation(-1)  # CCW rotation
        elif event.delta > 0:
            self.doRotation(+1)  # CW rotation
        else:
            return
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        self.paintBackground(x, y, self.checkFree(x, y))

    def applyEditing(self, event):
        """Only called if in Edit mode: removes the pentomino that is
        currently under the mouse pointer. The pentomino is popped from
        history and every other (more recent) pentomino is updated with
        a new pentNumber (decreased by 1) to mantain the consistence of
        history ordering
        """
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

    def setEditCursor(self, event):
        """Enters edit mode and sets the "X" cursor
        """
        self.editMode = True
        self.updateCursor("X_cursor")
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

    def clearEditCursor(self, event):
        """Exits from edit mode and restores the classic arrow cursor
        """
        self.editMode = False
        self.updateCursor("arrow")
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        self.paintBackground(x, y, self.checkFree(x, y))

    def changeColor(self, pentNumber, color):
        """Updates the internal color of the pentNumber-th pentomino in
        the insertion history
        """
        if not pentNumber:
            return
        assert(len(self.history) >= pentNumber)
        for cell in self.history[pentNumber - 1][1]:
            for item in cell[0]:
                self.canvas.itemconfigure(item, fill=color)

    def keyPressed(self, event):
        """Catches when a key is pressed
        """
        if event.char == "r":
            self.init()
            return
        elif event.char == ' ':
            if self.editMode:
                self.changeColor(self.lastChanged, self.colors['pentomino'])
                self.clearEditCursor(event)
                return
            self.correctPending()
            self.setEditCursor(event)
            return
        elif event.keysym == "BackSpace":
            self.goBackInTime()
        elif event.keysym == "Right":
            self.doRotation(+1)  # CW rotation
        elif event.keysym == "Left":
            self.doRotation(-1)  # CCW rotation
        else:
            return
        x = (event.y - self.margin) / self.cellSize
        y = (event.x - self.margin) / self.cellSize
        self.paintBackground(x, y, self.checkFree(x, y))

    def redrawAll(self):
        """Cleans the canvas and draws a new grid
        """
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

    def drawCell(self, x, y, bgColor, closedSection=255, borderColor="", bgPattern=""):
        """Draws a new cell at position (x, y) of the grid. Returns a
        2-tuple of lists: the first list contains the rectangles (at
        most 9) and the second list contains the lines (at most 8).
        These rectangles and lines represent the cell's shape for this
        pentomino piece (as defined in "info" array)
        """
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
        if closedSection & (1 << 0):
            sections[0].append(self.canvas.create_rectangle(
                left,
                top,
                1 + right - adjustValue,
                1 + bottom - adjustValue,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if closedSection & (1 << 1):
            sections[0].append(self.canvas.create_rectangle(
                left + self.pentPadding,
                top,
                1 + right - self.pentPadding,
                1 + bottom - adjustValue,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if closedSection & (1 << 2):
            sections[0].append(self.canvas.create_rectangle(
                left + adjustValue,
                top,
                1 + right,
                1 + bottom - adjustValue,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if closedSection & (1 << 3):
            sections[0].append(self.canvas.create_rectangle(
                left,
                top + self.pentPadding,
                1 + right - adjustValue,
                1 + bottom - self.pentPadding,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if closedSection & (1 << 4):
            sections[0].append(self.canvas.create_rectangle(
                left + adjustValue,
                top + self.pentPadding,
                1 + right,
                1 + bottom - self.pentPadding,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if closedSection & (1 << 5):
            sections[0].append(self.canvas.create_rectangle(
                left,
                top + adjustValue,
                1 + right - adjustValue,
                1 + bottom,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if closedSection & (1 << 6):
            sections[0].append(self.canvas.create_rectangle(
                left + self.pentPadding,
                top + adjustValue,
                1 + right - self.pentPadding,
                1 + bottom,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        if closedSection & (1 << 7):
            sections[0].append(self.canvas.create_rectangle(
                left + adjustValue,
                top + adjustValue,
                1 + right,
                1 + bottom,
                fill=bgColor, outline=borderColor, stipple=bgPattern
            ))
        # main section's borders
        if not closedSection & (1 << 1):
            sections[1].append(self.canvas.create_line(
                left + self.pentPadding,
                top + self.pentPadding,
                1 + right - self.pentPadding,
                bottom - adjustValue
            ))
        if not closedSection & (1 << 3):
            sections[1].append(self.canvas.create_line(
                left + self.pentPadding,
                top + self.pentPadding,
                right - adjustValue,
                1 + bottom - self.pentPadding
            ))
        if not closedSection & (1 << 4):
            sections[1].append(self.canvas.create_line(
                left + adjustValue,
                top + self.pentPadding,
                right - self.pentPadding,
                1 + bottom - self.pentPadding
            ))
        if not closedSection & (1 << 6):
            sections[1].append(self.canvas.create_line(
                left + self.pentPadding,
                top + adjustValue,
                1 + right - self.pentPadding,
                bottom - self.pentPadding
            ))
        # border sections' borders
        if (closedSection & (1 << 1)) and not (closedSection & (1 << 0)):
            sections[1].append(self.canvas.create_line(
                left + self.pentPadding,
                top,
                right - adjustValue,
                1 + bottom - adjustValue
            ))
        if (closedSection & (1 << 1)) and not (closedSection & (1 << 2)):
            sections[1].append(self.canvas.create_line(
                left + adjustValue,
                top,
                right - self.pentPadding,
                1 + bottom - adjustValue
            ))
        if (closedSection & (1 << 4)) and not (closedSection & (1 << 2)):
            sections[1].append(self.canvas.create_line(
                left + adjustValue,
                top + self.pentPadding,
                1 + right,
                bottom - adjustValue
            ))
        if (closedSection & (1 << 4)) and not (closedSection & (1 << 7)):
            sections[1].append(self.canvas.create_line(
                left + adjustValue,
                top + adjustValue,
                1 + right,
                bottom - self.pentPadding
            ))
        if (closedSection & (1 << 6)) and not (closedSection & (1 << 7)):
            sections[1].append(self.canvas.create_line(
                left + adjustValue,
                top + adjustValue,
                right - self.pentPadding,
                1 + bottom
            ))
        if (closedSection & (1 << 6)) and not (closedSection & (1 << 5)):
            sections[1].append(self.canvas.create_line(
                left + self.pentPadding,
                top + adjustValue,
                right - adjustValue,
                1 + bottom
            ))
        if (closedSection & (1 << 3)) and not (closedSection & (1 << 5)):
            sections[1].append(self.canvas.create_line(
                left,
                top + adjustValue,
                1 + right - adjustValue,
                bottom - self.pentPadding
            ))
        if (closedSection & (1 << 3)) and not (closedSection & (1 << 0)):
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
        self.refreshScore()

if __name__ == '__main__':
    game = Game(12, 12, 27)
    game.start()
