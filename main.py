# https://www.youtube.com/watch?v=61eX0bFAsYs&ab_channel=GrandmaCan-%E6%88%91%E9%98%BF%E5%AC%A4%E9%83%BD%E6%9C%83
# image https://drive.google.com/drive/folders/10-SA2Fiyf5cm3jUNW2s1zskh0-2eQl9V
import time

import pygame
import random

FPS = 60    # 60針
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WIDTH = 500
HEIGHT = 600
# 遊戲初始化 and 創建視窗
pygame.init()
# 視窗大小
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("escape room")    # 視窗標題

# 背景音樂
pygame.mixer.init()
pygame.mixer.music.load(f"./music/{random.randrange(0, 6)}.mp3")
pygame.mixer.music.play()

# 載入圖片 convert 轉成pygame 易讀檔案
background = pygame.image.load("./img/background.png").convert()

font_name = pygame.font.match_font('arial')  # 取的字型
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)    # 給定字型和大小# font:字型 render:使成為
    text_surface = font.render(text, True, WHITE)   # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surface.blit(text_surface, text_rect)

# 取的時間物件
clock = pygame.time.Clock()
ans_list = [5]
check_list = {5: True}
# 遊戲迴圈
running = True
while running:
    clock.tick(FPS)                     # 一秒最多刷新FPS次(1秒跑最多幾次while)
    # 取得輸入
    for event in pygame.event.get():     # 回傳所有動作
        if event.type == pygame.QUIT:    # 如果按下X ,pygame.QUIT 是按下X後的型態
            running = False             # 跳出迴圈
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_5:
                ans_list.append(ans_list[-1]+5)
    if check_list.get(ans_list[-1]):
        running = False
    else:
        check_list[ans_list[-1]] = True
    # 畫面顯示
    screen.blit(background, (0, 0))     # blit(畫) 第一個是圖片，第二個是位置
    draw_text(screen, f"{ans_list}", 18, WIDTH / 4, 10)
    pygame.display.update()                      # 更新畫面=pygame.display.flip()更新全部，update可以有參數
pygame.mixer.music.stop()

pygame.quit()
