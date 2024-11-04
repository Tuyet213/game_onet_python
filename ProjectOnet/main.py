import sys
from onet import PokemonGame
from menu import Menu
import pygame
from end import End
from score_tk import ScoreTK

WIDTH = 900
HEIGHT = 650

def main():
  pygame.init()

  row = 0
  col = 0
  num_poke = 0
  cell_size = 0
  time_limit = 0

  while True:
    my_menu = Menu((WIDTH, HEIGHT))
    my_menu.draw_buttons()
    dif_val = -1
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        dif_val = my_menu.get_val(event)

      if dif_val != -1:
        if dif_val == 0:
          row, col, num_poke, cell_size, time_limit =4, 4, 15, 60, 120
        elif dif_val == 1:
          row, col, num_poke, cell_size, time_limit = 8, 12, 20, 55, 300
        else:
          row, col, num_poke, cell_size, time_limit = 10, 16, 30, 45, 420
        break
      
      my_menu.draw_buttons()
      pygame.display.flip()

    game = PokemonGame(num_poke, row, col, cell_size, time_limit)
    status = game.run()
    if status == "quit": 
      pygame.quit()
      sys.exit()
    ending_screen = End((WIDTH, HEIGHT), status[0], status[1])
    while True:
        flag = False
        ending_screen.draw_buttons()
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
          option = ending_screen.buttons_handle(event)
          if option == "quit":
            pygame.quit()
            sys.exit()
          if option == "play again":
            flag = True
            break
          if option == "show score":
            score_tk = ScoreTK((WIDTH, HEIGHT), game.scores)
            sta = score_tk.run()
            if sta == "quit":
              pygame.quit()
              sys.exit()
            if sta == "play again":
              flag = True
              break
        if flag:
          break
        pygame.display.flip()
    
if __name__ == "__main__":
    main()
