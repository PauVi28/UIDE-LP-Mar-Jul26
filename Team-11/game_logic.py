import os
import pygame
import math

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 60

CHAR_WIDTH = 200
CHAR_HEIGHT = 200
BOWSER_WIDTH = 260
BOWSER_HEIGHT = 240

HP_MARIO = 200
DMG_MARIO = 40

HP_LUIGI = 200
DMG_LUIGI = 40

HP_BOWSER = 500
DMG_BOWSER = 50

ANIMATION_SPEED_MARIO = 70
ANIMATION_SPEED_LUIGI = 86
ANIMATION_SPEED_BOWSER = 60

WALK_IN_SPEED_MARIO = 10
WALK_IN_SPEED_LUIGI = 10
WALK_IN_SPEED_BOWSER = 8

ATTACK_WALK_SPEED_MARIO = 6
ATTACK_WALK_SPEED_LUIGI = 7
ATTACK_WALK_SPEED_BOWSER = 5

RETURNING_SPEED_MARIO = 12
RETURNING_SPEED_LUIGI = 12
RETURNING_SPEED_BOWSER = 8

DEFENSE_WINDOW_MS = 400
MAX_DEFENSE_SPAM = 3
DEFENSE_LOCKOUT_TURNS = 2

POS_MARIO_OFFSCREEN = (-400, 360)
POS_MARIO_CENTER = (700, 360)

POS_LUIGI_CENTER = (700, 500)
POS_LUIGI_OFFSCREEN = (-400, 560)

POS_BOWSER_OFFSCREEN = (2000, 390)
POS_BOWSER_CENTER = (1100, 390)

POS_MARIO_ATTACK_TARGET = (1000, 430)
POS_LUIGI_ATTACK_TARGET = (1000, 430)
POS_BOWSER_ATTACK_TARGET = (800, 350)
POS_BOWSER_ATTACK_LUIGI_TARGET = (200, 490)

STATE_IDLE = "idle"
STATE_ATTACKING = "attacking"
STATE_RETURNING = "returning"
STATE_DEFENSE = "defense"
STATE_HAMMER_ATTACK = "hammer_attack"
STATE_HAMMER_FAIL = "hammer_fail"
STATE_HAMMER_GOOD = "hammer_good"
STATE_HAMMER_EXCELENT = "hammer_excelent"
STATE_DEAD = "dead"
STATES = [STATE_IDLE, STATE_ATTACKING, STATE_RETURNING, STATE_DEFENSE, STATE_DEAD,
          STATE_HAMMER_ATTACK, STATE_HAMMER_FAIL, STATE_HAMMER_GOOD, STATE_HAMMER_EXCELENT]

class Character:
    def __init__(self, name, x, y, width, height, anim_speed, max_idle_frames, hp, damage, walk_in_speed, attack_walk_speed, returning_speed):
        self.name = name.lower()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.anim_speed = anim_speed
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.walk_in_speed = walk_in_speed
        self.attack_walk_speed = attack_walk_speed
        self.returning_speed = returning_speed
        self.entered_screen = False
        self.damage_dealt = False
        self.state = STATE_IDLE
        self.target_x = x
        self.target_y = y
        self.frames = {state: [] for state in STATES}
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

        self.is_defending = False
        self.defense_timer = 0
        self.defense_presses = 0
        self.lockout_turns = 0
        self.load_animations(max_idle_frames)
    def load_animations(self, max_idle_frames):
        base_path = os.path.join("assets", self.name)
        state_file_map = {
            STATE_IDLE: "idle",
            STATE_ATTACKING: "attack",
            STATE_RETURNING: "returning",
            STATE_DEFENSE: "defense",
            STATE_HAMMER_ATTACK: "attack",
            STATE_HAMMER_FAIL: "attack_miss",
            STATE_HAMMER_GOOD: "attack_good",
            STATE_HAMMER_EXCELENT: "attack_excelent",
            STATE_DEAD: "dead",
        }
        for state, file_key in state_file_map.items():
            prefixes = [f"{self.name}_{file_key}", file_key]
            for prefix in prefixes:
                i = 1
                while True:
                    path = os.path.join(base_path, f"{prefix}{i}.png")
                    if os.path.exists(path):
                        img = pygame.image.load(path).convert_alpha()
                        img = pygame.transform.scale(img, (self.width, self.height))
                        self.frames[state].append(img)
                        i += 1
                    else:
                        break
                if self.frames[state]:
                    break
            if not self.frames[state] and state != STATE_IDLE:
                self.frames[state] = list(self.frames[STATE_IDLE])
        print(f"[LOAD] {self.name}: " + ", ".join(f"{s}={len(self.frames[s])}" for s in self.frames))
    def update(self):
        now = pygame.time.get_ticks()
        if self.is_defending and now - self.defense_timer > DEFENSE_WINDOW_MS:
            self.is_defending = False
        now = pygame.time.get_ticks()
        if now - self.last_update > self.anim_speed:
            if self.current_frame == len(self.frames[self.state]) - 1:
                if self.state not in [STATE_IDLE, STATE_RETURNING]:
                    pass
                else:
                    self.current_frame = 0
                    self.last_update = now
            else:
                self.current_frame += 1
                self.last_update = now
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if self.state == STATE_RETURNING:
            current_speed = self.returning_speed
        else:
            current_speed = self.walk_in_speed if not self.entered_screen else self.attack_walk_speed
        if dist > current_speed:
            self.x += current_speed * (dx / dist)
            self.y += current_speed * (dy / dist)
        else:
            self.x = self.target_x
            self.y = self.target_y
            if self.target_x != POS_MARIO_OFFSCREEN[0] and self.target_x != POS_BOWSER_OFFSCREEN[0] and self.target_x != POS_LUIGI_OFFSCREEN[0]:
                self.entered_screen = True
    def draw(self, surface):
        if len(self.frames[self.state]) > 0:
            img = self.frames[self.state][self.current_frame]
            draw_x, draw_y = self.x, self.y
            if self.is_defending:
                import random
                draw_x += random.randint(-4, 4)
                draw_y += random.randint(-4, 4)
            if self.is_defending:
                glow_img = img.copy()
                glow_img.fill((150, 150, 150), special_flags=pygame.BLEND_RGB_ADD)
                surface.blit(glow_img, (draw_x, draw_y))
            elif self.lockout_turns > 0:
                now = pygame.time.get_ticks()
                if (now // 150) % 2 == 0:
                    red_img = img.copy()
                    red_img.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_MULT)
                    surface.blit(red_img, (draw_x, draw_y))
                else:
                    surface.blit(img, (draw_x, draw_y))
            else:
                surface.blit(img, (draw_x, draw_y))
    def activate_defense(self, now):
        if self.lockout_turns > 0:
            return
        self.defense_presses += 1
        if self.defense_presses >= MAX_DEFENSE_SPAM:
            self.lockout_turns = DEFENSE_LOCKOUT_TURNS
            self.is_defending = False
            return
        if not self.is_defending:
            self.is_defending = True
            self.defense_timer = now

    def set_state(self, new_state):
        if new_state in self.frames and new_state != self.state:
            self.state = new_state
            self.current_frame = 0
            self.last_update = pygame.time.get_ticks()

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

class Mario(Character):
    def __init__(self):
        super().__init__("mario", POS_MARIO_OFFSCREEN[0], POS_MARIO_OFFSCREEN[1], CHAR_WIDTH, CHAR_HEIGHT, ANIMATION_SPEED_MARIO, 154, HP_MARIO, DMG_MARIO, WALK_IN_SPEED_MARIO, ATTACK_WALK_SPEED_MARIO, RETURNING_SPEED_MARIO)

class Luigi(Character):
    def __init__(self):
        super().__init__("luigi", POS_LUIGI_OFFSCREEN[0], POS_LUIGI_OFFSCREEN[1], CHAR_WIDTH, CHAR_HEIGHT, ANIMATION_SPEED_LUIGI, 119, HP_LUIGI, DMG_LUIGI, WALK_IN_SPEED_LUIGI, ATTACK_WALK_SPEED_LUIGI, RETURNING_SPEED_LUIGI)

class Bowser(Character):
    def __init__(self):
        super().__init__("bowser", POS_BOWSER_OFFSCREEN[0], POS_BOWSER_OFFSCREEN[1], BOWSER_WIDTH, BOWSER_HEIGHT, ANIMATION_SPEED_BOWSER, 216, HP_BOWSER, DMG_BOWSER, WALK_IN_SPEED_BOWSER, ATTACK_WALK_SPEED_BOWSER, RETURNING_SPEED_BOWSER)

def ip_to_code(ip_str, port):
    parts = ip_str.split('.')
    if len(parts) == 4:
        octet = int(parts[3])
        port_offset = port - 50000
        if port_offset < 0: port_offset = 0
        if port_offset > 999: port_offset = 999
        code_int = port_offset * 1000 + octet
        return str(code_int).zfill(6)
    return "000000"

def code_to_ip(code):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '192.168.1.1'
    finally:
        s.close()
    parts = local_ip.split('.')
    base_ip = f"{parts[0]}.{parts[1]}.{parts[2]}."
    try:
        code_int = int(code)
    except ValueError:
        return base_ip + "1", 50000
    octet = code_int % 1000
    port_offset = code_int // 1000
    port = 50000 + port_offset
    return base_ip + str(octet), port
