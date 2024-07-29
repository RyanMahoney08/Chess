import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 650, 650
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 100, 20)
RED = (255, 0, 0)  # Color for the turn indicator

# Load images
def load_images():
    pieces = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))
    return images

# Draw the chess board
def draw_board(win):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 1:
                pygame.draw.rect(win, BLACK, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw the pieces on the board
def draw_pieces(win, pieces, images):
    for pos, piece in pieces.items():
        row, col = pos
        win.blit(images[piece], (col*SQUARE_SIZE, row*SQUARE_SIZE))

# Draw the turn indicator
def draw_turn_indicator(win, turn):
    font = pygame.font.SysFont('Arial', 36)
    text = font.render(f"{turn}'s Turn", True, RED)
    win.blit(text, (10, HEIGHT - 50))

# Piece movement rules
def is_valid_move(piece, start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Prevent moving onto a square occupied by a piece of the same color
    if board[end_row][end_col] != '--' and board[end_row][end_col][0] == piece[0]:
        return False

    if piece[1] == 'P':  # Pawn
        direction = -1 if piece[0] == 'w' else 1
        if start_col == end_col:  # Move forward
            if board[end_row][end_col] == '--' and (end_row == start_row + direction or 
                                                    (start_row == (6 if piece[0] == 'w' else 1) and end_row == start_row + 2 * direction and board[start_row + direction][start_col] == '--')):
                return True
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction and board[end_row][end_col] != '--':  # Capture
            return True

    elif piece[1] == 'R':  # Rook
        if start_row == end_row or start_col == end_col:
            step_row = (end_row - start_row) // max(1, abs(end_row - start_row))
            step_col = (end_col - start_col) // max(1, abs(end_col - start_col))
            for i in range(1, max(abs(end_row - start_row), abs(end_col - start_col))):
                if board[start_row + i * step_row][start_col + i * step_col] != '--':
                    return False
            return True

    elif piece[1] == 'N':  # Knight
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return True

    elif piece[1] == 'B':  # Bishop
        if abs(start_row - end_row) == abs(start_col - end_col):
            step_row = (end_row - start_row) // abs(end_row - start_row)
            step_col = (end_col - start_col) // abs(end_col - start_col)
            for i in range(1, abs(end_row - start_row)):
                if board[start_row + i * step_row][start_col + i * step_col] != '--':
                    return False
            return True

    elif piece[1] == 'Q':  # Queen
        if start_row == end_row or start_col == end_col:
            step_row = (end_row - start_row) // max(1, abs(end_row - start_row))
            step_col = (end_col - start_col) // max(1, abs(end_col - start_col))
            for i in range(1, max(abs(end_row - start_row), abs(end_col - start_col))):
                if board[start_row + i * step_row][start_col + i * step_col] != '--':
                    return False
            return True
        elif abs(start_row - end_row) == abs(start_col - end_col):
            step_row = (end_row - start_row) // abs(end_row - start_row)
            step_col = (end_col - start_col) // abs(end_col - start_col)
            for i in range(1, abs(end_row - start_row)):
                if board[start_row + i * step_row][start_col + i * step_col] != '--':
                    return False
            return True

    elif piece[1] == 'K':  # King
        if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
            return True

    return False  # Invalid move by default

# Main function
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    images = load_images()

    selected_piece = None
    current_turn = 'White'  # Start with White's turn

    pieces = {
        (0, 0): 'bR', (0, 1): 'bN', (0, 2): 'bB', (0, 3): 'bQ', (0, 4): 'bK', (0, 5): 'bB', (0, 6): 'bN', (0, 7): 'bR',
        (1, 0): 'bP', (1, 1): 'bP', (1, 2): 'bP', (1, 3): 'bP', (1, 4): 'bP', (1, 5): 'bP', (1, 6): 'bP', (1, 7): 'bP',
        (6, 0): 'wP', (6, 1): 'wP', (6, 2): 'wP', (6, 3): 'wP', (6, 4): 'wP', (6, 5): 'wP', (6, 6): 'wP', (6, 7): 'wP',
        (7, 0): 'wR', (7, 1): 'wN', (7, 2): 'wB', (7, 3): 'wQ', (7, 4): 'wK', (7, 5): 'wB', (7, 6): 'wN', (7, 7): 'wR'
    }

    board = [['--' for _ in range(COLS)] for _ in range(ROWS)]
    for pos, piece in pieces.items():
        row, col = pos
        board[row][col] = piece

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

                if selected_piece:
                    start_pos = selected_piece
                    end_pos = (row, col)
                    piece = board[start_pos[0]][start_pos[1]]
                    
                    if end_pos == start_pos:
                        # Clicked on the same piece, deselect it
                        selected_piece = None
                    elif is_valid_move(piece, start_pos, end_pos, board):
                        if board[end_pos[0]][end_pos[1]] != '--':
                            # Remove captured piece
                            del pieces[(end_pos[0], end_pos[1])]
                        pieces[end_pos] = pieces.pop(start_pos)
                        board[start_pos[0]][start_pos[1]] = '--'
                        board[end_pos[0]][end_pos[1]] = piece
                        selected_piece = None  # Deselect the piece after a valid move
                        current_turn = 'Black' if current_turn == 'White' else 'White'  # Switch turn
                    else:
                        # Move is invalid; keep the piece selected
                        selected_piece = start_pos
                else:
                    if board[row][col] != '--':  # Select the piece if a piece is present at the clicked position
                        if board[row][col][0] == ('w' if current_turn == 'White' else 'b'):  # Only allow selecting pieces of the current turn
                            selected_piece = (row, col)

        draw_board(win)
        draw_pieces(win, pieces, images)
        draw_turn_indicator(win, current_turn)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()