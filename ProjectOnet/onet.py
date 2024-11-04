import pygame
import random
import os
import time
from cell import Cell
from button import Button
from time_bar import TimeBar
from next_level import NextLevel


class PokemonGame:
    def __init__(self, N_POKEMON, N_ROW, N_COL, CELL_SIZE, time_limit):
        
        self.N_POKEMON = N_POKEMON
        self.N_ROW = N_ROW
        self.N_COL = N_COL
        WHITE = (255,255,255)
        BLACK = (0, 0, 0)

        if (N_ROW * N_COL) % 2 != 0:
          raise ValueError("Tích của N_ROW và N_COL phải chẵn!")

        pygame.init()
        self.WIN_WIDTH = 900
        self.WIN_HEIGHT = 650
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        pygame.display.set_caption("Onet pokemon")
        self.win.fill(WHITE)

        #Khởi gán các biến cho board
        self.cell = []
        self.scores = []
        

        #List chứa đường dẫn các hình ảnh
        self.img_pkm_path = []
        self.img_line_path = []
        self.folder_path = os.path.dirname(__file__)

        self.img_shuffle_path = os.path.join(self.folder_path, "images", "buttons", "shuffle_btn.jpg")
        self.img_hint_path = os.path.join(self.folder_path, "images", "buttons", "hint_btn.jpg")
        self.img_exit_path = os.path.join(self.folder_path, "images", "buttons", "exit_btn.jpg")
        self.img_pause_path = os.path.join(self.folder_path, "images", "buttons", "pause_btn.png")
        self.img_play_path = os.path.join(self.folder_path, "images", "buttons", "play_btn.png")
        self.img_sound_path = os.path.join(self.folder_path, "images", "buttons", "sound_btn.png")
        self.img_unsound_path = os.path.join(self.folder_path, "images", "buttons", "unsound_btn.png")

        #font 
        font_btn = pygame.font.Font(None, 15)
        
        #am thanh
        pygame.mixer.init()
        self.sound_click_cell = pygame.mixer.Sound(os.path.join(self.folder_path, "sounds", "cell_click.wav"))
        self.sound_conected = pygame.mixer.Sound(os.path.join(self.folder_path, "sounds", "connect.wav"))
        self.sound_level_up = pygame.mixer.Sound(os.path.join(self.folder_path, "sounds", "level_up.wav"))
        self.sound_winning = pygame.mixer.Sound(os.path.join(self.folder_path, "sounds", "winning_game.wav"))
        self.sound_gameover = pygame.mixer.Sound(os.path.join(self.folder_path, "sounds", "game_over.wav"))
        #Khai bao Buttons
        
        self.btn_shuffle = Button(0, 0, 50, 50, True, self.img_shuffle_path)
        self.btn_hint = Button(60, 0, 50, 50, True, self.img_hint_path)
        self.btn_exit = Button(120, 0, 50, 50, True, self.img_exit_path)
        self.btn_pause = Button(180, 0, 50, 50, True, self.img_pause_path)
        self.btn_sound = Button(240, 0, 50, 50, True, self.img_sound_path)

        self.done = 0
        self.current_cell = N_COL * N_ROW
        self.level = 0
        self.max_level = 12
        self.num_shuffle = 9
        self.num_hint = 2
        self.is_paused = False
        self.is_sound = True
        self.do_exit = False
        self.count_left_pkm = (self.N_COL*self.N_ROW)//2
        self.INT_MAX = 999999999
        self.UI_HEIGHT = 100
        self.time_bar = TimeBar((self.WIN_WIDTH-200)//2, (self.UI_HEIGHT-30)//2, 200, 10, WHITE, BLACK, 2, time.time(), time_limit, False)
        #self.scores=[0 for _ in range(self.max_level)]

        #Khai bao duong dan hinh anh

        for i in range(self.N_POKEMON):
          id = str(i+1)
          if i+1 < 10: id = "0" + id
          image_pokemon = "pokemon_" + id + ".jpg" 
          _img_path = os.path.join(self.folder_path, 'images', 'cell_pokemon', image_pokemon)
          self.img_pkm_path.append(_img_path)

        for i in range(6):
          img_p = "line_" + str(i) + ".jpg"
          _img_path = os.path.join(self.folder_path, 'images', 'cell_line', img_p)
          self.img_line_path.append(_img_path) 

        #Khởi tạo giá trị cho cell, gọi mỗi khi shuffle

        self.CELL_SIZE = CELL_SIZE
        self.LEFT_PADDING = (self.WIN_WIDTH - self.CELL_SIZE * (self.N_COL+2)) // 2
        self.TOP_PADDING = (self.WIN_HEIGHT - self.CELL_SIZE * (self.N_ROW+2)) // 2 + 50

        #Khai bao khac

        self.pos_lastest = (-1, -1) #để lưu cell cuối cùng được click vào
        self.delete_queue = [] #hàng đợi lưu thông tin các ô cần được xóa, (t, x, y). Với time là thời gian mà ô (x, y) được đẩy vào hàng đợi
                          #nếu thời gian hiện tại time.time() - t > 0.02 thì xóa ô đó
        self.delete_time_wait = 0.5 #thời gian đợi để xóa   

        #vecto huong
        self.V_UP = (-1, 0)
        self.V_DOWN = (1, 0)
        self.V_LEFT = (0, -1)
        self.V_RIGHT = (0, 1) 
 
    def initializate_board(self):

      id = [] #Lưu giá trị của các tuple tọa độ
      for i in range(1, self.N_ROW+1):
        for j in range(1, self.N_COL+1): id.append((i, j))

      #Khởi gán lại cho mảng cell
      self.cell =[[None for _ in range(self.N_COL+2)] for _ in range(self.N_ROW+2)]

      #Gán giá trị cell ảo
      for i in range(self.N_COL+2):
        self.cell[0][i] = Cell(self.LEFT_PADDING+i*self.CELL_SIZE, self.TOP_PADDING+0*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE, 0, i, 0, 0, False)
        self.cell[self.N_ROW+1][i] = Cell(self.LEFT_PADDING+i*self.CELL_SIZE, self.TOP_PADDING+(self.N_ROW+1)*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE, self.N_ROW+1, i, 0, 0, False)
      for i in range(self.N_ROW+2):
       self.cell[i][0] = Cell(self.LEFT_PADDING+0*self.CELL_SIZE, self.TOP_PADDING+i*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE, i, 0, 0, 0, False)
       self.cell[i][self.N_COL+1] = Cell(self.LEFT_PADDING+(self.N_COL+1)*self.CELL_SIZE, self.TOP_PADDING+i*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE, i, self.N_COL+1, 0, 0, False)

      #Gán giá trị các cell pokemon
      for _ in range((self.N_COL*self.N_ROW)//2):
        val = random.randint(1, self.N_POKEMON)
        t1 = random.choice(id) 
        id.remove(t1)
        t2 = random.choice(id)
        id.remove(t2)
        self.cell[t1[0]][t1[1]] = Cell(self.LEFT_PADDING+t1[1]*self.CELL_SIZE, self.TOP_PADDING+t1[0]*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE, t1[0], t1[1], 0, val, True, image_path=self.img_pkm_path[val-1])
        self.cell[t2[0]][t2[1]] = Cell(self.LEFT_PADDING+t2[1]*self.CELL_SIZE, self.TOP_PADDING+t2[0]*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE, t2[0], t2[1], 0, val, True, image_path=self.img_pkm_path[val-1])

    def handle_buttons(self, event):
      
      self.btn_exit.handle_event(event)
      if self.btn_exit.clicked(): 
        self.do_exit = True
        return
      
      for i in range(self.N_ROW+2):
        for j in range(self.N_COL+2):
          if self.cell[i][j].can_click:
            self.cell[i][j].handle_event(event)
            if self.cell[i][j].clicked(): #trong board, chỉ có 1 cell được click mỗi lần lặp
              if self.is_sound:
                self.sound_click_cell.play()
              self.cell[i][j].set_chosen(True)
              if self.pos_lastest != (-1, -1): #có một cell đã được click
                x, y = self.pos_lastest[0], self.pos_lastest[1]
                if (x, y) != (i, j): #ko trùng vs cell cũ thì kiểm tra có nối đươc
                  if self.can_connect(self.cell[i][j], self.cell[x][y], True):
                    self.cell[x][y].set_can_click(False)
                    self.cell[i][j].set_can_click(False)
                    self.delete_queue.append((time.time(), self.cell[x][y],  self.cell[i][j]))
                    self.count_left_pkm = self.count_left_pkm - 1
                    self.scores[self.level] += 10
                    self.pos_lastest = (-1, -1)
                  else:
                    self.cell[x][y].set_chosen(False)
                    self.pos_lastest = (i, j)
              else: 
                self.pos_lastest = (i, j)
            
      if self.btn_shuffle.can_click: self.btn_shuffle.handle_event(event)
      if self.btn_shuffle.clicked():
        self.shuffle_board()
        self.num_shuffle = self.num_shuffle - 1
        
      if self.btn_hint.can_click: self.btn_hint.handle_event(event)
      if self.btn_hint.clicked():
        self.hint()
        self.num_hint = self.num_hint - 1
        
      self.btn_pause.handle_event(event)
      if self.btn_pause.clicked():
        self.is_paused = not self.is_paused
        self.btn_shuffle.set_can_click(not self.btn_shuffle.can_click)
        self.btn_hint.set_can_click(not self.btn_hint.can_click)
        self.pause()
        if self.is_paused:
          self.btn_pause.update_img(self.img_play_path)
          self.time_bar.set_start_pause_time(time.time())
          self.time_bar.set_is_paused(True)
        else:
          self.btn_pause.update_img(self.img_pause_path)
          self.time_bar.set_is_paused(False)
        
      self.btn_sound.handle_event(event)
      if self.btn_sound.clicked():
        self.is_sound = not self.is_sound
        if self.is_sound:
          self.btn_sound.update_img(self.img_sound_path)
        else:
          self.btn_sound.update_img(self.img_unsound_path)

    def delete_cell(self):
      while len(self.delete_queue) > 0:
        t = self.delete_queue[0]
        if(time.time() - t[0] > self.delete_time_wait):
          if len(t) == 3:#pokemon
            self.change_state(self.level, t[1], t[2])
          else:#path
            t[1].delete() 
          self.delete_queue.pop(0)
        else:
          return
        
    def inside(self, x:int, y:int):
      if x >= 0 and y >= 0 and x < self.N_ROW + 2 and y < self.N_COL + 2:
        return True
      return False

    def get_path_value(self, v1:tuple, v2:tuple):
      if v1 == v2: #cùng hướng
        if v1[0] == 0: #x = 0 => vector (0, +-1), phải trái
          return 0
        else:          #y = 0 => vector (+-1, 0), trên dưới
          return 1
      else:
        if (v1 == self.V_UP and v2 == self.V_LEFT) or (v1 == self.V_RIGHT and v2 == self.V_DOWN): return 5
        elif (v1 == self.V_DOWN and v2 == self.V_LEFT) or (v1 == self.V_RIGHT and v2 == self.V_UP): return 3
        elif (v1 == self.V_LEFT and v2 == self.V_UP) or (v1 == self.V_DOWN and v2 == self.V_RIGHT): return 2
        elif (v1 == self.V_LEFT and v2 == self.V_DOWN) or (v1 == self.V_UP and v2 == self.V_RIGHT): return 4

    #flag = True: xử lí và hiển thị đường đi
    def has_path(self, a:Cell, b:Cell, flag): #flag true: kiểm tra có đường đi không và truy evets thêm ảnh=>xóa. flag false chỉ kiểm tra có đường đi hay không
      f = [[[self.INT_MAX] * 4 for _ in range(self.N_COL + 2)] for _ in range(self.N_ROW + 2)]
      trace = [[[(-1, -1, -1)] * 4 for _ in range(self.N_COL + 2)] for _ in range(self.N_ROW + 2)]
      queue = []
      d = [(1, 0), (0, 1), (-1, 0), (0, -1)]
      
      x_start, y_start, x_end, y_end = a.r, a.c, b.r, b.c
      
      for dir in range(4):
        f[x_start][y_start][dir] = 1
        queue.append((x_start, y_start, dir))

      while len(queue) > 0:
        t = queue[0]
        queue.pop(0)
        if (t[0], t[1]) == (x_end, y_end) and 1 <= f[t[0]][t[1]][t[2]] <= 3: break
        for dir, t1 in enumerate(d):
          x = t[0] + t1[0]
          y = t[1] + t1[1]
          if self.inside(x, y) and (self.cell[x][y].val_pokemon == 0 or (x, y) == (x_end, y_end)): 
            if dir != t[2] and f[x][y][dir] > f[t[0]][t[1]][t[2]] + 1:
              f[x][y][dir] = f[t[0]][t[1]][t[2]] + 1
              queue.append((x, y, dir))
              trace[x][y][dir] = (t[0], t[1], t[2])
            if dir == t[2] and f[x][y][dir] > f[t[0]][t[1]][t[2]]:
              f[x][y][dir] = f[t[0]][t[1]][t[2]]
              queue.insert(0, (x, y, dir))
              trace[x][y][dir] = (t[0], t[1], t[2]) 

      for dir in range(4):
        if 1 <= f[x_end][y_end][dir] <= 3:
          if flag == True:
            x, y, d = x_end, y_end, dir
            while True:
              t0 = (x, y, d)                    
              t1 = trace[x][y][d]             #tuple cell sẽ thêm ảnh
              t2 = trace[t1[0]][t1[1]][t1[2]]

              if (t1[0], t1[1]) == (x_start, y_start): 
                return True

              v1 = (t1[0]-t0[0], t1[1]-t0[1]) #vector 1
              v2 = (t2[0]-t1[0], t2[1]-t1[1]) #vector 2
              val = self.get_path_value(v1, v2)
              self.cell[t1[0]][t1[1]].update_path_val(val, self.img_line_path[val])
              self.delete_queue.append((time.time(), self.cell[t1[0]][t1[1]]))
              x, y, d = t1[0], t1[1], t1[2]

          return True
        
      return False 

    def can_connect(self, a:Cell, b:Cell, flag): #kiểm tra 2 cell có kết nối được hay không
      if a != b and a.val_pokemon != 0 and a.val_pokemon == b.val_pokemon and self.has_path(a, b, flag): return True
      return False

    def check_connectable_cells(self):
      no_cell_left = True
      for x1 in range(1, self.N_ROW+1):
        for y1 in range(1, self.N_COL+1):
          if self.cell[x1][y1].val_pokemon!=0: 
            no_cell_left = False
            for x2 in range(1, self.N_ROW+1):
              for y2 in range(1, self.N_COL+1):
                if self.can_connect(self.cell[x1][y1], self.cell[x2][y2], False):
                  return True
      if no_cell_left == True: return True
      return False 

    def draw_cell(self):
      for i in range(self.N_ROW+2):
        for j in range(self.N_COL+2):
          self.cell[i][j].draw(self.win)

    def draw_buttons(self):
      self.btn_shuffle.draw(self.win)
      self.btn_hint.draw(self.win)
      self.btn_pause.draw(self.win)
      self.btn_exit.draw(self.win)
      self.btn_sound.draw(self.win)

    def shuffle_board(self):
      val_pkm_arr=[]
      for i in range(1, self.N_ROW + 1):
        for j in range(1, self.N_COL + 1):
          if self.cell[i][j].val_pokemon != 0:
            val_pkm_arr.append(self.cell[i][j].val_pokemon)
      while len(val_pkm_arr) > 0:
        for i in range(1, self.N_ROW + 1):
          for j in range(1, self.N_COL + 1):
            if self.cell[i][j].val_pokemon != 0:
              new_val_pkm = random.choice(val_pkm_arr)
              self.cell[i][j].update_val_pokemon(new_val_pkm, self.img_pkm_path[new_val_pkm-1])
              val_pkm_arr.remove(new_val_pkm)

    def hint(self):
      for x1 in range(1, self.N_ROW+1):
        for y1 in range(1, self.N_COL+1):
          for x2 in range(1, self.N_ROW+1):
            for y2 in range(1, self.N_COL+1):
              if self.can_connect(self.cell[x1][y1], self.cell[x2][y2], False):
                self.cell[x1][y1].set_current_alpha(100)
                self.cell[x2][y2].set_current_alpha(100)
                return

    def pause(self):
      for x in range(1, self.N_ROW+1):
        for y in range(1, self.N_COL+1):
          self.cell[x][y].set_visible(not self.is_paused)
          self.cell[x][y].set_can_click(not self.is_paused)
    
   
    def draw_score(self, surface):
      font = pygame.font.Font(None, 36)
      number_text = font.render(str(sum(self.scores)), True, (0, 0, 0))  
      text_rect = number_text.get_rect(center=(600, 50))  
      pygame.draw.rect(surface, (255, 255, 255), text_rect) 
      surface.blit(number_text, text_rect.topleft) 
      
    def draw_hint(self, surface):
      font = pygame.font.Font(None, 36)
      number_text = font.render(str(self.num_hint), True, (0, 0, 0))  
      text_rect = number_text.get_rect(center=(80, 70))  
      pygame.draw.rect(surface, (255, 255, 255), text_rect) 
      surface.blit(number_text, text_rect.topleft) 
      
    def draw_shuffle(self, surface):
      font = pygame.font.Font(None, 36)
      number_text = font.render(str(self.num_shuffle), True, (0, 0, 0))  
      text_rect = number_text.get_rect(center=(20, 70))  
      pygame.draw.rect(surface, (255, 255, 255), text_rect) 
      surface.blit(number_text, text_rect.topleft) 
   
    def draw_level(self, surface):
      font = pygame.font.Font(None, 36)
      number_text = font.render("Level "+str(self.level+1), True, (0, 0, 0))  
      text_rect = number_text.get_rect(center=(800, 50))  
      pygame.draw.rect(surface, (255, 255, 255), text_rect) 
      surface.blit(number_text, text_rect.topleft) 
   
    def initializate_all(self):
      self.current_cell = self.N_COL * self.N_ROW
      self.win.fill((255,255,255))
      self.initializate_board()
      self.draw_cell()
      self.draw_buttons()
      self.time_bar.start_time = time.time()
      self.time_bar.draw(self.win)
      #pygame.draw.line(self.win, (0, 0, 0), (0, 100), (self.WIN_WIDTH, 100), 1)

    def run(self):
      
        while self.level <= self.max_level:
          self.initializate_all()
          if len(self.scores) <= self.level:
            self.scores.append(0)
          while True:
              
              for event in pygame.event.get():
                  self.handle_buttons(event)
                  if event.type == pygame.QUIT or self.do_exit:
                    return "quit"
              
              if self.current_cell == 0:
                self.scores[self.level] += round((self.time_bar.time_limit - self.time_bar.cur_time + self.time_bar.start_time)) * 2      
                
                if self.level == self.max_level:
                  self.level += 1
                  break
                
                next_lv = NextLevel((self.WIN_WIDTH, self.WIN_HEIGHT), sum(self.scores))
                
                if self.is_sound:
                  self.sound_level_up.play()
                  
                op = next_lv.run()
                
                if op == "next level": self.level += 1
                elif op == "exit": self.do_exit = True
                else: self.scores[self.level] = 0
                
                break

              self.draw_buttons()
              self.delete_cell()
              self.draw_score(self.win)
              self.draw_hint(self.win)
              self.draw_shuffle(self.win)
              self.time_bar.draw(self.win)
              self.draw_level(self.win)
              self.is_shuffle = False
              self.draw_cell()

              while not self.check_connectable_cells() and self.num_shuffle >= 0:
                  self.shuffle_board()
                  self.is_shuffle = True
                  self.num_shuffle -= 1
                  self.draw_cell()
              
              if self.num_shuffle < 0 or self.time_bar.is_over: 
                return ("lose", sum(self.scores))
              if self.num_hint == 0: self.btn_hint.can_click=False
              if self.num_shuffle == 0: self.btn_shuffle.can_click=False
              pygame.display.flip()
          
          
          #self.scores.append(self.score)
          
        if self.is_sound:
          self.sound_winning.play()
        return ("win", sum(self.scores))

    def fall_down1(self, c1:Cell, c2:Cell, flag=True):
      if c1.r < c2.r or c1.c != c2.c:
        self.fall_down(c1, flag)
        self.fall_down(c2, flag)  
      else: 
        self.fall_down(c2, flag)
        self.fall_down(c1, flag)

    def fall_up1(self, c1:Cell, c2:Cell, flag=True):
      if c1.r > c2.r or c1.c != c2.c:
        self.fall_up(c1, flag)
        self.fall_up(c2, flag)
      else :
        self.fall_up(c2, flag)
        self.fall_up(c1, flag)

    def fall_left1(self, c1:Cell, c2:Cell, flag=True):
      if c1.c > c2.c or c1.r != c2.r:
        self.fall_left(c1, flag)
        self.fall_left(c2, flag)
      else:
        self.fall_left(c2, flag)
        self.fall_left(c1, flag)

    def fall_right1(self, c1:Cell, c2:Cell, flag=True):
      if c1.c < c2.c or c1.r != c2.r:
        self.fall_right(c1, flag)
        self.fall_right(c2, flag)
      else :
        self.fall_right(c2, flag)
        self.fall_right(c1, flag)

    def fall_left_up1(self, c1:Cell, c2:Cell):
      if c1.r<c2.r and c1.c<c2.c and self.check_main_diagonal(c1,c2):
        self.fall_left_up(c2)
        self.fall_left_up(c1)
      else:
        self.fall_left_up(c1)
        self.fall_left_up(c2)
    
    def fall_left_down1(self, c1:Cell, c2:Cell):
      if c1.r>c2.r and c1.c<c2.c and self.check_off_diagonal(c1,c2):
        self.fall_left_down(c2)
        self.fall_left_down(c1)
      else:
        self.fall_left_down(c1)
        self.fall_left_down(c2)
        
    def fall_right_up1(self, c1:Cell, c2:Cell):
      if c1.r>c2.r and c1.c<c2.c and self.check_off_diagonal(c1,c2):
        self.fall_right_up(c1)
        self.fall_right_up(c2)
      else:
        self.fall_right_up(c2)
        self.fall_right_up(c1)
        
    def fall_right_down1(self, c1:Cell, c2:Cell):
      if c1.r<c2.r and c1.c<c2.c and self.check_main_diagonal(c1,c2):
        self.fall_right_down(c1)
        self.fall_right_down(c2)
      else:
        self.fall_right_down(c2)
        self.fall_right_down(c1)

    def fall_down(self, c:Cell, flag=True):
        i = c.r - 1
        limit = 0 if flag else self.N_ROW//2
        while self.cell[i][c.c].val_pokemon != 0 and i > limit:
          self.cell[i+1][c.c].get_from(self.cell[i][c.c])
          i -= 1
        self.cell[i+1][c.c].delete()

    def fall_up(self, c:Cell, flag=True):
      i = c.r + 1
      limit = self.N_ROW if flag else self.N_ROW//2
      while self.cell[i][c.c].val_pokemon != 0 and i <= limit:
        self.cell[i-1][c.c].get_from(self.cell[i][c.c])
        i += 1
      self.cell[i-1][c.c].delete()

    def fall_left(self, c:Cell, flag=True):
      j = c.c + 1
      limit = self.N_COL if flag else self.N_COL//2
      
      while self.cell[c.r][j].val_pokemon != 0 and j <= limit:
        self.cell[c.r][j-1].get_from(self.cell[c.r][j])
        j += 1
      self.cell[c.r][j-1].delete()

    def fall_right(self, c:Cell, flag=True):
      j = c.c - 1
      limit = 0 if flag else self.N_COL//2
      while self.cell[c.r][j].val_pokemon != 0 and j > limit:
        self.cell[c.r][j+1].get_from(self.cell[c.r][j])
        j -= 1
      self.cell[c.r][j+1].delete()
    
    def fall_left_up(self, c:Cell):
      i = c.r + 1
      j = c.c + 1
      while self.cell[i][j].val_pokemon != 0 and i <= self.N_ROW and j<= self.N_COL:
        self.cell[i-1][j-1].get_from(self.cell[i][j])
        i += 1
        j += 1
      self.cell[i-1][j-1].delete()
      
    def fall_left_down(self, c:Cell):
      i = c.r - 1
      j = c.c + 1
      while self.cell[i][j].val_pokemon != 0 and i >= 1 and j<= self.N_COL:
        self.cell[i+1][j-1].get_from(self.cell[i][j])
        i -= 1
        j += 1
      self.cell[i+1][j-1].delete()
      
    def fall_right_up(self, c:Cell):
      i = c.r + 1
      j = c.c - 1
      while self.cell[i][j].val_pokemon != 0 and i <= self.N_ROW and j>= 1:
        self.cell[i-1][j+1].get_from(self.cell[i][j])
        i += 1
        j -= 1
      self.cell[i-1][j+1].delete()
      
    def fall_right_down(self, c:Cell):
      i = c.r - 1
      j = c.c - 1
      while self.cell[i][j].val_pokemon != 0 and i >= 1 and j >= 1:
        self.cell[i+1][j+1].get_from(self.cell[i][j])
        i -= 1
        j -= 1
      self.cell[i+1][j+1].delete()
    
    def check_main_diagonal(self, c1:Cell, c2:Cell):
      i=c1.r
      j=c1.c
      while i<c2.r and j<c2.c:
        i += 1
        j += 1
        if i==c2.r and j==c2.c: return True
      return False
    
    def check_off_diagonal(self, c1:Cell, c2:Cell):
      i=c1.r
      j=c1.c
      while i>c2.r and j<c2.c:
        i -= 1
        j += 1
        if i==c2.r and j==c2.c: return True
      return False
    
    def change_state(self, level:int, c1:Cell, c2:Cell):
      
      if level == 0:
        c1.delete()
        c2.delete()

      elif level == 1: #rot xuong
        self.fall_down1(c1, c2)

      elif level == 2: #rot len
        self.fall_up1(c1, c2)

      elif level == 3: #rot trai
        self.fall_left1(c1, c2)

      elif level == 4: #rot phai
        self.fall_right1(c1, c2)

      elif level == 5: #rot vo giua theo chieu ngang
        if 2*c1.r <= self.N_ROW and 2*c2.r <= self.N_ROW:
          self.fall_down1(c1, c2)
        elif 2*c1.r > self.N_ROW and 2*c2.r > self.N_ROW:
          self.fall_up1(c1, c2)
        else:
          if c1.r < c2.r:
            self.fall_down(c1)
            self.fall_up(c2)
          else:
            self.fall_up(c1)
            self.fall_down(c2)
      
      elif level == 6: #rot vo giua theo chieu doc
        if 2*c1.c <= self.N_COL and 2*c2.c <= self.N_COL:
          self.fall_right1(c1, c2)
        elif 2*c1.c > self.N_COL and 2*c2.c > self.N_COL:
          self.fall_left1(c1, c2)
        else:
          if c1.c < c2.c:
            self.fall_right(c1)
            self.fall_left(c2)
          else:
            self.fall_left(c1)
            self.fall_right(c2)
        
      elif level == 7: #rot sang 2 ben theo chieu doc
        if 2*c1.c <= self.N_COL and 2*c2.c <= self.N_COL:
          self.fall_left1(c1, c2, False)
        elif 2*c1.c > self.N_COL and 2*c2.c > self.N_COL:
          self.fall_right1(c1, c2, False)
        else:
          if c1.c < c2.c:
            self.fall_left(c1, False)
            self.fall_right(c2, False)
          else:
            self.fall_right(c1, False)
            self.fall_left(c2, False)

      elif level == 8: #rot 2 ben theo chieu ngang
        if 2*c1.r <= self.N_ROW and 2*c2.r <= self.N_ROW:
          self.fall_up1(c1, c2, False)
        elif 2*c1.r > self.N_ROW and 2*c2.r > self.N_ROW:
          self.fall_down1(c1, c2, False)
        else:
          if c1.r < c2.r:
            self.fall_up(c1, False)
            self.fall_down(c2, False)
          else:
            self.fall_down(c1, False)
            self.fall_up(c2, False)
      
      elif level == 9:
        self.fall_left_up1(c1, c2)
      
      elif level == 10:
        self.fall_left_down1(c1, c2)
        
      elif level == 11:
        self.fall_right_up1(c1, c2)
        
      elif level == 12:
        self.fall_right_down1(c1, c2)
      
      if c2.val_pokemon:
        c2.set_chosen(False)
        c2.set_can_click(True)
        c2.unclick()
      if c1.val_pokemon:  
        c1.set_chosen(False)
        c1.set_can_click(True)
        c1.unclick()

      self.current_cell -= 2
      if self.is_sound:
        self.sound_conected.play()

