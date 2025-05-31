import pygame 

WIDTH = 1200
HEIGHT = 600 
SIZE = (WIDTH, HEIGHT)
FPS = 60

window = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
background = pygame.transform.scale(
    pygame.image.load("background.jpg"), SIZE
)

pygame.mixer.init()
pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename: str, coords: tuple[int, int], size: tuple [int, int], speed: int ):
        self.image = pygame.transform.scale(
            pygame.image.load(filename), size
        )
        self.rect  = pygame.Rect(coords, size)

        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.rect = self.image.get_rect(topleft=coords)

        self.speed = speed

    def draw(self, window):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed


class Enemy(GameSprite):
    def update(self, x1, x2):

        self.rect.x += self.speed

        if self.rect.x>= x2 or self.rect.x <= x1:
            self.speed = -self.speed


class Wall(pygame.sprite.Sprite):
    def __init__(self, coords: tuple[int, int],size: tuple, color:tuple[int,int,int]):
        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(coords, size)
        self.color = color
        self.image.fill(color)

player = Player("hero.png", (10, HEIGHT-130), (80,65), 5)
enemy = Enemy("cyborg.png", (WIDTH-200, HEIGHT//2), (80,65), 5)
gold = GameSprite("treasure.png", (WIDTH-200, HEIGHT-130),(50, 40), 0)

test_wall = Wall((100,100), (300,10), (0,255, 125))

run = True 
finish = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(event.pos)

    if not finish:
        window.blit(background, (0,0))

        player.draw(window)
        player.update()
        enemy.draw(window)
        enemy.update(WIDTH//2, WIDTH-10)
        gold.draw(window)
        test_wall.draw(window)



    pygame.display.update()
    clock.tick(FPS)
    