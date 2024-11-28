import pygame
import math
pygame.init()

# Variables
w_width = 1440
w_height = 770
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

grid_hw = 150
grid_list = []
center_blacklist = []

active_list = []
play = True

center_list = [[w_width/2-grid_hw, w_height/2-grid_hw], [w_width/2, w_height/2-grid_hw], [w_width/2+grid_hw,
               w_height/2-grid_hw], [w_width/2-grid_hw, w_height/2], [w_width/2, w_height/2], [w_width/2+grid_hw,
               w_height/2], [w_width/2-grid_hw, w_height/2+grid_hw], [w_width/2, w_height/2+grid_hw],
               [w_width/2+grid_hw, w_height/2+grid_hw]]

window = pygame.display.set_mode((w_width, w_height))

dist_list = []
item_list = []

location_list = ['', '', '', '', '', '', '', '', '']

# Text
font = pygame.font.SysFont('skia.ttf', 60)
x_first_font = font.render('X Goes First!', True, black)
play_again_font = font.render('Press Space To Play Again!', True, black)


def calc_dist_2_points(x2, x1, y2, y1):
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance


class Grid:

    wh = 150

    def __init__(self, center):
        self.center = center

    def draw_grid(self):
        pygame.draw.rect(window, black, pygame.Rect(self.center[0]-self.wh/2-2.5, self.center[1]-self.wh/2, 5, self.wh+5
                                                    ))
        pygame.draw.rect(window, black, pygame.Rect(self.center[0]+self.wh/2-2.5, self.center[1]-self.wh/2, 5, self.wh))
        pygame.draw.rect(window, black, pygame.Rect(self.center[0]-self.wh/2+2.5, self.center[1]-self.wh/2, self.wh, 5))
        pygame.draw.rect(window, black, pygame.Rect(self.center[0]-self.wh/2+2.5, self.center[1]+self.wh/2, self.wh, 5))


class Piece:
    def __init__(self, center, colour):
        self.center = center
        self.colour = colour

    def calculate_distance(self, mouse_pos, piece):
        dist_list.clear()
        item_list.clear()
        for item in center_list:
            dist = calc_dist_2_points(mouse_pos[0], item[0], mouse_pos[1], item[1])
            dist_list.append(dist)
            item_list.append(item)
            min_dist = min(dist_list)
            if len(dist_list) == 9:
                self.center = item_list[dist_list.index(min_dist)]
                if self.center[0]-75+2.5 < mouse_pos[0] < self.center[0]+75-2.5 and self.center[1]-75+2.5 < \
                        mouse_pos[1] < self.center[1]+75-2.5 and self.center not in center_blacklist:
                    active_list.append(piece)
                    location_list[center_list.index(self.center)] = piece
                    center_blacklist.append(self.center)


class X(Piece):
    def draw(self):
        pygame.draw.line(window, self.colour, (self.center[0]-60+2.5, self.center[1]-60+5),
                         (self.center[0]+60-2.5, self.center[1]+60), 5)
        pygame.draw.line(window, self.colour, (self.center[0] + 60 - 2.5, self.center[1] - 60 + 5),
                         (self.center[0] - 60 + 2.5, self.center[1] + 60), 5)


class O(Piece):
    def draw(self):
        pygame.draw.circle(window, self.colour, self.center, 60, 2)


def update_display():
    pygame.display.update()


def fill_screen(colour):
    print(window)
    window.fill(colour)


def end_game():
    global play
    play = False
    window.blit(play_again_font, (w_width / 2 - play_again_font.get_width() / 2, 100))
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        play = True
        fill_screen(white)
        active_list.clear()
        center_blacklist.clear()
        for i in range(len(location_list)):
            location_list[i] = ''


def check_for_winner(_list):
    for i in range(0, len(_list), 3):
        if isinstance(_list[i], X) or isinstance(_list[i], O):
            if type(_list[i]) == type(_list[i + 1]) == type(_list[i + 2]):
                _list[i].colour = red
                _list[i + 1].colour = red
                _list[i + 2].colour = red
                end_game()

    for h in range(3):
        if isinstance(_list[h], X) or isinstance(_list[h], O):
            if type(_list[h]) == type(_list[h + 3]) == type(_list[h + 6]):
                _list[h].colour = red
                _list[h + 3].colour = red
                _list[h + 6].colour = red
                end_game()

    if isinstance(_list[4], X) or isinstance(_list[4], O):
        if type(_list[0]) == type(_list[4]) == type(_list[8]):
            _list[0].colour = red
            _list[4].colour = red
            _list[8].colour = red
            end_game()
        elif type(_list[2]) == type(_list[4]) == type(_list[6]):
            _list[2].colour = red
            _list[4].colour = red
            _list[6].colour = red
            end_game()


def main():
    run = True
    x = True
    o = False
    turn_x = X((100, 100), black)
    turn_o = O((100, 300), black)
    for i in range(9):
        grid_list.append(Grid(center_list[i]))
    while run:
        for event in pygame.event.get():
            fill_screen(white)
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play:
                    if x:
                        active_piece = X([0, 0], black)
                        x = False
                        o = True
                        active_piece.calculate_distance(pygame.mouse.get_pos(), active_piece)
                    elif o:
                        active_piece = O([0, 0], black)
                        o = False
                        x = True
                        active_piece.calculate_distance(pygame.mouse.get_pos(), active_piece)
        if play:
            if x:
                turn_x.colour = red
                turn_o.colour = black
            elif o:
                turn_x.colour = black
                turn_o.colour = red
        else:
            turn_x.colour = black
            turn_o.colour = black

        turn_x.draw()
        turn_o.draw()

        if len(active_list) == 0:
            window.blit(x_first_font, (w_width/2-x_first_font.get_width()/2, 100))
            x = True
            o = False
        for t in grid_list:
            t.draw_grid()
        if len(active_list) > 0:
            for h in active_list:
                h.draw()
        if len(active_list) == 9:
            end_game()

        check_for_winner(location_list)

        update_display()

    pygame.quit()


main()
