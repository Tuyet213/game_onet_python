import pygame
import os
from button import Button

class Menu:
    def __init__(self, SCREEN_SIZE):
        pygame.font.init()
        self.WIN_WIDTH, self.WIN_HEIGHT = SCREEN_SIZE[0], SCREEN_SIZE[1]
        self.display_screen = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.display_screen.fill((255, 255, 255))
        self.font = pygame.font.Font(None, 36)
        self.options = ["Easy", "Medium", "Hard"]
        self.selected_option = 4
        self.background = None
        self.text_size = 60
        self.vertical_spacing = 20
        self.btn_difficulty = []
        for i, o in enumerate(self.options):
          btn_sz = [150, 50]
          btn = Button((SCREEN_SIZE[0] - btn_sz[0])//2, (SCREEN_SIZE[1] - btn_sz[1])//2 + (btn_sz[1]+20)*i, btn_sz[0], btn_sz[1], True, text=o, border_rad=10)
          self.btn_difficulty.append(btn)
        self.set_background()

    def set_selected_option(self, option):
        self.selected_option = option

    def set_background(self):
        try:
          screen_width, screen_height = self.display_screen.get_width(), self.display_screen.get_height()
          self.folder_path = os.path.dirname(__file__)
          self.background = pygame.image.load(os.path.join(self.folder_path, 'images', 'menu_bg.png'))
          self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        except pygame.error as e:
          print("Error loading background image:", e)
        if self.background:
          self.display_screen.blit(self.background, (0, 0))
        else:
          self.display_screen.fill((0, 0, 0))

    def draw_buttons(self):
      for i in range(len(self.btn_difficulty)):
        self.btn_difficulty[i].draw(self.display_screen)

    def get_val(self, event):
      for i in range(len(self.btn_difficulty)):
          self.btn_difficulty[i].handle_event(event)
          if self.btn_difficulty[i].clicked():
             return i
      return -1
      

      

        


