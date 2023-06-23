# Complete your game here
import random
import pygame

width = 640
height = 480
background = (128,128,128)

class CoinCollector:
    def __init__(self):
        pygame.init()
        self.load_images()
        
        self.to_right = False
        self.to_left = False
        self.robot_position_x = width/2 - self.images[2].get_width()
        self.robot_position_y = 480 - self.images[2].get_height()
        
        
        self.score = 0
        self.lives = 3
        self.falling_object_velocity = 2
        self.add_difficulty = False
        
        self.number = 10
        self.coins_list = []
        self.coin = self.images[0]
        for i in range(self.number):
            self.coins_list.append([-1000, height, False])
        
        self.ghosts_list = []
        self.ghost = self.images[1]
        for i in range(self.number):
            self.ghosts_list.append([-1000, height, False])
        self.game_font = pygame.font.SysFont("Arial", 24)
        
        
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Coin Collector")
        self.clock = pygame.time.Clock()
        self.main_loop()
        
    
    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
            self.robot()
            self.falling_objects(self.coin, self.coins_list)
            self.falling_objects(self.ghost, self.ghosts_list)
            self.collision(self.coins_list, self.coin, False)
            self.collision(self.ghosts_list, self.ghost, True)
            self.add_speed()
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def add_speed(self):
        if self.score % 5 == 0 and self.score > 1 and self.add_difficulty == False:
            self.falling_object_velocity += 1
            self.add_difficulty = True
        
    
    def draw_window(self):
        self.window.fill(background)
        text = self.game_font.render('Score: ' + str(self.score), True, (255,0, 0))
        score = self.game_font.render('Lives: ' + str(self.lives), True, (255, 0, 0))
        self.window.blit(text, (25, 0))
        self.window.blit(score, (500, 0))
        if self.game_over():
            self.window.fill(background)
            text = self.game_font.render("Game Over", True, (255,0,0))
            score = self.game_font.render(f'Final Score: {self.score}', True, (255,0,0))
            new = self.game_font.render('Press F2 for a new game', True, (255,0,0))
            middle_x = width / 2 - score.get_width()/2
            middle_y = height / 2 - (text.get_height() + score.get_height() + new.get_height())/2
            pygame.draw.rect(self.window, (0,0,0), ((width/2) - (new.get_width() /2), middle_y, new.get_width(), (text.get_height() + score.get_height() + new.get_height())))
            self.window.blit(text, ((width/2) - (text.get_width() /2), middle_y))
            self.window.blit(score, (middle_x, (middle_y + text.get_height())))
            self.window.blit(new, ((width/2) - (new.get_width() /2), middle_y + text.get_height() + new.get_height()))
            self.check_events()
    
    def game_over(self):
        if self.lives <= 0:
            return True
        return False
    
    def new_game(self):
        self.lives = 3
        self.score = 0
        self.falling_object_velocity = 2
        self.add_difficulty = False
        self.coins_list = []
        self.coin = self.images[0]
        for i in range(self.number):
            self.coins_list.append([-1000, height, False])
        
        self.ghosts_list = []
        self.ghost = self.images[1]
        for i in range(self.number):
            self.ghosts_list.append([-1000, height, False])
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.robot_position_x = width/2 - self.images[2].get_width()
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
            #look for keydown event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_F2:
                    self.new_game()
                    
            #look for keyup event
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
                if event.key == pygame.K_LEFT:
                    self.to_left = False
    
    #load images and put them in array
    def load_images(self):
        self.images = []
        for name in ["coin", 'monster', 'robot']:
            self.images.append(pygame.image.load(name + '.png'))
    
    #Add movement to robot, restrict movement to only on screen
    def robot(self):
        if self.game_over():
            return
        if self.to_right and self.robot_position_x <= width - self.images[2].get_width():
            self.robot_position_x += 3
        if self.to_left and self.robot_position_x >= 0:
            self.robot_position_x -= 3
        self.window.blit(self.images[2], (self.robot_position_x, self.robot_position_y))

    #Add falling objects
    def falling_objects(self, object, object_list):
        if self.game_over():
            return
        for i in range(self.number):
            #control speed at which the object is dropping
            if object_list[i][1]+object.get_height() < height + object.get_height():
                object_list[i][1] += self.falling_object_velocity
            else:
                #if an object reaches bottom of the screen
                if object_list[i][1] > -object.get_height() or object_list[i][1] > height or object_list[i][2] == True:
                    #new random starting point
                    object_list[i][0] = random.randint(0, width-object.get_width())
                    object_list[i][1] = -random.randint(object.get_height(), 1000)
                    object_list[i][2] = False
                
        for i in range(self.number):
            self.window.blit(object, (object_list[i][0], object_list[i][1]))
    
    #Adds collision detection if robot comes in contact with an object
    def collision(self, object_list, object, isEnemy):
        robo_position_x = self.robot_position_x + self.images[2].get_width()
        for i in range(self.number):
            #coordinates are being listed in upper left corner of image
            if self.robot_position_y <= (object_list[i][1] + object.get_height()):
                if ((self.robot_position_x - self.images[2].get_width() > object_list[i][0] and robo_position_x < (object_list[i][0] + object.get_width())) 
                    or ((self.robot_position_x + (self.images[2].get_width() / 2)) > object_list[i][0] and (self.robot_position_x + (self.images[2].get_width() / 2 )) <= (object_list[i][0] + object.get_width()))
                    and object_list[i][2] != True):
                    object_list[i][0] = random.randint(0, width-object.get_width())
                    object_list[i][1] = -random.randint(object.get_height(), 200)
                    if not isEnemy:
                        self.score += 1
                        self.add_difficulty = False
                    else:
                        self.lives -= 1
    

if __name__ == "__main__":
    CoinCollector()