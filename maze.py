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
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename: str, coords: tuple[int, int], size: tuple [int, int], speed: int ):
        super().__init__()
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
    def update(self, walls):
        keys = pygame.key.get_pressed()

        x,y = self.rect.x, self.rect.y

        if keys[pygame.K_w] and y >= 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and y <= HEIGHT - self.rect.height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and x >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and x <= WIDTH - self.rect.width:
            self.rect.x += self.speed

        for w in walls:
            if pygame.sprite.collide_rect(w,self):
                self.rect.x = x
                self.rect.y = y


class Enemy(GameSprite):
    def update(self, x1, x2):

        self.rect.x += self.speed

        if self.rect.x>= x2 or self.rect.x <= x1:
            self.speed = -self.speed
        
    def updatevertical(self, y1, y2):

        self.rect.y += self.speed

        if self.rect.y>= y2 or self.rect.y <= y1:
            self.speed = -self.speed
        
    


class Wall(pygame.sprite.Sprite):
    def __init__(self, coords: tuple[int, int],size: tuple, color:tuple[int,int,int]):
        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(coords, size)
        self.color = color
        self.image.fill(color)
        
    def draw(self, window):
        window.blit(self.image, self.rect)


player = Player("hero.png", (10, HEIGHT-130), (80,65), 5)
enemy1 = Enemy("cyborg.png", (WIDTH-200, HEIGHT//2), (80,65), 5)
enemy2 = Enemy("cyborg.png", (200,0), (80,65), 5)
gold = GameSprite("treasure.png", (WIDTH-150, HEIGHT-100),(50, 40), 0)

walls1 = [
    Wall((100,100), (400,10), (255,110, 100)), 
    Wall((100,100), (10,400), (255,110, 100)),
    Wall((500,100), (10,400), (255,110, 100)),
    Wall((200,180), (10,420), (255,110, 100)),
    Wall((400,180), (10,420), (255,110, 100)),
    Wall((500,0), (10,100), (255,110, 100)),
    Wall((200,180), (200,10), (255,110, 100)),
    Wall((650,0), (10,500), (255,110, 100)),
    Wall((800,100), (10,180), (255,110, 100)),
    Wall((800,380), (10,220), (255,110, 100)),

]   

walls2 = [
    Wall((320,0), (10,400), (130,255,0)),
    Wall((1090,100), (10,375), (130,255,0)),
    Wall((930,370), (160,10), (130,255,0)),
    Wall((930,370), (10,115), (130,255,0)),
    Wall((600,485), (340,10), (130,255,0)),
    Wall((600,485), (10,150), (130,255,0)),
    Wall((960,0), (10,285), (130,255,0)),
    Wall((835,0), (10,385), (130,255,0)),
    Wall((600,375), (60,10), (130,255,0)),
    Wall((760,375), (75,10), (130,255,0)),
    Wall((600,375), (10,115), (130,255,0)),
    Wall((650,240), (10,135), (130,255,0)),
    Wall((550,240), (100,10), (130,255,0)),
    Wall((650,0), (10,130), (130,255,0)),
    Wall((650,240), (90,10), (130,255,0)),
    Wall((740,75), (10,175), (130,255,0)),
    Wall((440,120), (100,10), (130,255,0)),
    Wall((440,120), (10,375), (130,255,0)),
    Wall((175,490), (275,10), (130,255,0)),
    Wall((175,315), (10,180), (130,255,0)),
    Wall((175,0), (10,235), (130,255,0)),
    Wall((0,315), (180,10), (130,255,0)),
]


level = 1

walls = walls1
enemy = enemy1

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
        player.update(walls)
        enemy.draw(window)
        
        gold.draw(window)

        for w in walls:
            w.draw(window)
        if pygame.sprite.collide_rect(player, enemy):
            finish = True
            font = pygame.font.SysFont("Helvetica", 60)
            text = font.render("ти програв", True, (255,0,0))
            window.blit(text, (WIDTH//2-100, HEIGHT//2-50))
            sound = pygame.mixer.Sound("kick.ogg")
            sound.play()

        if pygame.sprite.collide_rect(player, gold):
            level += 1

    
        if level == 1:
            walls = walls1
            enemy = enemy1
            enemy.update(WIDTH//2, WIDTH-10)
        elif level == 2:
            walls = walls2
            enemy = enemy2
            enemy.updatevertical(0, HEIGHT//2)
            gold.rect.x = 20
            gold.rect.y = 20
            #player.rect.center = (WIDTH-200, HEIGHT-130)

        if level > 2:
            finish = True
            font = pygame.font.SysFont("Helvetica", 60)
            text = font.render("You won ", True, (255,0,0))
            window.blit(text, (WIDTH//2-100, HEIGHT//2-50))
            sound = pygame.mixer.Sound("money.ogg")
            sound.play()



    pygame.display.update()
    clock.tick(FPS)
    