import pygame
import os
from button import Button
class ScoreTK:
    def __init__(self, SCREEN_SIZE, scores):
        pygame.font.init()
        self.WIN_WIDTH, self.WIN_HEIGHT = SCREEN_SIZE[0], SCREEN_SIZE[1]
        self.display_screen = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.display_screen.fill((0, 0, 0))
        self.font = pygame.font.Font(None, 36)
        self.scores = scores
        self.btn_score = []
        self.background = None
        self.text_size = 60
        self.vertical_spacing = 10
        btn_sz = [150, 50]
        if len(self.scores)>6:
          length=len(self.scores)//2
          for i, o in enumerate(self.scores[0:length]):
            text = 'Level ' + str(i+1) + ': '+str(o)
            btn = Button((SCREEN_SIZE[0] - btn_sz[0]*2)//3, (SCREEN_SIZE[1] - btn_sz[1]*10)//2 + (btn_sz[1]+20)*i, btn_sz[0], btn_sz[1], True, text=text, border_rad=10)
            self.btn_score.append(btn)
          for i, o in enumerate(self.scores[length:]):
            text = 'Level ' + str(length+i+1) + ': '+str(o)
            btn = Button(((SCREEN_SIZE[0] - btn_sz[0])//3)*2+btn_sz[0]-100, (SCREEN_SIZE[1] - btn_sz[1]*10)//2 + (btn_sz[1]+20)*i, btn_sz[0], btn_sz[1], True, text=text, border_rad=10)
            self.btn_score.append(btn)
        else:
          for i, o in enumerate(self.scores):
            text = 'Level ' + str(i+1) + ': '+str(o)
            btn = Button((SCREEN_SIZE[0] - btn_sz[0])//2, (btn_sz[1]+20)*i+100, btn_sz[0], btn_sz[1], True, text=text, border_rad=10)
            self.btn_score.append(btn)
        self.btn_total_score = Button((SCREEN_SIZE[0] - btn_sz[0])//2, btn_sz[1]-30, btn_sz[0], btn_sz[1], True, text="Total: " + str(sum(self.scores)), border_rad=10)
        self.btn_play_again = Button(SCREEN_SIZE[0]//2 - btn_sz[0] - 10, 550, btn_sz[0], btn_sz[1], True, text="Play again", border_rad=10)
        self.btn_exit = Button(SCREEN_SIZE[0]//2 + 10, 550, btn_sz[0], btn_sz[1], True, text="Exit", border_rad=10)
        
        self.display_screen.fill((255,255,255))
        self.set_background()
        
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
      color="PINK"
      self.btn_play_again.draw(self.display_screen)
      self.btn_exit.draw(self.display_screen)
      self.btn_total_score.draw(self.display_screen,color)
      for i in range(len(self.btn_score)):
        self.btn_score[i].draw(self.display_screen,False,color)

    def buttons_handle(self, event):
        self.btn_play_again.handle_event(event)
        if self.btn_play_again.clicked():
            return "play again"
        self.btn_exit.handle_event(event)
        if self.btn_exit.clicked():
            return "quit"
        return "None"
      
    
    def run(self):
      while True:
        self.draw_buttons()
        ev = "None"
        for event in pygame.event.get():
          ev = self.buttons_handle(event)
          if event.type == pygame.QUIT:
            return "quit"
        if ev != "None": return ev
        pygame.display.flip()
      

        


