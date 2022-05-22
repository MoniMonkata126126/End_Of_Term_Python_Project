import pygame
import sys


class Enemy:
    def __init__(self):
        self.wave = 1
        self.health = [self.wave for i in range(30)]
        self.loop_counter = 0
        self.enemy_img = pygame.image.load("game_enemy_img.png").convert_alpha()
        self.enemies_coord = []
        idx = 0
        while idx <= 3000:
            self.enemies_coord.append([-100 - idx, 150])
            idx += 100

    def change_coord(self):
        if self.loop_counter < 20:
            self.loop_counter += 1
            return
        for idx in range(30):
            if self.enemies_coord[idx][1] >= 730:
                self.loop_counter = 0
                self.enemies_coord[idx][0] -= 10
            elif self.enemies_coord[idx][0] >= 1200:
                self.loop_counter = 0
                self.enemies_coord[idx][1] += 10
            else:
                self.loop_counter = 0
                self.enemies_coord[idx][0] += 10
        self.loop_counter += 1

    def loose_health(self, enemy_coord, damage_taken):
        for idx in range(len(self.enemies_coord)):
            if self.enemies_coord[idx] == enemy_coord:
                if self.health[idx] <= damage_taken:
                    self.enemies_coord[idx] = [-10000, -10000]
                self.health[idx] -= damage_taken

    def deal_damage(self, take_damage):
        for idx in range(len(self.enemies_coord)):
            if self.enemies_coord[idx] == [-10, 730]:
                take_damage(self.health[idx])

    def new_wave(self):
        if self.enemies_coord[29] == [-10, 730] or self.enemies_coord[29] == [-10000, -10000]:
            self.enemies_coord.clear()
            idx = 0
            while idx <= 3000:
                self.enemies_coord.append([-100 - idx, 150])
                idx += 100
            self.wave += 1
            self.health.clear()
            self.health = [self.wave for i in range(30)]


class Tower:
    def __init__(self):
        self.price = 200
        self.upgrade_price = 250
        self.projectile = pygame.image.load("game_projectile_img.png").convert_alpha()
        self.tower_dict = {"height": 200, "width": 180, "dmg": 5, "range_x": 450, "range_y": 450}
        self.tower_list = []

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

    def attack_enemy(self, position):
        for pos in self.tower_list:
            if position[0] in range((pos[1][0] - pos[0]["range_x"]), (pos[1][0] + pos[0]["range_x"])) and \
                    position[1] in range((pos[1][1] - pos[0]["range_y"]), (pos[1][1] + pos[0]["range_y"])):
                return True

    def shoot_projectile(self, position, screen):
        for pos in self.tower_list:
            if position[0] in range((pos[1][0] - pos[0]["range_x"]), (pos[1][0] + pos[0]["range_x"])) and \
                    position[1] in range((pos[1][1] - pos[0]["range_y"]), (pos[1][1] + pos[0]["range_y"])):
                projectile_position_x = (pos[1][0]+position[0])//2
                projectile_position_y = (pos[1][1]+position[1])//2
                screen.blit(self.projectile, (projectile_position_x, projectile_position_y))


class YellowTower(Tower):
    def __init__(self):
        Tower.__init__(self)
        self.dmg = 10
        self.yellow_img = pygame.image.load("game_tower_one_img.png").convert_alpha()


class BlueTower(Tower):
    def __init__(self):
        Tower.__init__(self)
        self.price = 250
        self.range_x = 600
        self.range_y = 600
        self.blue_img = pygame.image.load("game_tower_two_img.png").convert_alpha()


class GreenTower(Tower):
    def __init__(self):
        Tower.__init__(self)
        self.range_x = 750
        self.range_y = 750
        self.dmg = 30
        self.green_img = pygame.image.load("game_tower_three_img.png").convert_alpha()


class Button:
    def __init__(self, x, y, image, width, height):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.width = width
        self.height = height

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.rect.x, self.rect.y))

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False


class GameMenu:
    def __init__(self):
        self.player_health = 100
        self.player_money = 300

    def take_damage(self, damage):
        if self.player_health <= damage:
            pygame.quit()
            sys.exit()
        self.player_health -= damage

    def loose_money(self, cost):
        if self.player_money < cost:
            return True
        self.player_money -= cost
