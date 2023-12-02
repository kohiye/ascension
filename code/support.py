import pygame
from os import walk


def import_dir(path):
    surf_list = []

    for folder, subfolder, img_files in walk(path):
        for image_name in img_files:
            full_path = path + "/" + image_name
            image_surf = pygame.image.load(full_path).convert_alpha()
            surf_list.append(image_surf)
    return surf_list


def import_dir_dict(path):
    surf_dict = {}

    for folder, subfolder, img_files in walk(path):
        for image_name in img_files:
            full_path = path + "/" + image_name
            image_surf = pygame.image.load(full_path).convert_alpha()
            surf_dict[image_name.split(".")[0]] = image_surf
    return surf_dict


def signum(number):
    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return 0
