import pygame
import os
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 800 на 600
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

FPS = 60

pygame.display.set_caption("Yandex project")

travplatlf = (576, 720, 70, 70)
travplatrt = (576, 576, 70, 70)
travplat = (504, 576, 70, 70)
kamplatleft = (432, 720, 70, 40)
kamplatsr = (648, 648, 70, 40)
kamplatrt = (792, 648, 70, 40)


class Platform(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet_data):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("data/tiles_spritesheet.png")
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])
        self.rect = self.image.get_rect()


class plat_mov(Platform):
    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    left_bn = 0
    right_bn = 0

    level = None
    gamer = None

    def update(self):
        self.rect.x += self.change_x
        hit = pygame.sprite.collide_rect(self, self.gamer)
        if hit:
            if self.change_x < 0:
                self.gamer.rect.right = self.rect.left
            else:
                self.gamer.rect.left = self.rect.right

        self.rect.y += self.change_y

        hit = pygame.sprite.collide_rect(self, self.gamer)
        if hit:
            if self.change_y < 0:
                self.gamer.rect.bottom = self.rect.top
            else:
                self.gamer.rect.top = self.rect.bottom

        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.wldshf
        if cur_pos < self.left_bn or cur_pos > self.right_bn:
            self.change_x *= -1


class Gamer(pygame.sprite.Sprite):
    global_x = 0
    change_x = 0
    change_y = 0

    walking_frames_l = []
    walking_frames_r = []

    direction = "R"

    level = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("data/p1_walk.png")

        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x

        pos = self.rect.x + self.level.wldshf
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        block_hit_list = pygame.sprite.spritecollide(self, self.level.mas_plat, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.mas_plat, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

            if isinstance(block, plat_mov):
                self.rect.x += block.change_x

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.mas_plat, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        self.change_x = -6
        self.direction = "L"

    def go_right(self):
        self.change_x = 6
        self.direction = "R"

    def stop(self):
        self.change_x = 0


class Level():
    mas_plat = None
    mas_en = None
    bckgrn = None

    wldshf = 0
    lim = -1000

    def __init__(self, gamer):
        self.mas_plat = pygame.sprite.Group()
        self.mas_en = pygame.sprite.Group()
        self.gamer = gamer

    def update(self):
        self.mas_plat.update()
        self.mas_en.update()

    def draw(self, screen):
        screen.fill((0, 0, 255))
        screen.blit(self.bckgrn, (self.wldshf // 3, 0))

        self.mas_plat.draw(screen)
        self.mas_en.draw(screen)

    def shift_world(self, shift_x):

        self.wldshf += shift_x

        for platform in self.mas_plat:
            platform.rect.x += shift_x

        for enemy in self.mas_en:
            enemy.rect.x += shift_x


class lvl1(Level):

    def __init__(self, gamer):
        Level.__init__(self, gamer)

        self.bckgrn = pygame.image.load("data/bg1.png").convert()
        self.bckgrn.set_colorkey((255, 255, 255))
        self.lim = -2500
        # массив платформ
        level = [[travplatlf, 500, 500],

                 [travplat, 90, 400],
                 [travplat, 90, 450],
                 [travplat, 90, 500],

                 [travplat, 90, 550],
                 [travplat, 90, 600],
                 [travplat, 90, 650],

                 [travplat, 20, 400],
                 [travplat, 20, 450],
                 [travplat, 20, 500],

                 [travplat, 20, 550],
                 [travplat, 20, 600],
                 [travplat, 20, 650],

                 [travplat, -50, 400],
                 [travplat, -50, 450],
                 [travplat, -50, 500],

                 [travplat, -50, 550],
                 [travplat, -50, 600],
                 [travplat, -50, 650],

                 [travplat, 570, 500],
                 [travplatrt, 640, 500],
                 [travplatlf, 800, 400],
                 [travplat, 870, 400],
                 [travplatrt, 940, 400],
                 [travplatlf, 1000, 500],
                 [travplat, 1070, 500],
                 [travplatrt, 1140, 500],
                 [kamplatleft, 1120, 280],
                 [kamplatsr, 1190, 280],
                 [kamplatrt, 1260, 280],
                 ]

        for platform in level:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.gamer = self.gamer
            self.mas_plat.add(block)

        block = plat_mov(kamplatsr)
        block.rect.x = 1350
        block.rect.y = 280
        block.left_bn = 1350
        block.right_bn = 1600
        block.change_x = 1
        block.gamer = self.gamer
        block.level = self
        self.mas_plat.add(block)


class lvl2(Level):

    def __init__(self, gamer):
        Level.__init__(self, gamer)

        self.bckgrn = pygame.image.load("data/bg2.png").convert()
        self.bckgrn.set_colorkey((255, 255, 255))
        self.lim = -1000
        # массив с платформами
        level = [[kamplatleft, 500, 550],

                 [travplat, 90, 400],
                 [travplat, 90, 450],
                 [travplat, 90, 500],

                 [travplat, 90, 550],
                 [travplat, 90, 600],
                 [travplat, 90, 650],

                 [travplat, 20, 400],
                 [travplat, 20, 450],
                 [travplat, 20, 500],

                 [travplat, 20, 550],
                 [travplat, 20, 600],
                 [travplat, 20, 650],

                 [travplat, -50, 400],
                 [travplat, -50, 450],
                 [travplat, -50, 500],

                 [travplat, -50, 550],
                 [travplat, -50, 600],
                 [travplat, -50, 650],

                 [kamplatsr, 570, 550],
                 [kamplatrt, 640, 550],
                 [travplatlf, 800, 400],
                 [travplat, 870, 400],
                 [travplatrt, 940, 400],
                 [travplatlf, 1000, 500],
                 [travplat, 1070, 500],
                 [travplatrt, 1140, 500],
                 [kamplatleft, 1120, 280],
                 [kamplatsr, 1190, 280],
                 [kamplatrt, 1260, 280],
                 ]
        for platform in level:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.gamer = self.gamer
            self.mas_plat.add(block)

        block = plat_mov(kamplatsr)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.gamer = self.gamer
        block.level = self
        self.mas_plat.add(block)


class SpriteSheet(object):
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))
        return image


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    '''
    Прерывание игры
    :return:
    '''
    pygame.quit()
    sys.exit()


def game_win():
    image = load_image("you.jpg")
    x = -800
    y = 0
    v = 400
    running = True
    while running:

        screen.fill((0, 0, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(image, (int(x), int(y)))
        clock.tick(FPS)
        if x < -1:
            x += v / FPS
        pygame.display.flip()

    terminate()


def main():
    gamer = Gamer()

    ##
    pygame.mixer.music.load('data/bck_music.mp3')
    pygame.mixer.music.play(-1)
    ##

    # Создание уровней

    lvl_list = []
    lvl_list.append(lvl1(gamer))
    lvl_list.append(lvl2(gamer))

    cur_lvl_no = 0
    cur_lvl = lvl_list[cur_lvl_no]

    all_sprites = pygame.sprite.Group()
    gamer.level = cur_lvl

    gamer.rect.x = 340
    gamer.rect.y = SCREEN_HEIGHT - gamer.rect.height
    all_sprites.add(gamer)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gamer.go_left()
                if event.key == pygame.K_RIGHT:
                    gamer.go_right()
                if event.key == pygame.K_UP:
                    gamer.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and gamer.change_x < 0:
                    gamer.stop()
                if event.key == pygame.K_RIGHT and gamer.change_x > 0:
                    gamer.stop()

        all_sprites.update()
        cur_lvl.update()
        pos = gamer.rect.x + cur_lvl.wldshf

        if gamer.rect.x >= 500:
            diff = gamer.rect.x - 500
            gamer.rect.x = 500
            cur_lvl.shift_world(-diff)

        # print(gamer.rect.x)

        if gamer.rect.x <= 120:
            diff = 120 - gamer.rect.x
            gamer.rect.x = 120
            cur_lvl.shift_world(diff)

        # Если игрок доходит до конца уровня
        # загружаутся следующий уровень

        pos = gamer.rect.x + cur_lvl.wldshf
        if pos < cur_lvl.lim:
            gamer.rect.x = 120

            if cur_lvl_no == len(lvl_list) - 1:
                game_win()

            if cur_lvl_no < len(lvl_list) - 1:
                cur_lvl_no += 1
                cur_lvl = lvl_list[cur_lvl_no]
                gamer.level = cur_lvl
                gamer.rect.x = 340

        cur_lvl.draw(screen)
        all_sprites.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


def start_screen():
    '''
    Начальная заставка с кнопками
    :return:
    '''

    font = pygame.font.Font('./data/Amatic-Bold.ttf', 36)
    screen.fill((0, 0, 0))
    button = load_image('button.png')

    screen.blit(button, (300, 200))
    render = font.render('START GAME', 1, pygame.Color('darkgreen'))
    intro_rect = render.get_rect().move(350, 200)
    screen.blit(render, intro_rect)

    screen.blit(button, (300, 250))
    render = font.render('EXIT', 1, pygame.Color('red'))
    intro_rect = render.get_rect().move(360, 250)
    screen.blit(render, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 300 <= event.pos[0] <= 500 and 200 <= event.pos[1] <= 245:
                    main()
                    return
                if 300 <= event.pos[0] <= 500 and 250 <= event.pos[1] <= 295:
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
