# https://www.youtube.com/watch?v=61eX0bFAsYs&ab_channel=GrandmaCan-%E6%88%91%E9%98%BF%E5%AC%A4%E9%83%BD%E6%9C%83
# image https://drive.google.com/drive/folders/10-SA2Fiyf5cm3jUNW2s1zskh0-2eQl9V
# 字體 https://www.pkstep.com/archives/5693
# 字體 https://www.twfont.com/chinese/
import time
import pygame
# import random
import os
from math import *

FPS = 60  # 60針
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FINISH_COLOR = (255, 240, 212)
WIDTH = 450
HEIGHT = 600
# 遊戲初始化 and 創建視窗
pygame.init()
# 視窗大小
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("escape room")  # 視窗標題
icon_image = pygame.image.load("./img/icon.png").convert()
icon_image.set_colorkey(WHITE)
pygame.display.set_icon(icon_image)
all_sprites = pygame.sprite.Group()

# 背景音樂
# pygame.mixer.init()
# pygame.mixer.music.load(f"./music/{random.randrange(0, 6)}.mp3")
# pygame.mixer.music.play()

# 載入圖片 convert 轉成pygame 易讀檔案
background = pygame.image.load("./img/background450.png").convert()
great_background = pygame.image.load("./img/Great.png").convert()
try_again_background = pygame.image.load("./img/try_again.png").convert()
finish_background = pygame.image.load("./img/finish_background.png").convert()
repeat_image = pygame.image.load("./img/repeat.png").convert()
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

clock = pygame.time.Clock()

font_name = os.path.join("./font.ttf")  # 取的字型
number_name = pygame.font.match_font('arial')


class Button(pygame.sprite.Sprite):
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
        global which_button_click
        mouse_press = pygame.mouse.get_pos()
        if self.click:
            self.animation_of_button()
        else:
            if self.sensor_rect.collidepoint(mouse_press):
                if pygame.mouse.get_pressed()[0]:
                    if not which_button_click:
                        which_button_click = True
                        self.keydown = True
                        global running
                        self.last_update = pygame.time.get_ticks()
                        self.click = True

    def input(self):
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

    def check_which_error(self):
        global running
        if check_list.get(ans_list[-1]):
            running = False
            which_error["repeat"][1] = True
        else:
            check_list[ans_list[-1]] = True
        if ans_list[-1] - int(ans_list[-1]) != 0:
            running = False
            which_error["decimal"][1] = True
        if ans_list[-1] > 50:
            running = False
            which_error["big than 50"][1] = True

    def animation_of_button(self):
        global which_button_click
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame:  # 瞬間當下時間 跟 創建時間差 到換圖時間(ex.時間差到50ms時換下張圖)
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
                    self.input()
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
                        which_button_click = False
                        self.check_which_error()


class ListText:

    def __init__(self):
        self.x = WIDTH / 4 - 100
        self.y = 100
        self.length = 0
        self.index = 0

    def reset(self):
        self.x = WIDTH / 4 - 55
        self.y = 100
        self.length = 0
        self.index = 0

    def update(self):
        self.x += 65
        self.length += 1

    def change_line(self):
        self.x = WIDTH / 4 - 55
        self.y += 55
        self.length = 0

    def draw(self, surface, text, size, color):
        font = pygame.font.Font(number_name, size)  # 給定字型和大小# font:字型 render:使成為
        text_surface = font.render(text, True, color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.x
        text_rect.centery = self.y
        surface.blit(text_surface, text_rect)

    def show(self):
        self.reset()
        for n in ans_list:
            if n in need_list[0:self.index + 1:]:
                self.draw(screen, f"{n}", 50, RED)
                self.index += 1
            else:
                self.draw(screen, f"{n}", 50, BLACK)
            self.update()
            if self.length > 5:
                self.change_line()


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
        self.rect.x = WIDTH / 4 - 150 + (length + 1) * self.tabx
        if self.rect.x == WIDTH / 4 + 240:
            self.rect.x = WIDTH / 4 - 85


class Great(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.last_update = pygame.time.get_ticks()
        self.show_time = 1000
        self.image = great_background.copy()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2 + 20)
        self.now = pygame.time.get_ticks()
        self.text = f"GREAT!"
        self.size = 80
        self.color = BLACK
        self.font = pygame.font.Font(font_name, self.size)

    def update(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_update < self.show_time:
            self.now = pygame.time.get_ticks()
            self.draw(self.rect.width / 2 + 10, self.rect.height / 2)
        else:
            self.kill()

    def draw(self, x, y):
        text_surface = self.font.render(self.text, True, self.color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.centery = y
        self.image.blit(text_surface, text_rect)


class Error(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = great_background.copy()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT * 2 / 3 - 20)
        self.now = pygame.time.get_ticks()
        for message in which_error:
            if which_error[message][1]:
                self.text = which_error[message][0]
                break
        self.size = 60
        self.color = BLACK
        self.font = pygame.font.Font(font_name, self.size)  # 給定字型和大小# font:字型 render:使成為

    def update(self):
        self.draw(self.rect.width / 2 + 10, self.rect.height / 2)

    def draw(self, x, y):
        text_surface = self.font.render(self.text, True, self.color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
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
        self.rect.center = (WIDTH / 2, HEIGHT / 2 + 200)
        self.text = f"Try again!"
        self.size = 60
        self.color = (68, 68, 68)
        self.show = True
        self.font = pygame.font.Font(font_name, self.size)

    def update(self):
        if self.show:
            self.draw(self.rect.width / 2 + 10, self.rect.height / 2)
            # screen.blit(self.image, self.rect.center)
        else:
            self.kill()

    def draw(self, x, y):
        text_surface = self.font.render(self.text, True, self.color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.centery = y
        self.image.blit(text_surface, text_rect)


class Rule:

    def __init__(self):
        self.sensor_rect = pygame.Rect((0, 0), (40, 40))
        self.text_background = pygame.Surface((40, 40)).convert()
        self.text_background.fill(WHITE)
        self.rect = self.text_background.get_rect(center=(0, 0))
        self.text = f"?"
        self.size = 40
        self.color = BLACK
        self.click = False
        self.font = pygame.font.Font(font_name, self.size)  # 給定字型和大小# font:字型 render:使成為
        self.draw(self.sensor_rect.width / 2, self.sensor_rect.height / 2)

    def update(self):
        global which_button_click
        mouse_press = pygame.mouse.get_pos()
        screen.blit(self.text_background, (0, 0))
        if self.click:
            self.click = False
            show_rule()
        elif self.sensor_rect.collidepoint(mouse_press):
            if pygame.mouse.get_pressed()[0]:
                if not which_button_click:
                    which_button_click = True
                    self.click = True

    def draw(self, x, y):
        text_surface = self.font.render(self.text, True, self.color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.centery = y
        self.text_background.blit(text_surface, text_rect)


class Repeat(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        repeat_image.set_colorkey(WHITE)
        self.image = repeat_image
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 20, 20)
        self.happen = False

    def update(self):
        global running, locate_text, which_button_click
        mouse_press = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_press) and pygame.mouse.get_pressed()[0]:
            if not self.happen and not which_button_click:
                which_button_click = True
                screen.fill(WHITE)
                pygame.display.update()  # 更新畫面=pygame.display.flip()更新全部，update可以有參數
                time.sleep(0.3)
                running = False
                self.happen = True


class Finish:

    def __init__(self):
        self.sensor_rect = pygame.Rect((0, 0), (WIDTH, 40))
        self.sensor_rect.left = 0
        self.sensor_rect.centery = HEIGHT - self.sensor_rect.height
        self.background = pygame.Surface((450, 200)).convert()
        self.background.fill(FINISH_COLOR)
        self.rect = self.background.get_rect(center=(WIDTH / 2, 500))
        self.text = [f"太棒了，你完成解謎了!", f"密碼是按了多少次+5", f"再玩一次~~"]
        self.size = [40, 40, 50]
        self.color = [BLACK, BLACK, RED]
        self.finish_running = True
        # screen.blit(self.image, self.rect.center)

    def draw(self):
        for a in range(len(self.text)):
            font = pygame.font.Font(font_name, self.size[a])  # 給定字型和大小# font:字型 render:使成為
            text_surface = font.render(self.text[a], True, self.color[a])  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
            text_rect = text_surface.get_rect()
            text_rect.left = 10 + (a // 2) * 80
            text_rect.centery = 40 + 65 * a
            self.background.blit(text_surface, text_rect)


def try_again_func():
    repeat.kill()
    try_again = TryAgain()
    error_message = Error()
    all_sprites.add(try_again)
    all_sprites.add(error_message)
    while try_again.show:
        clock.tick(FPS)
        for try_event in pygame.event.get():  # 回傳所有動作
            if try_event.type == pygame.QUIT:  # 如果按下X ,pygame.QUIT 是按下X後的型態
                global running, game
                running = False  # 跳出迴圈
                game = False
                try_again.show = False
            if try_event.type == pygame.MOUSEBUTTONDOWN:  # 如果按下X ,pygame.QUIT 是按下X後的型態
                mouse_pos = pygame.mouse.get_pos()
                if try_again.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    try_again.show = False  # 跳出迴圈
                    error_message.kill()
        screen.fill(WHITE)
        screen.blit(background, (0, 0))  # blit(畫) 第一個是圖片，第二個是位置
        locate_text.show()
        try_again.update()
        error_message.update()
        all_sprites.draw(screen)
        pygame.display.update()
    try_again.kill()
    time.sleep(0.3)


def show_rule():
    rule_text = ["規則",
                 "1.面板有三個按鈕，+5, +7 和開根號",
                 "2.用滑鼠按下按鈕完成謎題",
                 "3.計數從5開始",
                 "4.顯示器上要必須依序不用連續出現",
                 "      2, 10, 14這三個數字(如:1,2,6,10,21,14...)",
                 "5.顯示器上可以顯示任何數字，但有些條件:",
                 "      a)同一個數字不能出現兩次(包含第一個5)",
                 "      b)顯示器上的數字不能大於50",
                 "      c)不能出現小數(開根號不能有小數)",
                 "6.可以按下左上角'?'顯示規則",
                 "7.可以按下右上角圖示重新開始"]
    global running, game
    if running:
        rule_text.append("點擊或按任意鍵繼續遊戲!")
    else:
        rule_text.append("點擊或按任意鍵開始遊戲!")

    surface = pygame.Surface((WIDTH, HEIGHT)).convert()
    surface.get_rect(center=(0, 0))
    surface.fill((232, 255, 255))
    sensor_surface = pygame.Surface((WIDTH, 48)).convert()
    sensor_surface_rect = sensor_surface.get_rect()
    sensor_surface_rect.left = 0
    sensor_surface_rect.centery = 575

    for L in range(len(rule_text)):
        if L == len(rule_text) - 1:
            font = pygame.font.Font(font_name, 39)  # 給定字型和大小# font:字型 render:使成為
            text_surface = font.render(rule_text[L], True, RED)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        elif L == 0:
            font = pygame.font.Font(font_name, 50)  # 給定字型和大小# font:字型 render:使成為
            text_surface = font.render(rule_text[L], True, (163, 92, 219))  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        else:
            font = pygame.font.Font(font_name, 20)  # 給定字型和大小# font:字型 render:使成為
            text_surface = font.render(rule_text[L], True, BLACK)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        text_rect = text_surface.get_rect()
        if L == len(rule_text) - 1:
            text_rect.left = WIDTH / 2 - text_rect.width / 2
        else:
            text_rect.left = 15
        text_rect.centery = 30 + 45 * L
        surface.blit(text_surface, text_rect)

    rule_running = True
    while rule_running:
        clock.tick(FPS)  # 一秒最多刷新FPS次(1秒跑最多幾次while)
        for rule_event in pygame.event.get():  # 回傳所有動作
            if rule_event.type == pygame.QUIT:
                game = False
                running = False
                rule_running = False
            if rule_event.type == pygame.KEYDOWN:
                rule_running = False  # 跳出迴圈
            mouse_pos = pygame.mouse.get_pos()
            if rule_event.type == pygame.MOUSEBUTTONDOWN:
                if sensor_surface_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    global which_button_click
                    which_button_click = True
                    rule_running = False  # 跳出迴圈
        screen.blit(surface, (0, 0))
        pygame.display.update()
    time.sleep(0.1)


def show_finish():
    finish = Finish()
    finish.draw()
    finish.finish_running = True
    while finish.finish_running:
        clock.tick(FPS)  # 一秒最多刷新FPS次(1秒跑最多幾次while)
        for finish_event in pygame.event.get():  # 回傳所有動作
            if finish_event.type == pygame.QUIT:
                global game, running
                game = False
                running = False
                finish.finish_running = False

            if finish_event.type == pygame.MOUSEBUTTONDOWN:  # 如果按下X ,pygame.QUIT 是按下X後的型態
                mouse_pos = pygame.mouse.get_pos()
                if finish.sensor_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    finish.finish_running = False  # 跳出迴圈
        screen.fill(WHITE)
        screen.blit(background, (0, 0))  # blit(畫) 第一個是圖片，第二個是位置
        locate_text.show()
        screen.blit(finish.background, (0, HEIGHT - finish.rect.height))
        pygame.display.update()
    time.sleep(0.2)


need_list = [2, 10, 14]
game = True
running = False
first_start = True
which_button_click = False
which_error = {"repeat": ["數字重複啦", False], "decimal": ["啥?有小數點", False], "big than 50": ["數字>50啦", False]}
locate_text = ListText()
rule = Rule()

while game:
    # initial_game()
    # set origin
    for error in which_error:
        which_error[error][1] = False
    index = 0
    ans_list = [5]
    check_list = {5: True}
    if first_start:
        show_rule()
        first_start = False
    if game:
        running = True
    # create sprites
    add5 = Button((image_scale / 2 - 16, HEIGHT - image_scale / 2), 5)
    all_sprites.add(add5)
    add7 = Button((WIDTH / 2 + 4, HEIGHT - image_scale / 2), 7)
    all_sprites.add(add7)
    Sqrt = Button((WIDTH - image_scale / 2 + 17, HEIGHT - image_scale / 2), 'sqrt')
    all_sprites.add(Sqrt)
    bottom_line = BottomLine()
    all_sprites.add(bottom_line)
    repeat = Repeat()
    all_sprites.add(repeat)

    # 遊戲迴圈
    while running and index < 3:
        screen.fill(WHITE)
        clock.tick(FPS)  # 一秒最多刷新FPS次(1秒跑最多幾次while)
        # 取得輸入
        for event in pygame.event.get():  # 回傳所有動作
            if event.type == pygame.QUIT:  # 如果按下X ,pygame.QUIT 是按下X後的型態
                running = False  # 跳出迴圈
                game = False
            if event.type == pygame.MOUSEBUTTONUP and which_button_click:
                which_button_click = False
        # 更新顯示
        screen.blit(background, (0, 0))  # blit(畫) 第一個是圖片，第二個是位置
        all_sprites.update()
        rule.update()
        locate_text.show()
        bottom_line.reset(locate_text.length, len(ans_list) // 6)

        if need_list[index] == ans_list[-1] and index < 3:
            index += 1
            if not check_list.get(ans_list[-1]):
                great = Great()
                all_sprites.add(great)
        all_sprites.draw(screen)
        pygame.display.update()  # 更新畫面=pygame.display.flip()更新全部，update可以有參數
    if game:
        if index < 3:
            if not repeat.happen:
                try_again_func()
            else:
                repeat.kill()
            add5.kill()
            add7.kill()
            Sqrt.kill()
            bottom_line.kill()
            locate_text.__init__()
        else:
            add5.kill()
            add7.kill()
            Sqrt.kill()
            bottom_line.kill()
            show_finish()
            running = False
            first_start = True

# pygame.mixer.music.stop()
pygame.quit()
