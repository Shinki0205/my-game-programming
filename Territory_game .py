import pygame
import sys
import random
import math

BLACK = (  0,  0,  0) # 黒色
GRAY  = ( 80, 80, 80) # 灰色
WHITE = (255,255,255) # 白色
RED   = (255,  0,  0) # 赤色
PINK  = (255,204,229) # ピンク色
YOLLOW= (255,255, 51) # 黄色
BLUE  = (102,178,255) # 青色
GREEN = ( 51,255, 51) # 緑色
PURPLE= (178,102,255) # 紫色
ORANGE= (255,178,102) # 橙色

pl_cl = {1:PINK, 2:YOLLOW, 3:BLUE} # playerの陣地の色
cp_cl = {1:GREEN, 2:PURPLE, 3:ORANGE} # cpuの陣地の色

FIELD_X = 15 # 横の長さ（外の壁込み）
FIELD_Y = 11 # 縦の長さ（外の壁込み）

field=[]
for y in range(FIELD_Y):
    field.append([0]*FIELD_X)

# 画像の取込み
imgPlayer = pygame.image.load("player_char-removebg-preview.png")
img_p = pygame.transform.scale(imgPlayer, [48, 48])

index = 0 # 画面管理変数
tmr = 0 # 時間管理変数
speed = 5 # 処理速度管理変数

# フィールドを生成する
'''
fieldの値
０：白塗り陣地（まだ塗られていないマス）
１：playerの陣地
２：cpuの陣地
９：壁
１１：playerの場所
１２：cpuの場所
'''
def make_field(player_x, player_y, cpu_x, cpu_y):
    global field
    # 壁を作る
    for y in range(FIELD_Y):
        for x in range(FIELD_X):
            field[y][x] = 0
    for x in range(FIELD_X):
        field[0][x] = 9
        field[FIELD_Y-1][x] = 9
    for y in range(1, FIELD_Y-1):
        field[y][0] = 9
        field[y][FIELD_X-1] = 9
    field[player_y][player_x] = 11 # playerの座標
    field[cpu_y][cpu_x] = 12 # cpuの座標

# playerを動かす関数
def move_player(player_x, player_y):
    global field
    key = pygame.key.get_pressed()
    if key[pygame.K_UP] == 1: # 上に移動
        if field[player_y-1][player_x] != 9 and field[player_y-1][player_x] != 12:
            field[player_y-1][player_x] = 11
            field[player_y][player_x] = 1
            player_y = player_y - 1
    if key[pygame.K_DOWN] == 1: # 下に移動
        if field[player_y+1][player_x] != 9 and field[player_y+1][player_x] != 12:
            field[player_y+1][player_x] = 11
            field[player_y][player_x] = 1
            player_y = player_y + 1
    if key[pygame.K_LEFT] == 1: # 左に移動
        if field[player_y][player_x-1] != 9 and field[player_y][player_x-1] != 12:
            field[player_y][player_x-1] = 11
            field[player_y][player_x] = 1
            player_x = player_x - 1
    if key[pygame.K_RIGHT] == 1: # 右に移動 
        if field[player_y][player_x+1] != 9 and field[player_y][player_x+1] != 12:
            field[player_y][player_x+1] = 11
            field[player_y][player_x] = 1
            player_x = player_x + 1
    return player_x, player_y

# cpuを動かす関数
def move_cpu(cpu_x, cpu_y):
    global field
    move_dirc = random.randint(1, 4)
    if move_dirc == 1: # 上に移動
        if field[cpu_y-1][cpu_x] == 9 or field[cpu_y-1][cpu_x] == 11:
            field[cpu_y+1][cpu_x] = 12
            field[cpu_y][cpu_x] = 2
            cpu_y = cpu_y + 1
        if field[cpu_y-1][cpu_x] != 9 and field[cpu_y-1][cpu_x] != 11:
            field[cpu_y-1][cpu_x] = 12
            field[cpu_y][cpu_x] = 2
            cpu_y = cpu_y - 1
    if move_dirc == 2: # 下に移動
        if field[cpu_y+1][cpu_x] == 9 or field[cpu_y+1][cpu_x] == 11:
            field[cpu_y-1][cpu_x] = 12
            field[cpu_y][cpu_x] = 2
            cpu_y = cpu_y - 1
        if field[cpu_y+1][cpu_x] != 9 and field[cpu_y+1][cpu_x] != 11:
            field[cpu_y+1][cpu_x] = 12
            field[cpu_y][cpu_x] = 2
            cpu_y = cpu_y + 1
    if move_dirc == 3: # 左に移動
        if field[cpu_y][cpu_x-1] == 9 or field[cpu_y][cpu_x-1] == 11:
            field[cpu_y][cpu_x+1] = 12
            field[cpu_y][cpu_x] = 2
            cpu_x = cpu_x + 1
        if field[cpu_y][cpu_x-1] != 9 and field[cpu_y][cpu_x-1] != 11:
            field[cpu_y][cpu_x-1] = 12
            field[cpu_y][cpu_x] = 2
            cpu_x = cpu_x - 1
    if move_dirc == 4: # 右に移動
        if field[cpu_y][cpu_x+1] == 9 or field[cpu_y][cpu_x+1] == 11:
            field[cpu_y][cpu_x-1] = 12
            field[cpu_y][cpu_x] = 2
            cpu_x = cpu_x - 1
        if field[cpu_y][cpu_x+1] != 9 and field[cpu_y][cpu_x+1] != 11:
            field[cpu_y][cpu_x+1] = 12
            field[cpu_y][cpu_x] = 2
            cpu_x = cpu_x + 1
    return cpu_x, cpu_y

# 床の塗り状態を更新する関数
def draw_field(bg, color): 
    bg.fill(BLACK)
    fnt = pygame.font.Font(None, 20)
    for y in range(FIELD_Y):
        for x in range(FIELD_X):
            X = x * 50 
            Y = y * 50
            if field[y][x] == 0 or field[y][x] == 11 or field[y][x] == 12:
                pygame.draw.rect(bg, WHITE, [X+1,Y+1,49,49])
            if field[y][x] == 9:
                pygame.draw.rect(bg, GRAY, [X+1,Y+1,49,49])
            if field[y][x] == 1 or field[y][x] == 11:
                pygame.draw.rect(bg, pl_cl[color], [X+1,Y+1,49,49])
            if field[y][x] == 2 or field[y][x] == 12:
                pygame.draw.rect(bg, cp_cl[color], [X+1,Y+1,49,49])
            if field[y][x] == 11 or field[y][x] == 12:
                bg.blit(img_p, [X+1,Y+1])
            if field[y][x] == 11:
                txt_pl = fnt.render("YOU", True, BLACK)
                bg.blit(txt_pl, [X+5, Y-10])
            if field[y][x] == 12:
                txt_cp = fnt.render("CPU", True, BLACK)
                bg.blit(txt_cp, [X+5, Y-10])

# バトル終了までの時間を表示する関数
def battle_time(bg, fnt, time, fast):
    txt_time = fnt.render(str(60-math.floor(time/fast)), True, RED)
    bg.blit(txt_time, [350, 0])
    
# ロード画面を表示する関数（ロードはしておらず急に画面が切り替わるのを防ぐ）
def game_load(bg, fnt):
    bg.fill(BLACK)
    txt_load = fnt.render("Loading...", True, WHITE)
    bg.blit(txt_load, [500, 500])

# 勝敗判定をする関数
def battle_score(bg, color, fnt):
    bg.fill(WHITE)
    score_player = 0
    score_cpu = 0
    pygame.draw.circle(bg, BLACK, (270, 100), 60, 0)
    pygame.draw.circle(bg, BLACK, (270, 100), 60, 0)
    txt_pl_score = fnt.render(str(score_player), True, pl_cl[color])
    bg.blit(txt_pl_score, [240, 70])
    pygame.draw.circle(bg, BLACK, (480, 100), 60, 0)
    txt_cp_score = fnt.render(str(score_cpu), True, cp_cl[color])
    bg.blit(txt_cp_score, [450, 70])

    for y in range(1, FIELD_Y-1, 1):
        for x in range(1, FIELD_X-1, 1):
            if field[y][x] == 1 or field[y][x] == 11:
                score_player = score_player + 1
                pygame.draw.circle(bg, BLACK, (270, 100), 60, 0)
                txt_pl_score = fnt.render(str(score_player), True, pl_cl[color])
                bg.blit(txt_pl_score, [240, 70])
            if field[y][x] == 2 or field[y][x] == 12:
                score_cpu = score_cpu + 1
                pygame.draw.circle(bg, BLACK, (480, 100), 60, 0)
                txt_cp_score = fnt.render(str(score_cpu), True, cp_cl[color])
                bg.blit(txt_cp_score, [450, 70])
    return score_player, score_cpu

# 全体を処理する関数
def main():
    global index, tmr, speed
    pygame.init()
    pygame.display.set_caption("Territory game")
    screen = pygame.display.set_mode((FIELD_X*50,FIELD_Y*50)) # X=750, Y=550
    clock = pygame.time.Clock()
    font_eng = pygame.font.Font(None, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.event.pump()
        key = pygame.key.get_pressed()
        tmr = tmr + 1

        if index == 0 : # タイトル画面
            screen.fill(BLACK)
            txt_title = font_eng.render("Territory game ", True, BLUE)
            txt_button = font_eng.render("Press space key", True, WHITE)
            screen.blit(txt_title, [200, 100])
            screen.blit(txt_button, [200, 400])
            if key[pygame.K_SPACE] == True:
                tmr = 0
                index = 1
        elif index == 1: # ロード画面
            game_load(screen, font_eng)
            color_field = random.randint(1,3)
            if tmr == 2:
                index = 2
                tmr = 0
        elif index == 2: # 戦闘前
            pl_x = 1
            pl_y = FIELD_Y - 2
            cp_x = FIELD_X - 2
            cp_y = 1
            make_field(pl_x, pl_y, cp_x, cp_y)
            draw_field(screen, color_field)
            if tmr > 5:
                if key[pygame.K_SPACE] == True:
                    index = 3
                    tmr = 0
        elif index == 3: # 戦闘中
            move_pl = move_player(pl_x, pl_y)
            pl_x = move_pl[0]
            pl_y = move_pl[1]
            move_cp = move_cpu(cp_x, cp_y)
            cp_x = move_cp[0]
            cp_y = move_cp[1]
            draw_field(screen, color_field)
            battle_time(screen, font_eng, tmr, speed)
            if tmr > 60*speed:
                index = 4
                tmr = 0
        elif index == 4: # 戦闘後勝敗判定
            txt_end = font_eng.render("Time up!", True, RED)
            screen.blit(txt_end, [300, 200])
            if tmr == 5:
                score = battle_score(screen, color_field, font_eng)
                score_pl = score[0]
                score_cp = score[1]
                if tmr == 5:
                    if score_pl > score_cp:
                        index = 6
                        tmr = 0
                    elif score_pl < score_cp:
                        index = 7
                        tmr = 0
                    else:
                        index = 8
                        tmr = 0 
        elif index == 6: # playerの勝利
            txt_win = font_eng.render("You Win!", True, pl_cl[color_field])
            screen.blit(txt_win, [300, 200])
            if tmr == 10:
                index = 0
                tmr = 0
        elif index == 7: # cpuの勝利
            txt_lose = font_eng.render("You lose...", True, pl_cl[color_field])
            screen.blit(txt_lose, [270, 200])
            if tmr == 10:
                index = 0
                tmr = 0
        elif index == 8: # 同点
            txt_draw = font_eng.render("Draw", True, pl_cl[color_field])
            screen.blit(txt_draw, [360, 200])
            if tmr == 10:
                index = 0
                tmr = 0

        # print(index,tmr) 全体で重要な変数の管理（テスト時）
        pygame.display.update()
        clock.tick(speed)
        
if __name__ == '__main__':
    main()
