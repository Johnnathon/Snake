import pygame
import random
pygame.font.init()


pygame.init()

FPS = 10
VEL =20
WIDTH, HEIGHT = (900,500)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Lemon Snake')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED =  (255, 0, 0)
GRAY = (100, 100, 100)
GAMEOVER_FONT = pygame.font.SysFont('tiemsnewroman', 60)
SCORE_FONT = pygame.font.SysFont('tiemsnewroman', 40)

MAX_RATS = 1

EAT = pygame.USEREVENT + 1

def draw_window(snake, rats, snake_tail, score, game_over_text):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, YELLOW, snake)
    for x in snake_tail:
        pygame.draw.rect(WIN, YELLOW, x)
    for rat in rats:
        pygame.draw.rect(WIN, YELLOW, rat)
    grid_size = 20
    for x in range (0, WIDTH, grid_size):
        for y in range (0, HEIGHT, grid_size):
            grid = pygame.Rect(x, y, grid_size, grid_size)
            pygame.draw.rect(WIN, GRAY, grid, 1)
    score_text = SCORE_FONT.render("Score: " + str(score), 1, RED)
    gameover_text = GAMEOVER_FONT.render(game_over_text, 1, RED)
    WIN.blit(score_text, (700, 10))
    WIN.blit(gameover_text, (350, 200))

    pygame.display.update()

        
            
def score(snake_tail):
    score = 0
    for x in snake_tail:
        score += 100
    return score
    

        
        
class Lemon:
    def __init__(self):
        self.direction = None
        

    def snake_direction(self, lastkey, previous_key):
        if lastkey == pygame.K_a and previous_key != pygame.K_d: 
            self.direction = "L"
            
        elif lastkey == pygame.K_a and previous_key == pygame.K_d:
            self.direction = "R" #make sure player can't go the wrong ways
            
        elif lastkey == pygame.K_d and previous_key != pygame.K_a:
            self.direction = "R" #right
            
        elif lastkey == pygame.K_d and previous_key == pygame.K_a:
            self.direction = "L" #keepright
            
        elif lastkey == pygame.K_w and previous_key != pygame.K_s:
            self.direction = "U" #up
            
        elif lastkey == pygame.K_w and previous_key == pygame.K_s: #keepup
            
            self.direction = "D"
        elif lastkey == pygame.K_s and previous_key != pygame.K_w:#down
            
            self.direction = "D"
        elif lastkey == pygame.K_s and previous_key == pygame.K_w: #keepdown
            
            self.direction = "U"
    def snake_movement(self, snake, snake_tail):
        if self.direction == "L":
            snake.x -= VEL
        elif self.direction == "R":
            snake.x += VEL
        elif self.direction == "U":
            snake.y -= VEL
        elif self.direction == "D":
            snake.y += VEL
        
        if len(snake_tail) > 0:
            # Move each segment to the position of the previous segment
            for i in range(len(snake_tail) - 1, 0, -1):
                snake_tail[i].x = snake_tail[i - 1].x
                snake_tail[i].y = snake_tail[i - 1].y

            # Move the first segment to the position of the snake's head
            snake_tail[0].x = snake.x
            snake_tail[0].y = snake.y


class StartScreen:
    def __init__(self):
        self.start = False

    def startwindow(self):
        WIN.fill(BLACK)
        title_text = GAMEOVER_FONT.render("Lemon Da Snake", 1, YELLOW)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        start_text = SCORE_FONT.render("Press Space to Begin", 1, RED)
        WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 400))
        pygame.display.update()
    
    def press_start(self, keys_pressed):
        
        return pygame.K_SPACE in keys_pressed
        


            



class GameOver:
    def __init__(self):
        self.bounds = True
    
    def Out_of_Bounds(self, snake):
        if snake.x > 900 or snake.x < 0:
            self.bounds = False
        if snake.y > 500 or snake.y < 0:
            self.bounds = False
        return self.bounds
    
    def self_collision(self, snake, snake_tail):
        counter = 1
        check = False
        for x in snake_tail:
            if counter == 1:
                counter += 1
            else:
                if snake.colliderect(x):
                    check = True
                    return check
    
    def game_over_text(self):
        game_over_text = "Game Over"
        return game_over_text



def main():
    #defining variables
    snake_length = 20
    snake_left = 460
    snake_top = 260
    snake = pygame.Rect(snake_left, snake_top, 20, snake_length)
    snake_tail = []
    lastkey = None
    rats = []
    keys_pressed = []
    previouskey = None
    
    
    clock = pygame.time.Clock()
    run = True


    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                #most recent key pressed in a var
                lastkey = event.key
                #keeping record of keys pressed
                keys_pressed.append(lastkey)
            
            
                
                
        #variables for randomizing rats, keeping it off the edges
            
        random_x = random.randrange(20, 880, 20) 
        random_y = random.randrange(20, 480, 20)
            
        # making sure there is only one rat on the screen at a time
        if len(rats) < MAX_RATS:
            rat =  pygame.Rect(random_x, random_y, 20, 20)
            rats.append(rat)

        
        
        if snake.colliderect(rat):
            pygame.event.post(pygame.event.Event(EAT))
            snake_tail.append(pygame.Rect(snake.x, snake.y, 20, 20))
            rats.remove(rat)
               
              
        
        
        


        #keeping track of keys pressed before most recent so that 
        if len(keys_pressed) > 1:
            previouskey = keys_pressed[(len(keys_pressed) - 2)]

        L = Lemon()
        GO = GameOver()
        S = StartScreen()

        L.snake_direction(lastkey, previouskey)
        game_over_text = ""
        game_over_check = False
        game_start_check = 1
        L.snake_movement(snake, snake_tail)
        the_score = score(snake_tail)
        if GO.self_collision(snake, snake_tail) == True:
            game_over_text = GO.game_over_text()
            game_over_check = True
        if GO.Out_of_Bounds(snake) == False:
            game_over_text = GO.game_over_text()
            game_over_check = True
            
        # spawn_food(rats, random_x, random_y)
        
        if S.press_start(keys_pressed) == False:
            S.startwindow()        
        else:
            draw_window(snake, rats, snake_tail, the_score, game_over_text)
        # eat_rat(snake, rats)
        if game_over_check == True:
            pygame.time.wait(5000)
            


        
    pygame.quit()


if __name__ == "__main__":
    main()