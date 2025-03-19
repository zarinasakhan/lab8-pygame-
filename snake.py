import pygame
import random
pygame.init() # initializes all the pygame sub-modules

WIDTH = 600
HEIGHT = 600
CELL = 30  # Constants

colorRED = (255, 0, 0)
colorYELLOW = (255, 255, 0)
colorGREEN = (0, 255, 0)
colorGRAY = (169, 169, 169)
colorWHITE = (255, 255, 255) # Colors

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # creating the screen

def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)  # dividing the screen into cells with borders

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY] 
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))  # drawing 2 colored cells 

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}" #creatin class point for drawing objects

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0  # direction the snake is moving in, creation of class snake

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y # moving the snake
        self.body[0].x += self.dx #changing direction
        self.body[0].y += self.dy

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))  # drawing the red head
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))  # drawing yellow body

    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))  # Snake body grows as it gets food
            return True
        return False

    def check_wall_collision(self):
        head = self.body[0]
        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
            return True
        return False #Checking for border (wall) collision and whether the snake is leaving the playing area

class Food:
    def __init__(self, snake):
        self.snake = snake
        self.pos = self.generate_food_pos()  # Initialize food position

    def generate_food_pos(self):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)

            if not any(segment.x == x and segment.y == y for segment in self.snake.body): # checks if food is not placed on the snake's body
                return Point(x, y) #new posiiton

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))  # drawing food


FPS = 5
score = 0
level = 0
clock = pygame.time.Clock()

snake = Snake()
food = Food(snake)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # game loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1  # snake's movement with keyboard keys

    snake.move()

    if snake.check_collision(food):
        score += 1
        food = Food(snake)  # regenerate food

    if snake.check_wall_collision():
        print("Game over: Snake hit the wall")
        running = False  #Checking for border (wall) collision and whether the snake is leaving the playing area

    if score >= 4:  # increase level every 4 foods eaten
        level += 1
        score = 0
        FPS += 1  # increase speed when level increases

    
    draw_grid_chess()
    snake.draw()
    food.draw()

  
    font = pygame.font.SysFont("Verdana", 30)
    level_text = font.render(f"Level: {level}", True, "black")
    score_text = font.render(f"Score: {score}", True, "black")
    screen.blit(level_text, (WIDTH - 150, 20))
    screen.blit(score_text, (WIDTH - 150, 60))   # display score and level

    pygame.display.flip()
    clock.tick(FPS)  # the speed of the game

pygame.quit()  #exit
