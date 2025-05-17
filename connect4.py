#import library
import pygame
import random
import math
import sys

pygame.init()

#Unchangable variables
ROW_COUNT = 6
COLUMN_COUNT = 7
FOUND = True

SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE
size = (width, height)

RADIUS = int(SQUARE_SIZE/2 - 5)

screen = pygame.display.set_mode(size)
surface = pygame.Surface((width,height), pygame.SRCALPHA)

#Images
rules_img = pygame.image.load('rules.jpeg')
rules = pygame.transform.scale(rules_img, (width, height))
main_bg = pygame.image.load('main_menu_bg.png')
dark_bg = pygame.image.load('dark_bg.jpg')

#Colors
ORANGE = (255, 69, 0)

#Fonts
font = pygame.font.SysFont('Comic Sans MS',40)

#Function to create board
def game_board():
    global board
    board = [[0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]]
    return board
board = game_board()
#Function to print board
def print_board(board):
    for row in range(ROW_COUNT - 1,-1,-1):
        print(board[row])
        print()
        
#Function to put the piece
def drop_piece(board, row, col, piece):
    board[row][col] = piece

#Function to check if the location is clear
def valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

#Function to get the row
def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row
        
#Function to check for the win
def check_win(board, piece):
    
    #Check horizontal
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True
            
    #Check vertical
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True
            
    #Check positive diagonal
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True
            
    #Check negative diagonal
    for col in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True

#Function to check draw
def check_draw(board,piece):
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == 0 :
                return False
    return True
#draw board on screen
def draw_board(board):
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, 'blue', (col*SQUARE_SIZE, row*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, 'black', (int(col*SQUARE_SIZE+SQUARE_SIZE/2), int(row*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)

    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == 1:
                pygame.draw.circle(screen, 'red', (int(col*SQUARE_SIZE+SQUARE_SIZE/2), height - int(row*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, 'yellow', (int(col*SQUARE_SIZE+SQUARE_SIZE/2), height - int(row*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
#checks if the file already exists
def check_name():

    global file_name
    file_name = user_input +".txt"

    try:
        open(file_name,'r')
        print(f"The file exits")
        resume = open(file_name,'a')
        return FOUND
    except FileNotFoundError:
        error = "file created"
        print(error)
        new_file = open(file_name,'a')
        return file_name
#asks the user to start or continue if the file already exists  
def check_game():

    run = True
    active = False
    error = False
    name = check_name()

    while run:
        screen.blit(dark_bg, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                    
                if event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                    
                if back_button.collidepoint(event.pos):
                        run = False

        if name == True:
            
            text_width, text_height = font.size(user_input)

            if active:
                text_box = pygame.draw.rect(screen, ORANGE, (220, 300, max(250,text_width + 40), 50),0, 30)
            else:
                text_box = pygame.draw.rect(screen, 'grey', (220, 300, max(250,text_width + 40), 50),0, 30)

            if error:
                screen.blit(font.render('You need to enter a name',True,'red'), (110,400))
            
            screen.blit(font.render('Enter your name:',True,'white'), (190,100))
            screen.blit(font.render(user_input,True,'black'), (240,295))
        
            new_game_button = pygame.draw.rect(screen, ORANGE, (50, 500, 250, 50),0, 30)
            load_button = pygame.draw.rect(screen, ORANGE, (400, 500, 250, 50),0, 30)
            back_button = pygame.draw.rect(screen, ORANGE, (275, 600, 150, 50),0, 30)

            screen.blit(font.render('New Game',True,'black'), (80,495))
            screen.blit(font.render('Load Game',True,'black'), (420,495))
            screen.blit(font.render('Back',True,'black'), (300,595))

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if new_game_button.collidepoint(event.pos):
                        game_mode()
                    if load_button.collidepoint(event.pos):
                        load = load_game(file_name)
                        continue_game(load)
                    
        else:

            game_mode()
            
        pygame.display.flip()

#save the game after the user plays
def save_game(file_name,board):

    file = open(file_name,'w')
    for row in board:
        data = ''
        for value in row:
            data += str(value) + ''
        file.write(data.strip()+'\n')
    print(f'Game saved to {file_name}')

#retrieve the saved game from the file
def load_game(file_name):
    
    file = open(file_name,'r')
    board = []
    for line in file:
        row = [int(value) for value in line.strip()]
        board.append(row)
    print(f'Game loaded from {file_name}')
    print(board)
    return board
    
#MENU

def main_menu():
    game_board()
    screen = pygame.display.set_mode((size))
    
    while True:
        
        pygame.display.set_caption('Main Menu')
        screen.blit(main_bg, (0, 0))
        play_button = pygame.draw.rect(screen, ORANGE, (30, 280, 200, 50),0, 30)
        rules_button = pygame.draw.rect(screen, ORANGE, (30, 380, 200, 50),0, 30)
        credits_button = pygame.draw.rect(screen, ORANGE, (30, 480, 200, 50),0, 30)
        exit_button = pygame.draw.rect(screen, ORANGE, (30, 580, 200, 50),0, 30)
        
        screen.blit(font.render('Play',True,'black'), (90,275))
        screen.blit(font.render('Rules',True,'black'), (75,375))
        screen.blit(font.render('Credits',True,'black'), (55,475))
        screen.blit(font.render('Exit',True,'black'), (90,575))
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if play_button.collidepoint(event.pos):
                    name_page()

                if rules_button.collidepoint(event.pos):
                    rules_page()

                if credits_button.collidepoint(event.pos):
                    credits_page()

                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.flip()

def rules_page():
    
    run = True
    while run:
        
        pygame.display.set_caption('Rules')
        screen.blit(rules, (0, 0))
        back_button = pygame.draw.rect(screen, 'black', (275, 640, 150, 50),0, 30)
        screen.blit(font.render('Back',True,'white'), (300,635))

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if back_button.collidepoint(event.pos):
                    run = False

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    run = False
                
        pygame.display.flip()

def credits_page():
    
    run = True
    while run:

        pygame.display.set_caption('Credits')
        screen.blit(dark_bg, (0,0))
        screen.blit(font.render('CREDITS',True,'white'), (260,80))
        screen.blit(font.render('Made by:',True,'white'), (10,150))
        screen.blit(font.render('Karim Wael',True,'white'), (100,200))
        
        back_button = pygame.draw.rect(screen, ORANGE, (275, 600, 150, 50),0, 30)
        screen.blit(font.render('Back',True,'black'), (300,595))
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if back_button.collidepoint(event.pos):
                    run = False

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    run = False

        pygame.display.flip()

def pause_page():
    
    pygame.draw.rect(surface, (128, 128, 128, 7), (0, 0, width, height))
    pygame.draw.rect(surface, 'black', (100, 100, 500, 500),0, 10)
    
    continue_button = pygame.draw.rect(surface, ORANGE, (150, 250, 400, 50),0, 30)
    save_button = pygame.draw.rect(surface, ORANGE, (150, 350, 400, 50),0, 30)
    exit_button = pygame.draw.rect(surface, ORANGE, (150, 450, 400, 50),0, 30)

    surface.blit(font.render('Game Paused',True,'white'), (230,150))
    surface.blit(font.render('Continue',True,'black'), (270,245))
    surface.blit(font.render('Save',True,'black'), (300,345))
    surface.blit(font.render('Exit',True,'black'), (300,445))
    
    screen.blit(surface, (0, 0))
    return continue_button,save_button,exit_button

def game_mode():
    
    run = True
    while run:
        
        pygame.display.set_caption('Game Mode')
        screen.blit(dark_bg, (0,0))
        back_button = pygame.draw.rect(screen, ORANGE, (275, 600, 150, 50),0, 30)
        multiplayer_button = pygame.draw.rect(screen, ORANGE, (80, 300, 250, 50),0, 30)
        computer_button = pygame.draw.rect(screen, ORANGE, (380, 300, 250, 50),0, 30)

        screen.blit(font.render('Choose mode',True,'white'), (220,100))        
        screen.blit(font.render('Back',True,'black'), (300,595))
        screen.blit(font.render('Multiplayer',True,'black'), (100,293))
        screen.blit(font.render('Computer',True,'black'), (410,293))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if back_button.collidepoint(event.pos):
                    name_page()

                if multiplayer_button.collidepoint(event.pos):
                    play_page()

                if computer_button.collidepoint(event.pos):
                    computer_page()
            
            if event.type == pygame.KEYDOWN:
                    
                if event.key == pygame.K_ESCAPE:
                    run = False
                    
        pygame.display.flip()
#display the winner and show option to start a new game      
def win_page(piece):

    run = True
    while run:

        screen.blit(dark_bg, (0,0))
        pygame.display.set_caption('CONGRATULATIONS!')
        
        if piece == 1:
            screen.blit(font.render(f'Player {piece} WINS!',True,'white'), (200,100))
        elif piece == 2:
            screen.blit(font.render(f'Player {piece} WINS!',True,'white'), (200,100))

        new_game_button = pygame.draw.rect(screen, ORANGE, (80, 400, 250, 50),0, 30)
        main_menu_button = pygame.draw.rect(screen, ORANGE, (380, 400, 250, 50),0, 30)

        screen.blit(font.render('New Game',True,'black'), (100,395))
        screen.blit(font.render('Main Menu',True,'black'), (400,395))
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if new_game_button.collidepoint(event.pos):
                    play_page()

                if main_menu_button.collidepoint(event.pos):
                    main_menu()

        pygame.display.flip()
#displays that the game ended in a draw
def draw_page():
    
    run = True
    while run:

        screen.blit(dark_bg, (0,0))
        pygame.display.set_caption('DRAW!')
        
        screen.blit(font.render('NO ONE WON ITS A DRAW!',True,'white'), (80,100))

        new_game_button = pygame.draw.rect(screen, ORANGE, (80, 400, 250, 50),0, 30)
        main_menu_button = pygame.draw.rect(screen, ORANGE, (380, 400, 250, 50),0, 30)

        screen.blit(font.render('New Game',True,'black'), (100,395))
        screen.blit(font.render('Main Menu',True,'black'), (400,395))
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if new_game_button.collidepoint(event.pos):
                    play_page()

                if main_menu_button.collidepoint(event.pos):
                    main_menu()

        pygame.display.flip()
#Takes user input
def name_page():

    active = False
    error = False
    global user_input
    user_input = ''
    run = True
    while run:

        screen.blit(dark_bg, (0,0))
        pygame.display.set_caption('Welcome to Connect 4!')

        continue_button = pygame.draw.rect(screen, ORANGE,(450, 600, 190, 50),0, 30)
        back_button = pygame.draw.rect(screen, ORANGE, (50, 600, 160, 50),0, 30)
        text_width, text_height = font.size(user_input)

        if active:
            text_box = pygame.draw.rect(screen, ORANGE, (220, 300, max(250,text_width + 40), 50),0, 30)
        else:
            text_box = pygame.draw.rect(screen, 'grey', (220, 300, max(250,text_width + 40), 50),0, 30)

        if error:
            screen.blit(font.render('You need to enter a name',True,'red'), (110,400))
        
        screen.blit(font.render('Enter your name:',True,'white'), (190,100))
        screen.blit(font.render(user_input,True,'black'), (240,295))
        screen.blit(font.render('Continue',True,'black'), (470,595))
        screen.blit(font.render('Back',True,'black'), (75,595))

        

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:

                if text_box.collidepoint(event.pos):
                    active = True
                    error = False
                else:
                    active = False

                if continue_button.collidepoint(event.pos):
                    if user_input == '':
                        error = True
                    else:
                        check_game()
                    
                if back_button.collidepoint(event.pos):
                    main_menu()

            pygame.display.flip()
    return user_input

#allow you to play by choosing multiplayer
def play_page():
    
    
    draw_board(board)
    turn = 0
    pygame.display.flip()
    run = True
    pause = False
    while run:

        pygame.display.set_caption('Play')
       
        if pause:
            continue_button, save_button, exit_button = pause_page()
        else:
            draw_board(board)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause

            if not pause:
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, 'black', (0,0, width, SQUARE_SIZE))
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(screen, 'red', (posx, int(SQUARE_SIZE/2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, 'yellow', (posx, int(SQUARE_SIZE/2)), RADIUS)

                if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                    print(event.pos)

                    #Ask for player 1 selection
                    if turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARE_SIZE))
                        
                        if valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 1)

                            if check_win(board, 1):
                                win_page(1)
                                

                            if check_draw(board, 1):
                                draw_page()
                                
                    else:
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARE_SIZE))

                        #Ask for player 2 selection
                        if valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 2)

                            if check_win(board, 2):
                                win_page(2)

                            if check_draw(board,2):
                                draw_page()
                            

                    print_board(board)
                    draw_board(board)
                        
                    turn += 1
                    turn = turn % 2
                    
            if pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):
                        pause = False
                    if save_button.collidepoint(event.pos):
                        save_game(file_name,board)
                        main_menu()
                    if exit_button.collidepoint(event.pos):
                        main_menu()
        pygame.display.flip()

#allow you to play when choosing computer
def computer_page():

    board = game_board()
    draw_board(board)
    turn = 0
    pygame.display.flip()
    run = True
    pause = False
    player = 0
    computer = 1
    while run:

        pygame.display.set_caption('Play')
       
        if pause:
            continue_button, save_button, exit_button = pause_page()
        else:
            draw_board(board)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause

            if not pause:
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, 'black', (0,0, width, SQUARE_SIZE))
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(screen, 'red', (posx, int(SQUARE_SIZE/2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, 'yellow', (posx, int(SQUARE_SIZE/2)), RADIUS)

                if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                    print(event.pos)

                    #Ask for player 1 selection
                    if turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARE_SIZE))
                        
                        if valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 1)

                            if check_win(board, 1):
                                win_page(1)
                                

                            if check_draw(board, 1):
                                draw_page()

                            turn += 1
                            turn = turn % 2

                            print_board(board)
                            draw_board(board)
                            pygame.display.flip()
                                
            if turn == computer and run:

                col = random.randint(0, COLUMN_COUNT - 1)

                if valid_location(board, col):
                    pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if check_win(board, 2):
                        win_page(2)

                    if check_draw(board,2):
                        draw_page()
                            

                    print_board(board)
                    draw_board(board)
                        
                    turn += 1
                    turn = turn % 2
                    
            if pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):
                        pause = False
                    if save_button.collidepoint(event.pos):
                        save_game(file_name,board)
                        main_menu()
                    if exit_button.collidepoint(event.pos):
                        main_menu()
        pygame.display.flip()

#loads the saved game
def continue_game(load):
    board = load
    draw_board(board)
    turn = 0
    pygame.display.flip()
    run = True
    pause = False
    while run:

        pygame.display.set_caption('Play')
       
        if pause:
            continue_button, save_button, exit_button = pause_page()
        else:
            draw_board(board)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause

            if not pause:
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, 'black', (0,0, width, SQUARE_SIZE))
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(screen, 'red', (posx, int(SQUARE_SIZE/2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, 'yellow', (posx, int(SQUARE_SIZE/2)), RADIUS)

                if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                    print(event.pos)

                    #Ask for player 1 selection
                    if turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARE_SIZE))
                        
                        if valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 1)

                            if check_win(board, 1):
                                win_page(1)
                                

                            if check_draw(board, 1):
                                draw_page()
                                
                    else:
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARE_SIZE))

                        #Ask for player 2 selection
                        if valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 2)

                            if check_win(board, 2):
                                win_page(2)

                            if check_draw(board,2):
                                draw_page()
                            

                    print_board(board)
                    draw_board(board)
                        
                    turn += 1
                    turn = turn % 2
                    
            if pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):
                        pause = False
                    if save_button.collidepoint(event.pos):
                        save_game(file_name,board)
                        main_menu()
                    if exit_button.collidepoint(event.pos):
                        main_menu()

        pygame.display.flip()
        
run = True
# calls the function that has all the functions of the game
main_menu()
 
pygame.quit()

