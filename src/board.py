# Игровое поле тетриса

import pygame


class Board:
    """Класс для игрового поля тетриса."""
    
    def __init__(self, width: int = 10, height: int = 20, cell_size: int = 30):
        """
        Инициализация игрового поля.
        
        Args:
            width: Ширина поля в клетках (колонки)
            height: Высота поля в клетках (строки)
            cell_size: Размер одной клетки в пикселях
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        
        # Размеры поля в пикселях
        self.pixel_width = width * cell_size
        self.pixel_height = height * cell_size
    
    def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int):
        """
        Отрисовка игрового поля с сеткой.
        
        Args:
            screen: Поверхность для отрисовки
            offset_x: Смещение по X в пикселях
            offset_y: Смещение по Y в пикселях
        """
        # Рисуем фон поля
        board_rect = pygame.Rect(offset_x, offset_y, self.pixel_width, self.pixel_height)
        pygame.draw.rect(screen, (0, 0, 0), board_rect)
        pygame.draw.rect(screen, (100, 100, 100), board_rect, 2)
        
        # Рисуем сетку
        for x in range(self.width + 1):
            start_pos = (offset_x + x * self.cell_size, offset_y)
            end_pos = (offset_x + x * self.cell_size, offset_y + self.pixel_height)
            pygame.draw.line(screen, (50, 50, 50), start_pos, end_pos, 1)
        
        for y in range(self.height + 1):
            start_pos = (offset_x, offset_y + y * self.cell_size)
            end_pos = (offset_x + self.pixel_width, offset_y + y * self.cell_size)
            pygame.draw.line(screen, (50, 50, 50), start_pos, end_pos, 1)
    
    def draw_cell(self, screen: pygame.Surface, x: int, y: int, color: tuple, 
                  offset_x: int, offset_y: int):
        """
        Отрисовка одной клетки на поле.
        
        Args:
            screen: Поверхность для отрисовки
            x: Координата X в клетках
            y: Координата Y в клетках
            color: Цвет клетки (RGB)
            offset_x: Смещение по X в пикселях
            offset_y: Смещение по Y в пикселях
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            pixel_x = offset_x + x * self.cell_size
            pixel_y = offset_y + y * self.cell_size
            rect = pygame.Rect(pixel_x, pixel_y, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Белая обводка
    
    def can_place_piece(self, piece_matrix, x: int, y: int) -> bool:
        """
        Проверяет, можно ли разместить фигуру на указанной позиции.
        
        Args:
            piece_matrix: Матрица фигуры
            x: Координата X левого верхнего угла фигуры
            y: Координата Y левого верхнего угла фигуры
        
        Returns:
            True если можно разместить, False иначе
        """
        for row_idx, row in enumerate(piece_matrix):
            for col_idx, cell in enumerate(row):
                if cell:  # Если клетка заполнена
                    board_x = x + col_idx
                    board_y = y + row_idx
                    
                    # Проверка границ
                    if board_x < 0 or board_x >= self.width or board_y >= self.height:
                        return False
                    # Проверка столкновения с уже размещенными фигурами
                    if board_y >= 0 and self.grid[board_y][board_x] != 0:
                        return False
        return True
    
    def place_piece(self, piece_matrix, x: int, y: int, color_index: int):
        """
        Размещает фигуру на поле.
        
        Args:
            piece_matrix: Матрица фигуры
            x: Координата X левого верхнего угла фигуры
            y: Координата Y левого верхнего угла фигуры
            color_index: Индекс цвета для сохранения в grid
        """
        for row_idx, row in enumerate(piece_matrix):
            for col_idx, cell in enumerate(row):
                if cell:  # Если клетка заполнена
                    board_x = x + col_idx
                    board_y = y + row_idx
                    if 0 <= board_x < self.width and 0 <= board_y < self.height:
                        self.grid[board_y][board_x] = color_index
    
    def clear_lines(self) -> int:
        """
        Удаляет полностью заполненные линии и возвращает количество удаленных линий.
        
        Returns:
            Количество удаленных линий
        """
        lines_to_remove = []
        
        # Находим полностью заполненные линии
        for y in range(self.height):
            if all(cell != 0 for cell in self.grid[y]):  # Все клетки заполнены
                lines_to_remove.append(y)
        
        # Удаляем заполненные линии (снизу вверх)
        for y in reversed(lines_to_remove):
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(self.width)])
        
        return len(lines_to_remove)
    
    def draw_grid(self, screen: pygame.Surface, offset_x: int, offset_y: int, colors: dict):
        """
        Отрисовывает размещенные фигуры на поле.
        
        Args:
            screen: Поверхность для отрисовки
            offset_x: Смещение по X в пикселях
            offset_y: Смещение по Y в пикселях
            colors: Словарь цветов (по индексам)
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != 0:
                    color = colors.get(self.grid[y][x], (255, 255, 255))
                    self.draw_cell(screen, x, y, color, offset_x, offset_y)
