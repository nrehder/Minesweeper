from random import randint
from time import sleep

'''
To do:
    variable number of mines/flags
'''

#global variables used throughout the game
mines=[]
flags=[]
numbers=[]
lose=False
remaining=5
count=0

#sets up initial game.  Is called if the player starts a new game
def setup():
    global remaining
    
    #creates the whole window
    size(500,500)
    fill(125,125,125)
    rect(0,0,500,500)
    #creates a 5x5 grid to be played on
    fill(225,225,225)
    rect(125,200,250,250)
    for i in range(0,6):
        line(125,i*50+200,375,i*50+200)
        line(i*50+125,200,i*50+125,450)
    #places the new game button and mine counter display
    fill(100,100,225)
    rect(150,30,200,50)
    fill(200,125,125)
    rect(225,100,50,50)
    fill(0,0,0)
    textSize(32)
    textAlign(CENTER,CENTER)
    text("New Game",250,50)
    text(remaining,250,125)
    startGame()

#Randomizes the game
def startGame():
    global mines
    global numbers
    global flags
    global lose
    global count
    
    #creates a list to store where the mines are
    #mines[y][x] is the indexing
    mines=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    i=1
    while i<6:
        x=randint(0,4)
        y=randint(0,4)
        if mines[y][x]==0:
            mines[y][x]=1
            i=i+1
    #tells number of mines nearby
    numbers=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    #builds the numbers from mines.  i and j cycle through numbers
    #Fills out corners
    if mines[0][0]==0:
        numbers[0][0]=mines[0][1]+mines[1][0]+mines[1][1]
    if mines[4][0]==0:
        numbers[4][0]=mines[4][1]+mines[3][0]+mines[3][1]
    if mines[0][4]==0:
        numbers[0][4]=mines[0][3]+mines[1][4]+mines[1][3]
    if mines[4][4]==0:
        numbers[4][4]=mines[4][3]+mines[3][4]+mines[3][3]
    #Fills out left edge
    for j in range(1,4):
        if mines[j][0]==0:
            numbers[j][0]=mines[j][1]+mines[j+1][1]+mines[j-1][1]+mines[j+1][0]+mines[j-1][0]
    #Fills out right edge
    for j in range(1,4):
        if mines[j][4]==0:
            numbers[j][4]=mines[j][3]+mines[j+1][3]+mines[j-1][3]+mines[j+1][4]+mines[j-1][4]
    #Fills out top edge
    for i in range(1,4):
        if mines[0][i]==0:
            numbers[0][i]=mines[0][i+1]+mines[0][i-1]+mines[1][i+1]+mines[1][i]+mines[1][i-1]
    #Fills out bottom edge
    for i in range(1,4):
        if mines[4][i]==0:
            numbers[4][i]=mines[4][i+1]+mines[4][i-1]+mines[3][i+1]+mines[3][i]+mines[3][i-1]
    #Fills out the inner area
    for i in range(1,4):
        for j in range(1,4):
            if mines[j][i]==0:
                numbers[j][i]=mines[j-1][i-1]+mines[j-1][i]+mines[j-1][i+1]+mines[j+1][i-1]+mines[j+1][i]+mines[j+1][i+1]+mines[j][i-1]+mines[j][i+1]
    #sets flags to 0 for all
    flags=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    lose=False
    count=0
    remaining=5

#Function to check if a mine is where the user clicks
def checkMine(xm,ym):
    global mines
    global flags
    global lose
    global numbers
    global count
    #converts the pixel location to the mine indices
    mine_x=(xm-125)//50
    mine_y=(ym-200)//50
    if flags[mine_y][mine_x]==0:
        if mines[mine_y][mine_x]==1:
            textSize(32)
            fill(0,0,0)
            rect(125,200,250,250)
            fill(255,0,0)
            textAlign(CENTER,CENTER)
            text("You hit a mine!",250,325)
            lose=True
            count=1
            loseSmiley()
        elif numbers[mine_y][mine_x]>0:
            fill(0,150,0)
            rect(126+mine_x*50,201+mine_y*50,48,48)
            fill(0,0,0)
            textSize(32)
            textAlign(CENTER,CENTER)
            text(numbers[mine_y][mine_x],150+mine_x*50,225+mine_y*50)
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
        rect(126+checks[0][0]*50,201+checks[0][1]*50,48,48)
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
            if checks[0][0]<4 and checks[0][1]>0 and checked.count([checks[0][0]+1,checks[0][1]-1])==0 and checks.count([checks[0][0]+1,checks[0][1]-1])==0:
                checks.append([checks[0][0]+1,checks[0][1]-1])
            #checks if the spot 1 more x and the same y is in bounds and adds it
            if checks[0][0]<4 and checked.count([checks[0][0]+1,checks[0][1]])==0 and checks.count([checks[0][0]+1,checks[0][1]])==0:
                checks.append([checks[0][0]+1,checks[0][1]])
            #checks if the spot 1 more x and 1 more y is in bounds and adds it
            if checks[0][0]<4 and checks[0][1]<4 and checked.count([checks[0][0]+1,checks[0][1]+1])==0 and checks.count([checks[0][0]+1,checks[0][1]+1])==0:
                checks.append([checks[0][0]+1,checks[0][1]+1])
            #checks if the spot the same x and 1 more y is in bounds and adds it
            if checks[0][1]<4 and checked.count([checks[0][0],checks[0][1]+1])==0 and checks.count([checks[0][0],checks[0][1]+1])==0:
                checks.append([checks[0][0],checks[0][1]+1])
            #checks if the spot 1 less x and 1 more y is in bounds and adds it
            if checks[0][0]>0 and checks[0][1]<4 and checked.count([checks[0][0]-1,checks[0][1]+1])==0 and checks.count([checks[0][0]-1,checks[0][1]+1])==0:
                checks.append([checks[0][0]-1,checks[0][1]+1])
            checked.append(checks.pop(0))
        elif numbers[checks[0][1]][checks[0][0]]>0 and checked.count(checks[0])==0:
            fill(0,0,0)
            textSize(32)
            textAlign(CENTER,CENTER)
            text(numbers[checks[0][1]][checks[0][0]],150+checks[0][0]*50,225+checks[0][1]*50)
            checked.append(checks.pop(0))
        elif flags[checks[0][1]][checks[0][0]]==1:
            checked.append(checks.pop(0))

#function to place or remove flags
def flagMine(xf,yf):
    global mines
    global flags
    #converts the pixel location to the mine indices
    flag_x=(xf-125)//50
    flag_y=(yf-200)//50
    #if there currently isn't a flag
    if flags[flag_y][flag_x]==0:
        #marks location as a flag
        flags[flag_y][flag_x]=1
        #sets color to blue and then colors inside the lines
        fill(0,0,150)
        rect(126+flag_x*50,201+flag_y*50,48,48)
    #if there is already a flag
    elif flags[flag_y][flag_x]==1:
        #removes flag from location
        flags[flag_y][flag_x]=0
        #sets color back to the default grid and colors inside the lines
        fill(225,225,225)
        rect(126+flag_x*50,201+flag_y*50,48,48)
    sleep(0.1)

#prints the losing smiley when called
def loseSmiley():
    fill(0,0,0)
    rect(225,100,50,50)
    i=0
    j=0
    fill(200,200,0)
    ellipse(250,125,30,30)
    fill(0,0,0)
    ellipse(240,130,5,5)
    ellipse(260,130,5,5)
    noFill()
    arc(250,125,25,25,PI,TWO_PI)

def endgame(click):
    global mines
    global flags
    global lose
    global count
    lose=True
    for i in range(0,5):
        if count>1:
            break
        for j in range(0,5):
            if flags[j][i]!=1 and mines[j][i]==1 and click<20:
                fill(255,0,0)
                rect(126+i*50,201+j*50,48,48)
                fill(0,0,0)
                textAlign(CENTER,CENTER)
                textSize(20)
                text('mine',150+i*50,225+j*50)
                count=count+1
                loseSmiley()
                break
            elif flags[j][i]==1 and mines[j][i]==0:
                fill(200,0,0)
                rect(126+i*50,201+j*50,48,48)
                fill(0,0,0)
                textAlign(CENTER,CENTER)
                textSize(18)
                text('no',150+i*50,215+j*50)
                text('mine',150+i*50,235+j*50)
                count=count+1
                loseSmiley()
                break
    #if you missed 0 mines, prints the winning smiley
    if count==0 and lose==True:
        fill(0,0,0)
        rect(225,100,50,50)
        i=0
        j=0
        fill(200,200,0)
        ellipse(250,125,30,30)
        fill(0,0,0)
        ellipse(240,120,5,5)
        ellipse(260,120,5,5)
        noFill()
        arc(250,125,25,25,0,PI)

#main function that runs the game
def draw():
    global mines
    global flags
    global remaining
    global count
    #updates the counter
    remaining=0
    clicked=0
    for i in range(0,5):
        remaining=remaining+mines[i].count(1)-flags[i].count(1)
        clicked=clicked+flags[i].count('C')
    if remaining<0:
        remaining=0
    if lose==False:
        fill(200,125,125)
        rect(225,100,50,50)
        fill(0,0,0)
        textSize(32)
        textAlign(CENTER,CENTER)
        text(remaining,250,125)
    #if the counter hits 0, it checks if you found all the mines
    if remaining<=0 or clicked==20:
        endgame(clicked)
    
    x=mouseX
    y=mouseY
    #checks if it is in the grid and calls the function based on left or right click
    if x>125 and x<375 and y>200 and y<450 and lose==False:
        if mousePressed==True and mouseButton==LEFT:
            checkMine(x,y)
        if mousePressed==True and mouseButton==RIGHT:
            flagMine(x,y)
    #checks if the mouse is in the new game button and if it was clicked
    if x>150 and x<350 and y>30 and y<80 and mousePressed==True and mouseButton:
        setup()
    
