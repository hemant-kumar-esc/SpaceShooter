import pygame
pygame.font.init()
pygame.mixer.init()

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
MAX_BULLET_VEL=3
YELLOW_SPACESHIP_IMAGE = pygame.image.load('assets/spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load('assets/spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)
YELLOW_INITIAL_POS = (0, HEIGHT / 2 - SPACESHIP_HEIGHT / 2)
RED_INITIAL_POS = (WIDTH - SPACESHIP_WIDTH, HEIGHT / 2 - SPACESHIP_HEIGHT / 2)
BG = pygame.transform.scale(pygame.image.load('assets/space.png'),(WIDTH, HEIGHT))

YELLOW_HIT= pygame.USEREVENT + 1
RED_HIT= pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)

BULLET_HIT_SOUND = pygame.mixer.Sound('assets/gun_hit.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('assets/gun.mp3');

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BG, (0, 0))
    red_health_text = HEALTH_FONT.render('Health : '+ str(red_health), True, WHITE)
    yellow_health_text = HEALTH_FONT.render('Health : '+ str(yellow_health), True, WHITE)
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width(), red_health_text.get_height() + 10))
    WIN.blit(yellow_health_text,(0, yellow_health_text.get_height() + 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))


    pygame.draw.rect(WIN, BROWN, BORDER)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def draw_winner(text):
    winner_text = WINNER_FONT.render(text, True, WHITE)
    WIN.blit(winner_text, (WIDTH/2-winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)


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
        elif(bullet.x > WIDTH):
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif(bullet.x > WIDTH):
            red_bullets.remove(bullet)


def main():
    run = True
    clock = pygame.time.Clock()
    red = pygame.Rect(RED_INITIAL_POS, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    yellow = pygame.Rect(YELLOW_INITIAL_POS, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    red_bullets = []
    yellow_bullets = []

    red_health = 3
    yellow_health = 3
    winner_text = ''
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLET_VEL:
                    bullet = pygame.Rect((yellow.x, yellow.y + SPACESHIP_HEIGHT/2),(10,5))
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLET_VEL:
                    bullet = pygame.Rect((red.x, red.y + SPACESHIP_HEIGHT/2),(10,5))
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        if red_health <= 0:
            winner_text = 'Yellow Wins'

        if yellow_health <= 0:
            winner_text = 'Red Wins'

        if winner_text != "":
            draw_winner(winner_text)


        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)


    main()


if __name__ == "__main__":
    main()
