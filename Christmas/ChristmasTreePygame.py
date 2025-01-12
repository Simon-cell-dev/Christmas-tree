import pygame
import random
import math

pygame.init()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Christmas Tree with Pygame")

WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

tree_height = 150
tree_base_width = 200
levels = 10

# 绘制树干
def draw_trunk():
    trunk_height = width // 10
    offset = 90
    pygame.draw.rect(screen, BROWN, [width // 2 - trunk_height // 2, (height // 4) + tree_height + offset, trunk_height, trunk_height])

# 绘制树冠
def draw_tree_crown():

    for level in range(levels):
        y_offset = (height // 4) + (level * (tree_height // levels))
        width_offset = (tree_base_width // levels) * (levels - level)
        points = [
            (- (width // 2 - width_offset // 2) + width, -y_offset + height),
            (- (width // 2 + width_offset // 2) + width, -y_offset + height),
            (- (width // 2) + width, -(y_offset + (tree_height // levels)) + height)
        ]
        color = (0, int(128 * (1 - level / levels)), 0)
        pygame.draw.polygon(screen, color, points)

# 绘制圣诞树
def draw_christmas_tree():
    draw_tree_crown()
    draw_trunk()

# 添加花环
def add_wreath():
    tree_center_x = width // 2
    tree_center_y = (height // 4) + tree_height + 1  # 基于树干顶部中心的y坐标
    for angle in range(0, 360, 10):
        x = int(tree_center_x + (tree_base_width // 2 - 20) * math.cos(math.radians(angle)))
        y = int(tree_center_y + (tree_base_width // 2 - 20) * math.sin(math.radians(angle)))
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)
# 添加彩灯
def add_lights():
    tree_center_x = width // 2
    tree_bottom_y = (height // 4) + tree_height +100

    tree_levels_vertices = []
    for level in range(levels):
        y_offset = (height // 4) + (level * (tree_height // levels))
        width_offset = (tree_base_width // levels) * (levels - level)
        points = [
            (width // 2 - width_offset // 2, y_offset),
            (width // 2 + width_offset // 2, y_offset),
            (width // 2, y_offset + (tree_height // levels))
        ]
        tree_levels_vertices.append(points)

    for _ in range(30):
        # 随机选择一层树冠
        level_choice = random.randint(0, levels - 1)
        level_vertices = tree_levels_vertices[level_choice]
        x = width - random.randint(level_vertices[0][0], level_vertices[1][0])
        y = tree_bottom_y - (random.randint(level_vertices[0][1], level_vertices[2][1]) - (height // 4))
        color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        pygame.draw.circle(screen, color, (x, y), 3)
# 添加树顶星星
def add_star():
    tree_center_x = width // 2
    tree_center_y = (height // 4) + tree_height - 25
    pygame.draw.polygon(screen, YELLOW, [(tree_center_x - 10, tree_center_y - 20),
                       (tree_center_x + 10, tree_center_y - 20),
                                         (tree_center_x, tree_center_y - 30)])

# 模拟雪花（使用pygame.sprite）
class Snowflake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(5, 15)  # 随机生成雪花大小
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        points = []
        for i in range(6):
            angle = math.radians(i * 60)
            x = size // 2 + size // 4 * math.cos(angle)
            y = size // 2 + size // 4 * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(self.image, (255, 255, 255, 100), points)
        self.rect = self.image.get_rect(center=(random.randint(0, width), random.randint(0, height)))
        self.speed = random.randint(50, 80)
        self.angle_speed = random.randint(-5, 5)
        self.angle = random.randint(0, 360)

    def update(self):
        self.rect.y += self.speed
        self.angle += self.angle_speed
        if self.rect.y > height:
            self.rect.y = -10
            self.rect.x = random.randint(0, width)
        self.rotate()

    def rotate(self):
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image, self.angle_speed)
        self.rect = self.image.get_rect(center=old_center)

# 创建雪花组
snowflakes = pygame.sprite.Group()
for _ in range(100):
    snowflake = Snowflake()
    snowflakes.add(snowflake)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    draw_christmas_tree()
    add_wreath()
    add_lights()
    add_star()
    snowflakes.update()
    snowflakes.draw(screen)
    pygame.display.flip()

pygame.quit()