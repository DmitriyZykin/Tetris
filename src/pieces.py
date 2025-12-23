# Фигуры тетриса

import random

# Словарь с матрицами фигур тетриса (0 - пусто, 1 - заполнено)
SHAPES = {
    'I': [
        [1, 1, 1, 1]
    ],  # Палка
    'O': [
        [1, 1],
        [1, 1]
    ],  # Квадрат
    'T': [
        [0, 1, 0],
        [1, 1, 1]
    ],  # T-образная
    'S': [
        [0, 1, 1],
        [1, 1, 0]
    ],  # S-образная
    'Z': [
        [1, 1, 0],
        [0, 1, 1]
    ],  # Z-образная
    'J': [
        [1, 0, 0],
        [1, 1, 1]
    ],  # J-образная
    'L': [
        [0, 0, 1],
        [1, 1, 1]
    ],  # L-образная
}

# Словарь с цветами для каждой фигуры (RGB)
COLORS = {
    'I': (0, 255, 255),      # Cyan (бирюзовый)
    'O': (255, 255, 0),      # Yellow (желтый)
    'T': (128, 0, 128),      # Purple (фиолетовый)
    'S': (0, 255, 0),        # Green (зеленый)
    'Z': (255, 0, 0),        # Red (красный)
    'J': (0, 0, 255),        # Blue (синий)
    'L': (255, 165, 0),      # Orange (оранжевый)
}


def get_random_piece():
    """
    Возвращает случайную фигуру и её цвет.
    
    Returns:
        tuple: (shape_name, shape_matrix, color)
    """
    shape_name = random.choice(list(SHAPES.keys()))
    shape_matrix = SHAPES[shape_name]
    color = COLORS[shape_name]
    return shape_name, shape_matrix, color


def rotate_piece(shape_matrix):
    """
    Поворачивает фигуру на 90 градусов по часовой стрелке.
    
    Args:
        shape_matrix: Матрица фигуры (список списков)
    
    Returns:
        Повернутая матрица фигуры
    """
    if not shape_matrix or not shape_matrix[0]:
        return shape_matrix
    
    rows = len(shape_matrix)
    cols = len(shape_matrix[0])
    
    # Поворот на 90 градусов по часовой стрелке
    rotated = [[shape_matrix[rows - 1 - j][i] for j in range(rows)] for i in range(cols)]
    return rotated
