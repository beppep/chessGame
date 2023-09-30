import pygame
import random

gridSize = 64
boardX = 300
boardY = 100
screenWidth = gridSize*8 + boardX*2
screenHeight = gridSize*8 + boardY*2

gameDisplay = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Chess!')
pygame.display.set_icon(pygame.image.load("assets/sprites/queen2.png"))

managers={
    "":pygame_gui.UIManager(resolution), #Main menu
    "p":pygame_gui.UIManager(resolution), #play
    "e":pygame_gui.UIManager(resolution), #edit piece
}

def posToCoords(pos):
    x = (pos[0]-boardX)//gridSize
    y = (pos[1]-boardY)//gridSize
    return (x,y)

def loadImage(name):
    img = pygame.image.load("assets/sprites/"+name+".png")
    img = pygame.transform.scale(img, (64,64))
    return img

def makeDarkImage(img):
    image = img.copy()
    colorImage = pygame.Surface(image.get_size()).convert_alpha()
    colorImage.fill((100,100,100))
    image.blit(colorImage, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
    return image

def classicSetup():
    Piece(0,0,1,"rook2")
    Piece(1,0,1,"knight")
    Piece(2,0,1,"bishop2")
    Piece(3,0,1,"queen2")
    Piece(4,0,1,"king")
    Piece(5,0,1,"bishop2")
    Piece(6,0,1,"knight")
    Piece(7,0,1,"rook2")
    Piece(0,7,0,"rook2")
    Piece(1,7,0,"knight")
    Piece(2,7,0,"bishop2")
    Piece(3,7,0,"queen2")
    Piece(4,7,0,"king")
    Piece(5,7,0,"bishop2")
    Piece(6,7,0,"knight")
    Piece(7,7,0,"rook2")
    for i in range(8):
        Piece(i,1,1,"pawn")
        Piece(i,6,0,"pawn")

class Sprites():

    lightImages = {}
    for name in ["king","pawn","rook","rook2","knight","knight2","bishop","bishop2","queen","queen2"]:
        lightImages[name] = loadImage(name)
    darkImages = {}
    for key in lightImages:
        darkImages[key] = makeDarkImage(lightImages[key])
    images = [lightImages, darkImages]

    famousPatterns = {
        "king":[
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,1,0,1,0],
            [0,1,1,1,0],
            [0,0,0,0,0],
        ],
        "pawn":[
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ],
        "rook":[
            [0,0,0,0,0],
            [0,0,1,0,0],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
        ],
        "rook2":[
            [0,0,0,0,0],
            [0,0,2,0,0],
            [0,2,0,2,0],
            [0,0,2,0,0],
            [0,0,0,0,0],
        ],
        "bishop":[
            [0,0,0,0,0],
            [0,1,0,1,0],
            [0,0,0,0,0],
            [0,1,0,1,0],
            [0,0,0,0,0],
        ],
        "bishop2":[
            [0,0,0,0,0],
            [0,2,0,2,0],
            [0,0,0,0,0],
            [0,2,0,2,0],
            [0,0,0,0,0],
        ],
        "knight":[
            [0,1,0,1,0],
            [1,0,0,0,1],
            [0,0,0,0,0],
            [1,0,0,0,1],
            [0,1,0,1,0],
        ],
        "knight2":[
            [0,2,0,2,0],
            [2,0,0,0,2],
            [0,0,0,0,0],
            [2,0,0,0,2],
            [0,2,0,2,0],
        ],
        "queen2":[
            [0,0,0,0,0],
            [0,2,2,2,0],
            [0,2,0,2,0],
            [0,2,2,2,0],
            [0,0,0,0,0],
        ],
    }

class MovePattern():

    def __init__(self):
        self.friendlyGrid = []
        self.attackGrid = []
        for i in range(5):
            self.friendlyGrid.append([None,None,None,None,None])
            self.attackGrid.append([None,None,None,None,None])

class Game():

    def __init__(self):
        self.state = None
        self.turn = 0
        self.selected = None

        self.grid = []
        for i in range(8):
            self.grid.append([])
            for j in range(8):
                self.grid[i].append(None)


    def click(self,coords):
        if coords[0]<0 or 7<coords[0] or coords[1]<0 or 7<coords[1]:
            self.selected = None
            return
        target = self.grid[coords[0]][coords[1]]
        if self.selected == None:
            if target == None:
                return
            if target.team == self.turn:
                self.selected = coords
                return
        else:
            myPiece = self.grid[self.selected[0]][self.selected[1]]
            if coords in myPiece.possibleMoves():
                # move
                if target != None:
                    Piece.pieces.remove(target)
                self.grid[self.selected[0]][self.selected[1]] = None
                self.grid[coords[0]][coords[1]] = myPiece
                myPiece.x, myPiece.y = coords
                self.turn = 1 - self.turn
                self.selected = None
            else:
                # deselect
                self.selected = None
                self.click(coords)
                return

    def drawGrid(self):
        for y in range(8):
            for x in range(8):
                color = [(200,160,120),(120,90,60)][((x+y)%2)]
                if self.selected == (x,y):
                    color = (100,200,100)
                pygame.draw.rect(gameDisplay, color, (boardX+64*x, boardY+64*y, 64, 64), 0)

        if self.selected:
            selectedPiece = self.grid[self.selected[0]][self.selected[1]]
            if selectedPiece:
                selectedPiece.drawMoves()


    def draw(self):
        self.drawGrid()

        for piece in Piece.pieces:
            piece.draw()

class Piece():

    pieces = []

    def __init__(self, x,y, team, preset=None, movePattern=None):
        self.pieces.append(self)
        self.x = x
        self.y = y
        game.grid[x][y] = self
        self.team = team
        self.color = [(255,255,150),(100,50,0)][team]
        if preset:
            self.movePattern = Sprites.famousPatterns[preset]
            self.art = preset
        else:
            self.movePattern = movePattern
            self.art = "pawn"
        if self.team == 1:
            self.movePattern = self.movePattern.copy()
            self.movePattern.reverse()

    def possibleMoves(self):
        moves = []
        for Y in range(5):
            for X in range(5):
                moveOption = self.movePattern[Y][X]
                if moveOption==1:
                    pos = (self.x + (X-2), self.y + (Y-2))
                    if pos[0]<0 or 7<pos[0] or pos[1]<0 or 7<pos[1]:
                        continue
                    target = game.grid[pos[0]][pos[1]]
                    if target == None:
                        moves.append(pos)
                    elif target.team != self.team:
                        moves.append(pos)
                elif moveOption==2:
                    for i in range(1,8):
                        pos = (self.x + (X-2)*i, self.y + (Y-2)*i)
                        if pos[0]<0 or 7<pos[0] or pos[1]<0 or 7<pos[1]:
                            break
                        target = game.grid[pos[0]][pos[1]]
                        if target == None:
                            moves.append(pos)
                        else:
                            if target.team != self.team:
                                moves.append(pos)
                            break
        return moves

    def drawMoves(self):
        """
        for Y in range(5):
            for X in range(5):
                moveOption = self.movePattern[Y][X]
                if moveOption==1:
                    color = (200,200,200)
                x = X+self.x-2
                y = Y+self.y-2
                if color != (0,0,0):
                    pygame.draw.rect(gameDisplay, color, (boardX+64*x, boardY+64*y, 64, 64), 0)
        """
        for pos in self.possibleMoves():
            pygame.draw.rect(gameDisplay, (200,200,200), (boardX+64*pos[0], boardY+64*pos[1], 64, 64), 0)



    def draw(self):
        x = self.x*64+boardX
        y = self.y*64+boardY
        gameDisplay.blit(Sprites.images[self.team][self.art], (x,y))


game = Game()
classicSetup()

jump_out = False
while jump_out == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jump_out = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                coords = posToCoords(pos)
                game.click(coords)
            if event.button == 3:
                game.selected = None

    game.click((random.randint(0,7),random.randint(0,7)))

    pressed = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    #Draw
    gameDisplay.fill((150,100,200))
    game.draw()

    pygame.display.update()
        
pygame.quit()
quit()