import pygame
import random

# Initialize Pygame
pygame.init()

# Game Settings
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4
CARD_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.Font(None, 60)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (100, 100, 200)
GREEN = (0, 200, 100)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Card Game")

# Generate Symbols
symbols = [str(i) for i in range(1, 9)] * 2
random.shuffle(symbols)

def create_board():
    return [[{'symbol': symbols.pop(), 'revealed': False} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def flip_animation(x, y, symbol):
    for scale in range(CARD_SIZE, 0, -20):
        pygame.draw.rect(screen, PURPLE, (x, y, CARD_SIZE, CARD_SIZE))
        pygame.draw.rect(screen, WHITE, (x + (CARD_SIZE - scale)//2, y, scale, CARD_SIZE))
        pygame.display.update()
        pygame.time.delay(15)
    text = FONT.render(symbol, True, BLACK)
    text_rect = text.get_rect(center=(x + CARD_SIZE // 2, y + CARD_SIZE // 2))
    screen.blit(text, text_rect)
    pygame.display.update()

def draw_board(board, time_elapsed):
    screen.fill(WHITE)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x, y = j * CARD_SIZE, i * CARD_SIZE
            pygame.draw.rect(screen, PURPLE, (x, y, CARD_SIZE, CARD_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CARD_SIZE, CARD_SIZE), 3)
            if board[i][j]['revealed']:
                text = FONT.render(board[i][j]['symbol'], True, BLACK)
                text_rect = text.get_rect(center=(x + CARD_SIZE // 2, y + CARD_SIZE // 2))
                screen.blit(text, text_rect)
    timer = FONT.render(f"Time: {time_elapsed}s", True, BLACK)
    screen.blit(timer, (10, HEIGHT - 40))
    pygame.display.flip()

def get_card(pos):
    x, y = pos
    return y // CARD_SIZE, x // CARD_SIZE

def check_win(board):
    return all(cell['revealed'] for row in board for cell in row)

def show_win_message(time_elapsed):
    screen.fill(GREEN)
    msg = FONT.render(f"You Won! Time: {time_elapsed}s", True, BLACK)
    screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.delay(3000)

def main():
    board = create_board()
    selected = []
    start_ticks = pygame.time.get_ticks()
    running = True

    while running:
        elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
        draw_board(board, elapsed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and len(selected) < 2:
                row, col = get_card(event.pos)
                if not board[row][col]['revealed']:
                    board[row][col]['revealed'] = True
                    flip_animation(col * CARD_SIZE, row * CARD_SIZE, board[row][col]['symbol'])
                    selected.append((row, col))

        if len(selected) == 2:
            pygame.time.delay(500)
            r1, c1 = selected[0]
            r2, c2 = selected[1]
            if board[r1][c1]['symbol'] != board[r2][c2]['symbol']:
                board[r1][c1]['revealed'] = False
                board[r2][c2]['revealed'] = False
            selected = []

        if check_win(board):
            draw_board(board, elapsed)
            show_win_message(elapsed)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
