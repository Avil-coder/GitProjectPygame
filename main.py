import pygame
from random import randint
import sys

WIDTH, HEIGHT = 800, 600
R, G, B = 0, 0, 0
SPEED = 13
FPS = 13


def load_image(name):
    if name[-2:] == 'jpg':
        image = pygame.image.load(name).convert()
    else:
        image = pygame.image.load(name).convert_alpha()
    return image


pygame.init()
pygame.display.set_caption("PacSnake")
all_sprites = pygame.sprite.Group()
dot_sprites = pygame.sprite.Group()
block_sprites = pygame.sprite.Group()
heart_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((R, G, B))
font = pygame.font.Font(None, 25)
image_up = load_image("data/pacman_up3.png")
image_left = load_image("data/pacman_left3.png")
image_right = load_image("data/pacman_right3.png")
image_down = load_image("data/pacman_down3.png")
image_stop = load_image("data/pacman_stop.png")
dot_image = load_image('data/Dot2.png')
blk_image = load_image('data/block.png')
heart_image = load_image('data/heart3.png')
heart_image1 = load_image('data/heart3_1.png')
heart_image2 = load_image('data/heart3_2.png')
clock = pygame.time.Clock()
running = True
all_sprites.draw(screen)
x, y = WIDTH // 2, HEIGHT // 2
score = 0
speedx, speedy = 0, 0
text = font.render("Score: "+str(score), True, (255, 255, 255))
screen.blit(text, [300, 300])
pygame.mixer.music.load('data/Sound_06985.mp3')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1, 0.0)
live_score = 0



class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, kill=False):
        super().__init__(all_sprites)
        self.kill_ = kill
        if self.kill_:
            for item in all_sprites:
                item.kill()
        else:
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, sp_x, sp_y, x, y):
        global heart_image1, heart_image2, live_score
        self.rect.x, self.rect.y = x, y
        self.rect.topleft = self.rect.x, self.rect.y
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.rect.x += sp_x
        self.rect.y += sp_y
        if pygame.sprite.spritecollideany(self, block_sprites):
            print(live_score)
            live_score += 1
            if live_score == 1:
                screen.fill((R, G, B))
                Live(True)
                Live(False, heart_image2)
                heart_sprites.draw(screen)
                self.restart()
            elif live_score == 2:
                screen.fill((R, G, B))
                Live(True)
                Live(False, heart_image1)
                heart_sprites.draw(screen)
                self.restart()
            elif live_score == 3:
                draw_game_over()

    def restart(self):
        global x, y, speedy, speedx
        pygame.mixer.music.rewind()
        screen.fill((R, G ,B))
        x, y = WIDTH // 2, HEIGHT // 2
        speedx, speedy = 0, 0
        AnimatedSprite(image_stop, 1, 1, 8, 8, True)
        AnimatedSprite(image_stop, 1, 1, 8, 8)
        for item in block_sprites:
            item.kill()



class Live(pygame.sprite.Sprite):
    def __init__(self, kill=False, heart=heart_image):
        super().__init__(heart_sprites)
        self.kill_ = kill
        if self.kill_:
            for item in heart_sprites:
                item.kill()
        else:
            self.add(heart_sprites)
            self.image = heart
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(0, 0)

class Fall_blocks(pygame.sprite.Sprite):
    def __init__(self, blk):
        super().__init__(block_sprites)
        self.image = blk
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(randint(10, WIDTH - 10), -60)

    def update(self):
        self.rect.topleft = self.rect.x, self.rect.y
        if self.rect.y >= -60:
            self.rect.y += 9
        else:
            self.kill()



class Dot(pygame.sprite.Sprite):
    def __init__(self, dot):
        super().__init__(dot_sprites)
        self.add()
        self.image = dot
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(randint(30, WIDTH - 100), randint(30, HEIGHT -150))
        self.score = 0
        self.st = 0

    def update(self):
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.rect.x = randint(0, WIDTH - 10)
            self.rect.y = randint(0, HEIGHT - 10)
            self.score += 10
            for i in range(4):
                Fall_blocks(blk_image)
        font = pygame.font.Font(None, 15)
        textSurfaceObj = font.render('Score: ' + str(self.score), True, (255, 255, 255))
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (750, 30)
        screen.blit(textSurfaceObj, textRectObj)
        if self.score != 0 and self.score % 10 == 0:
            block_sprites.update()
            block_sprites.draw(screen)

def draw_game_over():
    img_end = pygame.image.load('data/game_over.png')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        screen.fill((R, G, B))
        screen.blit(img_end, [WIDTH // 2 - 50, HEIGHT // 2 - 50])
        pygame.mixer.music.stop()
        pygame.display.update()

def game_loop():
    global x, y, running, speedy, speedx
    AnimatedSprite(image_stop, 1, 1, 8, 8)
    Dot(dot_image)
    Live(False, heart_image)
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            speedy, speedx = 0, -SPEED
            for item in all_sprites:
                item.kill()
            AnimatedSprite(image_left, 4, 1, 8, 8)
        elif keystate[pygame.K_RIGHT]:
            speedy, speedx = 0, SPEED
            for item in all_sprites:
                item.kill()
            AnimatedSprite(image_right, 4, 1, 8, 8)
        elif keystate[pygame.K_UP]:
            speedx, speedy = 0, -SPEED
            for item in all_sprites:
                item.kill()
            AnimatedSprite(image_up, 4, 1, 8, 8)
        elif keystate[pygame.K_DOWN]:
            speedx, speedy = 0, SPEED
            for item in all_sprites:
                item.kill()
            AnimatedSprite(image_down, 4, 1, 8, 8)
        x += speedx
        y += speedy
        if x < -30:
            x += WIDTH + 30
        if x > WIDTH + 30:
            x = -30
        if y < -30:
            y += HEIGHT + 30
        if y > HEIGHT + 30:
            y = -30
        screen.fill((R, G, B))
        heart_sprites.draw(screen)
        dot_sprites.update()
        dot_sprites.draw(screen)
        all_sprites.update(speedx, speedy, x, y)
        all_sprites.draw(screen)
        pygame.display.flip()

game_loop()
pygame.quit()
