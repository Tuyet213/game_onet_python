import pygame
import time

class TimeBar:
    def __init__(self, x, y, width, height, color, border_color, border_width, start_time, time_limit, is_paused):
        self.start_time = start_time
        self.pause_time = 0.0
        self.start_pause_time = 0.0
        self.time_limit = time_limit
        self.is_paused = is_paused
        self.rect = pygame.Rect(x+border_width, y+border_width, width-border_width*2, height-border_width*2)
        self.rect_border = pygame.Rect(x, y, width, height)
        self.rect_counter = pygame.Rect(x+width-border_width, y+border_width, 0, height-border_width*2)
        self.color = color
        self.border_color = border_color #black
        self.border_width = border_width
        self.width = width
        self.height = height
        self.is_over = False
        

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.rect_border)
        pygame.draw.rect(surface, self.color, self.rect)
        self.update_rect_counter(time.time())
        pygame.draw.rect(surface, self.border_color, self.rect_counter)
    
    def set_start_pause_time(self, time):
        self.start_pause_time = time
    
    def set_is_paused(self, status):
        self.is_paused = status
    
    def update_rect_counter(self, cur_time):
        if self.is_paused:
            self.pause_time = cur_time - self.start_pause_time
            cur_time -= self.pause_time
        else:
            self.start_time += self.pause_time
            self.pause_time = 0             
        if cur_time - self.start_time > self.time_limit: 
            self.is_over = True
            return 
        new_w = (int)((self.width-self.border_width) * (cur_time-self.start_time) / self.time_limit)
        self.rect_counter.x = self.rect_counter.x + self.rect_counter.width - new_w
        self.rect_counter.width = new_w
        self.cur_time = cur_time
        
        
# def main():
#     pygame.init()

#     width, height = 400, 300
#     screen = pygame.display.set_mode((width, height))
#     pygame.display.set_caption("Hình chữ nhật có viền đen")
#     white = (255, 255, 255)
#     black = (0, 0, 0)
#     screen.fill(white)
#     rect_width, rect_height = 200, 100
#     rect_x, rect_y = (width - rect_width) // 2, (height - rect_height) // 2

#     Tạo đối tượng hình chữ nhật
#     my_rectangle = TimeBar(rect_x, rect_y, rect_width, rect_height, white, black, 2, time.time(), 60.0)

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         Vẽ hình chữ nhật
#         my_rectangle.draw(screen)

#         pygame.display.flip()

# if __name__ == "__main__":
#     main()
