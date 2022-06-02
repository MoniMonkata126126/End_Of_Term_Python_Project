
import pygame
import sys
from class_file import Enemy, GameMenu, Button, YellowTower, BlueTower, GreenTower

# Create constant values for screen width and height
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 950

# Start a pygame window and sett its size
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load needed images
background_img = pygame.image.load("game_background_img.png").convert_alpha()
menu_background_img = pygame.image.load("menu_screen.png").convert_alpha()
load_img = pygame.image.load("load.png").convert_alpha()
save_img = pygame.image.load("save-button-icon.png").convert_alpha()
buy_yellow_img = pygame.image.load("buy_yellow.png").convert_alpha()
buy_blue_img = pygame.image.load("buy_blue.png").convert_alpha()

# Set a clock to manipulate game run speed
clock = pygame.time.Clock()

# Create objects of the Button class with the loaded images
buy_yellow_button = Button(1350, 690, buy_yellow_img, 150, 80)
buy_blue_button = Button(1350, 790, buy_blue_img, 150, 80)
save_button = Button(20, 25, save_img, 100, 60)
load_button = Button(550, 480, load_img, 300, 250)

# Create objects of the classes needed ti run a game
enemy = Enemy()
y_tower = YellowTower.from_tuple()
b_tower = BlueTower.from_tuple()
g_tower = GreenTower.from_tuple()
game_menu = GameMenu()


# Create a main menu loop where you can load a new or pre-existing game
def menu_main():
    # Sets pygame window caption to "Main menu"
    pygame.display.set_caption("Main menu")

    # Main menu loop
    while True:
        # Gets mouse position
        mouse_pos = pygame.mouse.get_pos()
        # Checks for any events that occur during runtime, like mouse clicks
        for event in pygame.event.get():
            # Checks if pygame window is quit, if it is then the game and program stop running
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If load button is pressed, the game is loaded from information from file
            if event.type == pygame.MOUSEBUTTONDOWN:
                if load_button.check_for_input(mouse_pos):
                    # Open and read and load info from file
                    file_one = open("/game_data_saves.txt", "r+")
                    line = file_one.readline()
                    data = line.split(";")
                    enemy.wave = int(data[0])
                    game_menu.player_money = int(data[1])
                    game_menu.player_health = int(data[2])
                    # Close file
                    file_one.close()
                    # Enter game
                    game_main()

        # Print and draw Main menu graphics on screen
        screen.blit(pygame.transform.scale(menu_background_img, (1500, 950)), (0, 0))
        load_button.draw(screen)
        pygame.display.update()


# Create a game loop and Game menu to play, when save button pressed, save info in file and go to Main menu
def game_main():
    # Sets pygame window caption to "Game menu"
    pygame.display.set_caption("Game menu")

    # Variable checks how many mouse clicks there were made for yellow towers
    click_count_yellow = 0
    # Variable checks how many mouse clicks there were made for blue towers
    click_count_blue = 0
    # Variable that signals that there was a yellow tower purchase done
    can_buy_yellow = 0
    # Variable that signals that there was a blue tower purchase done
    can_buy_blue = 0

    # Game menu loop
    while True:
        # Gets mouse position
        mouse_position = pygame.mouse.get_pos()
        # Checks for any events that occur during runtime, like mouse clicks
        for event in pygame.event.get():
            # Checks if pygame window is quit or player is dead, if it is then the game and program stop running
            if event.type == pygame.QUIT or game_menu.player_health <= 0:
                pygame.quit()
                sys.exit()
            # Checks if there is a mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Checks if save button is clicked, if clicked game saves data in txt file and exits to main menu
                if save_button.check_for_input(mouse_position):
                    file_two = open("/game_data_saves.txt", "w+")
                    file_two.write("{};{};{}".format(enemy.wave, game_menu.player_money, game_menu.player_health))
                    file_two.close()
                    menu_main()

                # Checks if shop can be accessed based on money and purchase history
                if game_menu.player_money > 250 or can_buy_yellow >= 1:

                    # Checks for input on yellow tower buy button and gives coordinates of second mouse press to tower
                    if buy_yellow_button.check_for_input(mouse_position) and can_buy_yellow < 1:
                        click_count_yellow += 1
                        game_menu.loose_money(y_tower.price)
                        can_buy_yellow += 1
                    # If right click pressed, mouse coordinates are given
                    if event.button == 3 and click_count_yellow >= 1:
                        # If towers don't overlap they get placed on already given mouse coordinates
                        if not y_tower.check_for_input(game_menu.yellow_tower_list, mouse_position) or \
                                buy_blue_button.check_for_input(mouse_position):
                            yellow_tower = YellowTower.from_tuple(mouse_position)
                            game_menu.yellow_tower_list.append(yellow_tower)
                            click_count_yellow = 0
                            can_buy_yellow = 0
                        # If towers overlap they spawn a green buffed tower on given mouse coordinates and delete any
                        # pre-existing towers
                        else:
                            green_tower = GreenTower.from_tuple(mouse_position)
                            game_menu.green_tower_list.append(green_tower)
                            if b_tower.check_for_input(game_menu.blue_tower_list, mouse_position):
                                b_tower.delete_tower(game_menu.blue_tower_list, mouse_position)
                            if y_tower.check_for_input(game_menu.yellow_tower_list, mouse_position):
                                y_tower.delete_tower(game_menu.yellow_tower_list, mouse_position)

                # Checks if shop can be accessed based on money and purchase history
                if game_menu.player_money > 250 or can_buy_blue >= 1:

                    # Checks for input on blue tower buy button and gives coordinates of second mouse press to tower
                    if buy_blue_button.check_for_input(mouse_position) and can_buy_blue < 1:
                        click_count_blue += 1
                        game_menu.loose_money(b_tower.price)
                        can_buy_blue += 1
                    # If right click pressed, mouse coordinates are given
                    if event.button == 3 and click_count_blue >= 1:
                        # If towers don't overlap they get placed on already given mouse coordinates
                        if not b_tower.check_for_input(game_menu.blue_tower_list, mouse_position) or \
                                buy_blue_button.check_for_input(mouse_position):
                            blue_tower = BlueTower.from_tuple(mouse_position)
                            game_menu.blue_tower_list.append(blue_tower)
                            click_count_blue = 0
                            can_buy_blue = 0
                        # If towers overlap they spawn a green buffed tower on given mouse coordinates and delete any
                        # pre-existing towers
                        else:
                            green_tower = GreenTower.from_tuple(mouse_position)
                            game_menu.green_tower_list.append(green_tower)
                            if y_tower.check_for_input(game_menu.yellow_tower_list, mouse_position):
                                y_tower.delete_tower(game_menu.yellow_tower_list, mouse_position)
                            if b_tower.check_for_input(game_menu.blue_tower_list, mouse_position):
                                b_tower.delete_tower(game_menu.blue_tower_list, mouse_position)

                # Checks if yellow tower is pressed and if it is, it gets upgraded
                if y_tower.check_for_input(game_menu.yellow_tower_list, mouse_position) and event.button == 1:
                    y_tower.upgrade_tower(game_menu.yellow_tower_list, mouse_position)

                # Checks if blue tower id pressed and if it is, it gets upgraded
                if b_tower.check_for_input(game_menu.blue_tower_list, mouse_position) and event.button == 1:
                    b_tower.upgrade_tower(game_menu.blue_tower_list, mouse_position)

        # All images are printed on screen and all functions from classes are run and all checks for firing projectiles
        # and for current money, overlapping enemy and tower coordinates and wave number are made

        # Prints background
        screen.blit(background_img, (0, 0))

        # Prints tower buy buttons
        buy_yellow_button.draw(screen)
        buy_blue_button.draw(screen)

        # Changes enemy coordinates and moves them
        enemy.change_coord()

        # Prints enemies on screen
        enemy.draw_enemies(screen)

        # Prints yellow towers on screen
        y_tower.draw_towers(game_menu.yellow_tower_list, screen)

        # Prints blue towers on screen
        b_tower.draw_towers(game_menu.blue_tower_list, screen)

        # Prints green towers on screen
        g_tower.draw_towers(game_menu.green_tower_list, screen)

        # Checks if enemy is in yellow tower range and if it is, tower fires projectile and player gains money
        for position in enemy.enemies_coord:
            if y_tower.attack_enemy(game_menu.yellow_tower_list, position):
                y_tower.shoot_projectile(game_menu.yellow_tower_list, position, screen)
                enemy.loose_health(position, y_tower.dmg)
                y_tower.loop_counter += 1
                game_menu.player_money += enemy.money
        # Checks if enemy is in blue tower range and if it is, tower fires projectile and player gains money
        for position in enemy.enemies_coord:
            if b_tower.attack_enemy(game_menu.blue_tower_list, position):
                b_tower.shoot_projectile(game_menu.blue_tower_list, position, screen)
                enemy.loose_health(position, b_tower.dmg)
                b_tower.loop_counter += 1
                game_menu.player_money += enemy.money
        # Checks if enemy is in green tower range and if it is, tower fires projectile and player gains money
        for position in enemy.enemies_coord:
            if g_tower.attack_enemy(game_menu.green_tower_list, position):
                g_tower.shoot_projectile(game_menu.green_tower_list, position, screen)
                enemy.loose_health(position, g_tower.dmg)
                g_tower.loop_counter += 1
                game_menu.player_money += enemy.money

        # Checks if enemies crossed the finish line and if they did, player takes damage
        game_menu.take_damage(enemy)
        # Raises enemy wave level if needed
        enemy.new_wave()
        # Prints player health
        game_menu.get_health(screen)
        # Prints player money
        game_menu.get_money(screen)
        # Prints wave level
        game_menu.get_wave(screen, enemy.wave)
        # Prints Save button
        save_button.draw(screen)
        # Updates Screen
        pygame.display.update()
        # Sets pygame loop speed
        clock.tick(360)


# Calls Main menu when program starts running
game_main()
