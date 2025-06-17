import os
import sys
import pygame as pg
import random
import time
import math


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, +5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (+5, 0),}


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = get_kk_img((0, 0))
    bb_img = pg.Surface((20, 20))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    clock = pg.time.Clock()
    tmr = 0
    vx = +5
    vy = +5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)

        bb_imgs, bb_accs = init_bb_imgs()
        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_img.set_colorkey((0, 0, 0))
        bb_rct.move_ip(avx, avy)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        kk_img = get_kk_img(tuple(sum_mv))

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に半透明の黒い画面上に「Game Over」と表示し、
    泣いているこうかとん画像を張り付ける関数
    """
    fin_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(fin_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 0)
    fin_img.set_alpha(128)
    screen.blit(fin_img, [0, 0])

    kk2_img = pg.image.load("fig/8.png")
    screen.blit(kk2_img, [320, 300])
    screen.blit(kk2_img, [750, 300])

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    screen.blit(txt, [400, 300])

    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと
    加速度リストを返す
    """
    bb_accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return tuple(bb_imgs), tuple(bb_accs)


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    移動量の合計値タプルに対応する向きの画像Surfaceを返す
    """
    kk_img = pg.image.load("fig/3.png")
    kk_img = {(0, 0): pg.transform.rotozoom(kk_img, 0, 0.9),
                (0, -5): pg.transform.flip(pg.transform.rotozoom(kk_img, 270, 0.9), True, False),
               (+5, -5): pg.transform.flip(pg.transform.rotozoom(kk_img, 135, 0.9), False, True), 
               (+5, 0): pg.transform.flip(pg.transform.rotozoom(kk_img, 180, 0.9), False, True), 
               (+5, +5): pg.transform.flip(pg.transform.rotozoom(kk_img, 225, 0.9), False, True), 
               (0, +5): pg.transform.flip(pg.transform.rotozoom(kk_img, 90, 0.9), True, False), 
               (-5, +5): pg.transform.rotozoom(kk_img, 45, 0.9), 
               (-5, 0): pg.transform.rotozoom(kk_img, 360, 0.9), 
               (-5, -5): pg.transform.rotozoom(kk_img, 315, 0.9),
               }
    kk_img = kk_img[sum_mv]
    return kk_img


def calc_orientation(org: pg.Rect, dst: pg.Rect, current_xy: tuple[float, float]) -> tuple[float, float]:
    """
    orgから見て、dstがどこにあるのかを計算し、
    方向ベクトルをタプルで返す
    """
    v1 = dst - org
    norm = math.sqrt(v1[0]^2+v1[1]^2)
    u1 = v1 / norm
    u2 = u1 * math.sqrt(50)
    norm2 = u2^2 / 2
    return current_xy


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
