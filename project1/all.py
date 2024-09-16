# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from sys import exit
import random

# 初始化
pygame.init()
windows_width = 550
windows_height = 780
icoSize = 128  # 增大方块大小

# 颜色定义
colors = {
    'white': pygame.Color(255, 255, 255),
    'red': pygame.Color(255, 0, 0),
    'black': pygame.Color(0, 0, 0),
    'grey': pygame.Color(150, 150, 150),
    'blue': pygame.Color(0, 0, 255),
    'green': pygame.Color(0, 255, 0),
}


# 图像加载
def load_images():
    images = {
        'red': pygame.transform.scale(pygame.image.load('1.png'), (icoSize, icoSize)),
        'blue': pygame.transform.scale(pygame.image.load('2.png'), (icoSize, icoSize)),
        'green': pygame.transform.scale(pygame.image.load('3.png'), (icoSize, icoSize)),
        'grey': pygame.transform.scale(pygame.image.load('4.png'), (icoSize, icoSize)),
        'black': pygame.transform.scale(pygame.image.load('5.png'), (icoSize, icoSize)),
        'background': pygame.transform.scale(pygame.image.load('background.png'), (windows_width, windows_height))
    }
    return images


# 绘制文本
def draw_text(surface, text, font, color, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


# 绘制按钮
def draw_button(surface, font, text, color, rect):
    pygame.draw.rect(surface, color, rect)
    draw_text(surface, text, font, colors['white'], rect.centerx, rect.centery)
    pygame.draw.rect(surface, colors['black'], rect, 1)  # 按钮边框


# 保存得分到排行榜
def save_score(score):
    try:
        with open("high_scores.txt", "r") as file:
            scores = [int(line.strip()) for line in file]
    except FileNotFoundError:
        scores = []

    scores.append(score)
    scores = sorted(scores, reverse=True)[:10]

    with open("high_scores.txt", "w") as file:
        for s in scores:
            file.write(f"{s}\n")


# 读取排行榜
def load_scores():
    try:
        with open("high_scores.txt", "r") as file:
            scores = [int(line.strip()) for line in file]
    except FileNotFoundError:
        scores = []
    return scores


# 显示排行榜
def display_scores(surface, fonts):
    scores = load_scores()
    surface.fill(colors['white'])
    draw_text(surface, "排行榜", fonts['large'], colors['black'], windows_width // 2, 50)

    for i, score in enumerate(scores):
        draw_text(surface, f"{i + 1}. {score}", fonts['medium'], colors['black'], windows_width // 2, 100 + i * 50)

    pygame.display.update()
    pygame.time.wait(3000)


# 游戏主循环
def game_loop(playSurface, fonts, images):
    totalScore = 0
    score = 0
    itemCount = 5
    data = [[i + 1 for i in range(3)] for j in range(3)]

    # 随机打乱初始数据
    for r in range(3):
        for c in range(3):
            r1 = random.randint(0, 2)
            c1 = random.randint(0, 2)
            t = data[r1][c1]
            data[r1][c1] = data[r][c]
            data[r][c] = t

    store = [0] * 7
    offsetX = (windows_width - (3 * icoSize + icoSize)) / 2
    offsetY = (windows_height - (3 * icoSize + icoSize)) / 2
    end_button_rect = Rect(windows_width - 120, 20, 100, 40)

    start_time = pygame.time.get_ticks()

    while True:
        playSurface.blit(images['background'], (0, 0))
        draw_text(playSurface, f"得分: {totalScore}", fonts['small'], colors['black'], 50, 75)

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        remaining_time = 5 - elapsed_time

        if remaining_time <= 0:
            draw_text(playSurface, "时间到！游戏结束！", fonts['large'], colors['red'], windows_width // 2,
                      windows_height // 2)
            pygame.display.update()
            pygame.time.wait(2000)
            save_score(totalScore)
            display_scores(playSurface, fonts)
            pygame.quit()
            exit()

        draw_text(playSurface, f"剩余时间: {int(remaining_time)}", fonts['medium'], colors['black'], windows_width // 2,
                  100)

        for r in range(3):
            for c in range(3):
                block_color = data[r][c]
                image = images.get(['red', 'blue', 'green', 'grey', 'black'][block_color - 1])
                playSurface.blit(image, (offsetX + c * icoSize, offsetY + r * icoSize))

        for i in range(7):
            if store[i]:
                block_color = store[i]
                image = images.get(['red', 'blue', 'green', 'grey', 'black'][block_color - 1])
                playSurface.blit(image, (i * (icoSize + 2), 620))

        draw_button(playSurface, fonts['small'], "End Game", colors['green'], end_button_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == MOUSEBUTTONUP:
                x, y = event.pos
                if end_button_rect.collidepoint(x, y):
                    pygame.quit()
                    exit()

                for r in range(3):
                    for c in range(3):
                        bx = offsetX + c * icoSize
                        by = offsetY + r * icoSize
                        if bx <= x <= bx + icoSize and by <= y <= by + icoSize:
                            col = int((x - offsetX) / icoSize)
                            row = int((y - offsetY) / icoSize)

                            for i in range(7):
                                if store[i] == 0:
                                    store[i] = data[row][col]
                                    break

                            cnt = store.count(data[row][col])
                            if cnt == 3:
                                store = [0 if color == data[row][col] else color for color in store]
                                score += 1
                                totalScore += 1
                                if score > 10:
                                    itemCount += 1
                                    score = 0

                            data[row][col] = random.randint(1, 100) % itemCount + 1

        pygame.display.update()


# 开始界面
def start_screen(playSurface, fonts, images):
    while True:
        playSurface.blit(images['background'], (0, 0))
        draw_text(playSurface, "动物消消乐", fonts['large'], colors['black'], windows_width // 2,
                  windows_height // 2 - 200)
        draw_button(playSurface, fonts['small'], "点击这里开始", colors['green'],
                    Rect(windows_width // 2 - 60, windows_height // 2, 150, 40))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == MOUSEBUTTONUP:
                x, y = event.pos
                if Rect(windows_width // 2 - 60, windows_height // 2, 150, 40).collidepoint(x, y):
                    return

        pygame.display.update()


def main():
    playSurface = pygame.display.set_mode((windows_width, windows_height))
    pygame.display.set_caption("动物消消乐")

    font_path = 'C:/Users/qiuyu/PycharmProjects/pythonProject/Uranus_Pixel_11Px.ttf'
    fonts = {
        'small': pygame.font.Font(font_path, 24),
        'medium': pygame.font.Font(font_path, 36),
        'large': pygame.font.Font(font_path, 50)
    }

    images = load_images()

    start_screen(playSurface, fonts, images)
    game_loop(playSurface, fonts, images)


if __name__ == "__main__":
    main()
