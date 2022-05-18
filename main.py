# https://www.youtube.com/watch?v=61eX0bFAsYs&ab_channel=GrandmaCan-%E6%88%91%E9%98%BF%E5%AC%A4%E9%83%BD%E6%9C%83
# image https://drive.google.com/drive/folders/10-SA2Fiyf5cm3jUNW2s1zskh0-2eQl9V
import time
import pygame
import random
from math import *
FPS = 60    # 60針
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WIDTH = 450
HEIGHT = 600
# 遊戲初始化 and 創建視窗
pygame.init()
# 視窗大小
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("escape room")    # 視窗標題
all_sprites = pygame.sprite.Group()

# 背景音樂
pygame.mixer.init()
pygame.mixer.music.load(f"./music/{random.randrange(0, 6)}.mp3")
pygame.mixer.music.play()

# 載入圖片 convert 轉成pygame 易讀檔案
background = pygame.image.load("./img/background450.png").convert()
great_background = pygame.image.load("./img/Great.png").convert()
try_again_background = pygame.image.load("./img/try_again.png").convert()
button_line_image = []
for i in range(1, 3):
    Bottom_Line_Image = pygame.image.load(f"./img/bottom_line_{i}.png").convert()
    Bottom_Line_Image.set_colorkey(WHITE)
    button_line_image.append(Bottom_Line_Image)
image_scale = 180
button_image = {5: [], 7: [], 'sqrt': []}
for j in button_image:
    for i in range(1, 7):
        Button = pygame.image.load(f"./img/{j}_{i}.png").convert()
        Button.set_colorkey(WHITE)
        button_image[j].append(pygame.transform.scale(Button, (image_scale, image_scale)))


class button (pygame.sprite.Sprite):
    def __init__(self, center, button_name):
        self.click = False
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.name = button_name
        self.image = button_image[button_name][self.frame]
        self.rect = self.image.get_rect()
        self.origin_center = center
        self.rect.center = self.origin_center
        self.sensor_rect = pygame.Rect(center, (120, 110))
        self.sensor_rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 5000
        self.keydown = False
        self.downy = 4
        self.downx = 1

    def update(self):
        mouse_press = pygame.mouse.get_pos()
        if self.click:
            self.animationOfButton()
        else:
            if self.sensor_rect.collidepoint(mouse_press):
                if pygame.mouse.get_pressed()[0]:
                    self.keydown = True
                    global running
                    self.last_update = pygame.time.get_ticks()
                    self.click = True
                    if self.name == 5:
                        ans_list.append(ans_list[-1] + 5)
                    if self.name == 7:
                        ans_list.append(ans_list[-1] + 7)
                    if self.name == 'sqrt':
                        append_number = round(sqrt(ans_list[-1]), 2)  # round 四捨五入到小數兩位
                        if append_number - int(append_number) == 0:
                            ans_list.append(int(append_number))
                        else:
                            ans_list.append(append_number)

                    if check_list.get(ans_list[-1]):
                        running = False
                    else:
                        check_list[ans_list[-1]] = True
                    if ans_list[-1] - int(ans_list[-1]) != 0:
                        running = False
                    if ans_list[-1] > 50:
                        running = False

    def animationOfButton(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame:     # 瞬間當下時間 跟 創建時間差 到換圖時間(ex.時間差到50ms時換下張圖)
            self.last_update = now
            if self.keydown:
                self.frame += 1
                if self.frame < len(button_image[self.name]):
                    self.image = button_image[self.name][self.frame]
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.rect.y += self.downy
                    self.rect.x -= self.downx
                else:
                    self.keydown = False
            else:
                if not pygame.mouse.get_pressed()[0]:
                    self.frame -= 1
                    if self.frame >= 0:
                        self.image = button_image[self.name][self.frame]
                        center = self.rect.center
                        self.rect = self.image.get_rect()
                        self.rect.center = center
                        self.rect.y -= self.downy
                        self.rect.x += self.downx
                    else:
                        self.image = button_image[self.name][0]
                        self.rect = self.image.get_rect(center=self.origin_center)
                        self.rect.center = self.origin_center
                        self.frame = 0
                        self.keydown = True
                        self.click = False


class list_TEXT:

    def __init__(self):
        self.x = WIDTH/4-100
        self.y = 100
        self.length = 0

    def reset(self):
        self.x = WIDTH/4-55
        self.y = 100
        self.length = 0

    def update(self):
        self.x += 65
        self.length += 1

    def change_line(self):
        self.x = WIDTH/4-55
        self.y += 55
        self.length = 0

    def draw(self, surface, text, size, color):
        font = pygame.font.Font(font_name, size)  # 給定字型和大小# font:字型 render:使成為
        self.text_surface = font.render(text, True, color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.centerx = self.x
        self.text_rect.centery = self.y
        surface.blit(self.text_surface, self.text_rect)


class BottomLine(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = button_line_image[0]
        self.tabx = 65
        self.taby = 55
        self.rect = self.image.get_rect()
        self.last_update = pygame.time.get_ticks()
        self.rect.y = 70
        self.frame_rate = 200
        self.frame = 0

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = pygame.time.get_ticks()
            self.frame += 1
            self.frame %= 2
            center = self.rect.center
            self.image = button_line_image[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

    def reset(self, length, text_change_line_times):
        self.rect.y = 70 + text_change_line_times * self.taby
        self.rect.x = WIDTH/4 - 150 + (length+1) * self.tabx
        if self.rect.x == WIDTH/4 + 240:
            self.rect.x = WIDTH/4 - 85


class Great(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.last_update = pygame.time.get_ticks()
        self.show_time = 1000
        self.image = great_background
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2+20)
        self.now = pygame.time.get_ticks()
        self.text = f"GREAT!"
        self.size = 50
        self.color = BLACK

    def update(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_update < self.show_time:
            self.now = pygame.time.get_ticks()
            self.draw(self.rect.width/2+10, self.rect.height/2)
        else:
            self.kill()

    def draw(self, x, y):
        font = pygame.font.Font(font_name, self.size)  # 給定字型和大小# font:字型 render:使成為
        text_surface = font.render(self.text, True, self.color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.centery = y
        self.image.blit(text_surface, text_rect)


class TryAgain(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.last_update = pygame.time.get_ticks()
        # self.sensor_rect = pygame.Rect(center, (120, 110))
        self.image = try_again_background
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2+200)
        self.text = f"Try again!"
        self.size = 40
        self.color = (68, 68, 68)
        self.show = True

    def update(self):
        if self.show:
            self.draw(self.rect.width / 2 + 10, self.rect.height / 2)
            # screen.blit(self.image, self.rect.center)
        else:
            self.kill()

    def draw(self, x, y):
        font = pygame.font.Font(font_name, self.size)  # 給定字型和大小# font:字型 render:使成為
        text_surface = font.render(self.text, True, self.color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.centery = y
        self.image.blit(text_surface, text_rect)


font_name = pygame.font.match_font('arial')  # 取的字型


def draw_text(surface, text, size, color, x, y):
    font = pygame.font.Font(font_name, size)    # 給定字型和大小# font:字型 render:使成為
    text_surface = font.render(text, True, color)   # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_surface, text_rect)

# def initial_game():

def try_again_func():
    try_again = TryAgain()
    all_sprites.add(try_again)
    while try_again.show:
        for event in pygame.event.get():     # 回傳所有動作
            if event.type == pygame.MOUSEBUTTONDOWN:    # 如果按下X ,pygame.QUIT 是按下X後的型態
                mouse_pos = pygame.mouse.get_pos()
                if try_again.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    try_again.show = False             # 跳出迴圈
        screen.fill(WHITE)
        screen.blit(background, (0, 0))  # blit(畫) 第一個是圖片，第二個是位置
        locate_text.reset()
        for i in ans_list:
            if i in need_list[0:index+1:]:
                locate_text.draw(screen, f"{i}", 50, RED)
            else:
                locate_text.draw(screen, f"{i}", 50, BLACK)
            locate_text.update()
            if locate_text.length > 5:
                locate_text.change_line()
        try_again.update()
        all_sprites.draw(screen)
        pygame.display.update()
    time.sleep(0.2)



# 取的時間物件
clock = pygame.time.Clock()

need_list = [10, 10, 14]
game = True
running = True
while game:
    # initial_game()
    # set origin
    index = 0
    ans_list = [5]
    check_list = {5: True}
    # create sprites
    add5 = button((image_scale / 2 - 16, HEIGHT - image_scale / 2), 5)
    all_sprites.add(add5)
    add7 = button((WIDTH / 2 + 4, HEIGHT - image_scale / 2), 7)
    all_sprites.add(add7)
    Sqrt = button((WIDTH - image_scale / 2 + 17, HEIGHT - image_scale / 2), 'sqrt')
    all_sprites.add(Sqrt)
    bottom_line = BottomLine()
    all_sprites.add(bottom_line)
    locate_text = list_TEXT()

    # for event in pygame.event.get():  # 回傳所有動作
    #     if event.type == pygame.MOUSEBUTTONUP:  # 如果按下X ,pygame.QUIT 是按下X後的型態
    running = True

    # 遊戲迴圈
    while running and index < 3:
        screen.fill(WHITE)

        clock.tick(FPS)                     # 一秒最多刷新FPS次(1秒跑最多幾次while)
        # 取得輸入
        for event in pygame.event.get():     # 回傳所有動作
            if event.type == pygame.QUIT:    # 如果按下X ,pygame.QUIT 是按下X後的型態
                running = False             # 跳出迴圈
        # 更新顯示
        screen.blit(background, (0, 0))     # blit(畫) 第一個是圖片，第二個是位置
        all_sprites.update()
        locate_text.reset()
        for i in ans_list:
            if i in need_list[0:index+1:]:
                locate_text.draw(screen, f"{i}", 50, RED)
            else:
                locate_text.draw(screen, f"{i}", 50, BLACK)
            locate_text.update()
            if locate_text.length > 5:
                locate_text.change_line()
        bottom_line.reset(locate_text.length, len(ans_list)//6)

        if need_list[index] == ans_list[-1]:
            index += 1
            great = Great()
            all_sprites.add(great)
        all_sprites.draw(screen)
        pygame.display.update()                      # 更新畫面=pygame.display.flip()更新全部，update可以有參數
    try_again_func()
    # reset all sprites
    add5.kill()
    add7.kill()
    Sqrt.kill()
    bottom_line.kill()

end = False
while end:
    for event in pygame.event.get():     # 回傳所有動作
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                end = False  # 跳出迴圈
pygame.mixer.music.stop()

pygame.quit()