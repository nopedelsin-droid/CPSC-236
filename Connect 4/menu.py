# Mike Benko IV
# CPSC236 - Final Project
# menu.py

import pygame   # used for drawing and displaying graphic game
import sys      # used for font and app control
import main     # main gameplay file

# initialize pygame package
pygame.init()

# global constants for window and title
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 Menu")

# global constants for colors used
WHITE = (255, 250, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

font = pygame.font.SysFont("monospace", 36)

# button class
class Button:
    def __init__(self, text, x, y, width, height):               # called with pygame.init() in main.py and ai.py
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    # menu display class
    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)                                # apply base menu draw definitions
        pygame.draw.rect(screen, BLACK, self.rect, 2)                      # apply menu border draw definitions
        font_size = 40
        font = pygame.font.SysFont("monospace", font_size)                 # apply used font from sys package

        label = font.render(self.text, True, BLACK)

        while label.get_width() > self.rect.width - 20:                          # logic loop to shrink text if too wide (mostly for player vs ai btn)
            font_size -= 2
            font = pygame.font.SysFont("monospace", font_size)
            label = font.render(self.text, True, BLACK)

        # centering text fix
        text_x = self.rect.x + (self.rect.width - label.get_width()) // 2         # take half of the difference between button and window width + buffer
        text_y = self.rect.y + (self.rect.height - label.get_height()) // 2       # take half of the difference between button and window height + buffer

        screen.blit(label, (text_x, text_y))

    # click position passing class
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# create buttons with definitions
# apply coordinates for button placement and click area definition
btn_2player = Button("2 Player", 150, 150, 300, 80)
btn_ai = Button("1 Player vs AI", 150, 260, 300, 80)
btn_exit = Button("Exit", 150, 370, 300, 80)

# function to handle main menu window generation
def draw_menu():
    screen.fill(WHITE)

    title = font.render(" CONNECT 4", True, BLUE)
    screen.blit(title, (165, 50))

    btn_2player.draw()                                            # call 2 player button
    btn_ai.draw()                                                 # call player vs ai button
    btn_exit.draw()                                               # call exit game button

    pygame.display.update()                                       # force update display window

# menu logic loop
while True:                                                        # while loop to continue until exit button or close window is applied
    draw_menu()                                                      # initial draw of menu window

    for event in pygame.event.get():                                 # encapsulating for-loop for event handling
        if event.type == pygame.QUIT:                                  # user selects close window
            pygame.quit()                                                # safely close program
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:                       # nested if for mouse click event handling
            pos = event.pos                                              # determine position of mouse click

            if btn_2player.is_clicked(pos):                              # if mouse click position corresponds to 2 player game button
                main.run_game(vs_ai=False)                                 # set bool value to ignore ai logic
                # RESET window size for menu
                screen = pygame.display.set_mode((WIDTH, HEIGHT))          # reload window for gameplay

            if btn_ai.is_clicked(pos):                                   # if mouse click position corresponds to a player v ai game button
                main.run_game(vs_ai=True)                                  # set bool value to include ai logic
                # RESET window size for menu
                screen = pygame.display.set_mode((WIDTH, HEIGHT))          # reload window for gameplay

            if btn_exit.is_clicked(pos):                                 # if mouse click position corresponds to the game exit button
                pygame.quit()                                              # safely close program
                sys.exit()