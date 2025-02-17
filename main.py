from entities import *

pygame.init()
pygame.mixer.init()

menu = Menu()
game_state = "menu"

game = Basics()
last_nail_collected = pygame.time.get_ticks()
score = 0

broom = Broom(random.randint(0, game.window_width - 88), 150, game.window_width)

#HAMMER
hammer = Hammer(75, (game.window_height // 2) + 50, broom)

#NAILS
nails = []
last_nail_spawn_time = pygame.time.get_ticks()
nail_spawn_interval = 1000

#RUSTY NAILS
rusty_nails = []
last_rusty_nail_spawn_time = pygame.time.get_ticks()
rusty_nail_spawn_interval = random.randint(1500, 3000)

#GOLDEN NAILS
golden_nails = []
last_golden_nail_spawn_time = pygame.time.get_ticks()
golden_nail_spawn_interval = random.randint(20000, 40000)

#HEALTH
health = 3
current_health_sprite = three_hearts

gameover = False

#MAIN GAME LOOP
while not gameover:

    #TO HANDLE QUITTING
    game.handle_events()
    current_time = pygame.time.get_ticks()

    if game_state == "menu":
        menu.draw(game.window)
        new_state = menu.get_game_state()

        if new_state == "game":
            game_state = "game"

        pygame.display.update()
        game.clock.tick(60)
        continue

    if game_state == "game":

        #DRAW BASIC ELEMENTS
        game.draw()
        hammer.draw(game.window)
        keys = pygame.key.get_pressed()
        hammer.move(keys)
        hammer.jump(keys)
        hammer.update(keys)

        # SPAWN NAILS AT SET INTERVAL
        last_nail_spawn_time = Nail.spawn_nail(nails, nail_spawn_interval, last_nail_spawn_time, game.window_width, nail_img)
        #DRAW NAILS
        for nail in nails:
            nail.draw(game.window)

        # SPAWN GOLDEN NAILS AT RANDOM INTERVAL
        if current_time - last_golden_nail_spawn_time >= golden_nail_spawn_interval:
            last_golden_nail_spawn_time = Nail.spawn_nail(golden_nails, golden_nail_spawn_interval, last_golden_nail_spawn_time, game.window_width, golden_nail_img)
            golden_nail_spawn_interval = random.randint(20000, 40000)
        #DRAW GOLD NAILS
        for nail in golden_nails:
            nail.draw(game.window)

        #SPAWN RUSTY NAILS AT RANDOM INTERVAL
        if current_time - last_rusty_nail_spawn_time >= rusty_nail_spawn_interval:
            last_rusty_nail_spawn_time = Nail.spawn_nail(rusty_nails, rusty_nail_spawn_interval, last_rusty_nail_spawn_time, game.window_width, rusty_nail_img)
            rusty_nail_spawn_interval = random.randint(1500, 5000)
        #DRAW RUSTY NAILS
        for nail in rusty_nails:
            nail.draw(game.window)

        # CHECKS HAMMER AND NAIL COLLISION
        last_nail_collected, score, health = hammer.check_nail_collision(nails, rusty_nails, golden_nails, last_nail_collected, score, health)
        game.score = score
        game.window.blit(hammer.current_health_sprite, (9, 48))
        game.last_nail_collected = last_nail_collected

        if hammer.check_broom_collision(rusty_nails):
            broom.reset_spawn()

        broom.spawn(rusty_nails)
        if broom.broom_spawn:
            broom.draw(game.window)

    pygame.display.update()
    game.clock.tick(60)