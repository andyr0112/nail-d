import random
import pygame.mixer
from assets import *

class Basics:
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        pygame.display.set_caption("Nail'd!")
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.window_width, self.window_height),pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
        self.timer_limit = 6000
        self.score = 0
        self.last_nail_collected = pygame.time.get_ticks()

        self.score_text_img = pygame.image.load("images/score.png")
        self.score_text_img = pygame.transform.scale(self.score_text_img, (78, 21))

        self.time_left_img = pygame.image.load("images/time_left.png")
        self.time_left_img = pygame.transform.scale(self.time_left_img, (144, 21))

        scale_factor = 3
        self.digits = {
            "0": pygame.transform.scale(pygame.image.load("images/zero.png"), (4 * scale_factor, 7 * scale_factor)),
            "1": pygame.transform.scale(pygame.image.load("images/one.png"), (3 * scale_factor, 7 * scale_factor)),
            "2": pygame.transform.scale(pygame.image.load("images/two.png"), (4 * scale_factor, 7 * scale_factor)),
            "3": pygame.transform.scale(pygame.image.load("images/three.png"), (4 * scale_factor, 7 * scale_factor)),
            "4": pygame.transform.scale(pygame.image.load("images/four.png"), (5 * scale_factor, 7 * scale_factor)),
            "5": pygame.transform.scale(pygame.image.load("images/five.png"), (4 * scale_factor, 7 * scale_factor)),
            "6": pygame.transform.scale(pygame.image.load("images/six.png"), (4 * scale_factor, 7 * scale_factor)),
            "7": pygame.transform.scale(pygame.image.load("images/seven.png"), (4 * scale_factor, 7 * scale_factor)),
            "8": pygame.transform.scale(pygame.image.load("images/eight.png"), (4 * scale_factor, 7 * scale_factor)),
            "9": pygame.transform.scale(pygame.image.load("images/nine.png"), (4 * scale_factor, 7 * scale_factor)),
        }

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def draw(self):
        self.window.fill((255, 240, 213))
        self.window.blit(floor_img, (0, 430))
        self.draw_score()
        self.draw_timer()

    def get_time_left(self):
        current_time = pygame.time.get_ticks()
        time_elapsed = (current_time - self.last_nail_collected) / 1000
        time_left = max(0, int(self.timer_limit / 1000 - time_elapsed))

        return int(time_left)

    def draw_timer(self):
        time_left = self.get_time_left()

        self.window.blit(self.time_left_img, (615, 15))
        time_left_str = str(time_left)

        for digit in time_left_str:
            self.window.blit(self.digits[digit], (770, 15))

    def draw_score(self):
        self.window.blit(self.score_text_img, (10, 10))

        score_str = str(self.score)
        x_offset = 95
        y_position = 10

        for digit in score_str:
            spacing = 14

            if digit == "4":
                spacing = 18

            self.window.blit(self.digits[digit], (x_offset, y_position))
            x_offset += spacing

class Menu:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = pygame.image.load("images/menu.png")
        self.img = pygame.transform.scale(self.img, (800, 600))
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_click = pygame.mouse.get_pressed()
        self.mouse_rect = pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], 1, 1)
        self.start_rect = pygame.Rect(20, 400, 310, 70)
        self.quit_rect = pygame.Rect(550, 400, 230, 70)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def get_game_state(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_click = pygame.mouse.get_pressed()
        self.mouse_rect = pygame.Rect(self.mouse_pos[0], self.mouse_pos[1], 1, 1)
        if self.start_rect.colliderect(self.mouse_rect) and self.mouse_click[0]:
            return "game"

        elif self.quit_rect.colliderect(self.mouse_rect) and self.mouse_click[0]:
            pygame.quit()
            exit()

        return "menu"

class Hammer:
    def __init__(self, x, y, broom):
        self.x = x
        self.y = y
        self.broom = broom
        self.rect = pygame.Rect(self.x, self.y, 56, 80)
        self.jumping = False
        self.gravity = 0.75
        self.jump_height = 15
        self.y_velocity = self.jump_height
        self.speed = 3.3
        self.img = hammer_img
        self.health = 3
        self.current_health_sprite = three_hearts

    def update_health_sprite(self):
        if self.health == 3:
            self.current_health_sprite = three_hearts
        elif self.health == 2:
            self.current_health_sprite = two_hearts
        elif self.health == 1:
            self.current_health_sprite = one_heart

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        elif keys[pygame.K_RIGHT] and self.x < 744:
            self.x += self.speed

    def jump(self, keys):
        if keys[pygame.K_UP] and not self.jumping:
            self.jumping = True

        if self.jumping:
            self.y -= self.y_velocity  # SEND HAMMER UPWARDS
            self.y_velocity -= self.gravity  # PULLS HAMMER DOWNWARDS
            if self.y_velocity < -self.jump_height:
                self.jumping = False
                self.y_velocity = self.jump_height

    def check_nail_collision(self, nails, rusty_nails, golden_nails, last_nail_collected, score, health):
        nails_to_remove = []

        all_nails = [(nails, 1, "sounds/hammering.ogg"),
                     (golden_nails, 20, "sounds/hammering.ogg"),
                     (rusty_nails, -1, "sounds/hitrustynail.ogg")]

        for nail_list, point_value, sound in all_nails:
            for nail in nail_list:
                if self.rect.colliderect(nail.nail_rect) and self.rect.bottom >= nail.nail_rect.top and self.y_velocity < 0:
                    nails_to_remove.append((nail, nail_list))
                    sound = pygame.mixer.Sound(sound)
                    sound.set_volume(0.2)
                    sound.play()

                    if point_value > 0:
                        score += point_value
                        last_nail_collected = pygame.time.get_ticks()
                    else:
                        self.health += point_value
                        self.update_health_sprite()

        for nail, nail_list in nails_to_remove:
            nail_list.remove(nail)

        return last_nail_collected, score, health

    def check_broom_collision(self, rusty_nails):
        if self.rect.colliderect(self.broom.broom_rect) and self.broom.broom_spawn:
            pygame.mixer.music.load("sounds/sweep.ogg")
            pygame.mixer.music.play(1, 0.0)
            self.broom.reset_spawn()
            rusty_nails.clear()
            return True
        return False

    def update(self, keys):
        self.move(keys)
        self.jump(keys)
        self.rect.x = self.x
        self.rect.y = self.y

class Nail:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.nail_rect = pygame.Rect(self.x, self.y, 22, 46)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


    @staticmethod
    def spawn_nail(nails_list, spawn_interval, last_spawn_time, window_width, img):
        current_time = pygame.time.get_ticks()

        if current_time - last_spawn_time >=spawn_interval:
            nail_x = random.randint(0, window_width - 44)
            nail_y = 396
            new_nail = (Nail(nail_x, nail_y, img))
            nails_list.append(new_nail)
            last_spawn_time = current_time

        return last_spawn_time

class Broom:
    def __init__(self, x, y, window_width):
        self.x = x
        self.y = y
        self.window_width = window_width
        self.img = broom_img
        self.broom_rect = pygame.Rect(self.x, self.y, 84, 88)
        self.broom_spawn = False
        self.random_num = random.randint(10, 20)

    def draw(self, window):
        if self.broom_spawn:
            window.blit(self.img, (self.x, self.y))

    def spawn(self, rusty_nails):
        if len(rusty_nails) >= self.random_num and not self.broom_spawn:
            self.x = random.randint(0, self.window_width - 84)
            self.broom_spawn = True
            self.broom_rect.topleft = (self.x, self.y)

    def reset_spawn(self):
        self.random_num = random.randint(10, 20)
        self.broom_spawn = False
