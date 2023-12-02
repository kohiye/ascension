import pygame
import settings as s
from pygame.image import load

class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_data()
        self.create_buttons()
        
    def create_data(self):
        self.menu_surfs = {}
        for key, value in s.CANVAS_TEMPLATES.items():
            if value["menu"]:
                if not value["menu"] in self.menu_surfs:
                    self.menu_surfs[value["menu"]] = [(key,load(value["preview"]))]
                else:
                    self.menu_surfs[value["menu"]].append((key,load(value["preview"])))

    def create_buttons(self):

        # menu area
        size = 180
        margin = 6
        topleft = (s.WINDOW_WIDTH - size - margin, s.WINDOW_HEIGTH - size - margin )
        self.rect = pygame.Rect(topleft,(size,size))
        
        #button areas
        generic_button_rect = pygame.Rect(self.rect.topleft, (self.rect.width / 2, self.rect.height / 2))
        button_margin = 5
        self.tile_button_rect = generic_button_rect.copy().inflate(-button_margin,-button_margin)
        self.coin_button_rect = generic_button_rect.move(self.rect.height / 2,0).inflate(-button_margin, -button_margin)
        self.enemy_button_rect = generic_button_rect.move(self.rect.height / 2,self.rect.width / 2).inflate(-button_margin,-button_margin)
        self.chair_button_rect = generic_button_rect.move(0,self.rect.width / 2).inflate(-button_margin, -button_margin)
        
        #create the buttons
        self.buttons = pygame.sprite.Group()
        Button(self.tile_button_rect, self.buttons, self.menu_surfs["wall"])
        Button(self.coin_button_rect, self.buttons, self.menu_surfs["coin"])
        Button(self.enemy_button_rect, self.buttons, self.menu_surfs["enemy"])
        Button(self.chair_button_rect, self.buttons, self.menu_surfs["chair fg"], self.menu_surfs["chair bg"])

    def click(self, mouse_pos, mouse_button):
        for sprite in self.buttons:
            if sprite.rect.collidepoint(mouse_pos):
                if mouse_button[1]:
                    if sprite.items["alt"]:
                        sprite.main_active = not sprite.main_active
                if mouse_button[2]:
                    sprite.switch()
                return sprite.get_id()
            
    def highlight_indicator(self, index):
        if s.CANVAS_TEMPLATES[index]["menu"] == "wall":
            pygame.draw.rect(self.display_surface, "#000080", self.tile_button_rect.inflate(4,4),5,4)
        if s.CANVAS_TEMPLATES[index]["menu"] == "coin":
            pygame.draw.rect(self.display_surface, "#000080", self.coin_button_rect.inflate(4,4),5,4)
        if s.CANVAS_TEMPLATES[index]['menu'] == "enemy":
            pygame.draw.rect(self.display_surface, "#000080", self.enemy_button_rect.inflate(4,4),5,4)
        if s.CANVAS_TEMPLATES[index]["menu"] in ("chair bg", "chair fg"):
            pygame.draw.rect(self.display_surface, "#000080", self.chair_button_rect.inflate(4,4),5,4)

    def display(self, index):
        self.buttons.update()
        self.buttons.draw(self.display_surface)
        self.highlight_indicator(index)

class Button(pygame.sprite.Sprite):
    def __init__(self, rect, group, items, items_alt = None):
        super().__init__(group)
        self.image = pygame.Surface(rect.size)
        self.rect = rect

        #items
        self.items = {"main": items, "alt": items_alt}
        self.id = 0
        self.main_active = True

    def get_id(self):
        return self.items["main" if self.main_active else "alt"][self.id][0]
    
    def switch(self):
        self.id += 1
        self.id = 0 if self.id >= len(self.items["main" if self.main_active else "alt"]) else self.id

    def update(self):
        self.image.fill("#0000ff")
        surf = self.items["main" if self.main_active else "alt"][self.id][1]
        rect = surf.get_rect(center = (self.rect.width / 2, self.rect.height / 2))
        self.image.blit(surf, rect)