
import pygame
from pygame.locals import *
from random import shuffle

pygame.init()

edge = 10
fps = 60
black = (0, 0, 0)
white = (255, 255, 255)
card_background = pygame.image.load("pics/UI/2.png")
cover_card = pygame.image.load("pics/UI/4.png")
map_width = 6
map_height = 4
fontsize = 40
button_click_offset = 3
W = card_background.get_rect().width * map_width + edge * map_width + edge
H = card_background.get_rect().height * map_height + edge * map_height + edge + fontsize
cards_shown = 0
game_over = False

font = pygame.font.Font(None, fontsize)

pygame.display.set_caption("Memory")
clock = pygame.time.Clock()

sc = pygame.display.set_mode((W, H))


icons = []
for i in range(1, 13):
    icons.append({"icon_num": i, "surface": pygame.image.load("pics/ico/" + str(i) + ".png").convert_alpha(), "sprite": None, "hidden": True, "match": False})
    icons.append({"icon_num": i, "surface": pygame.image.load("pics/ico/" + str(i) + ".png").convert_alpha(), "sprite": None, "hidden": True, "match": False})

shuffle(icons)

selected_card = 0
selected_sprite = None


while True:

    for event in pygame.event.get():

        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONUP:
            if cards_shown == 2:
                for i in range(len(icons)):
                    icons[i]["hidden"] = True

                cards_shown = 0
                selected_card = 0
                selected_sprite = None
            else:
                pos = pygame.mouse.get_pos()
                for icon in icons:
                    if icon["sprite"].collidepoint(pos) and not icon["match"]:
                        if selected_sprite != icon["sprite"]:
                            if cards_shown == 0:
                                icon["hidden"] = False
                                selected_card = icon["icon_num"]
                                selected_sprite = icon["sprite"]
                                selected_sprite.left = selected_sprite.left + button_click_offset
                                selected_sprite.top = selected_sprite.top + button_click_offset
                                
                                cards_shown = cards_shown + 1

                            elif cards_shown == 1:
                                if icon["icon_num"] == selected_card:
                                    icon["match"] = True
                                    for j in icons:
                                        if j["icon_num"] == icon["icon_num"] :
                                            j["match"] = True

                                        cards_shown = 0
                                        selected_card = 0
                                        selected_sprite = None
                                else:      
                                    icon["hidden"] = False    
                                    cards_shown = cards_shown + 1


    matchcount = 0
    for icon in icons:
        if icon["match"]:
            matchcount = matchcount + 1

    if matchcount == len(icons):
        game_over = True

    sc.fill(black)


    if game_over:
        t = "Game Over!"
        text2 = font.render(t, 1, white)
        sc.blit(text2, (W / 2 - text2.get_width() / 2, H / 2 - text2.get_height() / 2))
        
    else:
        if selected_card == 0:
            selected_card = ""

        else:
            t1 = "Card selected: {}".format(selected_card)
            text = font.render(t1, 1, white)
            sc.blit(text, (20,20))


        image_count = 0
        for x in range(map_width):
            for y in range(map_height):
                if not icons[image_count]["match"]:                
                    if icons[image_count]["hidden"]:
                        sprite = sc.blit(cover_card, (edge + card_background.get_rect().width * x + edge * x ,
                        edge + card_background.get_rect().height * y + edge * y + fontsize))

                    else:
                        sprite = sc.blit(card_background, (edge + card_background.get_rect().width * x + edge * x + button_click_offset,
                        edge + card_background.get_rect().height * y + edge * y + fontsize + button_click_offset))

                        sc.blit(icons[image_count]["surface"], (edge + ((card_background.get_rect().width - icons[image_count]["surface"].get_rect().width) / 2) + card_background.get_rect().width * x + edge * x + button_click_offset,
                        edge + (card_background.get_rect().height - icons[image_count]["surface"].get_rect().height) / 2 + card_background.get_rect().height * y + edge * y + fontsize + button_click_offset))

                    icons[image_count]["sprite"] = sprite

                image_count = image_count + 1


    pygame.display.flip()
    clock.tick(fps)