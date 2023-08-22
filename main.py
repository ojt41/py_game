import pygame
import random

# constants are defined so that it can be changed throughout the code easilty
constant_width = 640
constant_height = 480
robot_velocit = 6
number_of_monsters = 3
knock_distance = 100

class Game:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((constant_width, constant_height))
        pygame.display.set_caption("Collecting Game")

        self.robot = pygame.image.load("robot.png")
        self.coin = pygame.image.load("coin.png")
        self.monster = pygame.image.load("monster.png")

        # for frame rate
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont("arial", 36)

        self.is_invincible = True
        self.invincibility_timer = 3.0
        self.init_positions()

    def display_instructions(self):
        # List of instruction lines
        instruction_lines = [
            "Use arrow keys to move.",
            "Your objective is to collect coins!",
            "Avoid monsters",
            "If you touch a monster you lose 2 coins",
            "You lose if you have 0 coins",
            "You are invincible for first 3 seconds",
            "Goodluck!",
            "Press any key to start"
        ]

        self.window.fill((200, 200, 200)) #chose gray for bg so monster is seen well
        y_position = constant_height//2-len(instruction_lines)*20
        
        # Display each instruction line on the screen
        for line in instruction_lines:
            instructions_text = self.font.render(line, True, (0,0,0))
            instructions_text_rect = instructions_text.get_rect(center=(constant_width // 2, y_position))
            self.window.blit(instructions_text, instructions_text_rect)
            y_position +=40
        pygame.display.flip()
        
        # dont start until key is pressed so user can be ready 
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    waiting_for_input = False

    def init_positions(self):
        self.robot_x = constant_width // 2
        self.robot_y = constant_height // 2
        self.monsters = []
        
        # random monsters are created
        for _ in range(number_of_monsters):
            self.monsters.append({
                'x': random.randint(0, constant_width - self.monster.get_width()),
                'y': random.randint(0, constant_height - self.monster.get_height()),
                'vel_x': random.choice([-1, 1]) * random.randint(1, 3),
                'vel_y': random.choice([-1, 1]) * random.randint(1, 3)
            })
        
        # coin pos
        self.coin_x = random.randint(0, constant_width - self.coin.get_width())
        self.coin_y = random.randint(0, constant_height - self.coin.get_height())
        
        # User gets 10 coins by default
        self.collected_coins = 10
        self.game_over = False

    def update_positions(self):
        # Handle invincibility timer so user gets time to reach
        if self.is_invincible:
            self.invincibility_timer -= 1 / 60
            if self.invincibility_timer <= 0:
                self.is_invincible = False
        
        self.handle_robot_movement()
        self.update_monster_positions()
        if not self.is_invincible:
            self.handle_robot_monster_collisions()
        self.handle_robot_coin_collisions()

    # robot movements
    def handle_robot_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.robot_x -= robot_velocit
        if keys[pygame.K_RIGHT]:
            self.robot_x += robot_velocit
        if keys[pygame.K_UP]:
            self.robot_y -= robot_velocit
        if keys[pygame.K_DOWN]:
            self.robot_y += robot_velocit
        
        # robot will stay in the walls
        self.robot_x = max(0, min(self.robot_x, constant_width - self.robot.get_width()))
        self.robot_y = max(0, min(self.robot_y, constant_height - self.robot.get_height()))

    def update_monster_positions(self):
        for monster_data in self.monsters:
            monster_data['x'] += monster_data['vel_x']
            monster_data['y'] += monster_data['vel_y']

            # monsters dont exit the walls
            if monster_data['x'] <= 0 or monster_data['x'] >= constant_width - self.monster.get_width():
                monster_data['vel_x'] *= -1
            if monster_data['y'] <= 0 or monster_data['y'] >= constant_height - self.monster.get_height():
                monster_data['vel_y'] *= -1

    def handle_robot_monster_collisions(self):
        robot_rect = pygame.Rect(self.robot_x, self.robot_y, self.robot.get_width(), self.robot.get_height())
        for monster_data in self.monsters:
            monster_rect = pygame.Rect(monster_data['x'], monster_data['y'], self.monster.get_width(), self.monster.get_height())
            if robot_rect.colliderect(monster_rect):
                # reduce coins and knockback the robot
                self.collected_coins -= 2
                self.robot_knockback()
                if self.collected_coins < 0:
                    self.collected_coins = 0

    def handle_robot_coin_collisions(self):
        robot_rect = pygame.Rect(self.robot_x, self.robot_y, self.robot.get_width(), self.robot.get_height())
        coin_rect = pygame.Rect(self.coin_x, self.coin_y, self.coin.get_width(), self.coin.get_height())
        if robot_rect.colliderect(coin_rect):
            # coin added
            self.collected_coins += 1
            self.coin_x = random.randint(0, constant_width - self.coin.get_width())
            self.coin_y = random.randint(0, constant_height - self.coin.get_height())

    # Robot is knocked away to ensure that it doesnt keep hitting the monster
    def robot_knockback(self):
        knock_direction = random.choice(["left", "right", "up", "down"])
        if knock_direction == "left":
            self.robot_x -= knock_distance
        elif knock_direction == "right":
            self.robot_x += knock_distance
        elif knock_direction == "up":
            self.robot_y -= knock_distance
        elif knock_direction == "down":
            self.robot_y += knock_distance

    def draw_message_box(self, message):
        message_surface = self.font.render(message, True, (0, 0, 0))
        message_rect = message_surface.get_rect(center=(constant_width // 2, constant_height // 2))
        pygame.draw.rect(self.window, (255, 255, 255), (message_rect.left - 10, message_rect.top - 10, message_rect.width + 20, message_rect.height + 20))
        self.window.blit(message_surface, message_rect)
    
    def draw_button_box(self, message, x, y):
        button_surface = self.font.render(message, True, (0, 0, 0))
        button_rect = button_surface.get_rect(center=(x, y))
        pygame.draw.rect(self.window, (255, 255, 255), (button_rect.left - 10, button_rect.top - 10, button_rect.width + 20, button_rect.height + 20))
        self.window.blit(button_surface, button_rect)

    def run(self):
        self.display_instructions()  # Print instructions on screen

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            if not self.game_over:
                self.update_positions()

            self.window.fill((200, 200, 200))

            self.window.blit(self.robot, (self.robot_x, self.robot_y))
            self.window.blit(self.coin, (self.coin_x, self.coin_y))
            for monster_data in self.monsters:
                self.window.blit(self.monster, (monster_data['x'], monster_data['y']))

            # Show the coins on GUI
            coin_text = self.font.render("Collected Coins: " + str(self.collected_coins), True, (0, 0, 0))
            self.window.blit(coin_text, (10, 10))

            # Game over or victory
            if self.collected_coins <= 0:  # Loss
                self.game_over = True
                self.draw_message_box("Game Over")
                self.draw_button_box("Press R to Restart", constant_width // 2, constant_height // 2 + 60)
                self.draw_button_box("Press Q to Quit", constant_width // 2, constant_height // 2 + 110)

            if self.collected_coins >= 50:  # Victory
                self.game_over = True
                self.draw_message_box("Congratulations! You won!!")
                self.draw_button_box("Press R to Restart", constant_width // 2, constant_height // 2 + 60)
                self.draw_button_box("Press Q to Quit", constant_width // 2, constant_height // 2 + 110)

            if self.game_over:
                pygame.display.flip()

                # Check for restart or quit key press
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.init_positions()
                    self.game_over = False
                elif keys[pygame.K_q]:
                    pygame.quit()
                    exit(0)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
