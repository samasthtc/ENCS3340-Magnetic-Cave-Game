# Usama Shoora - 1200796
# Dr. Yazan Abu Farha - Section 2
# Magnetic Cave Game

import copy
import pygame as p


# class to represent the game board
class GameState:
    def __init__(self):
        self.board = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]


# class to represent game moves/states
class Node:
    def __init__(self, board):
        self.board = board
        self.children = []


# global variables to implement UI
width = height = 512
dimension = 8
sq_size = height // dimension
max_fps = 30
images = {}

bricks_clicks = []  # list of all made moves

automatic = True  # whether one player will be played by the AI or not
current_player = 'bb'
manual_player = 'bb'


# main function to run the game
def main():
    global automatic, current_player, manual_player

    # print choices for game mode
    while True:
        mode = int(input("\nPlease choose your preferred mode:\n"
                         "  1. Manual entry for both ■’s (black) moves and □’s (white) moves .\n"
                         "  2. Manual entry for ■’s (black) moves & automatic moves for □ (white).\n"
                         "  3. Automatic entry for ■’s (black) moves & manual moves for □ (white).\n"))
        if mode in [1, 2, 3]:
            break
        else:
            print("Enter valid choice.")

    if mode == 1:
        automatic = False
    elif mode == 3:
        manual_player = 'wb'

    # draw interface
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    load_images()
    gs = GameState()  # initialize game board
    draw_game_state(screen, gs)
    clock.tick(max_fps)
    p.display.flip()

    # Variables for controlling the display duration
    display_duration = 15  # Number of frames the text will be displayed
    display_timer = 0  # Counter for the frames passed

    player_names = {'wb': 'White', 'bb': 'Black'}
    running = True
    while running:
        # manual move
        if current_player == manual_player:
            wait_for_event = True
            while wait_for_event:
                if display_timer > 0:
                    display_text(screen, "Illegal Move!", 80, 10)
                    p.display.update()
                    display_timer -= 1
                draw_game_state(screen, gs)
                clock.tick(max_fps)
                p.display.flip()
                for e in p.event.get():
                    if e.type == p.QUIT:
                        exit()
                    elif e.type == p.MOUSEBUTTONDOWN:
                        location = p.mouse.get_pos()
                        col = location[0] // sq_size
                        row = location[1] // sq_size
                        print((row, col))
                        if is_legal_move(row, col, gs.board):
                            if (row, col) not in bricks_clicks:
                                bricks_clicks.append((row, col))
                                gs.board[row][col] = current_player
                                wait_for_event = False
                                if mode == 1:
                                    manual_player = 'bb' if current_player == 'wb' else 'wb'
                                break
                        print("Illegal Move!")
                        display_timer = display_duration
                        break
            # print statement on interface
            if display_timer > 0:
                display_text(screen, "Illegal Move!", 80, 10)
                p.display.update()
                display_timer -= 1

        else:
            # automatic move
            if automatic:
                ai_move(gs.board)

        draw_game_state(screen, gs)
        clock.tick(max_fps)
        p.display.flip()

        # check if current player has won
        if check_if_win(current_player, gs.board):
            print(f'Player {player_names[current_player]} won!')
            display_timer = display_duration
            wait_for_event = True
            while wait_for_event:
                display_text(screen, f'Player {player_names[current_player]} won!', 10, 10)
                p.display.update()
                draw_game_state(screen, gs)
                clock.tick(max_fps)
                p.display.flip()
                for e in p.event.get():
                    if e.type == p.MOUSEBUTTONDOWN or e.type == p.QUIT:
                        exit()

        # check if a tie happened
        if all(gs.board[i][j] != ' ' for i in range(8) for j in range(8)):
            print("It's a tie!")
            wait_for_event = True
            while wait_for_event:
                display_text(screen, "It's a tie!", 80, 10)
                p.display.update()
                draw_game_state(screen, gs)
                clock.tick(max_fps)
                p.display.flip()
                for e in p.event.get():
                    if e.type == p.MOUSEBUTTONDOWN or e.type == p.QUIT:
                        exit()

        current_player = 'bb' if current_player == 'wb' else 'wb'


# function to load the images used for the bricks
def load_images():
    images['bb'] = p.transform.scale(
            p.image.load("images/bb1.png"), (sq_size, sq_size))
    images['wb'] = p.transform.scale(
            p.image.load("images/wb1.png"), (sq_size, sq_size))


# function to check if a player won
def check_if_win(player, board):
    # check rows
    for i in range(8):
        for j in range(4):
            if all(board[i][j + k] == player for k in range(5)):
                return True

    # check columns
    for i in range(4):
        for j in range(8):
            if all(board[i + k][j] == player for k in range(5)):
                return True

    # check diagonally
    for i in range(4):
        for j in range(4):
            if all(board[i + k][j + k] == player for k in range(5)):
                return True
            if all(board[i + 4 - k][j + k] == player for k in range(5)):
                return True

    return False


# function to check if a move is legal
def is_legal_move(row, col, board):
    if col == 0 or col == 7:
        return True  # Brick can be placed at the edge

    for i in range(col - 1, col + 2):
        if 0 <= i < 8 and board[row][i] != ' ':
            return True  # Brick can be placed next to a brick on the edge

    return False


# function to draw game interface
def draw_game_state(screen, gs):
    colors = [p.Color("gray90"), p.Color("gray60")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(
                    c * sq_size, r * sq_size, sq_size, sq_size))
            piece = gs.board[r][c]
            if piece != ' ':
                screen.blit(images[piece], p.Rect(
                        c * sq_size, r * sq_size, sq_size, sq_size))


# function to display text on interface
def display_text(screen, text, x, y, font_size=50, color=(0, 0, 0)):
    font = p.font.Font('Futura Extra Black font.ttf', font_size)
    text_surface = font.render(text, True, color)
    stroke_surfaces = [
        font.render(text, True, (255, 255, 255))
        for _ in range(3)
        ]

    # blit the stroke surfaces with offsets
    for i, stroke_surface in enumerate(stroke_surfaces):
        screen.blit(stroke_surface, (x - i, y))
        screen.blit(stroke_surface, (x + i, y))
        screen.blit(stroke_surface, (x, y - i))
        screen.blit(stroke_surface, (x, y + i))
    screen.blit(text_surface, (x, y))


# function to evaluate the heuristic of a board state
def evaluation(board):
    score_1 = 0  # Player □/wb score
    score_2 = 0  # Player ■/bb score

    # check rows
    for i in range(8):
        for j in range(4):
            row = [board[i][j + k] for k in range(5)]
            if row.count('wb') == 5:
                score_1 += 1
            if row.count('bb') == 5:
                score_2 += 1

    # check columns
    for i in range(4):
        for j in range(8):
            col = [board[i + k][j] for k in range(5)]
            if col.count('wb') == 5:
                score_1 += 1
            if col.count('bb') == 5:
                score_2 += 1

    # check diagonally
    for i in range(4):
        for j in range(4):
            diagonal1 = [board[i + k][j + k] for k in range(5)]
            diagonal2 = [board[i + 4 - k][j + k] for k in range(5)]
            if diagonal1.count('wb') == 5 or diagonal2.count('wb') == 5:
                score_1 += 1
            if diagonal1.count('bb') == 5 or diagonal2.count('bb') == 5:
                score_2 += 1

    if manual_player == 'bb':
        return score_1 - score_2
    else:
        return score_2 - score_1


#  minimax function with alpha-beta pruning
def minimax(node, depth, alpha, beta, maximizing_player):
    player_max = 'wb' if manual_player == 'bb' else 'bb'
    player_min = 'bb' if manual_player == 'bb' else 'wb'

    # if depth limit is reached or game finished then exit function and return evaluation
    if depth == 0 or check_if_win('wb', node.board) or check_if_win('bb', node.board):
        return evaluation(node.board)

    if maximizing_player:
        max_eval = -999
        for i in range(8):
            for j in range(8):
                if is_legal_move(i, j, node.board) and node.board[i][j] == ' ':
                    temp1_board = copy.deepcopy(node.board)
                    temp1_board[i][j] = player_max
                    child = Node(temp1_board)
                    node.children.append(child)
                    eval_score = minimax(child, depth - 1, alpha, beta, False)
                    if eval_score is not None:
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = 999
        for i in range(8):
            for j in range(8):
                if is_legal_move(i, j, node.board) and node.board[i][j] == ' ':
                    temp2_board = copy.deepcopy(node.board)
                    temp2_board[i][j] = player_min
                    child = Node(temp2_board)
                    node.children.append(child)
                    eval_score = minimax(child, depth - 1, alpha, beta, True)
                    if eval_score is not None:
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
        return min_eval


# function to make an automatic move by AI
def ai_move(board):
    root = Node(board)
    best_score = -9999
    best_move = None
    player = 'wb' if manual_player == 'bb' else 'bb'

    # for depth in range(1, 3):  # optional, to implement iterative deepening
    for i in range(8):
        for j in range(8):
            if is_legal_move(i, j, root.board) and root.board[i][j] == ' ':
                temp_board = copy.deepcopy(root.board)
                temp_board[i][j] = player
                child = Node(temp_board)
                root.children.append(child)
                score = minimax(child, 3, -9999, 9999, False)
                if score is not None and score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move is not None:
        row, col = best_move
        board[row][col] = 'wb' if manual_player == 'bb' else 'bb'
        bricks_clicks.append((row, col))


if __name__ == "__main__":
    main()
