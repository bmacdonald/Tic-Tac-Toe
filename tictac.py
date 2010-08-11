import random
import sys
from types import IntType

# Created 8/09/2010
# Author: Bryan MacDonald
# bmacdon1@gmail.com

# display the board
def display_board(board):
    print "\nOpen spaces are marked with a number."
    print " ======== "
    print "%s | %s | %s" % (board[0],board[1],board[2])
    print "%s | %s | %s" % (board[3],board[4],board[5]) 
    print "%s | %s | %s" % (board[6],board[7],board[8])
    print " ======== \n"
    
#setup the shapes
def select_shape():
    print "MIKE >>> Welcome Player\n"
    input = raw_input('Player One type X or O to begin: ')
    
    #if x or os are not present ask for selection
    if input not in 'O o X x'.split():
        return select_shape()
    
    if input.upper() == 'O':
        return {'one':'O','two':'X' }
    
    return {'one':'X','two':'O' }

#player input
def player_input(player, error=False):   
    error_string = ''
    if error:
        error_string = "Space already taken. \n"
    
    print '%sEnter 0-8 to move: ' % error_string
    input = raw_input()
    
    #input digit validation            
    while not input.isdigit():
        return player_input(player)
    
    #input digit validation  
    if int(input) < 9:
        return int(input)
    else:
        return player_input(player)
    
def play_again():
    print "Would you like to play again? (Y/N)"
    input = raw_input()
    
    if input not in 'Y y N n'.split():
        return play_again()
    
    if input in ('Y','y'):
        return True
    
    return False
#computer taunt
def computer_message():
    return "\nMIKE >>> I have made my move. It is your turn."

def win_condition(board,player):
    #winning conditions
    cond = [[0,1,2],
            [0,3,6],
            [0,4,8],
            [1,4,7],
            [2,5,8],
            [2,4,6],
            [3,4,5],
            [6,7,8],
        ]
    #cycling through the conditions
    for row in cond:  
        if board[row[0]] == 'X' and board[row[1]] == 'X' and board[row[2]] == 'X':
            return True
        
        if board[row[0]] == 'O' and board[row[1]] == 'O' and board[row[2]] == 'O':
            return True

    return False

#checks to see if space is marked    
def is_marked(board, move):
    if board[move] == 'X' or board[move] == 'O':
        return True
    return False

#block the player at all cost
def computer_block(board,computer):
    #player assignment
    if computer == 'O':
        human = 'X'
    else:
        human = 'O'
        
    move = -1
    #winning condition
    cond = [[0,1,2],
            [0,3,6],
            [0,4,8],
            [1,4,7],
            [2,5,8],
            [2,4,6],
            [3,4,5],
            [6,7,8],
        ]    
    #cycling through the conditions
    for row in cond:
        #checks to see if column in row is free
        if type(board[row[0]]) is IntType and board[row[1]] == human and board[row[2]] == human:
            move=row[0]
        
        if board[row[0]] == human and type(board[row[1]]) is IntType and board[row[2]] == human:
            move=row[1]
        
        if board[row[0]] == human and board[row[1]] == human and type(board[row[2]]) is IntType:
            move=row[2]
        
                        

                         
    return move
            
#computer complete - checks to see if the computer can complete the move to win
def computer_complete(board,computer):
    move=-1
    #winning conditions
    cond = [[0,1,2],
            [0,3,6],
            [0,4,8],
            [1,4,7],
            [2,5,8],
            [2,4,6],
            [3,4,5],
            [6,7,8],
        ] 
    #cycling through the conditions
    for row in cond:                    
        # checks to see if column in row is free
        if type(board[row[0]]) is IntType and board[row[1]] == computer and board[row[2]] == computer:
            move = row[0]
                    
        if board[row[0]] == computer and type(board[row[1]]) is IntType and board[row[2]] == computer:
            move = row[1]
                    
        if board[row[0]] == computer and board[row[1]] == computer and type(board[row[2]]) is IntType: 
            move = row[2]
        
    return move

#free space list
def free_spaces(board):
    temp = []
    for x in range(len(board)):      
        if board[x] not in ("X","O"):
            temp.append(x)
    return temp

#generates random move
def computer_random(board,player):
    move = -1
    temp=free_spaces(board)
    if temp != []:
        move=random.sample(temp,1)[0]               
    return move

#checks for first move
def first_move(board):
    space_cache=len(board) - len(free_spaces(board))
    if space_cache < 2:
        return True

    return False

#moves the computer makes
def computer_move(board, computer):
    #player assignment
    if computer == 'O':
        human = 'X'
    else:
        human = 'O'
            
    move = -1
    first = first_move(board)

    #check the block
    move = computer_block(board,computer) 
    
    if move > -1:
        return move

    #check to see if move is going to win
    move = computer_complete(board,computer)
    
    if move > -1:
        return move
    
    #second move conditionals to throw the player off
    if first:
        #if first move is center
        if board[0] == human or board[2] == human or board[6] == human or board[8] == human:
            return 4
        #if first move is a corner
        elif board[4] == human:
            return computer_random(board,computer)     
        #if not edge or center hit, them with the wrench
        elif board[1] == human or board[3] == human or board[5] == human or board[7] == human:
            return 4
    
    if board[0] == computer:
        return 8 
    elif board[2] == computer:
        return 6
    elif board[6] == computer:
        return 2
    elif board[8] == computer:
        return 0
    
    #Generate Random Move
    if move < 0:
        move = computer_random(board,computer)
        
    return move

#move mark
def mark_move(board,move,player):
    board[move] = player

#move the player mmakes
def player_move(board, human):
    display_board(board)   
    move=player_input(human)
    
    #if the space is taken keep ask for a new space
    while is_marked(board, move):
        display_board(board)
        move=player_input(human,True)
    return move

win = 0
loss = 0
draw = 0

while True:
        #START THE GAME
    board = [0,1,2,3,4,5,6,7,8]
    player_shape=select_shape()        
    
    #Defines player
    PLAYER_1 = player_shape['one']
    PLAYER_2 = player_shape['two']
    
    print "====== STATS ======"
    print "player wins: %s" % win
    print "player losses: %s" % loss
    print "player draws: %s" % draw
    print "==================="
    
    for i in range(0,9):
        #Player 1 Move and Mark
        human_move = player_move(board, PLAYER_1)
        mark_move(board,human_move,PLAYER_1)
        
        if win_condition(board,PLAYER_1):
            print "\n%s is the WINNER" % PLAYER_1
            display_board(board)
            print "MIKE >>> Player 1 you have won!  I have been defeated..."
            win+=1
            
            print "====== STATS ======"
            print "player wins: %s" % win
            print "player losses: %s" % loss
            print "player draws: %s" % draw
            print "==================="          
                         
            if not play_again():
                print "MIKE >>> GOOD BYE \n"
                sys.exit()
           
            break
            
        #Player 2 Move
        comp_move = computer_move(board, PLAYER_2)
        print computer_message()
        
        if comp_move < 0:
            print "\nMIKE >>> Every move has been blocked DRAW!!!\n"
            draw+=1
            
            print "====== STATS ======"
            print "player wins: %s" % win
            print "player losses: %s" % loss
            print "player draws: %s" % draw
            print "==================="
            
            if not play_again():
                print "MIKE >>> GOOD BYE \n"
                sys.exit()
                
            break
        
        #Player 2 mark
        mark_move(board,comp_move,PLAYER_2)
        
        if win_condition(board,PLAYER_2):
            print "\n%s is the WINNER" % PLAYER_2
            display_board(board)
            print "MIKE >>> I have won!\n"
            loss+=1

            print "====== STATS ======"
            print "player wins: %s" % win
            print "player losses: %s" % loss
            print "player draws: %s" % draw
            print "==================="   
                     
            if not play_again():
                print "MIKE >>> GOOD BYE \n"
                sys.exit()
         
            break