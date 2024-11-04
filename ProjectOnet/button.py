import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (248, 131, 121)

class Button:
    def __init__(self, x, y, w, h, can_click, image_path="", text="", border_rad:int=0, visible:bool=True):
        self.w = w
        self.h = h
        self.x = x 
        self.y = y
        self.rect = pygame.Rect(x, y, w, h)
        self.is_hovered = False
        self.is_clicked = False
        self.text = text
        self.clicked_once = False
        self.border_rad = border_rad
        self.can_click = can_click
        self.image_path = image_path
        self.alpha_default = 255
        self.current_alpha = self.alpha_default
        self.alpha_hover = 150
        self.alpha_click = 100
        self.font = pygame.font.Font(None, 36)
        self.is_chosen = False #Dùng để xác định cell có được chọn hay không (chỉ được gọi khi button là cell)
        self.visible = visible
        if self.image_path != "":
            self.image = pygame.image.load(self.image_path)
            self.image.set_alpha(self.alpha_default)
            self.image = pygame.transform.scale(self.image, (w, h))
        if self.text != "":
            self.color_text = (0, 0, 0)
            self.text_render = self.font.render(self.text, True, self.color_text)

    def delete(self):
        self.image_path = ""
        self.val_pokemon = 0
        self.val_path = 0
        self.is_chosen = False
        self.current_alpha = self.alpha_default
        self.can_click = False

    def set_current_alpha(self, new_current_alpha):
        self.current_alpha = new_current_alpha
    
    def set_visible(self, status):
        self.visible = status

    def set_can_click(self, status:bool):
        self.can_click = status

    def set_chosen(self, status:bool):
        self.is_chosen = status

    def update_img(self, new_img):
        self.image_path = new_img
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))

    def draw(self, screen, is_poke=False, color=WHITE):
        # if not is_poke:
        #     pygame.draw.rect(screen, WHITE, self.rect, border_radius=self.border_rad)
        # else:
        #     pygame.draw.rect(screen, WHITE, self.rect, border_radius=10)
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_rad)
        if self.visible:
            if self.image_path != "":
                if self.is_chosen: self.image.set_alpha(self.alpha_click)
                else: self.image.set_alpha(self.current_alpha)
                screen.blit(self.image, self.rect)
            if self.text != "":
                text_width, text_height = self.text_render.get_size()
                x = self.rect.x + (self.rect.width - text_width) // 2
                y = self.rect.y + (self.rect.height - text_height) // 2
                screen.blit(self.text_render, (x, y))
                
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.handle_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.handle_release(event.pos)

    def handle_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
            self.current_alpha = self.alpha_hover
        else:
            self.is_hovered = False
            self.current_alpha = self.alpha_default

    def unclick(self):
        self.is_clicked = False
        self.clicked_once = False
        self.current_alpha = self.alpha_default

    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.is_clicked == False:
                self.is_clicked = True
                self.current_alpha = self.alpha_click

    def handle_release(self, mouse_pos):
        self.is_clicked = False
        self.is_hovered = False
        self.handle_hover(mouse_pos)
        self.clicked_once = False

    def clicked(self):
        if not self.is_clicked: return False
        if self.clicked_once: return False
        else:
            self.clicked_once = True
            return True
