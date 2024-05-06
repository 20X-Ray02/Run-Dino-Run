import pygame
import random

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Run Dino! Run!')

# Музыка
jump_sound = pygame.mixer.Sound('music/Rrr.wav')
fall_sound = pygame.mixer.Sound('music/Bdish.wav')
loss_sound = pygame.mixer.Sound('music/loss.wav')
heart_plus_sound = pygame.mixer.Sound('music/hp+.wav')
button_sound = pygame.mixer.Sound('music/button.wav')
bullet_sound = pygame.mixer.Sound('music/shot.wav')

# картинки
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

cactus_img = [pygame.image.load('img/Cactus0.png'), pygame.image.load('img/Cactus1.png'), pygame.image.load('img/Cactus2.png')]
cactus_options = [69, 449, 37, 410, 40, 420]

stone_img = [pygame.image.load('img/Stone0.png'), pygame.image.load('img/Stone1.png')]
cloud_img = [pygame.image.load('img/Cloud0.png'), pygame.image.load('img/Cloud1.png')]

dino_img = [pygame.image.load('img/Dino0.png'), pygame.image.load('img/Dino1.png'), pygame.image.load('img/Dino2.png'),
            pygame.image.load('img/Dino3.png'), pygame.image.load('img/Dino4.png')]

bird_img = [pygame.image.load('img/Bird0.png'), pygame.image.load('img/Bird1.png'), pygame.image.load('img/Bird2.png'),
            pygame.image.load('img/Bird3.png'), pygame.image.load('img/Bird4.png'), pygame.image.load('img/Bird5.png')]

light_img = [pygame.image.load('img/Light0.png'), pygame.image.load('img/Light1.png'), pygame.image.load('img/Light2.png'),
            pygame.image.load('img/Light3.png'), pygame.image.load('img/Light4.png'), pygame.image.load('img/Light5.png'),
            pygame.image.load('img/Light6.png'), pygame.image.load('img/Light7.png'), pygame.image.load('img/Light8.png'),
            pygame.image.load('img/Light9.png'), pygame.image.load('img/Light10.png')]


health_img = pygame.image.load('img/heart.png')
health_img = pygame.transform.scale(health_img, (30, 30))

bullet_img = pygame.image.load('img/shot.png')
bullet_img = pygame.transform.scale(bullet_img, (30, 9))

img_counter = 0
health = 2

class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        # Передвижение кактуса
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            self.x = display_width + 100 + random.randrange(-80, 60)
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = (23, 204, 58)
        self.active_clr = (13, 162, 58)
        self.draw_effects = False
        self.clear_effects = False
        self.rect_h = 10
        self.rect_w = width

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        self.draw_beatiful_rect(mouse[0], mouse[1], x, y)
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)

    def draw_beatiful_rect(self, ms_x, ms_y, x, y):
        if x <= ms_x <= x + self.width and y <= ms_y <= y + self.height:
            self.draw_effects = True

        if self.draw_effects:
            if ms_x < x or ms_x > x + self.width or ms_y < y or ms_y > y + self.height:
                self.clear_effects = True
                self.draw_effects = False

            if self.rect_h < self.height:
                self.rect_h += (self.height - 10) / 40

        if self.clear_effects and not self.draw_effects:
            if self.rect_h > 10:
                self.rect_h -= (self.height - 10) / 40
            else:
                self.clear_effects = False

        draw_y = y + self.height - self.rect_h
        pygame.draw.rect(display, self.active_clr, (x, draw_y, self.rect_w, self.rect_h))


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = 8
        self.speed_y = 0
        self.dest_x = 0
        self.dest_y = 0

    def move(self):
        self.x += self.speed_x
        if self.x <= display_width:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False

    def find_path(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y

        delta_x = dest_x - self.x
        count_up = delta_x // self.speed_x

        if self.y >= dest_y:
            delta_y = self.y - dest_y
            self.speed_y = delta_y / count_up
        else:
            delta_y = dest_y - self.y
            self.speed_y = -(delta_y / count_up)

    def move_to(self, reverse=False):
        if not reverse:
            self.x += self.speed_x
            self.y -= self.speed_y
        else:
            self.x -= self.speed_x
            self.y += self.speed_y

        if self.x <= display_width and not reverse:
            display.blit(bullet_img, (self.x, self.y))
            return True
        elif self.x >= 0 and reverse:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False


class Bird:
    def __init__(self, away_y):
        self.x = self.x = random.randrange(550, 730)
        self.y = away_y
        self.width = 105
        self.height = 55
        self.ay = away_y
        self.speed = 3
        self.dest_y = self.speed * random.randrange(20, 70)
        self.img_cnt = 0
        self.cd_hide = 0
        self.come = True
        self.go_away = False
        self.cd_shoot = 0
        self.all_bullets = []

    def draw(self):
        if self.img_cnt == 30:
            self.img_cnt = 0

        display.blit(bird_img[self.img_cnt // 5], (self.x, self.y))
        self.img_cnt += 1

        if self.come and self.cd_hide == 0:
            return 1
        elif self.go_away:
            return 2
        elif self.cd_hide > 0:
            self.cd_hide -= 1

        return 0

    def show(self):
        if self.y < self.dest_y:
            self.y += self.speed
        else:
            self.come = False
            self.go_away = True
            self.dest_y = self.ay

    def hide(self):
        if self.y > self.dest_y:
            self.y -= self.speed
        else:
            self.come = True
            self.go_away = False
            self.x = random.randrange(550, 730)
            self.dest_y = self.speed * random.randrange(20, 70)
            self.cd_hide = 80

    def check_dmg(self, bullet):
        if self.x <= bullet.x <= self.x + self.width:
            if self.y <= bullet.y <= self.y + self.height:
                self.go_away = True

    def shoot(self):
        if not self.cd_shoot:
            pygame.mixer.Sound.play(bullet_sound)

            new_bullet = Bullet(self.x, self.y)
            new_bullet.find_path(usr_x + usr_width // 2, usr_y + usr_height // 2)

            self.all_bullets.append(new_bullet)
            self.cd_shoot = 200
        else:
            self.cd_shoot -= 1

        for bullet in self.all_bullets:
            if not bullet.move_to(reverse=True):
                self.all_bullets.remove(bullet)


# параметры персонажа
usr_width = 60
usr_height = 100
usr_x = display_width // 3  # Начальная позиция
usr_y = display_height - usr_height - 100

# параметры кактуса
cactus_width = 20
cactus_height = 70
cactus_x = display_width - 50
cactus_y = display_height - cactus_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0
max_scores = 0
max_above = 0

cooldown = 0

mouse_counter = 0
need_draw_click = False

def show_menu():
    menu_bckgr = pygame.image.load('img/Menu.jpg')
    show = True

    pygame.mixer.music.load('music/Big_Slinker.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    start_btn = Button(288, 70)
    quit_btn = Button(120, 70)

    while show:
        for event in pygame.event.get():
            # Закрытие окна при нажатии крестика
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(menu_bckgr, (0, 0))
        start_btn.draw(270, 200, 'Start game', start_game, 50)
        quit_btn. draw(358, 300, 'Quit', quit, 50)

        draw_mouse()

        pygame.display.update()
        clock.tick(60)


def start_game():
    global scores, make_jump, jump_counter, usr_y, health, cooldown

    pygame.mixer.music.load('music/background.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    cooldown = 0

    while game_cycle():
        scores = 0
        make_jump = False
        jump_counter = 30
        usr_y = display_height - usr_height - 100
        health = 2


def game_cycle():
    global make_jump, cooldown

    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load(r'img/Land.jpg')

    stone, cloud = open_random_objects()
    heart = Object(display_width, 280, 30, health_img, 4)

    all_btn_bullets = []
    all_ms_bullets = []

    button = Button(100, 50)

    bird1 = Bird(-80)
    bird2 = Bird(-49)

    all_birds = [bird1, bird2]

    while game:
        for event in pygame.event.get():
            # Закрытие окна при нажатии крестика
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Если нажата клавиша пробела, моделька прыгает
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_UP]:
            pygame.mixer.Sound.play(jump_sound)

        if make_jump:
            jump()

        count_scores(cactus_arr)

        display.blit(land, (0, 0))
        print_text('Scores: ' + str(scores), 600, 10)

        button.draw(20, 100, 'wow')

        draw_array(cactus_arr)
        move_objects(stone, cloud)

        # pygame.draw.rect(display, (247, 240, 22), (usr_x, usr_y, usr_width, usr_height))
        draw_dino()

        if check_collision(cactus_arr):
            # pygame.mixer.music.stop()
            # pygame.mixer.Sound.play(fall_sound)
            # if not check_health():
            game = False

        if keys[pygame.K_ESCAPE]:
            pause()

        if not cooldown:
            if keys[pygame.K_x]:
                pygame.mixer.Sound.play(button_sound)
                all_btn_bullets.append(Bullet(usr_x + usr_width, usr_y + 28))
                cooldown = 50
            elif click[0]:
                pygame.mixer.Sound.play(bullet_sound)
                add_bullet = Bullet(usr_x + usr_width, usr_y + 28)
                add_bullet.find_path(mouse[0], mouse[1])

                all_ms_bullets.append(add_bullet)
                cooldown = 50
        else:
            print_text('Cooldown time: ' + str(cooldown // 10), 482, 40)
            cooldown -= 1

        for bullet in all_btn_bullets:
            if not bullet.move():
                all_btn_bullets.remove(bullet)

        for bullet in all_ms_bullets:
            if not bullet.move_to():
                all_ms_bullets.remove(bullet)

        heart.move()
        hearts_plus(heart)

        show_health()

        draw_birds(all_birds)
        check_birds_dmg(all_ms_bullets, all_birds)

        draw_mouse()

        pygame.display.update()
        clock.tick(70)
    return game_over()


def jump():
    global usr_y, make_jump, jump_counter

    if jump_counter >= -30:
        if jump_counter == 30:
            pygame.mixer.Sound.play(jump_sound)
        if jump_counter == -28:
            pygame.mixer.Sound.play(fall_sound)

        usr_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 280
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(250, 400)

    return radius


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            object_return(array, cactus)


def open_random_objects():
    choice = random.randrange(0, 2)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
    cloud = Object(display_width, 80, 70, img_of_cloud, 2)

    return stone, cloud


def move_objects(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(10, 200), cloud.width, img_of_cloud)


def draw_dino():
    global img_counter
    if img_counter == 30:
        img_counter = 0
    display.blit(dino_img[img_counter // 6], (usr_x, usr_y))
    img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True

    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Paused. Press enter to continue', 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)

    pygame.mixer.music.unpause()


def check_collision(barriers):
    for barrier in barriers:
        if barrier.y == 449:
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 22 <= barrier.x + barrier.width:
                    if check_health():
                        object_return(barriers, barrier)
                        return False
                    else:
                        return True
            elif jump_counter >= 0:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 22 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            else:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
        else:
            if not make_jump:
                if barrier.x <= usr_x + usr_width + 5 <= barrier.x + barrier.width:
                    if check_health():
                        object_return(barriers, barrier)
                        return False
                    else:
                        return True
            elif jump_counter == 10:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 5 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            elif jump_counter <= 1:
                if usr_y + usr_height - 2 >= barrier.y:
                    if barrier.x <= usr_x + 13 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            elif jump_counter >= 1:
                if usr_y + usr_height - 2 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 22 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            else:
                if usr_y + usr_height - 3 >= barrier.y:
                    if barrier.x <= usr_x + usr_width + 5 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True

    return False


def game_over():
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores

    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over. Press Enter to play again, Esc to exit', 40, 250)
        print_text('Max scores: ' + str(max_scores), 300, 350)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)


def count_scores(barriers):
    global scores, max_above
    above_cactus = 0

    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + usr_height - 5 <= barrier.y:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    above_cactus += 1
                elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                    above_cactus += 1

        max_above = max(max_above, above_cactus)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0


def show_health():
    global health
    show = 0
    x = 20
    while show != health:
        display.blit(health_img, (x, 20))
        x += 40
        show += 1


def check_health():
    global health
    health -= 1
    if health == 0:
        pygame.mixer.Sound.play(loss_sound)
        return False
    else:
        pygame.mixer.Sound.play(fall_sound)
        return True


def object_return(objects, obj):
    radius = find_radius(objects)

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]

    obj.return_self(radius, height, width, img)


def hearts_plus(heart):
    global health, usr_x, usr_y, usr_width, usr_height

    if heart.x <= -heart.width:
        radius = display_width + random.randrange(500, 1700)
        heart.return_self(radius, heart.y, heart.width, heart.image)

    if usr_x <= heart.x <= usr_x + usr_width:
        if usr_y <= heart.y <= usr_y + usr_height:
            pygame.mixer.Sound.play(heart_plus_sound)
            if health < 5:
                health += 1

            radius = display_width + random.randrange(500, 1700)
            heart.return_self(radius, heart.y, heart.width, heart.image)


def draw_birds(birds):
    for bird in birds:
        action = bird.draw()
        if action == 1:
            bird.show()
        elif action == 2:
            bird.hide()
        else:
            bird.shoot()


def check_birds_dmg(bullets, birds):
    for bird in birds:
        for bullet in bullets:
            bird.check_dmg(bullet)


def draw_mouse():
    global mouse_counter, need_draw_click
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    mouse_size = [10, 12, 16, 20, 28, 34, 40, 45, 48, 54, 58]

    if click[0] or click[1]:
        need_draw_click = True

    if need_draw_click:
        draw_x = mouse[0] - mouse_size[mouse_counter] // 2
        draw_y = mouse[1] - mouse_size[mouse_counter] // 2

        display.blit(light_img[mouse_counter], (draw_x, draw_y))
        mouse_counter += 1

        if mouse_counter == 10:
            mouse_counter = 0
            need_draw_click = False


show_menu()
pygame.quit()
quit()
