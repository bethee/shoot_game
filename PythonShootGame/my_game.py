from pygame.locals import *
import random
import pygame
import sys


"""
pygame.sprit.Sprit模块：
    一般用于制作动画画面。当程序中有大量实体时，可以使用pygame.sprit.Sprit.Group()容器来统一管理。
    Group()中也有update和draw函数
"""


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640


class Bullet(pygame.sprite.Sprite):
    # 调用父类的初始化函数
    def __init__(self, bullet_img, init_pos):
        super().__init__()
        self.image = bullet_img
        # get_rect()函数返回surface实例的rect对象
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        super().__init__()
        self.image = []    # 存储玩家飞机图片的列表
        for i in range(len(player_rect)):
            # convert_alpha()：修改图像(Surface对象)的像素格式，包含alpha通道
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]    # 初始化玩家所在的矩形
        self.rect.topleft = init_pos    # 初始化玩家左上角坐标
        self.speed = 6
        self.bullets = pygame.sprite.Group()    # 初始化玩家子弹的集合
        self.img_index = 0    # 玩家图片索引
        self.is_hit = False    # 玩家是否被击中

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        pos = self.rect.top
        self.rect.top = 0 if pos <= 0 else (pos - self.speed)

    def moveDown(self):
        pos = self.rect.bottom
        self.rect.bottom = SCREEN_HEIGHT if pos >= SCREEN_HEIGHT else (pos + self.speed)

    def moveLeft(self):
        pos = self.rect.left
        self.rect.left = 0 if pos <= 0 else (pos - self.speed)

    def moveRight(self):
        pos = self.rect.right
        self.rect.right = SCREEN_WIDTH if pos >= SCREEN_WIDTH else (pos + self.speed)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 3
        self.down_index = 0

    def move(self):
        self.rect.bottom += self.speed


# 初始化pygame
pygame.init()

# 设置游戏窗口大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 设置游戏窗口标题
pygame.display.set_caption("打飞机")
# 加载游戏背景图片
background = pygame.image.load(r'resources/image/background.png').convert()
# 设置游戏结束图片
game_over = pygame.image.load(r'resources/image/gameover.png')
# 玩家，敌机和子弹图片集合
plane_img = pygame.image.load('resources/image/shoot.png')
# 击落敌机分数
ENEMY_SCORE = 100


# 设置玩家飞机不同状态的图片列表，多张图片展示为动画效果
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家飞机图片0, 1
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸图片
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
# player_pos = [200, 600]
player_pos = [200, 500]
# 实例化玩家
player = Player(plane_img, player_rect, player_pos)

# 子弹图片
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)



# 敌机不同状态的图片列表，多张图片展示为动画效果
enemy1_rect = pygame.Rect(534, 612, 57, 43)
# 敌机图片
enemy1_img = plane_img.subsurface(enemy1_rect)
# 敌机坠毁图片
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))
# 敌机集合
enemies1 = pygame.sprite.Group()

# 初始化射击及敌机移动频率,完成玩家的“喷气效果”
shoot_frequency = 0
enemy_frequency = 0

# 玩家飞机被击中后的效果处理
player_down_index = 16

# 初始化分数
score = 0

# 字体
game_font = pygame.font.SysFont('宋体', 20, True)

# 游戏循环帧率设置
clock = pygame.time.Clock()

# 判断游戏循环退出的参数
running = True


while running:
    # 最大帧率30
    clock.tick(60)
    # 生成子弹，需要控制发射频率
    # 首先判断玩家飞机没有被击中
    if not player.is_hit:
        if shoot_frequency % 20 == 0:
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 20:
            shoot_frequency = 0


    # 生成敌机，需要控制生成频率
    if enemy_frequency % 40 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 40:
        enemy_frequency = 0

    for bullet in player.bullets:
        # 以固定速度移动子弹
        bullet.move()
        # 移动出屏幕后删除子弹
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    for enemy in enemies1:
        # 2. 移动敌机
        enemy.move()
        # 3. 敌机与玩家飞机碰撞效果处理
        if pygame.sprite.collide_circle(enemy, player):
            # enemies1_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            break
    #     4. 移动出屏幕后删除飞机
        if enemy.rect.top >= SCREEN_HEIGHT:
            enemies1.remove(enemy)

    # 敌机被子弹击中效果处理
    # 将被击中的敌机对象添加到击毁敌机 Group 中，用来渲染击毁动画
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)

    # 绘制背景
    screen.fill(0)
    screen.blit(background, (0, 0))

    # 绘制玩家飞机
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # 更换图片索引使飞机有动画效果
        player.img_index = shoot_frequency // 10
    else:
        # 玩家飞机被击中后的效果处理
        player.img_index = player_down_index // 10
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            # 击中效果处理完成后游戏结束
            running = False

    # 敌机被子弹击中效果显示
    for enemy_down in enemies1_down:
        screen.blit(enemy_down.down_imgs[enemy_down.down_index], enemy_down.rect)
        if enemy_down.down_index < 4:
            enemy_down.down_index += 1
        else:
            enemies1_down.remove(enemy_down)
    score += len(enemies1_down) * ENEMY_SCORE


    # 显示子弹
    player.bullets.draw(screen)
    # 显示敌机
    enemies1.draw(screen)

    # 绘制得分
    screen.blit(game_font.render("score: {}".format(score), True, (255, 0, 0)), (20, 20))

    # 更新屏幕
    pygame.display.update()

    # 处理游戏退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 获取键盘事件（上下左右按键）
    key_pressed = pygame.key.get_pressed()

    # 处理键盘事件（移动飞机的位置）
    if key_pressed[K_w] or key_pressed[K_UP]:
        player.moveUp()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        player.moveDown()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        player.moveLeft()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        player.moveRight()

# 游戏 Game Over 后显示最终得分
# font = pygame.font.Font(None, 48)
# text = font.render('Score: ' + str(score), True, (255, 0, 0))
# text_rect = text.get_rect()
# text_rect.centerx = screen.get_rect().centerx
# text_rect.centery = screen.get_rect().centery + 24
# screen.blit(game_over, (0, 0))
# screen.blit(text, text_rect)

# 显示得分并处理游戏退出
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#     pygame.display.update()