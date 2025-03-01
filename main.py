import pygame

pygame.font.init()
WIDTH = 1200
HEIGHT = 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (200, 200, 255)
BROWN = (66, 66, 66)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH/2-5,0,10, HEIGHT)
pygame.display.set_caption('Space Shooter')
FONT = pygame.font.SysFont('comicsans', 30)
FPS = 60
VAL = 5
SPACESHIP_WIDTH = WIDTH / 20
SPACESHIP_HEIGHT = HEIGHT / 20
BULLET_VEL=7
MAX_BULLET_VEL=10
YELLOW_SPACESHIP_IMAGE = pygame.image.load('assets/spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load('assets/spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)
YELLOW_INITIAL_POS = (0, HEIGHT / 2 - SPACESHIP_HEIGHT / 2)
RED_INITIAL_POS = (WIDTH - SPACESHIP_WIDTH, HEIGHT / 2 - SPACESHIP_HEIGHT / 2)
BG = pygame.image.load('assets/space.png')

YELLOW_HIT= pygame.USEREVENT + 1
RED_HIT= pygame.USEREVENT + 2

def draw_window(red, yellow, red_bullets, yellow_bullets):
    WIN.blit(BG, (0, 0))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.draw.rect(WIN, BROWN, BORDER)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x-VAL >0:
        yellow.x -= VAL
    if keys_pressed[pygame.K_d] and yellow.x+SPACESHIP_WIDTH < WIDTH/2:
        yellow.x += VAL
    if keys_pressed[pygame.K_w] and yellow.y-VAL > 0:
        yellow.y -= VAL
    if keys_pressed[pygame.K_s] and yellow.y + VAL < HEIGHT- SPACESHIP_HEIGHT - 10: yellow.y += VAL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x > WIDTH/2  :
        red.x -= VAL
    if keys_pressed[pygame.K_RIGHT] and red.x + VAL + SPACESHIP_WIDTH < WIDTH:
        red.x += VAL
    if keys_pressed[pygame.K_UP] and red.y-VAL:
        red.y -= VAL
    if keys_pressed[pygame.K_DOWN] and red.y + VAL < HEIGHT- SPACESHIP_HEIGHT - 10:
        red.y += VAL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)


    for rbullet in red_bullets:
        rbullet.x -= BULLET_VEL
        if yellow.colliderect(rbullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(rbullet)


def main():
    run = True
    clock = pygame.time.Clock()
    red = pygame.Rect(RED_INITIAL_POS, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    yellow = pygame.Rect(YELLOW_INITIAL_POS, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    red_bullets = []
    yellow_bullets = []
    rb = []
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLET_VEL:
                    bullet = pygame.Rect((yellow.x, yellow.y + SPACESHIP_HEIGHT/2),(10,5))
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLET_VEL:
                    bullet = pygame.Rect((red.x, red.y + SPACESHIP_HEIGHT/2),(10,5))
                    red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets)

    pygame.quit()


if __name__ == "__main__":
    main()
