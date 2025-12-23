# Главный файл запуска тетриса

import pygame
import sys
from src.game_logic import Game

# Инициализация pygame
pygame.init()

# Создание окна
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Тетрис")

# Часы для ограничения FPS
clock = pygame.time.Clock()

# Создание и запуск игры
game = Game()
game.run(screen, clock)

# Корректный выход из pygame
pygame.quit()
sys.exit()
