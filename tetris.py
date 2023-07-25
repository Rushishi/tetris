### Command Line Tetris Game
### By: Rummy 
### For: Shane

import numpy as np
import time
import random
import keyboard

#initializing
x = 20 #amount of rows
y = 10 #amount of columns
field = np.zeros([x,y]) #0 is empty, 1 is falling block, 2 is settled block
next_field = np.zeros([5,6]) #for showing the "next" block
i_blocks_templates = [[[0,0],[0,1],[1,0],[1,1]] , [[0,-1],[0,0],[0,1],[0,2]] , [[0,-1],[1,-1],[0,0],[0,1]] , [[0,-1],[0,0],[0,1],[1,0]], [[0,-1],[1,1],[0,0],[0,1]], [[0,0],[1,0],[0,1],[1,-1]], [[0,0],[0,-1],[1,0],[1,1]]] #the possible blocks that can spawn
# 0: ██ 1: ████ 2: ███ 3: ███ 4: ███ 5:  ██ 6: ██
#    ██            █       █       █    ██      ██
random.seed(time.monotonic_ns())
time_raffer = 0 #board update timing
left_pressed = False #variable to limit speed of left movement
right_pressed = False #variable to limit speed of right movement
rot_pressed = False #variable to limit speed of rotation
fast = False #variable to detect if blocks should fall fast
run_bool = True #game will run while True
score = 0
current_block = [] #the shape of the currently falling block will be saved in this array
next_block = []
c = [-1,-1] #the location of the center piece of the currently falling block
speed = 500000000 #time between block falling in ns

#this function will print the area 
def print_area():
    print('|----------|')
    for i in range(0,x):
        print('|', end='')
        for j in range(0,y):
            if field[i][j] == 0:
                print(' ', end='')
            elif field[i][j] == 2:
                print('█', end='')
            elif field[i][j] == 1:
                print('O', end='')
        print('|', end='')
        if i==0:
            print('   Next   ', end='')
        if i==1:
            print(' ########', end='')
        if i>1 and i<6:
            print(' #', end='')
            for j2 in range(0,6):
                if next_field[i-2][j2] == 0:
                    print(' ', end='')

                else:
                    print('O', end='')
            print('#', end='')
        if i==6:
            print(' ########', end='')
        print('')
    print('|----------|')

#this function will end the game
def game_over():
    global run_bool
    run_bool = False
    print('GAME OVER! Your final score is', score)

#this function will spawn a new block
def new_block():
    global c
    global current_block
    global next_block
    global next_field
    if next_block == []:
        current_block = i_blocks_templates[random.randint(0,len(i_blocks_templates)-1)]
    else:
        current_block = next_block
    next_block = i_blocks_templates[random.randint(0,len(i_blocks_templates)-1)]
    c = [0,4]
    next_field = np.zeros([5,6])
    for block in next_block:
        next_field[block[0]+1][block[1]+2] = int(1)
    for block in current_block:
        i = block[0]+c[0]
        j = block[1]+c[1]
        if field[i][j] == 0:
            field[i][j] = 1
        else:
            print_area()
            game_over()
            break

#this function checks if a line is filled and will delete it if so
def check_line():
    global score
    global speed
    for i in range(0,x):
        full_line = True
        for j in range(0,y):
            if field[i][j] != 2:
                full_line = False
        if full_line == True:
            score += 1
            speed = speed * 0.95 #make the game run faster as score increases
            print(score)
            for jj in range(0,y):
                field[i][jj] = 0
            for i2 in range(i-1,-1,-1):
                for j2 in range(0,y):
                    if field[i2][j2] == 2:
                        print(i2)
                        print(j2)
                        field[i2+1][j2] = 2
                        field[i2][j2] = 0

#this function will settle the currently falling block
def settle_blocks():
    for i in range(0,x):
        for j in range(0,y):
            if field[i][j] == 1:
                field[i][j] = 2
    check_line()
    new_block()    

#this function checks if a block can be moved in a given direction
def i_check_move_blocks(direction):
    move = True
    for block in current_block:
        if c[0]+block[0]+direction[0] < 0 or c[0]+block[0]+direction[0] > 19 or c[1]+block[1]+direction[1] < 0 or c[1]+block[1]+direction[1] > 9:
            move = False
            if direction[0] == 1:
                settle_blocks()
            break
        elif field[c[0]+block[0]+direction[0]][c[1]+block[1]+direction[1]] == 2:
            move = False
            if direction[0] == 1:
                settle_blocks()
            break
    return move   

#this function moves blocks in a given direction
def i_move_blocks(direction):
    if i_check_move_blocks(direction) == True:
        for block in current_block:
            field[c[0]+block[0]][c[1]+block[1]] = 0
        c[0],c[1] = c[0]+direction[0],c[1]+direction[1]
        for block in current_block:
            field[c[0]+block[0]][c[1]+block[1]] = 1
        print_area()

#this function will rotate the current block if possible
def i_rotate(counter_clockwise = False):
    global current_block
    global field
    can_rotate = True
    new_current_block = []
    for block in current_block:
        if counter_clockwise == True:
            new_current_block.append([-block[1], +block[0]])
        else:
            new_current_block.append([+block[1], -block[0]])
        field[block[0]+c[0],block[1]+c[1]] = 0
    for block in new_current_block:
        if block[0]+c[0] > 19 or block[0]+c[0] < 0 or block[1]+c[1] > 9 or block[1]+c[1] < 0:
            can_rotate = False
        elif field[block[0]+c[0],block[1]+c[1]] == 2:
            can_rotate = False            
    if can_rotate:
        current_block = new_current_block
    for block in current_block:
        field[block[0]+c[0],block[1]+c[1]] = 1
    print_area()


new_block()
while(run_bool):
    if time.monotonic_ns() > time_raffer:
        time_raffer = time.monotonic_ns() + speed
        fast = False
        i_move_blocks([1,0])
        if(run_bool):
            print_area()
    if keyboard.is_pressed('a') and left_pressed == False:
        i_move_blocks([0,-1])
        left_pressed = True
    if not keyboard.is_pressed('a'):
        left_pressed = False
    if keyboard.is_pressed('d') and right_pressed == False:
        i_move_blocks([0,1])
        right_pressed = True
    if not keyboard.is_pressed('d'):
        right_pressed = False
    if keyboard.is_pressed('s') and fast == False:
        if speed > 25000000:
            time_raffer = time_raffer - speed + 25000000
        fast = True
    if keyboard.is_pressed('q') and current_block != [] and rot_pressed == False:
        i_rotate(True)
        rot_pressed = True
    if keyboard.is_pressed('e') and current_block != [] and rot_pressed == False:
        i_rotate(False)
        rot_pressed = True
    if not (keyboard.is_pressed('q') or keyboard.is_pressed('e')):
        rot_pressed = False