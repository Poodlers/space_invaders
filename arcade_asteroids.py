import pygame
import math
import random
import os

pygame.init()

#INITIALIZE MUSIC
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Space Shooter")
#load images
power_up_life = pygame.image.load("heart_sprite.png").convert_alpha()
power_up_faster_firing = pygame.image.load("faster_firing.png").convert_alpha()
char = pygame.image.load("spaceship_sprite.png").convert_alpha()
char = pygame.transform.scale(char, (50, 30))
asteroid_image = pygame.image.load("asteroid_sprite.png")
asteroid_image = pygame.transform.scale(asteroid_image,(70,50))
asteroid_small_image = pygame.transform.scale(asteroid_image,(40,30))
background = pygame.image.load("space_background.png")
play_again = True

#get the file containing the highscore
file = open("highscore.txt","r+")
if os.stat("highscore.txt").st_size == 0:
    file.write("Nobody\n")
    file.write(str(0))
highscore_name = file.readline()
highscore = int(file.readline())

file.close()



def set_globalvars():
    global x
    x = 500 / 2
    global y
    y = 500 / 2
    global width
    width = 50
    global height
    height = 50
    global velocity
    velocity = 2
    global asteroid_spawn_rate
    asteroid_spawn_rate = 25
    global list_of_bullets
    list_of_bullets = []
    global list_of_asteroids
    list_of_asteroids = []
    global powerup_list
    powerup_list = []
    global score
    score = 0
    global lives
    lives = 3
    global run
    run = True
    global x_accel
    x_accel = 0
    global y_accel
    y_accel = 0
    global cooldown
    cooldown = 10
    global faster_firing
    faster_firing = 0
    main()

def point_to_mouse(x,y,char):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    vector_x, vector_y = mouse_x - x, mouse_y - y
    angle = (180 / math.pi) * -math.atan2(vector_y, vector_x) - 90
    updated_image = pygame.transform.rotate(char,int(angle))
    image_location = updated_image.get_rect(center= (x,y))
    win.blit(updated_image,image_location)

def display_score():
    global score
    global lives
    font = pygame.font.Font('freesansbold.ttf',20)
    text_surface = font.render("Score: " + str(score),True,(255,255,255))
    text_surface_rect = text_surface.get_rect()
    text_surface_rect.center = (50,10)
    win.blit(text_surface,text_surface_rect)
    text_surface2 = font.render("Lives: " + str(lives),True,(255,255,255))
    text_surface2_rect = text_surface2.get_rect()
    text_surface2_rect.center = (450, 10)
    win.blit(text_surface2,text_surface2_rect)

def update_game(x,y,width,height,char):
    win.blit(background,(0,0))
    display_score()
    for bullet in list_of_bullets:
        pygame.draw.rect(win, (0, 0, 255), (int(bullet[0]), int(bullet[1]), 5, 5))
    for asteroid in list_of_asteroids:
        #rotate the asteroid a little
        asteroid[3] = asteroid[3] + 3
        if asteroid[4] == True:
            rotated_asteroid = pygame.transform.rotate(asteroid_image,asteroid[3])
            image_location = rotated_asteroid.get_rect(center=(asteroid[0], asteroid[1]))
            win.blit(rotated_asteroid,image_location)
        else:
            rotated_asteroid = pygame.transform.rotate(asteroid_small_image, asteroid[3])
            image_location = rotated_asteroid.get_rect(center=(asteroid[0], asteroid[1]))
            win.blit(rotated_asteroid, image_location)
    for powerup in powerup_list:
        img_location = powerup[2].get_rect(center = (powerup[0], powerup[1]))
        win.blit(powerup[2],img_location)

    point_to_mouse(x, y, char)
    pygame.display.update()

def spawn_asteroids(x,y):
    global list_of_asteroids
    #randomize the spawn location near the edges
    #0:up
    #1:left
    #2:right
    #3:down
    where_to_spawn = random.randint(0,3)
    if where_to_spawn == 0:
        asteroid_x = random.randint(10,490)
        asteroid_y = random.randint(0,20)
    elif where_to_spawn == 1:
        asteroid_x = random.randint(10, 20)
        asteroid_y = random.randint(5,490)
    elif where_to_spawn == 2:
        asteroid_x = random.randint(475, 490)
        asteroid_y = random.randint(5,490)
    elif where_to_spawn == 3:
        asteroid_x = random.randint(5, 490)
        asteroid_y = random.randint(470, 490)
    random_offset = random.randint(-10,10)
    vector_x = (x + random_offset) - asteroid_x
    vector_y = (y + random_offset) - asteroid_y
    distance = math.sqrt(vector_x ** 2 + vector_y ** 2)
    speed = 5
    normalized_vec = [speed * vector_x / distance, speed * vector_y / distance]
    rotation_angle = 0
    big = True
    just_spawned = 50
    list_of_asteroids.append([int(asteroid_x), int(asteroid_y),normalized_vec,rotation_angle,big,just_spawned])

def create_small_asteroids(x,y,vector):
    speed = 6
    vector_x = vector[0] / 2 - random.randint(8,10)
    normalized_vec = [(speed * vector_x)/5,(speed * vector[1])/5]
    rotation_angle = 0
    invulnerable_time = 50
    bige = False
    list_of_asteroids.append([int(x), int(y), normalized_vec, rotation_angle, bige,invulnerable_time])
    vector_x = vector[0] * 2 + random.randint(8,10)
    normalized_vec = [(speed * vector_x) / 5, (speed * vector[1]) / 5]
    list_of_asteroids.append([int(x), int(y), normalized_vec, rotation_angle, bige,invulnerable_time])



def spawn_bullet(x,y):
    bullet_Sound = pygame.mixer.Sound("laser.wav")
    global list_of_bullets
    initial_x = x
    initial_y = y
    mouse_x, mouse_y = pygame.mouse.get_pos()
    vector_x, vector_y = mouse_x - x, mouse_y - y
    #normalize the vector
    speed = 15
    distance = math.sqrt(vector_x ** 2 + vector_y **2)
    normalized_vec = (speed * vector_x/ distance, speed * vector_y/distance)
    list_of_bullets.append([initial_x,initial_y,normalized_vec])
    bullet_Sound.play()

def game_over():
    global score
    global highscore
    global highscore_name
    name = ""
    while True:
        pygame.time.delay(100)
        win.fill((0,0,0))
        font = pygame.font.Font('freesansbold.ttf', 17)
        text = font.render('You Lose!', True, (255,0,0), (0,0,0))
        text4 = font.render("Your final score was " + str(score),True,(255,255,255),(0,0,0))
        text4_rect = text4.get_rect()
        text4_rect.center = (250, 100)
        win.blit(text4,text4_rect)
        if score > highscore:
            text3 = font.render("You beat the previous highscore of " + str(highscore),True,(255,255,255),(0,0,0))
            text7 = font.render( "achieved by " + str(highscore_name),True,(255,255,255),(0,0,0))
            text7_rect = text7.get_rect()
            text7_rect.center = (250,170)
            win.blit(text7,text7_rect)
            text5 = font.render("Please write a username for your highscore to be saved:",True,(255,255,255),(0,0,0))
            text5_rect = text5.get_rect()
            text5_rect.center = (250,190)
            win.blit(text5,text5_rect)
            input_text = font.render(name,True,(255,255,255),(0,0,0))
            input_rect = input_text.get_rect()
            input_rect.center = (250,220)
            win.blit(input_text,input_rect)
        else:
            text3 = font.render("You were so close to beating the previous highscore of " + str(highscore),True,(255,255,255),(0,0,0))
            text6 = font.render("achieved by " + str(highscore_name),True,(255,255,255),(0,0,0))
            text6_rect = text6.get_rect()
            text6_rect.center = (250,170)
            win.blit(text6,text6_rect)
        text3_rect = text3.get_rect()
        text3_rect.center = (250,150)
        win.blit(text3,text3_rect)
        Text_Rect = text.get_rect()
        Text_Rect.center = (250,250)
        win.blit(text,Text_Rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    name += event.unicode
                if event.key == pygame.K_RETURN and score > highscore:
                    file = open("highscore.txt","w")
                    file.write(str(name) + "\n")
                    file.write(str(score))
                    file.close()
                    pygame.quit()

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 150 < mouse[0] < 350 and 300 < mouse[1] < 400:
                    return "Restart"

        mouse = pygame.mouse.get_pos()
        if 150 < mouse[0] < 350 and 300 < mouse[1] < 400:
            pygame.draw.rect(win,(0,255,0),(150,300,200,100))
        else:
            pygame.draw.rect(win,(0,0,255),(150,300,200,100))
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text2 = smallText.render("Try Again?",True,(0,0,0))
        text2_rect = text2.get_rect()
        text2_rect.center = (150 + 200//2, 300 + 100//2)
        win.blit(text2,text2_rect)

        pygame.display.update()

def create_powerup(x,y,power_up_life = power_up_life,power_up_faster_firing = power_up_faster_firing):
    global powerup_list
    a = random.randint(0,1)
    if a == 0:
        powerup_list.append((x,y,power_up_life))
    else:
        powerup_list.append((x,y,power_up_faster_firing))

def check_for_collision(asteroid_image,char,x,y):
    explosion_Sound = pygame.mixer.Sound("explosion.wav")
    global score
    global lives
    global powerup_list
    global run
    global faster_firing
    #create the rect for the player
    char_rect = char.get_rect()
    char_rect.center = (x,y)
    for asteroid in list_of_asteroids:
        if asteroid[4] == True:
            asteroid_rect = asteroid_image.get_rect()
        else:
            asteroid_rect = asteroid_small_image.get_rect()
        asteroid_rect.center = (asteroid[0],asteroid[1])
        if asteroid_rect.colliderect(char_rect):
            lives -= 1
            explosion_Sound.play()
            del list_of_asteroids[list_of_asteroids.index(asteroid)]
            if lives == 0:
                run = False
                if game_over() == "Restart":
                    set_globalvars()

        for x in list_of_asteroids:
            if x[4] == False and x[5] > 0:
                continue
            if x[4] == True:
                asteroid2_rect = asteroid_image.get_rect()
            else:
                asteroid2_rect = asteroid_small_image.get_rect()
            asteroid2_rect.center = (x[0], x[1])
            if asteroid_rect.colliderect(asteroid2_rect) and x != asteroid:
                if asteroid[4] == True:
                    create_small_asteroids(asteroid[0], asteroid[1], asteroid[2])
                elif x[4] == True:
                    create_small_asteroids(asteroid[0] , asteroid[1], x[2])
                del list_of_asteroids[list_of_asteroids.index(x)]
                del list_of_asteroids[list_of_asteroids.index(asteroid)]

        for powerup in powerup_list:
            powerup_rect = powerup[2].get_rect()
            powerup_rect.center = (powerup[0],powerup[1])
            if powerup_rect.colliderect(char_rect):
                if powerup[2] == power_up_life and lives < 3:
                    lives += 1
                if powerup[2] == power_up_faster_firing:
                    faster_firing = 30
                del powerup_list[powerup_list.index(powerup)]



        for bullets in list_of_bullets:
            bullet_rect = pygame.Rect(0,0,5,5)
            bullet_rect.center = (bullets[0],bullets[1])
            if asteroid_rect.colliderect(bullet_rect):
                x = random.randrange(0,5)
                if x == 1:
                    create_powerup(asteroid[0],asteroid[1])
                explosion_Sound.play()
                if asteroid[4] == True:
                     create_small_asteroids(asteroid[0], asteroid[1], asteroid[2])
                try:
                    del list_of_asteroids[list_of_asteroids.index(asteroid)]
                except:
                    pass
                list_of_bullets.pop(list_of_bullets.index(bullets))
                score += 1

def main():
    global x
    global y
    global width
    global height
    global velocity
    global asteroid_spawn_rate
    global list_of_bullets
    global list_of_asteroids
    global score
    global lives
    global run
    global x_accel
    global y_accel
    global play_again
    global cooldown
    global faster_firing
    while run:
        #check for an event
        pygame.time.delay(75)
        cooldown -= 1
        asteroid_spawn_rate -= 1
        if faster_firing > 0:
            faster_firing -= 1
        if asteroid_spawn_rate == 0:
            asteroid_spawn_rate = 30
            spawn_asteroids(x,y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and faster_firing > 0:
                spawn_bullet(x,y)
            elif event.type == pygame.MOUSEBUTTONDOWN and cooldown < 0:
                cooldown = 10
                spawn_bullet(x,y)
        check_for_collision(asteroid_image,char,x,y)

        for bullet in list_of_bullets:
            bullet[0] = bullet[0] + bullet[2][0]
            bullet[1] = bullet[1] + bullet[2][1]

            if bullet[0] > 500 or bullet[0] < 0 or bullet[1] < 0 or bullet[1] > 500:
                del list_of_bullets[list_of_bullets.index(bullet)]

        for asteroid in list_of_asteroids:
            if asteroid[5] > 0:
                asteroid[5] -= 1

            asteroid[0] = asteroid[0] + asteroid[2][0]
            asteroid[1] = asteroid[1] + asteroid[2][1]
            if asteroid[5] < 40:
                if asteroid[0] <= 9:
                    asteroid[2][0] = -asteroid[2][0] + random.randint(-2,2)
                    asteroid[2][1] = asteroid[2][1] + random.randint(-2,2)
                if asteroid[0] >= 490:
                    asteroid[2][0] = -asteroid[2][0] + random.randint(-2,2)
                    asteroid[2][1] = asteroid[2][1] + random.randint(-2,2)
                if asteroid[1] <= 10:
                    asteroid[2][1] = -asteroid[2][1] + random.randint(-2,2)
                    asteroid[2][0] = asteroid[2][0] + random.randint(-2,2)
                if asteroid[1] >= 490:
                    asteroid[2][1] = -asteroid[2][1] + random.randint(-2,2)
                    asteroid[2][0] = asteroid[2][0] + random.randint(-2,2)



        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > 0 + width:
            x_accel -= 1
        if keys[pygame.K_RIGHT] and x < 500 - width:
            x_accel += 1
        if keys[pygame.K_UP] and y > 0 + width:
            y_accel -= 1
        if keys[pygame.K_DOWN] and y < 500 - width:
            y_accel += 1

        if y_accel > 0:
            y_accel -= 0.5
        if y_accel < 0:
            y_accel += 0.5
        if x_accel > 0:
            x_accel -= 0.5
        if x_accel < 0:
            x_accel += 0.5

        x = x + x_accel
        y = y + y_accel

        if x < 0 + width/2 or x > 500 - width/2:
            x = x - x_accel
        if y < 0 + height/2 or y > 500 - height/2:
            y = y - y_accel
        update_game(x,y,width,height,char)
set_globalvars()
pygame.quit()
