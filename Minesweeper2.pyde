from time import sleep
from random import randint

#global variables used throughout the game
numberMines=5
horizontal=5
vertical=5
leftEdge=0
topEdge=0
mines=[]
flags=[]
numbers=[]
lose=False
remaining=0
count=0
started=False

#sets up initial game.  Is called if the player starts a new game
def setup():
    global started
    global remaining
    global horizontal
    global vertical
    global topEdge
    global leftEdge
    size(800,800)
    if started==False:
        background(0,0,125)
        fill(125)
        rect(225,225,325,325)
        fill(0,0,0)
        textSize(32)
        textAlign(CENTER,CENTER)
        #Creates title at top of window
        text("Krimsweeper",400,250)
        fill(100,100,225)
        rect(300,490,200,50)
        fill(0,0,0)
        #Creates start game button at bottom of window
        text("Start Game",400,510)
        textSize(20)
        textAlign(LEFT,TOP)
        #Creates the names for the controls for the number of mines, horizontal spaces and vertical spaces
        text("Mines",310,315)
        text("Horiz",310,370)
        text("Vert",310,425)
    else:
        clear()
        background(125)
        fill(0,0,0)
        textSize(32)
        textAlign(CENTER,CENTER)
        #Creates title at top of window
        text("Krimsweeper",400,25)
        #places the new game button and mine counter display
        fill(100,100,225)
        rect(300,62,200,50)
        fill(200,125,125)
        rect(375,125,50,50)
        fill(0,0,0)
        textSize(32)
        textAlign(CENTER,CENTER)
        text("New Game",400,83)
        remaining=numberMines
        text(remaining,400,145)
        #creates the game board centered on 400,488 and with a size based on the sizes chosen by the user
        rectMode(CENTER)
        fill(225)
        rect(400,488,24*horizontal,24*vertical)
        rectMode(CORNER)
        #draws in the grid
        #also finds the top and left edges
        fill(0)
        bound_vert=vertical//2
        bound_hor=horizontal//2
        #draw lines when there are an even of vertical spaces and even horizontal spaces
        if vertical%2==0 and horizontal%2==0:
            topEdge=488-vertical*12
            leftEdge=400-horizontal*12
            for i in range(-1*horizontal/2,horizontal/2+1):
                line(400+i*24,488-vertical*12,400+i*24,488+vertical*12)
            for i in range(-1*vertical/2,vertical/2+1):
                line(400-horizontal*12,488+i*24,400+horizontal*12,488+i*24)
        #draw lines when there are an even of vertical spaces and odd horizontal spaces
        if vertical%2==0 and horizontal%2==1:
            leftEdge=388-(horizontal//2)*24
            topEdge=488-vertical*12
            for i in range(-(horizontal//2),horizontal//2+1):
                line(388+i*24,488-24*(vertical//2),388+i*24,488+24*(vertical//2))
            for i in range(-1*vertical/2,vertical/2+1):
                line(400-horizontal*12,488+i*24,400+horizontal*12,488+i*24)
        #draw lines when there are an odd of vertical spaces and even horizontal spaces
        if vertical%2==1 and horizontal%2==0:
            leftEdge=400-horizontal*12
            topEdge=476-(vertical//2)*24
            for i in range(-1*horizontal/2,horizontal/2+1):
                line(400+i*24,488-vertical*12,400+i*24,488+vertical*12)
            for i in range(-(vertical//2),vertical//2+1):
                line(400-24*(horizontal//2),476+i*24,400+24*(horizontal//2),476+i*24)
        #draw lines when there are an odd of vertical spaces and odd horizontal spaces
        if vertical%2==1 and horizontal%2==1:
            leftEdge=388-(horizontal//2)*24
            topEdge=476-(vertical//2)*24
            for i in range(-(horizontal//2),horizontal//2+1):
                line(388+i*24,476-24*(vertical//2),388+i*24,476+24*(vertical//2+1))
            for i in range(-(vertical//2),vertical//2+1):
                line(388-24*(horizontal//2),476+i*24,388+24*(horizontal//2+1),476+i*24)
        startGame()

def startGame():
    global numberMines
    global horizontal
    global vertical
    global mines
    global flags
    global numbers
    global lose
    global count
    
    mines=[]
    flags=[]
    numbers=[]
    lose=False
    count=0
    
    #creates a list of lists based on the horizontal and vertical values
    #Mines
    for i in range(0,vertical):
        horiz=[]
        for j in range(0,horizontal):
            horiz.append(0)
        mines.append(horiz)
    #Flags
    for i in range(0,vertical):
        horiz=[]
        for j in range(0,horizontal):
            horiz.append(0)
        flags.append(horiz)
    #numbers
    for i in range(0,vertical):
        horiz=[]
        for j in range(0,horizontal):
            horiz.append(0)
        numbers.append(horiz)
    
    #Places the mines randomly on board
    i=0
    while i<numberMines:
        x=randint(0,horizontal-1)
        y=randint(0,vertical-1)
        if mines[y][x]==0:
            mines[y][x]=1
            i=i+1
    
    #builds the number of mines near each space
    #fills out corners
    if mines[0][0]==0:
        numbers[0][0]=mines[0][1]+mines[1][0]+mines[1][1]
    if mines[vertical-1][0]==0:
        numbers[vertical-1][0]=mines[vertical-1][1]+mines[vertical-2][0]+mines[vertical-2][1]
    if mines[0][horizontal-1]==0:
        numbers[0][horizontal-1]=mines[0][horizontal-2]+mines[1][horizontal-2]+mines[1][horizontal-1]
    if mines[vertical-1][horizontal-1]==0:
        numbers[vertical-1][horizontal-1]=mines[vertical-2][horizontal-1]+mines[vertical-1][horizontal-2]+mines[vertical-2][horizontal-2]
    #fills out left edge
    for i in range(1,vertical-1):
        if mines[i][0]==0:
            numbers[i][0]=mines[i][1]+mines[i+1][1]+mines[i-1][1]+mines[i+1][0]+mines[i-1][0]
    #Fills out right edge
    for i in range(1,vertical-1):
        if mines[i][horizontal-1]==0:
            numbers[i][horizontal-1]=mines[i][horizontal-2]+mines[i+1][horizontal-2]+mines[i-1][horizontal-2]+mines[i+1][horizontal-1]+mines[i-1][horizontal-1]
    #Fills out top edge
    for i in range(1,horizontal-1):
        if mines[0][i]==0:
            numbers[0][i]=mines[0][i+1]+mines[0][i-1]+mines[1][i+1]+mines[1][i]+mines[1][i-1]
    #Fills out bottom edge
    for i in range(1,horizontal-1):
        if mines[vertical-1][i]==0:
            numbers[vertical-1][i]=mines[vertical-1][i+1]+mines[vertical-1][i-1]+mines[vertical-2][i+1]+mines[vertical-2][i]+mines[vertical-2][i-1]
    #Fills out the inner area
    for i in range(1,horizontal-1):
        for j in range(1,vertical-1):
            if mines[j][i]==0:
                numbers[j][i]=mines[j-1][i-1]+mines[j-1][i]+mines[j-1][i+1]+mines[j+1][i-1]+mines[j+1][i]+mines[j+1][i+1]+mines[j][i-1]+mines[j][i+1]

#Checks if a mine is where the user clicks
def checkMine(xm,ym):
    global mines
    global flags
    global lose
    global numbers
    global count
    global horizontal
    global vertical
    global topEdge
    global leftEdge
    #converts the pixel location to the mine indices
    mine_x=(xm-leftEdge)//24
    mine_y=(ym-topEdge)//24
    if flags[mine_y][mine_x]==0:
        if mines[mine_y][mine_x]==1:
            textSize(32)
            fill(0,0,0)
            rect(200,300,400,400)
            fill(255,0,0)
            textAlign(CENTER,CENTER)
            text("You hit a mine!",400,500)
            lose=True
            count=1
            loseSmiley()
        elif numbers[mine_y][mine_x]>0:
            fill(0,150,0)
            rect(leftEdge+1+mine_x*24,topEdge+1+mine_y*24,22,22)
            fill(0,0,0)
            textSize(20)
            textAlign(CENTER,CENTER)
            text(numbers[mine_y][mine_x],leftEdge+12+mine_x*24,topEdge+12+mine_y*24)
            flags[mine_y][mine_x]='C'
        elif numbers[mine_y][mine_x]==0:
            check=[[mine_x,mine_y]]
            cascade(check)

#Cascades when a blank space is revealed by click
def cascade(checks):
    global flags
    global numbers
    checked=[]
    while len(checks)>0:
        fill(0,150,0)
        rect(leftEdge+1+checks[0][0]*24,topEdge+1+checks[0][1]*24,22,22)
        flags[checks[0][1]][checks[0][0]]='C'
        #checks if the current cell being checked has a 0, and if it does it adds the surrounding cells and removes itself
        #also checks if this spot has been checked yet
        x=checks[0][0]
        y=checks[0][1]
        if numbers[checks[0][1]][checks[0][0]]==0 and checked.count(checks[0])==0 and flags[checks[0][1]][checks[0][0]]!=1:
            #checks if the spot 1 less x and the same y is in bounds and adds it
            if checks[0][0]>0 and checked.count([checks[0][0]-1,checks[0][1]])==0 and checks.count([checks[0][0]-1,checks[0][1]])==0:
                checks.append([checks[0][0]-1,checks[0][1]])
            #checks if the spot 1 less x and 1 less y is in bounds and adds it
            if checks[0][0]>0 and checks[0][1]>0 and checked.count([checks[0][0]-1,checks[0][1]-1])==0 and checks.count([checks[0][0]-1,checks[0][1]-1])==0:
                checks.append([checks[0][0]-1,checks[0][1]-1])
            #checks if the spot same x and 1 less y is in bounds and adds it
            if checks[0][1]>0 and checked.count([checks[0][0],checks[0][1]-1])==0 and checks.count([checks[0][0],checks[0][1]-1])==0:
                checks.append([checks[0][0],checks[0][1]-1])
            #checks if the spot 1 more x and 1 less y is in bounds and adds it
            if checks[0][0]<(horizontal-1) and checks[0][1]>0 and checked.count([checks[0][0]+1,checks[0][1]-1])==0 and checks.count([checks[0][0]+1,checks[0][1]-1])==0:
                checks.append([checks[0][0]+1,checks[0][1]-1])
            #checks if the spot 1 more x and the same y is in bounds and adds it
            if checks[0][0]<(horizontal-1) and checked.count([checks[0][0]+1,checks[0][1]])==0 and checks.count([checks[0][0]+1,checks[0][1]])==0:
                checks.append([checks[0][0]+1,checks[0][1]])
            #checks if the spot 1 more x and 1 more y is in bounds and adds it
            if checks[0][0]<(horizontal-1) and checks[0][1]<(vertical-1) and checked.count([checks[0][0]+1,checks[0][1]+1])==0 and checks.count([checks[0][0]+1,checks[0][1]+1])==0:
                checks.append([checks[0][0]+1,checks[0][1]+1])
            #checks if the spot the same x and 1 more y is in bounds and adds it
            if checks[0][1]<(vertical-1) and checked.count([checks[0][0],checks[0][1]+1])==0 and checks.count([checks[0][0],checks[0][1]+1])==0:
                checks.append([checks[0][0],checks[0][1]+1])
            #checks if the spot 1 less x and 1 more y is in bounds and adds it
            if checks[0][0]>0 and checks[0][1]<(vertical-1) and checked.count([checks[0][0]-1,checks[0][1]+1])==0 and checks.count([checks[0][0]-1,checks[0][1]+1])==0:
                checks.append([checks[0][0]-1,checks[0][1]+1])
            checked.append(checks.pop(0))
        elif numbers[checks[0][1]][checks[0][0]]>0 and checked.count(checks[0])==0:
            fill(0,0,0)
            textSize(20)
            textAlign(CENTER,CENTER)
            text(numbers[checks[0][1]][checks[0][0]],leftEdge+12+checks[0][0]*24,topEdge+12+checks[0][1]*24)
            checked.append(checks.pop(0))
        elif flags[checks[0][1]][checks[0][0]]==1:
            checked.append(checks.pop(0))

#function to place or remove flags
def flagMine(xf,yf):
    global mines
    global flags
    global leftEdge
    global topEdge
    #converts the pixel location to the mine indices
    flag_x=(xf-leftEdge)//24
    flag_y=(yf-topEdge)//24
    #if there currently isn't a flag
    if flags[flag_y][flag_x]==0:
        #marks location as a flag
        flags[flag_y][flag_x]=1
        #sets color to blue and then colors inside the lines
        fill(0,0,150)
        rect(leftEdge+1+flag_x*24,topEdge+1+flag_y*24,22,22)
    #if there is already a flag
    elif flags[flag_y][flag_x]==1:
        #removes flag from location
        flags[flag_y][flag_x]=0
        #sets color back to the default grid and colors inside the lines
        fill(225,225,225)
        rect(leftEdge+1+flag_x*24,topEdge+1+flag_y*24,22,22)

#prints the losing smiley when called
def loseSmiley():
    fill(0,0,0)
    rect(375,125,50,50)
    i=0
    j=0
    fill(200,200,0)
    ellipse(400,150,30,30)
    fill(0,0,0)
    ellipse(390,155,5,5)
    ellipse(410,155,5,5)
    noFill()
    arc(400,150,25,25,PI,TWO_PI)

def endgame(click):
    global mines
    global flags
    global lose
    global count
    global leftEdge
    global topEdge
    lose=True
    for i in range(0,5):
        if count>1:
            break
        for j in range(0,5):
            if flags[j][i]!=1 and mines[j][i]==1 and click<20:
                fill(255,0,0)
                rect(leftEdge+1+i*24,topEdge+1+j*24,22,22)
                fill(0,0,0)
                textAlign(CENTER,CENTER)
                textSize(20)
                text('mine',leftEdge+12+i*24,topEdge+12+j*24)
                count=count+1
                loseSmiley()
                break
            elif flags[j][i]==1 and mines[j][i]==0:
                fill(200,0,0)
                rect(leftEdge+1+i*24,topEdge+1+j*24,22,22)
                fill(0,0,0)
                textAlign(CENTER,CENTER)
                textSize(18)
                text('no',leftEdge+12+i*24,topEdge+12+j*24)
                count=count+1
                loseSmiley()
                break
    #if you missed 0 mines, prints the winning smiley
    if count==0 and lose==True:
        fill(0,0,0)
        rect(375,125,50,50)
        fill(200,200,0)
        ellipse(400,150,30,30)
        fill(0,0,0)
        ellipse(390,145,5,5)
        ellipse(410,145,5,5)
        noFill()
        arc(400,150,25,25,0,PI)

def draw():
    global numberMines
    global horizontal
    global vertical
    global started
    global mines
    global flags
    global remaining
    global count
    x=mouseX
    y=mouseY
    sleep(0.1)
    #places the default values and allows for adjusting them
    if started==False:
        #Mines - button
        if numberMines==1:
            fill(175)
        else:
            fill(0)
        triangle(395,325,420,310,420,340)
        #horizontal - button
        if horizontal==5:
            fill(175)
        else:
            fill(0)
        triangle(395,380,420,365,420,395)
        #vertical - button
        if vertical==5:
            fill(175)
        else:
            fill(0)
        #mines + button
        triangle(395,435,420,420,420,450)
        if numberMines==horizontal*vertical*4//5:
            fill(175)
        else:
            fill(0)
        #horizontal + button
        triangle(495,325,470,310,470,340)
        if horizontal==30:
            fill(175)
        else:
            fill(0)
        #vertical + button
        triangle(495,380,470,365,470,395)
        if vertical==24:
            fill(175)
        else:
            fill(0)
        triangle(495,435,470,420,470,450)
        fill(255,255,255)
        textSize(22)
        textAlign(CENTER,CENTER)
        text("-",411,321)
        text("-",411,376)
        text("-",411,431)
        text("+",480,321)
        text("+",480,376)
        text("+",480,431)
        #Creates the rectangles which will have the three values displayed
        fill(0)
        rect(430,310,31,30)
        rect(430,365,31,30)
        rect(430,420,31,30)
        #Updates the values inside the rectangles
        fill(255)
        textAlign(CENTER,CENTER)
        if numberMines<100:
            textSize(24)
        else:
            textSize(16)
        text(numberMines,446,323)
        textSize(24)
        text(horizontal,446,378)
        text(vertical,446,433)
        if x>395 and x<420 and y>310 and y<340 and numberMines>1 and mousePressed==True:
            numberMines=numberMines-1
        if x>470 and x<495 and y>310 and y<340 and numberMines<.8*(horizontal*vertical) and mousePressed==True:
            numberMines=numberMines+1
        if x>395 and x<420 and y>420 and y<480 and vertical>5 and mousePressed==True:
            vertical=vertical-1
        if x>470 and x<495 and y>420 and y<480 and vertical<24 and mousePressed==True:
            vertical=vertical+1
        if x>395 and x<420 and y>365 and y<395 and horizontal>5 and mousePressed==True:
            horizontal=horizontal-1
        if x>470 and x<495 and y>365 and y<395 and horizontal<30 and mousePressed==True:
            horizontal=horizontal+1
        if x>300 and x<500 and y>495 and y<545 and mousePressed==True:
            started=True
            setup()
    else:
        #updates the counter
        remaining=numberMines
        clicked=0
        for i in range(0,vertical):
            remaining=remaining-flags[i].count(1)
            clicked=clicked+flags[i].count('C')
        if remaining<0:
            remaining=0
        if lose==False:
            fill(200,125,125)
            rect(375,125,50,50)
            fill(0,0,0)
            textSize(32)
            textAlign(CENTER,CENTER)
            text(remaining,400,145)
        #if the counter hits 0, it checks if you found all the mines
        if remaining<=0 or clicked==horizontal*vertical-numberMines:
            endgame(clicked)
    
        x=mouseX
        y=mouseY
        #checks if it is in the grid and calls the function based on left or right click
        if x>leftEdge and x<leftEdge+horizontal*24 and y>topEdge and y<topEdge+vertical*24 and lose==False:
            if mousePressed==True and mouseButton==LEFT:
                checkMine(x,y)
            if mousePressed==True and mouseButton==RIGHT:
                flagMine(x,y)
        #checks if the mouse is in the new game button and if it was clicked
        if x>300 and x<500 and y>62 and y<112 and mousePressed==True and mouseButton:
            started=False
            setup()
