# python打包exe
# pip intall pyinstaller
# 切换到我们的文件目录在终端输入Pyinstaller -F -w -i 图标.ico AirplaneWars_zmt.py进行打包
import pygame
import random
import math
# 初始化
pygame.init()
from tkinter import messagebox
# 窗口显示
# 设置窗口大小
screen = pygame.display.set_mode((442, 672))
# 设置标题
pygame.display.set_caption("Airplane Wars game - zmt ")
# 设置图标
icon = pygame.image.load('image/ufo.png')
pygame.display.set_icon(icon)

# 加载背景
bgImg = pygame.image.load('image/背景.png')

# 加载音效
pygame.mixer.music.load('image/bg.flac')
pygame.mixer.music.play(-1)

# 加载玩家飞机
playerImg = pygame.image.load('image/player.png')
playerX = 210
playerY = 600
playerStep1 = 0  # 玩家移动速度
playerStep2 = 0  # 玩家移动速度

# 分数
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)


def show_score():
    text = f"Score:{score}"
    score_render = font.render(text, True, (0, 255, 0))
    screen.blit(score_render, (10, 10))


# 游戏结束
is_over = False
over_font = pygame.font.Font('freesansbold.ttf', 40)


def check_is_over():
    if is_over:
        text = "Game Over"
        render = over_font.render(text, True, (255, 0, 0))
        screen.blit(render, (200, 270))


# 加载敌人飞机
# 多个敌人
# 敌人的数量
number_of_enemies = 4


# 敌人移动
class Enemy():
    def __init__(self):
        self.enemyImg = pygame.image.load('image/enemy.png')
        self.enemyX = random.randint(20, 55)
        self.enemyY = random.randint(20, 60)
        self.enemyStep = random.randint(1, 2)  # 敌人移动速度

    # 敌人复原
    def reset(self):
        self.enemyX = random.randint(20, 55)
        self.enemyY = random.randint(20, 70)


# 保存所有所有的敌人
enemies = []
for i in range(number_of_enemies):
    enemies.append(Enemy())


# 两个点之间的距离
def distance(bx, by, ex, ey):
    a = bx - ex
    b = by - ey
    return math.sqrt(a * a + b * b)  # 开根号


# 子弹类
class Bullet():
    def __init__(self):
        self.img = pygame.image.load('image/bullet.png')
        self.x = playerX + 8  # 子弹位置x
        self.y = playerY + 10  # 子弹位置y
        self.step = 10  # 子弹移动速度

    # 击中检测
    def hit(self):
        global score
        for e in enemies:
            if (distance(self.x, self.y, e.enemyX, e.enemyY) < 10):
                # 击中目标
                try:
                    bullets.remove(self)
                except:
                    messagebox.showinfo('提示', '系统故障，请退出后重启!')
                    exit()
                # 恢复位置
                e.reset()
                score += 1


bullets = []  # 保存现有子弹


# 显示并移动子弹
def show_bullets():
    for b in bullets:
        screen.blit(b.img, (b.x, b.y))
        # 尝试射击，查看是否击中目标
        b.hit()
        b.y -= b.step
        if b.y < 0:
            bullets.remove(b)


# 敌人显示
def show_enemy():
    global is_over
    for e in enemies:
        screen.blit(e.enemyImg, (e.enemyX, e.enemyY))
        e.enemyX += e.enemyStep
        if (e.enemyX > 382 or e.enemyX < 0):
            e.enemyStep *= -1
            # 可依据此次调整难度
            e.enemyY += 10
            if e.enemyY > 500:
                is_over = True
                enemies.clear()
                pygame.mixer.music.stop()


# 玩家移动
def move_player():
    global playerX
    global playerY
    # 移动飞机
    playerX += playerStep1
    playerY += playerStep2
    # 防止出界
    # (442代表背景图大小，60代表player大小)
    # (382=442-60)
    if playerX > 382:
        playerX = 382
    if playerX < 0:
        playerX = 0
    if playerY > 617:
        playerY = 617
    if playerY < 0:
        playerY = 0


# 游戏主循环
running = True
while running:
    clock = pygame.time.Clock()
    clock.tick(180)
    # 显示背景图片
    screen.blit(bgImg, (0, 0))
    # 显示分数
    show_score()
    # 控制玩家移动
    for event in pygame.event.get():
        # 退出事件
        if event.type == pygame.QUIT:
            running = False
        #     如果是键盘按下,右按键向右移动，反之类似
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerStep1 = 1
            elif event.key == pygame.K_LEFT:
                playerStep1 = -1
            elif event.key == pygame.K_UP:
                playerStep2 = -1
            elif event.key == pygame.K_DOWN:
                playerStep2 = 1
            #     发射子弹
            elif event.key == pygame.K_SPACE:
                # 创建一颗子弹
                bullets.append(Bullet())

        # 按键抬起，停止不动
        if event.type == pygame.KEYUP:
            playerStep1 = 0
            playerStep2 = 0

    # 显示玩家
    screen.blit(playerImg, (playerX, playerY))

    # 移动玩家
    move_player()

    # 展示敌人
    show_enemy()

    # 显示子弹
    show_bullets()

    # 游戏结束
    check_is_over()

    pygame.display.update()
pygame.quit()
