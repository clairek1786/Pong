# this is pong v1.0; this project is complete (still buggy but I will practice some pygame to make it better :fingers crossed:)
# using turtle and not pygame

import turtle
import time
import keyboard
import random

# defines screen as window
window = turtle.Screen()

# sets screensize
window.setup(width=750, height=580)

# sets screen title
window.title("Pong")

# disables screen updates
window.tracer(0)

window.bgcolor("black")

# rectangle size
rectangleWidth = 20
rectangleLength = 120

# player speed
playerSpeed = 8

# defines player 1's turtle
player1 = turtle.Turtle()
player1.speed(0)
player1.up()
player1.fillcolor("#2596be")
player1.color("#2596be")
player1.hideturtle()
player1Score = 0

# defines player 1's starting coordinates
player1X = -335
player1Y = 0

# defines player 2's turtle
player2 = turtle.Turtle()
player2.speed(0)
player2.up()
player2.fillcolor("#d93a4a")
player2.color("#d93a4a")
player2.hideturtle()
player2Score = 0

# for ai random paddle landing
paddleLandingDetermined = False

# defines player 2's starting coordinates
player2X = 325
player2Y = 0

# defines the pong
pong = turtle.Turtle()
pong.speed(0)
pong.hideturtle()
pong.fillcolor("white")
pong.color("white")
pong.up()
pongRadius = 6
pongX = 0
pongY = 0
pongSpeedMult = 1

# defines pong serving velocity
pongVX = -1 * random.randrange(6,9)
pongVY = random.randrange(2,5)

# defines score turtle for player 1
scoreWriter = turtle.Turtle()
scoreWriter.up()
scoreWriter.hideturtle()
scoreWriter.color("#2596be")

# defines score turtle for player 2
scoreWriter2 = turtle.Turtle()
scoreWriter2.up()
scoreWriter2.hideturtle()
scoreWriter2.color("#d93a4a")

# defines top and bottom barriers
barrierLength = 20
barrierWidth = 700

# top barrier
topBarrier = turtle.Turtle()
topBarrier.up()
topBarrier.hideturtle()
topBarrier.fillcolor("white")
topBarrier.color("white")
topBarrierX = 0
topBarrierY = 255

# bottom barrier
bottomBarrier = turtle.Turtle()
bottomBarrier.up()
bottomBarrier.hideturtle()
bottomBarrier.fillcolor("white")
bottomBarrier.color("white")
bottomBarrierX = 0
bottomBarrierY = -255

# defines the net
net = turtle.Turtle()
net.up()
net.hideturtle()
net.fillcolor("white")
net.color("white")
netSideLength = 6
netDistance = 20
netX = 0
netY = 250

# animated shapes
def drawRectangle(rectangle, w, l, x, y):
    # x and y are center coordinates
    # moves turtle to top left corner of rectangle
    startCoordinatesX = x - (w / 2)
    startCoordinatesY = y + (l / 2)

    # goes to top left corner
    rectangle.goto(startCoordinatesX, startCoordinatesY)

    # resets heading
    rectangle.setheading(0)

    # draws rectangle and fills it
    rectangle.down()
    rectangle.begin_fill()
    rectangle.forward(w)
    rectangle.right(90)
    rectangle.forward(l)
    rectangle.right(90)
    rectangle.forward(w)
    rectangle.right(90)
    rectangle.forward(l)
    rectangle.end_fill()
    rectangle.up()

    # returns turtle to center
    rectangle.goto(x, y)
    
def drawPong(pong, radius, x, y):
    # x and y are center coordinates
    startCoordinatesX = x
    startCoordinatesY = y - 3

    # goes to starting coords
    pong.goto(startCoordinatesX, startCoordinatesY)

    # draws pong
    pong.down()
    pong.begin_fill()
    pong.circle(radius)
    pong.end_fill()
    pong.up()

    pong.goto(x, y)

def displayScore():
    # turtle.write(arg, move=False, align=’left’, font=(‘Arial’, 8, ‘normal’))
    global scoreWriter
    global scoreWriter2

    global player1Score
    global player2Score

    # moves writing spot to the left a little bit if the score gets higher than 10
    if player1Score >= 10:
        scoreWriter.goto(-50, 200)
    else:
        scoreWriter.goto(-40, 200)
    scoreWriter.write(str(player1Score), font=("Consolas", 20, "normal"))

    scoreWriter2.goto(25, 200)
    scoreWriter2.write(str(player2Score), font=("Consolas", 20, "normal"))

# draws animated shapes
def drawShapes():
    # paddles
    drawRectangle(player1, rectangleWidth, rectangleLength, player1X, player1Y)
    drawRectangle(player2, rectangleWidth, rectangleLength, player2X, player2Y)

    # pong
    drawPong(pong, pongRadius, pongX, pongY)

# clears animated shapes
def clearShapes():
    # paddles
    player1.clear()
    player2.clear()

    # pong
    pong.clear()

    # score
    scoreWriter.clear()
    scoreWriter2.clear()

# static shapes
def drawNet():
    global netX
    global netY
    global netSideLength
    global netDistance

    while netY > -250:
        drawRectangle(net, netSideLength, netSideLength, netX, netY)
        netY = netY - netDistance

def drawBarriers():
    drawRectangle(topBarrier, barrierWidth, barrierLength, topBarrierX, topBarrierY)
    drawRectangle(bottomBarrier, barrierWidth, barrierLength, bottomBarrierX, bottomBarrierY)

# player inputs
def receivePlayer1Inputs():
    if keyboard.is_pressed("w"):
        return "up"
    if keyboard.is_pressed("s"):
        return "down"

def receivePlayer2Inputs():
    if keyboard.is_pressed("up arrow"):
        return "up"
    if keyboard.is_pressed("down_arrow"):
        return "down"
    
# moving players an AI alike
def movePlayer1():
    global player1Y
    global playerSpeed

    # checks player 1's inputs and collisions

    # 190 is top barrier and -190 is bottom barrier
    if player1Y < (190 - playerSpeed):
        if receivePlayer1Inputs() == "up":
            player1Y += playerSpeed

    if player1Y > (-190 + playerSpeed):
        if receivePlayer1Inputs() == "down":
            player1Y -= playerSpeed
    
def movePlayer2():
    global player2Y
    global playerSpeed

    # checks player 2's inputs and collisions

    # 190 is top barrier and -190 is bottom barrier
    if player2Y < (190 - playerSpeed):
        if receivePlayer2Inputs() == "up":
            player2Y += playerSpeed

    if player2Y > (-190 + playerSpeed):
        if receivePlayer2Inputs() == "down":
            player2Y -= playerSpeed

def moveAI1():
    global pongVX
    global player1Y
    global rectangleLength
    global playerSpeed
    global paddleLandingDetermined

    pongLanding = determinePongLanding1()

    # for random
    paddleLanding = player1Y + random.randrange(-51, 50)

    # for stable
    #paddleTop = player2Y + (rectangleLength / random.randrange(2,8))
    #paddleBottom = player2Y - (rectangleLength / random.randrange(2,8))

    # 190 is top barrier and -190 is bottom barrier
    # moves ai when pongVX > 0
    if pongVX < 0:
        if player1Y < (190 - playerSpeed):
            if pongLanding > paddleLanding:
                player1Y += playerSpeed

        if player1Y > (-190 + playerSpeed):
            if pongLanding < paddleLanding:
                player1Y -= playerSpeed
    elif pongVX > 0:
        if player1Y < (190 - playerSpeed):
            if player1Y < 0:
                player1Y += playerSpeed
        
        if player1Y > (-190 + playerSpeed):
            if player1Y > 0:
                player1Y -= playerSpeed

def moveAI2():
    global pongVX
    global player2Y
    global rectangleLength
    global playerSpeed
    global paddleLandingDetermined

    pongLanding = determinePongLanding2()

    # for random
    paddleLanding = player2Y + random.randrange(-51, 50)

    # for stable
    #paddleTop = player2Y + (rectangleLength / random.randrange(2,8))
    #paddleBottom = player2Y - (rectangleLength / random.randrange(2,8))

    # 190 is top barrier and -190 is bottom barrier
    # moves ai when pongVX > 0
    if pongVX > 0:
        if player2Y < (190 - playerSpeed):
            if pongLanding > paddleLanding:
                player2Y += playerSpeed

        if player2Y > (-190 + playerSpeed):
            if pongLanding < paddleLanding:
                player2Y -= playerSpeed
    elif pongVX < 0:
        if player2Y < (190 - playerSpeed):
            if player2Y < 0:
                player2Y += playerSpeed
        
        if player2Y > (-190 + playerSpeed):
            if player2Y > 0:
                player2Y -= playerSpeed

# moving the pong
def movePong():
    global pongX
    global pongY
    global pongVX
    global pongVY

    pongX = pongX + pongVX
    pongY = pongY + pongVY

# pong calculations for AI and velocity
def checkPongCollisions():
    global pongX
    global pongY
    
    global pongVX
    global pongVY

    global player1X
    global player1Y

    global player2X
    global player2Y

    global pongSpeedMult

    collision = False

    # 238 and -238 are the top and bottom barriers

    # flips vertical velocity if it hits top or bottom barrier
    if pongY > (244 - 6 - pongVY):
        pongVY = pongVY * -1
        pongY = pongY - 6
    
    if pongY < (-250 + 6 - pongVY):
        pongVY = pongVY * -1
        pongY = pongY + 6


    # resets pong when player 1 scores
    if pongX > 350: 
        pointScored(1)
    
    # resets pong when player 2 scores
    if pongX < -350:
        pointScored(2)

    # checks if pong has hit paddle horizontally
    if pongX < (player1X + 16 - pongVX):
        # subdivides paddles to determine direction and velocity
        if pongY <= (player1Y + 60) and pongY > (player1Y + 40):
            pongVX = 6
            pongVY = 8

        if pongY <= (player1Y + 40) and pongY > (player1Y + 20):
            pongVX = 6
            pongVY = 6

        if pongY <= (player1Y + 20) and pongY > player1Y:
            pongVX = 8
            pongVY = 2

        if pongY == player1Y and pongY == player1Y:
            pongVX = 8
            pongVY = 0

        if pongY < player1Y and pongY >= (player1Y - 20):
            pongVX = 8
            pongVY = -2

        if pongY < (player1Y - 20) and pongY >= (player1Y - 40):
            pongVX = 6
            pongVY = -6

        if pongY < (player1Y - 40) and pongY >= (player1Y - 60):
            pongVX = 6
            pongVY = -8

        if pongY <= (player1Y + 60) and pongY >= (player1Y - 60):
            collision = True
    
    if pongX > (player2X - 16 - pongVX):
        # subdivides paddles to determine direction and velocity
        if pongY <= (player2Y + 60) and pongY > (player2Y + 40):
            pongVX = -6
            pongVY = 8

        if pongY <= (player2Y + 40) and pongY > (player2Y + 20):
            pongVX = -6
            pongVY = 6

        if pongY <= (player2Y + 20) and pongY > player2Y:
            pongVX = -8
            pongVY = 2

        if pongY == player2Y and pongY == player2Y:
            pongVX = -8
            pongVY = 0

        if pongY < player2Y and pongY >= (player2Y - 20):
            pongVX = -8
            pongVY = -2

        if pongY < (player2Y - 20) and pongY >= (player2Y - 40):
            pongVX = -6
            pongVY = -6

        if pongY < (player2Y - 40) and pongY >= (player2Y - 60):
            pongVX = -6
            pongVY = -8

        if pongY <= (player2Y + 60) and pongY >= (player2Y - 60):
            collision = True   

    if collision == True:
        if pongSpeedMult < 3:
            pongSpeedMult += 0.1
        pongVX = pongVX * pongSpeedMult
        pongVY = pongVY * pongSpeedMult

def determinePongLanding1():
    # do math you fucking nerd
    global pongVX
    global pongVY
    global pongY
    global pongX
    global player1X

    pongLanding = 0

    paddleX = player1X + 10

    # determine y intercept
    pongSlope = pongVY / pongVX
    # b = y - mx
    pongYIntercept = pongY - (pongSlope * pongX)

    # y = mx + b
    tempPongLanding = (pongSlope * paddleX) + pongYIntercept

    # if the landing spot is over the barrier (calculates for up to two bounces)
    if tempPongLanding > 250:
        heightBeyondBarrier = tempPongLanding - 250
        pongLanding = 250 - heightBeyondBarrier
    elif tempPongLanding < -250:
        heightBeyondBarrier = tempPongLanding + 250
        pongLanding = -250 - heightBeyondBarrier
    elif pongLanding > 250:
        heightBeyondBarrier = pongLanding - 250
        pongLanding = 250 - heightBeyondBarrier
    elif tempPongLanding < -250:
        heightBeyondBarrier = pongLanding + 250
        pongLanding = -250 - heightBeyondBarrier
    else:
        return tempPongLanding

    return pongLanding

def determinePongLanding2():
    # do math you fucking nerd
    global pongVX
    global pongVY
    global pongY
    global pongX
    global player2X

    pongLanding = 0

    paddleX = player2X - 10

    # determine y intercept
    pongSlope = pongVY / pongVX
    # b = y - mx
    pongYIntercept = pongY - (pongSlope * pongX)

    # y = mx + b
    tempPongLanding = (pongSlope * paddleX) + pongYIntercept

    # if the landing spot is over the barrier (calculates for up to two bounces)
    if tempPongLanding > 250:
        heightBeyondBarrier = tempPongLanding - 250
        pongLanding = 250 - heightBeyondBarrier
    elif tempPongLanding < -250:
        heightBeyondBarrier = tempPongLanding + 250
        pongLanding = -250 - heightBeyondBarrier
    elif pongLanding > 250:
        heightBeyondBarrier = pongLanding - 250
        pongLanding = 250 - heightBeyondBarrier
    elif tempPongLanding < -250:
        heightBeyondBarrier = pongLanding + 250
        pongLanding = -250 - heightBeyondBarrier
    else:
        return tempPongLanding

    return pongLanding

# victory conditions and score
def pointScored(playerScored):
    global pongX
    global pongY
    global pongVX
    global pongVY

    global player1Y
    global player2Y

    global player1Score
    global player2Score

    global pongSpeedMult

    # randomizes serving direction and speed
    tempDirection = random.randrange(0,2)
    serveVX = random.randrange(6,9)
    serveVY = random.randrange(1,3)

    # when player 1 scores
    if playerScored == 1: 
        # serving velocity
        pongVX = serveVX
        if tempDirection == 1:
            pongVY = serveVY
        elif tempDirection == 2:
            pongVY = -1 * serveVY
        player1Score += 1
    
    # when player 2 scores
    if playerScored == 2:
        # serving velocity
        pongVX = -1 * serveVX
        if tempDirection == 1:
            pongVY = serveVY
        elif tempDirection == 2:
            pongVY = -1 * serveVY
        player2Score += 1

    # when point scored
    # resets pong position
    pongX = 0
    pongY = 0

    # resets player positions
    player1Y = 0
    player2Y = 0

    # resets pong speed
    pongSpeedMult = 1

    # waits 1 second before serving again
    time.sleep(1)


# only need to draw these once
drawNet()
drawBarriers()

while True:
    # clears all shapes before drawing new ones
    clearShapes()
    
    # moves players and checks for vertical collisions
    #movePlayer1()

    # uncomment this for two player
    #movePlayer2()

    # comment this out for two player
    moveAI1()
    moveAI2()

    # moves pong in 4 different directions
    checkPongCollisions()
    movePong()

    # displays scores
    displayScore()

    # draws shapes after checking location
    drawShapes()

    window.update()
    time.sleep(0.01)