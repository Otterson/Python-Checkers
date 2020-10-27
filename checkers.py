import pygame
import sys

pygame.init()

screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (54,89,74)
GREY = (50,50,50)
YELLOW = (255, 255,0)


square_size = (screen_height - 100) / 8

board_grid = [["empty", "empty"]*8]*8


#gets the cell index of a given mouse click, returns (x,y)
#X index 0 is on the left, Y index 0 is on the top of the board
def get_click_index(position):
    x = position[0]
    y = position[1]

    #accounts for the offset of where the board starts
    board_x_pos = x-200
    board_y_pos = y-50

    x_index = int(board_x_pos / square_size)
    y_index = int(board_y_pos / square_size)

    return (x_index, y_index)


#Higlights the square available for moves
def find_moves(index):
    x_index = index[0]
    y_index = index[1]
    piece_color= board_grid[x_index][y_index][0]
    piece_type= board_grid[x_index][y_index][1]

    possible_moves = []
    

    if piece_type == "king":
        print("king")
        if y_index +1 <8:
            
            if x_index -1 > 0 and (board_grid[x_index -1][y_index+1][0] == "e"):
                possible_moves.append((x_index-1, y_index+1))
            if x_index + 1 < 8 and (board_grid[x_index +1][y_index+1][0] == "e"):
                possible_moves.append((x_index + 1, y_index +1))
        if y_index -1 >=0:
            if x_index -1 > 0 and board_grid[x_index -1][y_index-1][0] == "e":
                possible_moves.append((x_index-1, y_index-1))
            if x_index + 1 < 8 and board_grid[x_index +1][y_index-1][0] == "e":
                possible_moves.append((x_index + 1, y_index -1))

    elif piece_color == "red":
        if y_index -1 >=0:
            if x_index -1 >= 0 and (board_grid[x_index -1][y_index-1][0] == "e"):
                possible_moves.append((x_index-1, y_index-1))
            if x_index + 1 < 8 and (board_grid[x_index +1][y_index-1][0] == "e"):
                possible_moves.append((x_index + 1, y_index -1))

                

    elif piece_color == "black":
        if y_index +1 <8:
            if x_index -1 >= 0 and board_grid[x_index -1][y_index+1][0] == "e":
                possible_moves.append((x_index-1, y_index+1))
            if x_index + 1 < 8 and board_grid[x_index +1][y_index+1][0] == "e":
                possible_moves.append((x_index + 1, y_index +1))

    return possible_moves
    


def move_piece(piece, position, color):
    build_board_x = 200
    build_board_y = 50
    if color is "red":
        pygame.draw.circle(screen,RED, (int(build_board_x + square_size/2 + position[0]*square_size), int(build_board_y + square_size/2 + position[1]*square_size)), int(square_size/3))
        pygame.draw.circle(screen,GREY, (int(build_board_x + square_size/2 + piece[0]*square_size), int(build_board_y + square_size/2 + piece[1]*square_size)), int(square_size/3))
    
    else:
        pygame.draw.circle(screen,BLACK, (int(build_board_x + square_size/2 + position[0]*square_size), int(build_board_y + square_size/2 + position[1]*square_size)), int(square_size/3))
        pygame.draw.circle(screen,GREY, (int(build_board_x + square_size/2 + piece[0]*square_size), int(build_board_y + square_size/2 + piece[1]*square_size)), int(square_size/3))

    board_grid[piece[0]][piece[1]] = ("empty","empty")
    board_grid[position[0]][position[1]] = (color, "normal")


def highlight_moves(moves):
    build_board_x = 200
    build_board_y = 50
    for move in moves:
        pygame.draw.rect(screen, YELLOW, (build_board_x + move[0]*square_size, build_board_y + move[1] * square_size, square_size, square_size))

    print(moves)


def clear_highlights(moves):
    build_board_x = 200
    build_board_y = 50
    for move in moves:
        pygame.draw.rect(screen, GREY, (build_board_x + move[0]*square_size, build_board_y + move[1] * square_size, square_size, square_size))


#Build game board and grid
build_board_x = 200
build_board_y = 50
black = True
screen.fill(GREEN)
for i in range(0,8):
    for j in range(0,8):
        if black:
            pygame.draw.rect(screen, GREY, (build_board_x, build_board_y, square_size, square_size))
            if i<3:
                pygame.draw.circle(screen,BLACK, (int(build_board_x + square_size/2), int(build_board_y + square_size/2)), int(square_size/3))
                board_grid[j][i] = ("black", "normal")
            if i>=5:
                pygame.draw.circle(screen,RED, (int(build_board_x + square_size/2), int(build_board_y + square_size/2)), int(square_size/3))
                board_grid[j][i] = ("red", "normal")
            black = False
        else:
            pygame.draw.rect(screen, WHITE, (build_board_x, build_board_y, square_size, square_size))
            black = True
        build_board_x += square_size
    black = not black
    build_board_x = 200
    build_board_y+= square_size

possible_moves = []
selected_piece = (0,0)
selected_color= ""  
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        #left mouse click
        if pygame.mouse.get_pressed() == (1,0,0):
            mouse_pos = pygame.mouse.get_pos()
            click_index = get_click_index(mouse_pos)
            if click_index in possible_moves:
                clear_highlights(possible_moves)
                move_piece(selected_piece, click_index, selected_color)
                possible_moves = []
                selected_color = ""
                selected_piece = (0,0)
            elif board_grid[click_index[0]][click_index[1]][0] != "e":
                print("elif"    )
                selected_color = (board_grid[click_index[0]][click_index[1]])[0]
                selected_piece = click_index
                possible_moves = find_moves(click_index) 
                highlight_moves(possible_moves)
           
        

        

    pygame.display.update()