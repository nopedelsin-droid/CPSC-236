import pygame   # used for drawing and displaying graphic game
import sys      # used for font and app control
import main     # main gameplay file

pygame.init()

# global constants for window and title
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 Menu")

# global constants for colors used
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

font = pygame.font.SysFont("monospace", 36)

# Button class
class Button:
    def __init__(self, text, x, y, width, height):               # called with pygame.init()
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Start with base font size
        font_size = 40
        font = pygame.font.SysFont("monospace", font_size)

        label = font.render(self.text, True, BLACK)

        # Shrink text if too wide (mostly for player vs ai btn)
        while label.get_width() > self.rect.width - 20:
            font_size -= 2
            font = pygame.font.SysFont("monospace", font_size)
            label = font.render(self.text, True, BLACK)

        # Center text
        text_x = self.rect.x + (self.rect.width - label.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - label.get_height()) // 2

        screen.blit(label, (text_x, text_y))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
btn_2player = Button("2 Player", 150, 150, 300, 80)
btn_ai = Button("1 Player vs AI", 150, 260, 300, 80)
btn_exit = Button("Exit", 150, 370, 300, 80)

# function to handle
def draw_menu():
    screen.fill(WHITE)

    title = font.render("CONNECT 4", True, BLUE)
    screen.blit(title, (150, 50))

    btn_2player.draw()
    btn_ai.draw()
    btn_exit.draw()

    pygame.display.update()

# Menu loop
while True:
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if btn_2player.is_clicked(pos):
                main.run_game(vs_ai=False)
                # RESET window size for menu
                screen = pygame.display.set_mode((WIDTH, HEIGHT))

            if btn_ai.is_clicked(pos):
                main.run_game(vs_ai=True)
                # RESET window size for menu
                screen = pygame.display.set_mode((WIDTH, HEIGHT))

            if btn_exit.is_clicked(pos):
                pygame.quit()
                sys.exit()