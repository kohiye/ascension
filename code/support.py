import pygame
from os import walk


def import_dir(path):
    surface_list = []

    for folder, subfolder, img_files in walk(path):
        for image_name in img_files:
            full_path = path + "/" + image_name
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list
