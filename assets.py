import pygame

# FUNCTION TO LOAD/SCALE IMAGES
def load_image(image_path, width, height):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (width, height))

menu_img = load_image("images/menu.png", 800, 600)
floor_img = load_image("images/floor.png", 800, 170)

hammer_img = load_image("images/hammer.png", 56, 80)
nail_img = load_image("images/nail1.png", 22, 46)
rusty_nail_img = load_image("images/rustynail.png", 22, 46)
golden_nail_img = load_image("images/gold_nail.png", 22, 46)

three_hearts = load_image("images/threehearts.png", 96, 27)
two_hearts = load_image("images/twohearts.png", 96, 27)
one_heart = load_image("images/oneheart.png", 96, 27)

broom_img = load_image("images/broom.png", 84, 88)
