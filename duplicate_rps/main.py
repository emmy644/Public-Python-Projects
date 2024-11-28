import pygame
import random

pygame.init()

# Length Variables
s_width, s_height = 1440, 790
b_width, b_height = 80, 50

# Rect Variable
b_x = s_width / 4
b_y = s_height / 2 + 100
rock = pygame.Rect((b_x - b_width / 2, b_y), (b_width, b_height))
paper = pygame.Rect((b_x * 2 - b_width / 2, b_y), (b_width, b_height))
scissors = pygame.Rect((b_x * 3 - b_width / 2, b_y), (b_width, b_height))
cover_rect = pygame.Rect((0, b_y), (s_width, s_height))
streak_cover_rect = pygame.Rect((0, 50), (50, 500))

# Other Variables
screen = pygame.display.set_mode((s_width, s_height))
button_list = []
rps = ['rock', 'paper', 'scissors']
red = (255, 0, 0)
win_list = []
streak_num = 0
rect_list = [rock, paper, scissors]

# Image
rock_pic = pygame.image.load('rock.png')
rock_pic = pygame.transform.scale(rock_pic, (70, 100))
paper_pic = pygame.image.load('paper.png')
paper_pic = pygame.transform.scale(paper_pic, (70, 100))
scissors_pic = pygame.image.load('scissors.png')
scissors_pic = pygame.transform.scale(scissors_pic, (70, 100))

# Text
random_font = random.choice(pygame.font.get_fonts())
print(random_font)
font = pygame.font.SysFont(random_font, 60)
small_font = pygame.font.SysFont(random_font, 30)
title_text = font.render("ROCK, PAPER, SCISSORS", True, red)
winning_text = font.render("WINNER!", True, red)
losing_text = font.render('YOU LOSE', True, red)
tie_text = font.render('TIE', True, red)
comp_text = small_font.render('COMPUTER CHOICE', True, red)
user_text = small_font.render('YOUR CHOICE', True, red)
streak_text = font.render('STREAK:', True, red)

text_list = [winning_text, losing_text, tie_text]
text_word_list = ['win', 'lose', 'tie']

# FPS


class Button:
    def __init__(self, x, y, colour, rect, img, name, beat):
        self.x = x
        self.y = y
        self.colour = colour
        self.rect = rect
        self.img = img
        self.name = name
        self.beat = beat
        button_list.append(self)

    def press(self):
        mouse_pos = pygame.mouse.get_pos()
        if_pressed = pygame.mouse.get_pressed()
        if if_pressed[0] and (self.x < mouse_pos[0] < self.x + b_width and self.y < mouse_pos[1] < self.y + b_height):
            self.colour = (255, 0, 0)
        else:
            self.colour = (0, 12, 21)

    def draw(self):
        pygame.draw.rect(screen, self.colour, self.rect)
        screen.blit(self.img, (self.x + 40 - 35, self.y - 180))

    def comp(self):
        screen.blit(comp_text, (self.x + 40 - comp_text.get_width() / 2, self.y + 50))

    def user(self):
        screen.blit(user_text, (self.x + 40 - user_text.get_width() / 2, self.y + 90))

    def check_win(self, comp_choice):
        pygame.draw.rect(screen, (102, 102, 255), cover_rect)
        if comp_choice == self.beat:
            return 'lose', self.name, comp_choice
        elif comp_choice == self.name:
            return 'tie', self.name, comp_choice
        else:
            return 'win', self.name, comp_choice


def comp_pick(options_list):
    comp_choice = random.choice(options_list)
    return comp_choice


def streak(streak_p):
    pygame.draw.rect(screen, (102, 102, 255), streak_cover_rect)
    streak_p = str(streak_p)
    screen.blit(streak_text, (0, 0))
    actual_streak = font.render(streak_p, True, red)
    screen.blit(actual_streak, (0, 50))


def blit_text():
    global streak_num
    for i in range(3):
        if i == 1:
            button_list[(rps.index(win_list[0][1]))].user()
        elif i == 2:
            button_list[(rps.index(win_list[0][2]))].comp()
        elif i == 0:
            screen.blit(text_list[text_word_list.index(win_list[0][0])], (s_width / 2 -
                        text_list[text_word_list.index(win_list[0][0])].get_width() / 2, s_height-50))
            if win_list[0][0] == 'win':
                streak_num += 1
            elif win_list[0][0] == 'lose':
                streak_num = 0
            elif win_list[0][0] == 'tie':
                streak_num = 0
    return streak_num


def main():
    global streak_num
    screen.fill((102, 102, 255))
    b_colour = (0, 12, 21)
    Button(rock.x, rock.y, b_colour, rock, rock_pic, 'rock', 'paper')
    Button(paper.x, paper.y, b_colour, paper, paper_pic, 'paper', 'scissors')
    Button(scissors.x, scissors.y, b_colour, scissors, scissors_pic, 'scissors', 'rock')
    screen.blit(title_text, (s_width / 2 - title_text.get_width() / 2, 30))
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in pygame.font.get_fonts():
                    print(item)
                i = 0
                for thing in button_list:
                    if thing.x < pygame.mouse.get_pos()[0] < thing.x + b_width and thing.y < pygame.mouse.get_pos()[
                         1] < thing.y + b_height:
                        win_list.append(thing.check_win(comp_pick(rps)))
                        thing.check_win(win_list[0][2])
                        streak_num = blit_text()
                    i += 1
        win_list.clear()
        for item in button_list:
            item.press()
            item.draw()

        streak(streak_num)

        pygame.display.update()

    pygame.quit()


main()
