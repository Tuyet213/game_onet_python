import pygame
from button import Button

class Cell(Button):
  def __init__(self, x, y, w, h, r, c, val_path:int, val_pokemon:int, can_click:bool, image_path=""):
    self.val_path = val_path
    self.val_pokemon = val_pokemon
    self.can_click = can_click
    self.image_path = image_path
    self.r = r
    self.c = c
    super().__init__(x, y, w, h, self.can_click, self.image_path, border_rad = 10)
  
  def update_val_pokemon(self, new_val_pokemon, new_img):
    super().update_img(new_img)
    self.val_pokemon = new_val_pokemon
  
  def get_from(self, fr):
    #super().update_img(fr.image_path)
    self.update_val_pokemon(fr.val_pokemon, fr.image_path)
  
  def draw(self, screen):
    super().draw(screen, self.val_pokemon>0)

  def update_path_val(self, new_val_path, new_img):
    super().update_img(new_img)
    self.val_path = new_val_path
    