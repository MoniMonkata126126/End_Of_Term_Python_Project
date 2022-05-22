import pygame


# Create Enemy class
class Enemy:
    def __init__(self):
        """
        Holds value of price for killing an enemy,
        wave level
        enemy unit health per wave
        counter for change_coord method calls
        enemy image
        list of enemy coordinates
        """
        self.money = 15
        self.wave = 1
        self.health = [self.wave*2 for i in range(30)]
        self.loop_counter = 0
        self.enemy_img = pygame.image.load("game_enemy_img.png").convert_alpha()
        self.enemies_coord = []
        idx = 0
        while idx <= 3000:
            self.enemies_coord.append([-100 - idx, 150])
            idx += 100

    # Changes enemy coordinates
    def change_coord(self):
        if self.loop_counter < 20:
            self.loop_counter += 1
            return
        for idx in range(30):
            if self.enemies_coord[idx][1] >= 730:
                self.loop_counter = 0
                self.enemies_coord[idx][0] -= (10*self.wave)
            elif self.enemies_coord[idx][0] >= 1200:
                self.loop_counter = 0
                self.enemies_coord[idx][1] += (10*self.wave)
            else:
                self.loop_counter = 0
                self.enemies_coord[idx][0] += (10*self.wave)
        self.loop_counter += 1

    # Enemies take damage when method called
    def loose_health(self, enemy_coord, damage_taken):
        for idx in range(len(self.enemies_coord)):
            if self.enemies_coord[idx] == enemy_coord:
                if self.health[idx] <= damage_taken:
                    self.enemies_coord[idx] = [-10000, -10000]
                self.health[idx] -= damage_taken

    # Spawns a new UPGRADED wave
    def new_wave(self):
        if self.enemies_coord[29] == [-10, 730] or self.enemies_coord[29] == [-10000, -10000]:
            self.enemies_coord.clear()
            idx = 0
            while idx <= 3000:
                self.enemies_coord.append([-100 - idx, 150])
                idx += 100
            self.wave += 1
            self.health.clear()
            self.health = [self.wave*2 for i in range(30)]


# Create Tower class
class Tower:
    def __init__(self):
        """
        Sets Tower price
        Sets upgrade price
        Sets loop counter for attack_enemy method
        Sets tower projectile image
        Sets a dict of all values held from a tower
        Makes a list for the dictionaries of the towers
        """
        self.price = 200
        self.upgrade_price = 250
        self.loop_counter = 0
        self.projectile = pygame.image.load("game_projectile_img.png").convert_alpha()
        self.tower_dict = {"height": 200, "width": 180, "dmg": 5, "range_x": 450, "range_y": 450}
        self.tower_list = []

    # Upgrade tower stats
    def upgrade_tower(self, position):
        for idx in range(len(self.tower_list)):
            if self.tower_list[idx][1] == position:
                right = self.tower_list[idx][1][0] + (self.tower_list[idx][0]["width"] // 2)
                left = self.tower_list[idx][1][0] - (self.tower_list[idx][0]["width"] // 2)
                top = self.tower_list[idx][1][1] - (self.tower_list[idx][0]["height"] // 2)
                bottom = self.tower_list[idx][1][1] - (self.tower_list[idx][0]["height"] // 2)
                if position[0] in range(left, right) and position[1] in range(top, bottom):
                    self.tower_list[idx][0]["height"] += 25
                    self.tower_list[idx][0]["width"] += 25
                    self.tower_list[idx][0]["range_x"] += 50
                    self.tower_list[idx][0]["range_y"] += 50
                    return

    # Check if tower x, y overlaps with the x, y of a given target ( mouse position or other tower x, y coordinates )
    def check_for_input(self, position):
        for idx in range(len(self.tower_list)):
            if self.tower_list[idx][1] == position:
                right = self.tower_list[idx][1][0] + (self.tower_list[idx][0]["width"]//2)
                left = self.tower_list[idx][1][0] - (self.tower_list[idx][0]["width"]//2)
                top = self.tower_list[idx][1][1] - (self.tower_list[idx][0]["height"]//2)
                bottom = self.tower_list[idx][1][1] - (self.tower_list[idx][0]["height"]//2)
                if position[0] in range(left, right) and position[1] in range(top, bottom):
                    return True
            return False

    # Checks if enemy is in tower range
    def attack_enemy(self, position):
        if self.loop_counter < 15:
            self.loop_counter += 1
            return
        for pos in self.tower_list:
            if position[0] in range((pos[1][0] - pos[0]["range_x"]), (pos[1][0] + pos[0]["range_x"])) and \
                    position[1] in range((pos[1][1] - pos[0]["range_y"]), (pos[1][1] + pos[0]["range_y"])):
                return True

    # Shoots a projectile
    def shoot_projectile(self, position, screen):
        for pos in self.tower_list:
            if position[0] in range((pos[1][0] - pos[0]["range_x"]), (pos[1][0] + pos[0]["range_x"])) and \
                    position[1] in range((pos[1][1] - pos[0]["range_y"]), (pos[1][1] + pos[0]["range_y"])):
                projectile_position_x = (pos[1][0]+position[0])//2
                projectile_position_y = (pos[1][1]+position[1])//2
                screen.blit(self.projectile, (projectile_position_x, projectile_position_y))


# Create varius classes from base Tower class with little changes to base parameters
class YellowTower(Tower):
    def __init__(self):
        Tower.__init__(self)
        self.dmg = 10
        self.yellow_img = pygame.image.load("game_tower_one_img.png").convert_alpha()


# Create varius classes from base Tower class with little changes to base parameters
class BlueTower(Tower):
    def __init__(self):
        Tower.__init__(self)
        self.price = 50
        self.range_x = 600
        self.range_y = 600
        self.blue_img = pygame.image.load("game_tower_two_img.png").convert_alpha()


# Create varius classes from base Tower class with little changes to base parameters
class GreenTower(Tower):
    def __init__(self):
        Tower.__init__(self)
        self.range_x = 750
        self.range_y = 750
        self.dmg = 30
        self.green_img = pygame.image.load("game_tower_three_img.png").convert_alpha()


# Create a button class for all buttons in game
class Button:
    def __init__(self, x, y, image, width, height):
        """
        __init__ constructor method
        :param x: x coord
        :param y: y coord
        :param image: image for button
        :param width: width of button
        :param height: height of button
        """
        self.image = image
        # Creates a rectangle box object for the image and button
        self.rect = self.image.get_rect(topleft=(x, y))
        self.width = width
        self.height = height

    # Draws the button
    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.rect.x, self.rect.y))

    # Checks if button is pressed by given position and button x, y and width, and height coordinates
    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False


# Create a class for the main features of the player
class GameMenu:
    def __init__(self):
        """
        Sets base health
        Sets Base money
        Makes a constant for the RGB value of the colour white
        Sets a font for text printing
        """
        self.player_health = 100
        self.player_money = 300
        self.WHITE = (255, 255, 255)
        self.font = pygame.font.Font(None, 50)

    # Player takes damage if enemy crosses finish line
    def take_damage(self, damage):
        self.player_health = self.player_health - damage

    # Prints player health
    def get_health(self, screen):
        text_health = self.font.render("Health: " + str(self.player_health), True, self.WHITE)
        text_health_rect = text_health.get_rect(center=(1375, 90))
        screen.blit(text_health, text_health_rect)

    # Prints player money
    def get_money(self, screen):
        text_money = self.font.render("Money: " + str(self.player_money), True, self.WHITE)
        text_money_rect = text_money.get_rect(center=(1375, 140))
        screen.blit(text_money, text_money_rect)

    # Prints wave level
    def get_wave(self, screen, wave):
        text_wave = self.font.render("Wave: " + str(wave), True, self.WHITE)
        text_wave_rect = text_wave.get_rect(center=(1375, 190))
        screen.blit(text_wave, text_wave_rect)

    # Player money drops after a purchase
    def loose_money(self, cost):
        self.player_money -= cost
