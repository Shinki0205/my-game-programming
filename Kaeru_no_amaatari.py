import pygame
import sys
import random

# 色の設定
BLACK = (  0,  0,  0) # 黒色
GRAY  = ( 80, 80, 80) # 灰色
WHITE = (255,255,255) # 白色
RED   = (255,  0,  0) # 赤色
BLUE  = (178,178,255) # 青色
GREEN = ( 51,255, 51) # 緑色

field = []
for y in range(10):
    field.append([0]*7)
    
# 画像の取込み
imgKaeru   = pygame.image.load("kaeru.png")
imgCloud   = pygame.image.load("cloud.png")
imgLock    = pygame.image.load("lock.png")
imgAme     = pygame.image.load("amamizu.png")
imgKaraame = pygame.image.load("karaamamizu.png")
img_Kaeru = pygame.transform.scale(imgKaeru, [50, 50])
img_Cloud = pygame.transform.scale(imgCloud, [250, 50])
img_Lock  = pygame.transform.scale(imgLock, [50, 50])
img_Ame   = pygame.transform.scale(imgAme, [50, 50])
img_STame   = pygame.transform.scale(imgAme, [30, 30])
img_KRame = pygame.transform.scale(imgKaraame, [30, 30])

index = 0 # 画面遷移変数
tmr = 0 # 時間管理変数
speed = 2 # 処理時間管理変数
score = 0 # スコア
best_score = 0 # ベストスコア
ame = 3 # ame管理変数

# 画面の背景を生成する関数
'''
fieldの値
０：スコア表示画面
１：空
２：カエル
３：雨水
４：岩
９：床（スコア表示画面とあまり変わらない）
１０：枠外（move_kaeruの処理の際にインデントエラーを起こさないようにする）
'''
def make_field(player_x, player_y):
    global field
    for y in range(10):
        for x in range(7):
            if y == 0: # スコア表示画面
                field[y][x] = 0
            elif y == 9: # 床
                field[y][x] = 9
            elif x == 0 or x == 6: # 枠外
                field[y][x] = 10
            else: # 青空
                field[y][x] = 1
    field[player_y][player_x] = 2 # カエルの座標

# 画面を塗る関数
def draw_field(bg):
    bg.fill(BLACK)
    for y in range(10):
        for x in range(1, 6, 1):
            X = (x-1) * 50
            Y = y * 50
            if field[y][x] == 0: # スコア表示画面
                pygame.draw.rect(bg, BLACK, [X, Y, 50, 50])
            if field[y][x] == 9: # 床
                pygame.draw.rect(bg, GRAY, [X, Y, 50, 50])
            if field[y][x] == 1 or field[y][x] == 2: # 空
                pygame.draw.rect(bg, BLUE, [X, Y, 50, 50])
            if field[y][x] == 2: # カエル
                bg.blit(img_Kaeru, [X,Y])
            if index == 1:
                if field[y][x] == 3: # ame
                    pygame.draw.rect(bg, BLUE, [X, Y, 50, 50])
                    bg.blit(img_Ame, [X,Y])
                if field[y][x] == 4: # 岩
                    pygame.draw.rect(bg, BLUE, [X, Y, 50, 50])
                    bg.blit(img_Lock, [X,Y])
    
    if index == 1: # 曇
        bg.blit(img_Cloud, [0, 50])

# Kaeruを動かす関数
def move_kaeru(ky, player_x, player_y):
    global field
    if ky[pygame.K_LEFT] == 1: # 左に移動
        if field[player_y][player_x-1] != 10:
            field[player_y][player_x-1] = 2
            field[player_y][player_x] = 1
            player_x = player_x - 1
    elif ky[pygame.K_RIGHT] == 1: # 右に移動 
        if field[player_y][player_x+1] != 10:
            field[player_y][player_x+1] = 2
            field[player_y][player_x] = 1
            player_x = player_x + 1 
    return player_x

# 障害物を生成する関数
def make_item():
    global field
    if (tmr-1)%5 == 0:
        for i in range(5):
            atem_int = random.randint(1,100)
            '''
　　　　　　tmrの値によってAmeと空の出現量を調整
            '''
            if tmr < 50:
                if atem_int >= 1 and atem_int <= 15:
                    field[1][i+1] = 3
                elif atem_int <= 50:
                    field[1][i+1] = 4
            elif tmr < 100:
                if atem_int >= 1 and atem_int <= 15:
                    field[1][i+1] = 3
                elif atem_int <= 55:
                    field[1][i+1] = 4
            else:
                if atem_int >= 1 and atem_int <= 10:
                    field[1][i+1] = 3
                elif atem_int <= 70:
                    field[1][i+1] = 4

# 障害物を移動させる関数
def move_item():
    global field, ame
    for y in range(9, 0, -1):
        for x in range(1, 6, 1):
            if field[y][x] == 4:
                '''
                下にカエルがいるときはゲーム終了となるため-1で返す。
                また、下が床の時は岩は消滅、何もない時は１つ下げる。
                '''
                if field[y+1][x] == 2:
                    field[y+1][x] = 4
                    field[y][x] = 1
                    return -1
                elif field[y+1][x] == 9:
                    field[y][x] = 1
                else:
                    field[y+1][x] = 4
                    field[y][x] = 1
            elif field[y][x] == 3:
                '''
                下にカエルがいるときはameを一つ増やす。
                また、下が床の時と何もない時は岩同様の処理を行う。
                '''
                if field[y+1][x] == 2:
                    field[y][x] = 1
                    ame = ame + 1
                elif field[y+1][x] == 9:
                    field[y][x] = 1
                else:
                    field[y+1][x] = 3
                    field[y][x] = 1
    return 0 # ０を返す時はプレイ継続

# タイトルを描画する関数
def draw_title(bg, fnt):
    txt_title = fnt.render("Kaeru no Amaatari", True, GREEN)
    txt_start = fnt.render("play start!", True, WHITE)
    txt_buttom= fnt.render("Press space key", True, WHITE)
    txt_bscore= fnt.render("best score", True, RED)
    txt_bten  = fnt.render(str(best_score), True, WHITE)
    bg.blit(txt_title, [50,80])
    bg.blit(txt_start, [80,270])
    bg.blit(txt_buttom, [60, 300])
    bg.blit(txt_bscore, [160, 0])
    bg.blit(txt_bten, [160, 25])

# ゲーム管理を行う関数
def game_manage(bg, fnt):
    global score, best_score, ame, speed
    if ame >= 4 :
        ame = 3
    score = score + speed * ame
    if score > best_score:
        best_score = score
    txt_score = fnt.render("score", True, RED)
    txt_ten = fnt.render(str(score), True, WHITE)
    bg.blit(txt_score, [100, 0])
    bg.blit(txt_ten, [100, 25])

    # tmrの値によりspeedを上げる
    if tmr == 50:
        speed = 3
    elif tmr == 100:
        speed = 4
    '''
    tmrが１５進むごとにameが一つ減り
    ameの数が０になったらゲーム終了となり-1を返す
    '''
    if tmr%15 == 0:
        ame = ame - 1
    for x in range(3):
        X = x * 30
        if x+1 <= ame:
            bg.blit(img_STame, [X,0])
        else:
            bg.blit(img_KRame, [X,0])
    if ame == 0:
        return -1
    return 0 # ゲーム継続

# 全体を管理する関数
def main():
    global index, tmr, speed, score, ame
    pygame.init()
    pygame.display.set_caption("Kaeru No Amaatari")
    screen = pygame.display.set_mode((250, 500))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 25)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.event.pump()
        key = pygame.key.get_pressed()

        if index == 0: # タイトル画面
            pl_x = 3
            pl_y = 8
            make_field(pl_x, pl_y)
            draw_field(screen)
            draw_title(screen, font)
            if key[pygame.K_SPACE] == True:
                tmr = 0
                index = 1
                score = 0
                ame = 3
        elif index == 1: # ゲームメイン画面
            make_item()
            pl_x = int(move_kaeru(key, pl_x, pl_y))
            flag_a = move_item()
            draw_field(screen)
            flag_b = game_manage(screen, font)
            if flag_a == -1 or flag_b == -1:
                index = 2
                tmr = 0
                speed = 2
        elif index == 2: # リザルト画面
            txt_end = font.render("game set!", True, RED)
            screen.blit(txt_end, [80, 230])
            if tmr > 5:
                index = 0

        tmr = tmr + 1
        # print(index, tmr, speed) # プログラム内の重要な変数を出力（テスト時）
        pygame.display.update()
        clock.tick(speed)
            
if __name__ == '__main__':
    main()
