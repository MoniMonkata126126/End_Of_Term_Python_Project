
import pygame
import sys
from class_file import Enemy, GameMenu, Button, YellowTower, BlueTower, GreenTower

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 950


def game_start():
    pygame.init()
    surface_init = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    return surface_init


screen = game_start()

background_img = pygame.image.load("game_background_img.png").convert_alpha()
menu_background_img = pygame.image.load("menu_screen.png").convert_alpha()
load_img = pygame.image.load("load.png").convert_alpha()
save_img = pygame.image.load("save-button-icon.png").convert_alpha()
buy_yellow_img = pygame.image.load("buy_yellow.png").convert_alpha()
buy_blue_img = pygame.image.load("buy_blue.png").convert_alpha()

clock = pygame.time.Clock()

buy_yellow_button = Button(1350, 690, buy_yellow_img, 150, 80)
buy_blue_button = Button(1350, 790, buy_blue_img, 150, 80)
save_button = Button(20, 25, save_img, 100, 60)
load_button = Button(550, 480, load_img, 300, 250)

enemy = Enemy()
yellow_tower = YellowTower()
blue_tower = BlueTower()
game_menu = GameMenu()


def menu_main():
    # Sets pygame window caption to "Main menu"
    pygame.display.set_caption("Main menu")

    while True:
        # Gets mouse position
        mouse_pos = pygame.mouse.get_pos()
        # Checks for any events that occur during runtime, like mouse clicks
        for event in pygame.event.get():
            # Checks if pygame window is quit, if it is then the game and program stop running
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if load_button.check_for_input(mouse_pos):
                    file_one = open("/game_data_saves.txt", "r")
                    line = file_one.readline()
                    file_one.close()
                    data = line.split(";")
                    enemy.wave = int(data[0])
                    game_menu.player_money = int(data[1])
                    game_menu.player_health = int(data[2])
                    game_main()

        screen.blit(pygame.transform.scale(menu_background_img, (1500, 950)), (0, 0))
        load_button.draw(screen)
        pygame.display.update()


def game_main():
    # Sets pygame window caption to "Game menu"
    pygame.display.set_caption("Game menu")

    # Variable checks how many mouse clicks there were made for yellow towers
    click_count_yellow = 0
    # Variable checks how many mouse clicks there were made for blue towers
    click_count_blue = 0
    while True:
        # Gets mouse position
        mouse_position = pygame.mouse.get_pos()
        # Checks for any events that occur during runtime, like mouse clicks
        for event in pygame.event.get():
            # Checks if pygame window is quit, if it is then the game and program stop running
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Checks if there is a mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Checks if save button is clicked, if clicked game saves data in txt file and exits to main menu
                if save_button.check_for_input(mouse_position):
                    file_two = open("/game_data_saves.txt", "w+")
                    file_two.write("{0};{1};{2}".format(enemy.wave, game_menu.player_money, game_menu.player_health))
                    file_two.close()
                    menu_main()

                # Checks for input on yellow tower buy button and gives bought tower coordinates of second mouse press
                if buy_yellow_button.check_for_input(mouse_position):
                    click_count_yellow += 1
                    game_menu.loose_money(yellow_tower.price)
                if event.button == 3 and click_count_yellow >= 1:
                    yellow_tower.tower_list.append([yellow_tower.tower_dict, mouse_position])
                    click_count_yellow = 0

                # Checks for input on blue tower buy button and gives bought tower coordinates of second mouse press
                if buy_blue_button.check_for_input(mouse_position):
                    click_count_blue += 1
                    game_menu.loose_money(blue_tower.price)
                if event.button == 3 and click_count_blue >= 1:
                    blue_tower.tower_list.append([yellow_tower.tower_dict, mouse_position])
                    click_count_blue = 0

                # Checks if yellow tower is pressed and if it is, it gets upgraded
                if yellow_tower.check_for_input(mouse_position) and event.button == 1:
                    yellow_tower.upgrade_tower(mouse_position)

                # Checks if blue tower id pressed and if it is, it gets upgraded
                if blue_tower.check_for_input(mouse_position) and event.button == 1:
                    blue_tower.upgrade_tower(mouse_position)

        screen.blit(background_img, (0, 0))
        buy_yellow_button.draw(screen)
        buy_blue_button.draw(screen)
        enemy.change_coord()
        for coordinates in enemy.enemies_coord:
            screen.blit(pygame.transform.scale(enemy.enemy_img, (100, 90)), coordinates)
        for yellow in yellow_tower.tower_list:
            screen.blit(pygame.transform.scale(yellow_tower.yellow_img, (yellow[0]["width"], yellow[0]["height"])), yellow[1])
        for blue in blue_tower.tower_list:
            screen.blit(pygame.transform.scale(blue_tower.blue_img, (blue[0]["width"], blue[0]["height"])), blue[1])
        for position in enemy.enemies_coord:
            if yellow_tower.attack_enemy(position):
                yellow_tower.shoot_projectile(position, screen)
                enemy.loose_health(position, yellow_tower.tower_dict["dmg"])
        for position in enemy.enemies_coord:
            if blue_tower.attack_enemy(position):
                blue_tower.shoot_projectile(position, screen)
                enemy.loose_health(position, blue_tower.tower_dict["dmg"])
        enemy.new_wave()
        save_button.draw(screen)
        pygame.display.update()
        clock.tick(120)

game_main()
