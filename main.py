import pygame
import random
from player import Player
from bullet import Bullet
from asteroid import Asteroid

pygame.init()

sw = 800
sh = 800

bg = pygame.image.load('img/background.png')

pygame.display.set_caption('Asteroids')
screen = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()

gameover = False
lives = 3
score = 0
rapid_fire = False
fire_start = -1
high_score = 0


def redraw_game_window():
    screen.blit(bg, (0, 0))
    font = pygame.font.SysFont('arial', 30)
    lives_text = font.render('Lives: ' + str(lives), 1, (255, 255, 255))
    play_again_text = font.render('Press Tab to Play Again', 1, (255, 255, 255))
    score_text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    high_score_text = font.render('High Score: ' + str(high_score), 1, (255, 255, 255))

    player.draw(screen)
    for a in asteroids:
        a.draw(screen)
    for b in bullets:
        b.draw(screen)

    if rapid_fire:
        pygame.draw.rect(screen, (0, 0, 0), [sw // 2 - 51, 19, 102, 22])
        pygame.draw.rect(screen, (255, 255, 255), [sw // 2 - 50, 20, 100 - 100 * (count - fire_start) / 500, 20])

    if gameover:
        screen.blit(play_again_text,
                    (sw // 2 - play_again_text.get_width() // 2, sh // 2 - play_again_text.get_height() // 2))
    screen.blit(score_text, (sw - score_text.get_width() - 25, 25))
    screen.blit(lives_text, (25, 25))
    screen.blit(high_score_text, (sw - high_score_text.get_width() - 25, 35 + score_text.get_height()))
    pygame.display.update()


player = Player()
bullets = []
asteroids = []
count = 0
run = True
while run:
    clock.tick(60)
    count += 1
    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1, 1, 1, 2, 2, 3])
            asteroids.append(Asteroid(ran))

        player.update_location()
        for b in bullets:
            b.move()
            if b.check_off_screen():
                bullets.pop(bullets.index(b))

        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            if (player.x - player.w // 2 <= a.x <= player.x + player.w // 2) or (
                    player.x + player.w // 2 >= a.x + a.w >= player.x - player.w // 2):
                if (player.y - player.h // 2 <= a.y <= player.y + player.h // 2) or (
                        player.y - player.h // 2 <= a.y + a.h <= player.y + player.h // 2):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    break

            for b in bullets:
                if (a.x <= b.x <= a.x + a.w) or a.x <= b.x + b.w <= a.x + a.w:
                    if a.y <= b.y <= a.y + a.h or a.y <= b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                            score += 10
                            na1 = Asteroid(2)
                            na2 = Asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            score += 20
                            na1 = Asteroid(1)
                            na2 = Asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                        asteroids.pop(asteroids.index(a))
                        bullets.pop(bullets.index(b))
                        break

        if lives <= 0:
            gameover = True

        if fire_start != -1:
            if count - fire_start > 500:
                rapid_fire = False
                fire_start = -1

        player.move_forward()
        player.speed_up(-1)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turn_left()
        if keys[pygame.K_RIGHT]:
            player.turn_right()
        if keys[pygame.K_UP]:
            player.speed_up(2)
        if keys[pygame.K_SPACE]:
            if rapid_fire:
                bullets.append(Bullet(player))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    if not rapid_fire:
                        bullets.append(Bullet(player))
            if event.key == pygame.K_TAB:
                if gameover:
                    gameover = False
                    lives = 3
                    asteroids.clear()
                    player.x = sw // 2
                    player.y = sh // 2
                    if score > high_score:
                        high_score = score
                    score = 0
    redraw_game_window()
pygame.quit()
