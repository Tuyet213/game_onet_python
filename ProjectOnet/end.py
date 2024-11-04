import pygame
import os
from button import Button

class End:
    def __init__(self, SCREEN_SIZE, status, score=-1):
        pygame.font.init()
        self.WIN_WIDTH, self.WIN_HEIGHT = SCREEN_SIZE[0], SCREEN_SIZE[1]
        self.display_screen = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.display_screen.fill((255, 255, 255))
        self.font = pygame.font.Font(None, 36)
        self.background = None
        btn_sz = [150, 50]
        self.btn_play_again = Button((SCREEN_SIZE[0] - btn_sz[0])//2, (SCREEN_SIZE[1] - btn_sz[1])//2 + (btn_sz[1]+20)*0, btn_sz[0], btn_sz[1], True, text="Play again", border_rad=10)
        self.btn_exit = Button((SCREEN_SIZE[0] - btn_sz[0])//2, (SCREEN_SIZE[1] - btn_sz[1])//2 + (btn_sz[1]+20)*1, btn_sz[0], btn_sz[1], True, text="Exit", border_rad=10)
        self.btn_show_score = Button((SCREEN_SIZE[0] - btn_sz[0])//2, (SCREEN_SIZE[1] - btn_sz[1])//2 + (btn_sz[1]+20)*2, btn_sz[0], btn_sz[1], True, text="Show score", border_rad=10)
        font = pygame.font.Font(None, 70)

        self.set_background(status)

        text_status = font.render("Congrats, you win!", True, (0, 0, 0))
        if status == "lose":
           text_status = font.render("Sorry, you lose!", True, (0, 0, 0))
        
        text_score = font.render("Your score: " + str(score), True, (0, 0, 0))
        self.display_screen.blit(text_status, ((SCREEN_SIZE[0] - text_status.get_width()) // 2, 100))
        self.display_screen.blit(text_score, ((SCREEN_SIZE[0] - text_score.get_width()) // 2, 200))
        
        
    def set_background(self, status):
        try:
          screen_width, screen_height = self.display_screen.get_width(), self.display_screen.get_height()
          self.folder_path = os.path.dirname(__file__)
          if status == "win": 
             self.background = pygame.image.load(os.path.join(self.folder_path, 'images', 'winning_bg.png'))
          else:
             self.background = pygame.image.load(os.path.join(self.folder_path, 'images', 'lose_bg.jpg'))
          self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        except pygame.error as e:
          print("Error loading background image:", e)
        if self.background:
          self.display_screen.blit(self.background, (0, 0))
        else:
          self.display_screen.fill((0, 0, 0))
        
    def draw_buttons(self):
        self.btn_exit.draw(self.display_screen)
        self.btn_play_again.draw(self.display_screen)
        self.btn_show_score.draw(self.display_screen)
        
    def buttons_handle(self, event):
        self.btn_play_again.handle_event(event)
        if self.btn_play_again.clicked():
            return "play again"
        self.btn_exit.handle_event(event)
        if self.btn_exit.clicked():
            return "quit"
        self.btn_show_score.handle_event(event)
        if self.btn_show_score.clicked():
            return "show score"