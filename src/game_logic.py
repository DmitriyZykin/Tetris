# Основная логика игры тетрис

import pygame
from src.pieces import get_random_piece, rotate_piece, COLORS
from src.board import Board


class Game:
    """Класс для управления игрой Тетрис."""
    
    def __init__(self):
        """Инициализация игры."""
        # Константы
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.FPS = 60
        self.BACKGROUND_COLOR = (20, 20, 50)  # Темно-синий цвет для тетриса
        
        # Параметры игрового поля
        self.BOARD_WIDTH = 10  # Колонок
        self.BOARD_HEIGHT = 20  # Строк
        
        # Расчет размера клетки так, чтобы поле занимало 2/3 экрана по ширине
        available_width = (self.WINDOW_WIDTH * 2) // 3
        self.CELL_SIZE = available_width // self.BOARD_WIDTH
        
        # Проверяем, что высота тоже помещается (с небольшим отступом сверху и снизу)
        available_height = self.WINDOW_HEIGHT - 40  # Отступы сверху и снизу по 20px
        max_cell_size_by_height = available_height // self.BOARD_HEIGHT
        if self.CELL_SIZE > max_cell_size_by_height:
            self.CELL_SIZE = max_cell_size_by_height
        
        # Создание игрового поля
        self.board = Board(self.BOARD_WIDTH, self.BOARD_HEIGHT, self.CELL_SIZE)
        
        # Позиция поля на экране (ближе к центру, с местом справа для информации)
        self.INFO_PANEL_WIDTH = 250  # Место справа для панели информации
        self.board_offset_x = (self.WINDOW_WIDTH - self.board.pixel_width - self.INFO_PANEL_WIDTH) // 2
        self.board_offset_y = 20  # Небольшой отступ сверху
        
        # Создание словаря цветов по индексам (для сохранения на поле)
        self.color_index_map = {i + 1: list(COLORS.values())[i] for i in range(len(COLORS))}
        
        # Игровые переменные
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        
        # Таймер для падения фигуры
        self.fall_time = 0
        self.fall_speed = 500  # Миллисекунды между падениями
        
        # Шрифты
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Инициализация фигур (сначала создаем следующую фигуру)
        self.next_shape_name, self.next_shape_matrix, self.next_color = get_random_piece()
        self.next_color_index = list(COLORS.keys()).index(self.next_shape_name) + 1
        
        # Затем создаем текущую фигуру
        self._spawn_new_piece()
    
    def _spawn_new_piece(self):
        """Создает новую фигуру из очереди следующей фигуры."""
        # Текущая фигура становится следующей
        self.current_shape_name = self.next_shape_name
        self.current_shape_matrix = [row[:] for row in self.next_shape_matrix]  # Копия
        self.current_color = self.next_color
        self.current_color_index = self.next_color_index
        
        # Генерируем новую следующую фигуру
        self.next_shape_name, self.next_shape_matrix, self.next_color = get_random_piece()
        self.next_color_index = list(COLORS.keys()).index(self.next_shape_name) + 1
        
        # Устанавливаем позицию новой фигуры
        self.piece_x = self.BOARD_WIDTH // 2 - len(self.current_shape_matrix[0]) // 2
        self.piece_y = 0
        
        # Проверяем Game Over (если нельзя разместить новую фигуру)
        if not self.board.can_place_piece(self.current_shape_matrix, self.piece_x, self.piece_y):
            self.game_over = True
    
    def _lock_piece(self):
        """Фиксирует текущую фигуру на поле."""
        # Размещаем фигуру на поле
        self.board.place_piece(self.current_shape_matrix, self.piece_x, self.piece_y, self.current_color_index)
        
        # Очищаем заполненные линии
        cleared = self.board.clear_lines()
        if cleared > 0:
            self.lines_cleared += cleared
            # Подсчет очков: 100 * (количество линий ^ 2) * уровень
            self.score += 100 * (cleared ** 2) * self.level
            # Увеличение уровня каждые 10 линий
            self.level = self.lines_cleared // 10 + 1
            # Ускорение игры с уровнем
            self.fall_speed = max(50, 500 - (self.level - 1) * 50)
        
        # Создаем новую фигуру
        self._spawn_new_piece()
    
    def _restart_game(self):
        """Перезапускает игру."""
        # Сбрасываем поле
        self.board = Board(self.BOARD_WIDTH, self.BOARD_HEIGHT, self.CELL_SIZE)
        
        # Получаем новые фигуры
        self.current_shape_name, self.current_shape_matrix, self.current_color = get_random_piece()
        self.current_color_index = list(COLORS.keys()).index(self.current_shape_name) + 1
        self.next_shape_name, self.next_shape_matrix, self.next_color = get_random_piece()
        self.next_color_index = list(COLORS.keys()).index(self.next_shape_name) + 1
        
        # Сбрасываем позицию
        self.piece_x = self.BOARD_WIDTH // 2 - len(self.current_shape_matrix[0]) // 2
        self.piece_y = 0
        
        # Сбрасываем игровые переменные
        self.fall_time = 0
        self.fall_speed = 500
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
    
    def _draw_next_piece(self, screen, offset_x, offset_y):
        """Отрисовывает следующую фигуру."""
        # Заголовок
        text = self.font_small.render("Следующая:", True, (255, 255, 255))
        screen.blit(text, (offset_x, offset_y))
        
        # Размер для отрисовки следующей фигуры
        preview_cell_size = 20
        preview_start_x = offset_x
        preview_start_y = offset_y + 30
        
        # Отрисовка фигуры
        for row_idx, row in enumerate(self.next_shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell:  # Если клетка заполнена
                    x = preview_start_x + col_idx * preview_cell_size
                    y = preview_start_y + row_idx * preview_cell_size
                    rect = pygame.Rect(x, y, preview_cell_size, preview_cell_size)
                    pygame.draw.rect(screen, self.next_color, rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
    
    def _draw_info_panel(self, screen, offset_x, offset_y):
        """Отрисовывает панель информации."""
        y_pos = offset_y
        
        # Счет
        score_text = self.font_medium.render(f"Счет: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (offset_x, y_pos))
        y_pos += 40
        
        # Уровень
        level_text = self.font_medium.render(f"Уровень: {self.level}", True, (255, 255, 255))
        screen.blit(level_text, (offset_x, y_pos))
        y_pos += 40
        
        # Линии
        lines_text = self.font_medium.render(f"Линии: {self.lines_cleared}", True, (255, 255, 255))
        screen.blit(lines_text, (offset_x, y_pos))
        y_pos += 60
        
        # Следующая фигура
        self._draw_next_piece(screen, offset_x, y_pos)
    
    def _draw_game_over(self, screen):
        """Отрисовывает экран Game Over."""
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 50))
        screen.blit(game_over_text, text_rect)
        
        score_text = self.font_medium.render(f"Финальный счет: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        screen.blit(score_text, score_rect)
        
        restart_text = self.font_small.render("Нажмите R для рестарта", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_rect)
    
    def handle_events(self):
        """Обрабатывает события игры."""
        for event in pygame.event.get():
            # Обработка выхода (крестик окна)
            if event.type == pygame.QUIT:
                return False
            
            # Обработка управления
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self._restart_game()
                else:
                    if event.key == pygame.K_LEFT:
                        # Движение влево
                        if self.board.can_place_piece(self.current_shape_matrix, self.piece_x - 1, self.piece_y):
                            self.piece_x -= 1
                    elif event.key == pygame.K_RIGHT:
                        # Движение вправо
                        if self.board.can_place_piece(self.current_shape_matrix, self.piece_x + 1, self.piece_y):
                            self.piece_x += 1
                    elif event.key == pygame.K_DOWN:
                        # Ускоренное падение
                        if self.board.can_place_piece(self.current_shape_matrix, self.piece_x, self.piece_y + 1):
                            self.piece_y += 1
                        else:
                            self._lock_piece()
                    elif event.key == pygame.K_UP:
                        # Поворот фигуры
                        rotated = rotate_piece(self.current_shape_matrix)
                        if self.board.can_place_piece(rotated, self.piece_x, self.piece_y):
                            self.current_shape_matrix = rotated
        
        return True
    
    def update(self, dt: int):
        """Обновляет состояние игры."""
        if not self.game_over:
            self.fall_time += dt
            
            # Падение фигуры с течением времени
            if self.fall_time >= self.fall_speed:
                if self.board.can_place_piece(self.current_shape_matrix, self.piece_x, self.piece_y + 1):
                    self.piece_y += 1
                else:
                    self._lock_piece()
                self.fall_time = 0
    
    def draw(self, screen):
        """Отрисовывает игру."""
        # Заливка экрана цветом
        screen.fill(self.BACKGROUND_COLOR)
        
        # Отрисовка игрового поля
        self.board.draw(screen, self.board_offset_x, self.board_offset_y)
        
        # Отрисовка размещенных фигур на поле
        self.board.draw_grid(screen, self.board_offset_x, self.board_offset_y, self.color_index_map)
        
        # Отрисовка текущей фигуры
        if not self.game_over:
            for row_idx, row in enumerate(self.current_shape_matrix):
                for col_idx, cell in enumerate(row):
                    if cell:  # Если клетка заполнена
                        self.board.draw_cell(
                            screen,
                            self.piece_x + col_idx,
                            self.piece_y + row_idx,
                            self.current_color,
                            self.board_offset_x,
                            self.board_offset_y
                        )
        
        # Отрисовка панели информации
        info_panel_x = self.board_offset_x + self.board.pixel_width + 20
        self._draw_info_panel(screen, info_panel_x, self.board_offset_y)
        
        # Отрисовка Game Over
        if self.game_over:
            self._draw_game_over(screen)
    
    def run(self, screen, clock):
        """Главный игровой цикл."""
        running = True
        while running:
            # Вычисляем время кадра
            dt = clock.tick(self.FPS)
            
            # Обработка событий
            running = self.handle_events()
            
            # Обновление игры
            self.update(dt)
            
            # Отрисовка
            self.draw(screen)
            
            # Обновление экрана
            pygame.display.flip()
