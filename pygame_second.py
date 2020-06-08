import pygame
pygame.init()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")
walkRight = [pygame.image.load('R1.png').convert_alpha(), pygame.image.load('R2.png').convert_alpha(), pygame.image.load('R3.png').convert_alpha(), pygame.image.load('R4.png').convert_alpha(), pygame.image.load('R5.png').convert_alpha(), pygame.image.load('R6.png').convert_alpha(), pygame.image.load('R7.png').convert_alpha(), pygame.image.load('R8.png').convert_alpha(), pygame.image.load('R9.png').convert_alpha()]
walkLeft = [pygame.image.load('L1.png').convert_alpha(), pygame.image.load('L2.png').convert_alpha(), pygame.image.load('L3.png').convert_alpha(), pygame.image.load('L4.png').convert_alpha(), pygame.image.load('L5.png').convert_alpha(), pygame.image.load('L6.png').convert_alpha(), pygame.image.load('L7.png').convert_alpha(), pygame.image.load('L8.png').convert_alpha(), pygame.image.load('L9.png').convert_alpha()]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()
x = 100
y = 200
width = 64
height = 64
velocity = 10
isJumping = False
jumpCount = 10
left = False
right = False
walk_count = 0

def redraw_gamewindow():
    global walk_count
    win.blit(bg,(0,0))
    if walk_count + 1 >= 27:
        walk_count = 0
    if left:
        win.blit(walkLeft[walk_count//3],(x,y))
        walk_count += 1
    elif right:
        win.blit(walkRight[walk_count//3],(x,y))
        walk_count += 1
    else:
        win.blit(char,(x,y))
    pygame.display.update()

run = True
while run:
    clock.tick(27)
    redraw_gamewindow()
    pygame.time.delay(100)
    #check for event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 1:
        x = x - velocity
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < 500 - width:
        x = x + velocity
        right = True
        left = False
    else:
        right = False
        left = False
        walk_count = 0
    if not(isJumping):
        if keys[pygame.K_SPACE]:
            isJumping = True
            right = False
            left = False
            walk_count = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJumping = False
            jumpCount = 10



pygame.quit()