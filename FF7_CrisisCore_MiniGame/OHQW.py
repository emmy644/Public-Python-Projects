# Import
import pygame
import random
from pygame import mixer
pygame.init()
mixer.init()

# Variables
s_width = 1440
s_height = 780
velocity = 6
jump_velocity = 15
jump = False
e_press = False
within_vicinity = False
nv = None
increasing_num = 0
line_num = 0
num_of_surface_obj = 0

red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
green = (0, 204, 0)
blue = (0, 128, 255)
purple = (127, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
darker_white = (249, 252, 220)

# Lists
ground_list = []
npc_list = []
on_screen_dialogue_list = []

# Images
arrow = pygame.image.load('Images/arrow.png')
arrow = pygame.transform.scale(arrow, (84, 66))

zack_left = pygame.image.load('Images/zack.png')
zack_left = pygame.transform.scale(zack_left, (80, 120))
zack_walk_left = pygame.image.load('Images/zack_1.png')
zack_walk_left = pygame.transform.scale(zack_walk_left, (80, 120))
zack_jump_left = pygame.image.load('Images/zack_stretch.png')
zack_jump_left = pygame.transform.scale(zack_jump_left, (80, 120))
zack_jump_right = pygame.transform.flip(zack_jump_left, True, False)
zack_right = pygame.transform.flip(zack_left, True, False)
zack_walk_right = pygame.transform.flip(zack_walk_left, True, False)
zack_crouch_left = pygame.image.load('Images/zack_crouch_left.png')
zack_crouch_left = pygame.transform.scale(zack_crouch_left, (80, 120))
zack_crouch_right = pygame.transform.flip(zack_crouch_left, True, False)

zack_list = [zack_left, zack_walk_left, zack_right, zack_walk_right, zack_jump_left, zack_jump_right,
             zack_crouch_left, zack_crouch_right]

cloud_left = pygame.image.load('Images/cloud_left.png')
cloud_left = pygame.transform.scale(cloud_left, (80, 120))
cloud_right = pygame.transform.flip(cloud_left, True, False)

cloud_list = [cloud_left, cloud_right]

genesis_left = pygame.image.load('Images/genesis_left.png')
genesis_left = pygame.transform.scale(genesis_left, (80, 120))
genesis_right = pygame.transform.flip(genesis_left, True, False)

genesis_list = [genesis_left, genesis_right]

aerith_left = pygame.image.load('Images/aerith_left.png')
aerith_left = pygame.transform.scale(aerith_left, (80, 120))
aerith_right = pygame.transform.flip(aerith_left, True, False)

aerith_list = [aerith_left, aerith_right]

sephy_left = pygame.image.load('Images/sephy_left.png')
sephy_left = pygame.transform.scale(sephy_left, (80, 120))
sephy_right = pygame.transform.flip(sephy_left, True, False)

sephy_list = [sephy_left, sephy_right]

angeal_left = pygame.image.load('Images/Angeal.png')
angeal_left = pygame.transform.scale(angeal_left, (80, 120))
angeal_right = pygame.transform.flip(angeal_left, True, False)

angeal_list = [angeal_left, angeal_right]

barret_left = pygame.image.load('Images/barret_left.png')
barret_left = pygame.transform.scale(barret_left, (105, 120))
barret_right = pygame.transform.flip(barret_left, True, False)

barret_list = [barret_left, barret_right]

text_box = pygame.image.load('Images/text_box.png')
text_box = pygame.transform.scale(text_box, (900, 113))

diamond = pygame.image.load('Images/diamond.png')
diamond = pygame.transform.scale(diamond, (113, 113))

# Dialogue Lists
cloud_dialogue_list = [['Not interested.']]
aerith_dialogue_list = [['Helloooooo??!?!?????']]
sephy_dialogue_list = [['DO DO DO DO DO DO DO DO DODODODODOODDODODODO DO DO DO DO']]
genesis_dialogue_list = [['Infinite in mystery... is the gift of the goddess. We seek it thus, and take to the sky. '
                         'Ripples form on the water\'s surface.', 'The wandering soul knows no rest. Even if the '
                          'morrow is barren of promises, nothing shall forestall my return.']]
angeal_dialogue_list = [['Use brings about wear, tear, and rust. And that\'s a real waste.']]
barret_dialogue_list = [['There ain\'t no getting offa this train we\'re on!']]

# Now I shall give smash despair.
# FPS
FPS = 60
Clock = pygame.time.Clock()
frame = 1
text_frame_nums = 1

facing_left = True
facing_right = False

# Fonts
random_font = random.choice(pygame.font.get_fonts())
font = pygame.font.SysFont('trattatello', 18)
# name_text_box_font = pygame.font.SysFont('trattatello', 30)
press_e = font.render('Press E To Interact', True, black)


class Window:
    def __init__(self, width, height, colour):
        self.width = width
        self.height = height
        self.colour = colour
        self.display = pygame.display.set_mode((self.width, self.height))

    def colour_screen(self):
        self.display.fill(self.colour)


class Ground:
    def __init__(self, width, height, colour, coords):
        self.width = width
        self.height = height
        self.colour = colour
        self.coords = coords
        ground_list.append(self)

    def draw(self):
        pygame.draw.rect(main_window.display, self.colour, pygame.Rect(self.coords[0], self.coords[1], self.width,
                                                                       self.height))
        pygame.draw.rect(main_window.display, black, pygame.Rect(self.coords[0], self.coords[1], self.width,
                                                                 self.height), 4)


class Player:
    def __init__(self, coords):
        self.images = zack_list
        self.coords = coords
        self.rect = pygame.Rect(self.coords[0], self.coords[1], self.images[0].get_width(), self.images[0].get_height())

    def draw(self, index):
        main_window.display.blit(self.images[index], (self.rect.x, self.rect.y+20))

    def jump(self, key_pressed):
        global jump_velocity
        global jump
        if key_pressed[pygame.K_SPACE]:
            jump = True
        if jump:
            for ground in ground_list:
                ground.coords[1] += jump_velocity
            for npc in npc_list:
                npc.coords[1] += jump_velocity
            jump_velocity -= 1

        for h in ground_list:
            if jump_velocity < 0 and self.rect.y+zack_left.get_height() <= h.coords[1] and if_above_platform(h, self):
                if self.rect.y+zack_left.get_height() == h.coords[1] or self.rect.y+zack_left.get_height() - \
                        jump_velocity > h.coords[1]:
                    jump = False
                    vertical_dist = h.coords[1]-(self.rect.y + zack_left.get_height())
                    for ground in ground_list:
                        ground.coords[1] -= vertical_dist
                    for npc in npc_list:
                        npc.coords[1] -= vertical_dist
                    jump_velocity = 15
            if self.rect.y + zack_left.get_height() == h.coords[1] and if_above_platform(h, self) is False:
                jump = True
                if jump_velocity == 15:
                    jump_velocity = 0

    def respawn(self):
        global jump_velocity
        global jump
        if main_ground.coords[1] < -1000:
            jump_velocity = 15
            jump = False
            h_dist = main_ground.coords[0] - self.rect.x
            v_dist = main_ground.coords[1] - self.rect.y - zack_left.get_height()
            for h in ground_list:
                h.coords[0] -= h_dist
                h.coords[1] -= v_dist
            for g in npc_list:
                g.coords[0] -= h_dist
                g.coords[1] -= v_dist

    def move(self, key_pressed):
        global frame
        global facing_right
        global facing_left
        frame += 1
        if pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed()[pygame.K_d]:
            if facing_right and jump_velocity == 15:
                draw_frame(frame, 2, 7, self)
            elif facing_right and jump_velocity != 15:
                self.draw(5)
            elif facing_left and jump_velocity == 15:
                draw_frame(frame, 0, 6, self)
            elif facing_left and jump_velocity != 15:
                self.draw(4)
        elif key_pressed[pygame.K_a] or key_pressed[pygame.K_d]:
            if key_pressed[pygame.K_a] and jump_velocity == 15:
                facing_left = True
                facing_right = False
                draw_frame(frame, 0, 1, self)
                move_background(facing_left, facing_right)
            if key_pressed[pygame.K_a] and jump_velocity != 15:
                facing_left = True
                facing_right = False
                self.draw(4)
                move_background(facing_left, facing_right)
            if key_pressed[pygame.K_d] and jump_velocity == 15:
                facing_left = False
                facing_right = True
                draw_frame(frame, 2, 3, self)
                move_background(facing_left, facing_right)
            if key_pressed[pygame.K_d] and jump_velocity != 15:
                facing_left = False
                facing_right = True
                self.draw(5)
                move_background(facing_left, facing_right)
        else:
            if facing_right and jump_velocity == 15:
                draw_frame(frame, 2, 7, self)
            elif facing_right and jump_velocity != 15:
                self.draw(5)

            if facing_left and jump_velocity == 15:
                draw_frame(frame, 0, 6, self)
            elif facing_left and jump_velocity != 15:
                self.draw(4)

        if frame == 30:
            frame = 1

    def interact(self):
        global text_frame_nums
        global within_vicinity
        global nv
        global increasing_num
        global e_press
        global line_num
        for npc in npc_list:
            text_frame_nums += 1
            if text_frame_nums == 15:
                text_frame_nums = 1
            if self.within_vicinity(npc):
                nv = npc
                npc.play_music()
                if pygame.key.get_pressed()[pygame.K_e]:
                    e_press = True
                    within_vicinity = True
                elif self.within_vicinity(nv) is False:
                    e_press = False
            if nv is not None:
                if self.within_vicinity(nv) is False:
                    mixer.music.pause()
                    increasing_num = 0

            if not e_press and nv is not None:
                if self.within_vicinity(nv):
                    # Draw Press E Box and Name Above Head Box
                    interact_name_text = font.render(nv.name, True, black)
                    width = interact_name_text.get_width() + 10
                    pygame.draw.rect(main_window.display, white, pygame.Rect(nv.coords[0], nv.coords[1] - 40, width,
                                                                             30))
                    pygame.draw.rect(main_window.display, black, pygame.Rect(nv.coords[0], nv.coords[1] - 40, width,
                                                                             30), 3)
                    pygame.draw.rect(main_window.display, white, pygame.Rect(nv.coords[0], nv.coords[1] - 75, press_e.
                                                                             get_width() + 10, 30))
                    pygame.draw.rect(main_window.display, black, pygame.Rect(nv.coords[0], nv.coords[1] - 75, press_e.
                                                                             get_width() + 10, 30), 3)
                    main_window.display.blit(interact_name_text, (nv.coords[0] + 5, nv.coords[1]-40))
                    main_window.display.blit(press_e, (nv.coords[0] + 5, nv.coords[1]-75, 100, 30))

            if e_press and Zack.within_vicinity(nv):
                # Draw Big Chat Window Box
                main_window.display.blit(text_box, (self.coords[0]+zack_left.get_width()/2-text_box.get_width()/2-3,
                                                    self.coords[1] + 250))
                main_window.display.blit(diamond, (
                 self.coords[0] + zack_left.get_width() / 2 - text_box.get_width() / 2 - diamond.get_width() / 2,
                 self.coords[1] + 250 + text_box.get_height() / 2 - diamond.get_height() / 2))
                main_window.display.blit(resize_for_chat_icon(nv.images[1]), (self.coords[0]+zack_left.get_width()/2 -
                                         text_box.get_width()/2 - resize_for_chat_icon(nv.images[1]).get_width()/2+6,
                                         self.coords[1]+250+text_box.get_height()/2 - resize_for_chat_icon(nv.images[1])
                                         .get_height()/2))
                name_text = font.render(nv.name.upper(), True, black)
                main_window.display.blit(name_text, (self.coords[0]+zack_left.get_width()/2-text_box.get_width()/2+80,
                                                     self.coords[1]+250+text_box.get_height()/2 -
                                                     resize_for_chat_icon(nv.images[1]).get_height()/2-10))
                # Dialogue
                if len(on_screen_dialogue_list) == 0:
                    for i in range(len(nv.dialogue_list[0])):
                        on_screen_dialogue_list.append('a')
                dialogue_text = font.render(nv.dialogue_list[0][line_num][0:increasing_num], True, black)
                on_screen_dialogue_list[line_num] = dialogue_text
                for line in on_screen_dialogue_list:
                    if line != 'a':
                        main_window.display.blit(line, (self.coords[0]+zack_left.get_width()/2-text_box.get_width()/2 +
                                                        80, self.coords[1] +
                                                        (288 + 30*on_screen_dialogue_list.index(line))))
                if len(nv.dialogue_list[0][line_num]) != len(nv.dialogue_list[0][line_num][0:increasing_num]):
                    if text_frame_nums == 7:
                        increasing_num += 1
                else:
                    if len(nv.dialogue_list[0])-1 == line_num:
                        main_window.display.blit(arrow, (self.coords[0]+zack_left.get_width()/2+text_box.get_width() /
                                                         2+5, self.coords[1] + 250 + text_box.get_height() / 2
                                                         - arrow.get_height() / 2))

                    elif (line_num + 1) < len((nv.dialogue_list[0])):
                        line_num += 1
                        increasing_num = 0
                    if pygame.key.get_pressed()[pygame.K_RIGHT]:
                        increasing_num = 0
                        line_num = 0
                        on_screen_dialogue_list.clear()
                        e_press = False

            elif e_press and Zack.within_vicinity(nv) is False:
                on_screen_dialogue_list.clear()
                increasing_num = 0
                line_num = 0
                e_press = False

    def within_vicinity(self, npc):
        if npc.coords[0] - 100 < self.rect.x + zack_left.get_width() / 2 < npc.coords[0] + npc.width + 100 and \
                npc.coords[1]-30 <= self.rect.y + zack_left.get_height() <= npc.coords[1] + npc.height:
            return True
        else:
            return False


class NPC:
    def __init__(self, coords, images, name, music, dialogue_list):
        self.coords = coords
        self.images = images
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.name = name
        self.music = music
        self.dialogue_list = dialogue_list
        npc_list.append(self)

    def draw(self):
        if Zack.rect.x <= self.coords[0]:
            main_window.display.blit(self.images[0], (self.coords[0], self.coords[1]))
        else:
            main_window.display.blit(self.images[1], (self.coords[0], self.coords[1]))

    def play_music(self):
        if not mixer.music.get_busy():
            mixer.music.set_volume(0.5)
            mixer.music.load(self.music)
            mixer.music.play(-1)


def if_above_platform(ground, player):
    if ground.coords[0] <= player.rect.x + 0.23 * zack_left.get_width() <= ground.coords[0] + ground.width or \
            ground.coords[0] <= player.rect.x + zack_left.get_width() / 2 <= ground.coords[0] + ground.width or \
            ground.coords[0] <= player.rect.x + 0.8 * zack_left.get_width() <= ground.coords[0] + ground.width:
        return True
    else:
        return False


def update_display():
    pygame.display.update()


def move_background(left, right):
    if left:
        for p in ground_list:
            p.coords[0] += velocity
        for n in npc_list:
            n.coords[0] += velocity
    elif right:
        for p in ground_list:
            p.coords[0] -= velocity
        for n in npc_list:
            n.coords[0] -= velocity


def draw_frame(frame_num, draw1, draw2, self):
    if frame_num <= 15:
        self.draw(draw1)
    elif frame_num > 15:
        self.draw(draw2)


def resize_for_chat_icon(regular_image):
    return pygame.transform.scale(regular_image, (regular_image.get_width()/1.7, 120/1.7))


# Windows
main_window = Window(s_width, s_height, blue)

# Main Ground
main_ground = Ground(2000, 500, green, [0, 680])
# Platforms
platform_1 = Ground(200, 20, black, [100, 600])
platform_2 = Ground(400, 20, black, [400, 500])
platform_3 = Ground(120, 20, black, [300, 400])
platform_4 = Ground(400, 20, black, [1200, 460])
platform_5 = Ground(200, 20, black, [900, 390])
platform_6 = Ground(300, 20, black, [500, 300])

# Player
Zack = Player((s_width/2-zack_left.get_width()/2, 500-zack_left.get_height()))

# NPC'S
Cloud = NPC([200, 600-cloud_left.get_height()+20], cloud_list, 'Cloud', 'Music/Cloud.mp3', cloud_dialogue_list)
Genesis = NPC([300, 400-genesis_left.get_height()+20], genesis_list, 'Genesis', 'Music/Genesis.mp3',
              genesis_dialogue_list)
Aerith = NPC([650, 500-aerith_left.get_height()+20], aerith_list, 'Aerith', 'Music/Aerith.mp3', aerith_dialogue_list)
Sephiroth = NPC([1000, 390-sephy_left.get_height()+20], sephy_list, 'Sephiroth', 'Music/Sephy.mp3',
                sephy_dialogue_list)
Angeal = NPC([1300, 460-angeal_right.get_height()+20], angeal_list, 'Angeal', 'Music/Angeal.mp3', angeal_dialogue_list)
Barret = NPC([600, 300-barret_left.get_height()+20], barret_list, 'Barret', 'Music/Barret.mp3', barret_dialogue_list)


def main():
    run = True
    while run:
        Clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        main_window.colour_screen()
        for t in ground_list:
            t.draw()
        for y in npc_list:
            y.draw()
        Zack.respawn()
        Zack.interact()
        Zack.jump(pygame.key.get_pressed())
        Zack.move(pygame.key.get_pressed())
        update_display()

    pygame.quit()


main()
