"""Импортирование модуля random"""

from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 640
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption("Змейка")

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Создание класса - родителя для игровых объектов"""

    def __init__(self,
                 color=BOARD_BACKGROUND_COLOR,
                 border_color=BORDER_COLOR,
                 position=SCREEN_CENTER
                 ):
        self.position = position
        self.body_color = color
        self.border_color = border_color

    def draw(self) -> None:
        """Метод основа для дальнейших методов отрисовок объектов"""
        raise NotImplementedError("Отсутствует метод отрисовки объекта")


class Apple(GameObject):
    """Создание класса для игрового элемента - яблоко"""

    def __init__(self,
                 color=APPLE_COLOR,
                 bord_color=BORDER_COLOR
                 ):
        super().__init__(color, bord_color)
        self.randomize_position()

    def randomize_position(self, busy_positions=[SCREEN_CENTER]) -> None:
        """Выбор случайных координат для яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        while self.position in busy_positions:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

    # Метод draw класса Apple
    def draw(self) -> None:
        """Создание модели яблока на игровом поле"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)


class Snake(GameObject):
    """Создание класса для игрового элемента - змейка"""

    def __init__(self, color=SNAKE_COLOR, bord_color=BORDER_COLOR):
        super().__init__(color, bord_color)
        self.last = None
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = self.direction

    def reset(self) -> None:
        """Возвращение параметров змейки в начальное состояние"""
        self.positions = [self.position]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])
        self.next_direction = self.direction

    # Метод совершения движения
    def move(self) -> None:
        """
        Движение змейки - добавление элемента на следующую позицию
        в начало и удаление элемента в хвосте
        """
        x, y = self.direction
        temp_x, temp_y = self.get_head_position()
        temp_x = (temp_x + x * GRID_SIZE) % SCREEN_WIDTH
        temp_y = (temp_y + y * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (temp_x, temp_y))

    def get_head_position(self) -> tuple:
        """Определение текущих координат головы змейки"""
        return self.positions[0]

    def collision(self) -> bool:
        """Определение столкновения головы змейки с телом"""
        return self.get_head_position() in self.positions[1:]

    # Метод draw класса Snake
    def draw(self) -> None:
        """Отрисовка модели змейки на игровом поле"""
        for position in self.positions[:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def main():
    """Основная логика работы программы"""
    # Инициализация PyGame:
    pg.init()

    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # Выполняем рост змейки если съели яблоко
        if snake.get_head_position() == apple.position:
            apple.randomize_position([snake.positions])
        # Иначе совершаем движение выбрасывая последний элемент
        else:
            snake.last = snake.positions.pop()
        # При столкновении с собой - сброс
        if snake.collision():
            snake.reset()
            apple.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


# Функция обработки действий пользователя
def handle_keys(game_object) -> None:
    """Функция обработки нажатия клавиш"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.K_ESCAPE:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


if __name__ == "__main__":
    main()
