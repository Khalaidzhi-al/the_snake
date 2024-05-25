"""Импортирование модуля random"""
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 640
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Создание класса - родителя для игровых объектов"""

    def __init__(self):
        self.position = None
        self.body_color = None

    def draw(self) -> None:
        """Метод основа для дальнейших методов отрисовок объектов"""


class Apple(GameObject):
    """Создание класса для игрового элемента - яблоко"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def randomize_position(self) -> None:
        """Выбор случайных координат для яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    # Метод draw класса Apple
    def draw(self) -> None:
        """Создание модели яблока на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Создание класса для игрового элемента - змейка"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.last = None
        self.body_color = SNAKE_COLOR
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = RIGHT

    def reset(self) -> None:
        """Возвращение параметров змейки в начальное состояние"""
        self.clear_dead()
        self.length = 1
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = RIGHT

    def grow(self, next_loc: tuple) -> None:
        """Добавление элемента к змейке в следующей ячейке сетки поля"""
        self.positions.insert(0, next_loc)

    # Метод совершения движения
    def move(self, next_loc: tuple) -> None:
        """
        Движение змейки - добавление элемента на следующую позицию
        в начало и удаление элемента в хвосте
        """
        self.positions.insert(0, next_loc)
        self.last = self.positions.pop()

    def get_head_position(self) -> tuple:
        """Определение текущих координат головы змейки"""
        return self.positions[0]

    def next_cell(self) -> tuple:
        """
        Определение логики выбора следующей ячейки поля с учетом
        возможного перехода за границы
        """
        [temp_x, temp_y] = list(self.get_head_position())
        temp_change = [GRID_SIZE * x for x in self.direction]
        temp_x += temp_change[0]
        temp_y += temp_change[1]
        if temp_x < 0:
            temp_x = SCREEN_WIDTH
        elif temp_x >= GRID_WIDTH * GRID_SIZE:
            temp_x = 0
        if temp_y < 0:
            temp_y = SCREEN_HEIGHT
        elif temp_y >= GRID_HEIGHT * GRID_SIZE:
            temp_y = 0
        return (temp_x, temp_y)

    def collision(self) -> bool:
        """Определение столкновения головы змейки с телом"""
        if len(self.positions) > 1 and self.positions[0] in self.positions[1:]:
            return True
        return False

    # Метод draw класса Snake
    def draw(self) -> None:
        """Отрисовка модели змейки на игровом поле"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def clear_dead(self) -> None:
        """
        Очистка старой модели змейки в случае пройгрыша и
        выполнения метода reset
        """
        for position in self.positions[:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def main():
    """Основная логика работы программы"""
    # Инициализация PyGame:
    pygame.init()

    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        apple.draw()
        snake.draw()
        # Увеличиваем размер змейки при встрече с яблоком
        if snake.get_head_position() == apple.position:
            snake.grow(snake.next_cell())
            apple.randomize_position()
        else:
            snake.move(snake.next_cell())
        # При столкновении с собой - сброс
        if snake.collision():
            snake.reset()
        pygame.display.update()


# Функция обработки действий пользователя
def handle_keys(game_object) -> None:
    """Функция обработки нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


if __name__ == "__main__":
    main()
