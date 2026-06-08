import pygame
import random

ANCHO_VENTANA = 1920
ALTO_VENTANA = 1080
FPS = 60

ANCHO_BOTON = 300
ALTO_BOTON = 80
BOTON_X = ANCHO_VENTANA // 2 - ANCHO_BOTON // 2
BOTON_Y = ALTO_VENTANA // 2 + 50

PLAYER_SPEED = 5
PORTAL_X = ANCHO_VENTANA - 150
PORTAL_Y = ALTO_VENTANA // 2 - 60
PORTAL_SIZE = 80
PORTAL_PROXIMITY_DISTANCE = 90

ANIMATION_SPEED = 55

LUIGI_BATTLE_WIDTH = 90
LUIGI_BATTLE_HEIGHT = 140
BOWSER_BATTLE_WIDTH = 150
BOWSER_BATTLE_HEIGHT = 190
BOWSER_FRAMES = 16

DISCOVERY_PORT = 5556
ROOM_CODE_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

BATTLE_BACKGROUND = "assets/background/battle_bg1.png"

BATTLE_MUSIC = "assets/music/battle_music1.flac"
BATTLE_MUSIC_VOLUME = 0.1

PERSONAJE_X_INICIAL = 350
PERSONAJE_Y_INICIAL = ALTO_VENTANA // 2 - LUIGI_BATTLE_HEIGHT // 2
LOBBY_PLAYER_X_INICIAL = 200
LOBBY_PLAYER_Y_INICIAL = ALTO_VENTANA // 2 - 60

JEFE_X_INICIAL = ANCHO_VENTANA - BOWSER_BATTLE_WIDTH - 350
JEFE_Y_INICIAL = PERSONAJE_Y_INICIAL + LUIGI_BATTLE_HEIGHT - BOWSER_BATTLE_HEIGHT

PLAYER_ATTACK_X = 1050
BOSS_ATTACK_X = 700

ANCHO_BARRA = ANCHO_VENTANA
ALTO_BARRA = 110
BARRA_Y = ALTO_VENTANA - ALTO_BARRA

ANCHO_BOTON_ATACAR = 320
ALTO_BOTON_ATACAR = 70
BOTON_ATACAR_X = 100
BOTON_ATACAR_Y_NORMAL = BARRA_Y + 20
BUTTON_ANIMATION_DURATION = 400

TIMING_RED_FRACTION_ATTACK    = 0.25
TIMING_RED_FRACTION_DEFENSE   = 0.25
TIMING_ORANGE_FRACTION_ATTACK = 0.25
TIMING_ORANGE_FRACTION_DEFENSE= 0.25
TIMING_GREEN_FRACTION_ATTACK  = 0.12
TIMING_GREEN_FRACTION_DEFENSE = 0.035

TIMING_BAR_X = 200
TIMING_BAR_Y = 820
TIMING_BAR_WIDTH = 1520
TIMING_BAR_HEIGHT = 45
TIMING_SPEED_ATTACK = 12
TIMING_SPEED_DEFENSE = 18

MAX_HP_JUGADOR = 100
MAX_HP_JEFE = 120
ANCHO_BARRA_VIDA = 380
ALTO_BARRA_VIDA = 32
JUGADOR_HP_X = 100
JUGADOR_HP_Y = 50
JEFE_HP_X = ANCHO_VENTANA - 480
JEFE_HP_Y = 50

TIEMPO_ESPERA_JEFE = 1800
VICTORY_DURATION = 3500
GAME_OVER_DURATION = 3500


class Luigi:
    def __init__(self):
        self.animations = load_luigi_idle_animations()
        self.battle_x = PERSONAJE_X_INICIAL
        self.current_direction = 'right'
        self.animation_frame = 0
        self.last_animation_time = 0

    def get_current_frame(self):
        return self.animations[self.current_direction][self.animation_frame]

    def update_battle_animation(self, current_time):
        if current_time - self.last_animation_time > ANIMATION_SPEED:
            self.animation_frame = (self.animation_frame + 1) % len(self.animations[self.current_direction])
            self.last_animation_time = current_time


class Mario:
    def __init__(self):
        self.animations = load_mario_idle_animations()
        self.battle_x = PERSONAJE_X_INICIAL
        self.current_direction = 'right'
        self.animation_frame = 0
        self.last_animation_time = 0

    def get_current_frame(self):
        return self.animations[self.current_direction][self.animation_frame]

    def update_battle_animation(self, current_time):
        if current_time - self.last_animation_time > ANIMATION_SPEED:
            self.animation_frame = (self.animation_frame + 1) % len(self.animations[self.current_direction])
            self.last_animation_time = current_time


class Bowser:
    def __init__(self):
        self.idle_animations = load_bowser_idle_animations()
        self.battle_x = JEFE_X_INICIAL
        self.animation_frame = 0
        self.last_animation_time = 0
        self.is_moving = False

    def update_animation(self, current_time):
        if self.is_moving:
            self.animation_frame = 0
            return
        if current_time - self.last_animation_time > ANIMATION_SPEED:
            self.animation_frame = (self.animation_frame + 1) % len(self.idle_animations)
            self.last_animation_time = current_time

    def get_current_frame(self):
        return self.idle_animations[self.animation_frame]

    def move_to_attack(self):
        self.is_moving = True
        self.animation_frame = 0
        self.battle_x -= 7
        return self.battle_x <= BOSS_ATTACK_X

    def return_to_position(self):
        self.is_moving = True
        self.animation_frame = 0
        self.battle_x += 7
        return self.battle_x >= JEFE_X_INICIAL

    def stop_moving(self):
        self.is_moving = False
        self.animation_frame = 0


class Game:
    def __init__(self, character="mario"):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Boss Slayer Arena - Equipo 11")
        self.clock = pygame.time.Clock()

        self.font_titulo, self.font_boton, self.font_grande, self.font_pequeña = create_fonts()

        if character.lower() == "mario":
            self.player = Mario()
        else:
            self.player = Luigi()

        self.player2 = Luigi()
        self.boss = Bowser()

        self.boton_iniciar = pygame.Rect(BOTON_X, BOTON_Y, ANCHO_BOTON, ALTO_BOTON)
        self.boton_multijugador = pygame.Rect(BOTON_X, BOTON_Y + 120, ANCHO_BOTON, ALTO_BOTON)
        self.boton_local_multi = pygame.Rect(BOTON_X, BOTON_Y + 240, ANCHO_BOTON, ALTO_BOTON)
        self.boton_atacar_rect = pygame.Rect(BOTON_ATACAR_X, BOTON_ATACAR_Y_NORMAL, ANCHO_BOTON_ATACAR, ALTO_BOTON_ATACAR)

        self.state = True
        self.selected_menu_option = 0

        self.room_code = ""
        self.joining_code = ""
        self.input_active = False
        self.is_hosting = False

        self.player_hp = MAX_HP_JUGADOR
        self.boss_hp = MAX_HP_JEFE
        self.current_turn = "player"
        self.boss_attack_timer = 0
        self.victory_start_time = 0
        self.game_over_start_time = 0
        self.level_intro_start_time = 0

        self.timing_active = False
        self.timing_position = 0
        self.timing_direction = 1
        self.is_defense = False

        self.floating_damages = []
        self.timing_feedback = None
        self.feedback_timer = 0
        self.shake_duration = 0

        self.player_moving_to_attack = False
        self.boss_moving_to_attack = False
        self.returning_to_position = False
        self.running = True

        self.is_multiplayer = False
        self.is_server = False
        self.network = None
        self.local_multiplayer = False

        self.battle_music_loaded = False
        try:
            pygame.mixer.music.load(BATTLE_MUSIC)
            self.battle_music_loaded = True
        except:
            print(f"No se pudo cargar la música: {BATTLE_MUSIC}")

    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()
            self.handle_events(current_time)
            self.update(current_time)
            self.draw(current_time)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self, current_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state is True:
                    if event.key == pygame.K_UP:
                        self.selected_menu_option = max(0, self.selected_menu_option - 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected_menu_option = min(2, self.selected_menu_option + 1)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_menu_option == 0:
                            self.local_multiplayer = False
                            self.state = "level_intro"
                            self.level_intro_start_time = current_time
                        elif self.selected_menu_option == 1:
                            self.state = "multiplayer_select"
                        elif self.selected_menu_option == 2:
                            self.local_multiplayer = True
                            self.state = "level_intro"
                            self.level_intro_start_time = current_time

                elif self.state == "level_intro":
                    self.start_battle(current_time)
                elif self.state is False:
                    self.handle_battle_input(current_time)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state == "multiplayer_select":
                crear_rect = pygame.Rect(ANCHO_VENTANA//2 - 200, 200, 400, 80)
                if crear_rect.collidepoint(event.pos):
                    self.room_code = generar_codigo_partida()
                    self.is_hosting = True
                    self.state = "hosting"

                unir_rect = pygame.Rect(ANCHO_VENTANA//2 - 200, 320, 400, 80)
                if unir_rect.collidepoint(event.pos):
                    self.joining_code = ""
                    self.input_active = True
                    self.state = "joining"

            if self.state == "joining" and self.input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(self.joining_code) >= 4:
                        self.input_active = False
                        self.state = "level_intro"
                        self.level_intro_start_time = current_time
                    elif event.key == pygame.K_BACKSPACE:
                        self.joining_code = self.joining_code[:-1]
                    elif len(self.joining_code) < 6 and event.unicode.isalnum():
                        self.joining_code += event.unicode.upper()

    def start_battle(self, current_time):
        self.state = False
        self.player_hp = MAX_HP_JUGADOR
        self.boss_hp = MAX_HP_JEFE
        self.current_turn = "player"
        self.boss_attack_timer = 0
        self.player.battle_x = PERSONAJE_X_INICIAL
        self.player2.battle_x = 200
        self.boss.battle_x = JEFE_X_INICIAL
        self.player.current_direction = 'right'
        self.player2.current_direction = 'right'
        self.player.animation_frame = 0
        self.player2.animation_frame = 0
        self.boss.current_direction = 'left'
        self.boss.stop_moving()

        if self.local_multiplayer:
            self.current_turn = "player"
        self.timing_active = False
        self.floating_damages.clear()
        self.timing_feedback = None

        if self.battle_music_loaded:
            pygame.mixer.music.set_volume(BATTLE_MUSIC_VOLUME)
            pygame.mixer.music.play(-1)

    def handle_battle_input(self, current_time):
        if self.local_multiplayer:
            if self.current_turn == "player" and not self.timing_active:
                if not self.player_moving_to_attack and not self.returning_to_position:
                    self.player_moving_to_attack = True
            elif self.current_turn == "player2" and not self.timing_active:
                if not self.player_moving_to_attack and not self.returning_to_position:
                    self.player_moving_to_attack = True
            elif self.timing_active:
                if self.current_turn == "player":
                    self.execute_player_attack(current_time)
                elif self.current_turn == "player2":
                    self.execute_player2_attack(current_time)
        else:
            if self.current_turn == "player":
                if not self.timing_active and not self.player_moving_to_attack and not self.returning_to_position:
                    self.player_moving_to_attack = True
                elif self.timing_active:
                    self.execute_player_attack(current_time)
            elif self.current_turn == "boss" and self.timing_active and self.is_defense:
                self.execute_defense(current_time)

    def execute_player_attack(self, current_time):
        self.boss_hp, damage_done = player_attack(self.boss_hp, self.timing_position)
        if damage_done == 35: self.timing_feedback = "PERFECT"
        elif damage_done == 22: self.timing_feedback = "GOOD"
        else: self.timing_feedback = "MISS"
        self.feedback_timer = current_time

        if damage_done > 0:
            self.floating_damages.append({
                "x": JEFE_X_INICIAL + 30, "y": JEFE_Y_INICIAL - 40,
                "text": str(damage_done), "color": (255, 80, 80), "alpha": 255, "life": 70
            })
            self.shake_duration = 12

        self.timing_active = False
        self.returning_to_position = True

        if self.local_multiplayer:
            self.current_turn = "boss"
        else:
            self.current_turn = "boss"

        self.boss_attack_timer = current_time

    def execute_player2_attack(self, current_time):
        self.boss_hp, damage_done = player_attack(self.boss_hp, self.timing_position)
        if damage_done == 35: self.timing_feedback = "PERFECT"
        elif damage_done == 22: self.timing_feedback = "GOOD"
        else: self.timing_feedback = "MISS"
        self.feedback_timer = current_time

        if damage_done > 0:
            self.floating_damages.append({
                "x": JEFE_X_INICIAL + 30, "y": JEFE_Y_INICIAL - 40,
                "text": str(damage_done), "color": (255, 80, 80), "alpha": 255, "life": 70
            })
            self.shake_duration = 12

        self.timing_active = False
        self.returning_to_position = True
        self.current_turn = "boss"
        self.boss_attack_timer = current_time

    def execute_defense(self, current_time):
        self.player_hp, damage_taken = boss_attack(self.player_hp, self.timing_position, True)
        if damage_taken == 0: self.timing_feedback = "¡BIEN!"
        elif damage_taken == 8: self.timing_feedback = "GOOD"
        else: self.timing_feedback = "MISS"
        self.feedback_timer = current_time

        if damage_taken > 0:
            self.floating_damages.append({
                "x": PERSONAJE_X_INICIAL + 10, "y": PERSONAJE_Y_INICIAL - 40,
                "text": str(damage_taken), "color": (255, 80, 80), "alpha": 255, "life": 70
            })
            self.shake_duration = 12

        self.timing_active = False
        self.returning_to_position = True
        self.current_turn = "player"

    def update(self, current_time):
        if self.state is False:
            self.player.update_battle_animation(current_time)
            if self.local_multiplayer:
                self.player2.update_battle_animation(current_time)

            if self.player_moving_to_attack:
                self.player.battle_x += 7
                self.player.current_direction = 'right'
                if self.player.battle_x >= PLAYER_ATTACK_X:
                    self.player.battle_x = PLAYER_ATTACK_X
                    self.player_moving_to_attack = False
                    self.timing_active = True
                    self.timing_position = 0
                    self.timing_direction = 1
                    self.is_defense = False

            if self.boss_moving_to_attack:
                if self.boss.move_to_attack():
                    self.boss_moving_to_attack = False
                    self.timing_active = True
                    self.timing_position = 0
                    self.timing_direction = 1
                    self.is_defense = True
                    self.boss.stop_moving()

            if self.returning_to_position:
                if self.player.battle_x > PERSONAJE_X_INICIAL:
                    self.player.battle_x -= 7
                    self.player.current_direction = 'left'
                if self.boss.battle_x < JEFE_X_INICIAL:
                    self.boss.return_to_position()
                else:
                    self.boss.stop_moving()

                if self.player.battle_x <= PERSONAJE_X_INICIAL and self.boss.battle_x >= JEFE_X_INICIAL:
                    self.player.battle_x = PERSONAJE_X_INICIAL
                    self.boss.battle_x = JEFE_X_INICIAL
                    self.returning_to_position = False
                    self.player.current_direction = 'right'
                    self.player.animation_frame = 0
                    self.boss.stop_moving()

                    if self.local_multiplayer:
                        if self.current_turn == "player":
                            self.current_turn = "player2"
                        else:
                            self.current_turn = "player"
                    else:
                        self.current_turn = "player"

            self.boss.update_animation(current_time)

            if self.timing_active:
                speed = TIMING_SPEED_DEFENSE if self.is_defense else TIMING_SPEED_ATTACK
                self.timing_position += speed * self.timing_direction
                if self.is_defense and self.timing_position >= TIMING_BAR_WIDTH:
                    self.player_hp, damage_taken = boss_attack(self.player_hp, self.timing_position, False)
                    self.timing_feedback = "MISS"
                    self.feedback_timer = current_time
                    if damage_taken > 0:
                        self.floating_damages.append({
                            "x": PERSONAJE_X_INICIAL + 10, "y": PERSONAJE_Y_INICIAL - 40,
                            "text": str(damage_taken), "color": (255, 80, 80), "alpha": 255, "life": 70
                        })
                        self.shake_duration = 12
                    self.timing_active = False
                    self.returning_to_position = True
                    if self.local_multiplayer:
                        if self.current_turn == "player":
                            self.current_turn = "player2"
                        else:
                            self.current_turn = "player"
                    else:
                        self.current_turn = "player"
                elif self.timing_position >= TIMING_BAR_WIDTH or self.timing_position <= 0:
                    self.timing_direction *= -1

            for dmg in self.floating_damages[:]:
                dmg["y"] -= 1
                dmg["life"] -= 1
                dmg["alpha"] = int(255 * (dmg["life"] / 70))
                if dmg["life"] <= 0:
                    self.floating_damages.remove(dmg)

            if self.timing_feedback and current_time - self.feedback_timer > 1200:
                self.timing_feedback = None

            if self.shake_duration > 0:
                self.shake_duration -= 1

            if (self.current_turn == "boss" and not self.timing_active and 
                not self.boss_moving_to_attack and not self.returning_to_position):
                if current_time - self.boss_attack_timer >= TIEMPO_ESPERA_JEFE:
                    self.boss_moving_to_attack = True
                    if self.local_multiplayer:
                        if self.current_turn == "player":
                            self.current_turn = "player2"
                        else:
                            self.current_turn = "player"
                    else:
                        self.current_turn = "player"

            if self.boss_hp <= 0:
                self.state = "victory"
                self.victory_start_time = current_time
                if self.battle_music_loaded:
                    pygame.mixer.music.stop()
            if self.player_hp <= 0:
                self.state = "game_over"
                self.game_over_start_time = current_time
                if self.battle_music_loaded:
                    pygame.mixer.music.stop()

        elif self.state == "victory":
            if draw_victory(self.screen, self.font_grande, self.victory_start_time):
                self.reset_to_menu()
        elif self.state == "game_over":
            if draw_game_over(self.screen, self.font_grande, self.game_over_start_time):
                self.reset_to_menu()

    def reset_to_menu(self):
        self.state = True
        self.player.battle_x = PERSONAJE_X_INICIAL
        self.boss.battle_x = JEFE_X_INICIAL
        self.boss.current_direction = 'left'
        self.boss.stop_moving()
        self.timing_active = False
        self.floating_damages.clear()
        self.timing_feedback = None
        self.local_multiplayer = False
        if self.battle_music_loaded:
            pygame.mixer.music.stop()

    def draw(self, current_time):
        if self.state is True:
            draw_menu(self.screen, self.font_titulo, self.font_boton, 
                      self.boton_iniciar, self.boton_multijugador, self.boton_local_multi, self.selected_menu_option)
        elif self.state == "level_intro":
            draw_level_intro(self.screen, self.font_grande, self.font_boton, self.font_pequeña)
        elif self.state == "multiplayer_select":
            self.draw_multiplayer_select()
        elif self.state == "hosting":
            self.draw_hosting_screen()
        elif self.state == "joining":
            self.draw_joining_screen()
        elif self.state is False:
            shake = (random.randint(-6, 6), random.randint(-3, 3)) if self.shake_duration > 0 else (0, 0)
            player_frame = self.player.get_current_frame()
            boss_frame = self.boss.get_current_frame()
            luigi_frame = self.player2.get_current_frame() if self.local_multiplayer else None

            draw_battle(self.screen, self.font_boton, self.font_pequeña, self.boton_atacar_rect,
                        self.player_hp, self.boss_hp, self.current_turn, self.boss_attack_timer,
                        self.timing_active, self.timing_position, self.is_defense, self.timing_feedback,
                        self.player.battle_x, self.boss.battle_x, shake, player_frame, boss_frame,
                        local_multiplayer=self.local_multiplayer,
                        player2_battle_x=self.player2.battle_x,
                        player2_sprite=luigi_frame)

            font_damage = pygame.font.SysFont("Arial", 42, bold=True)
            for dmg in self.floating_damages:
                text_surf = font_damage.render(dmg["text"], True, dmg["color"])
                text_surf.set_alpha(dmg["alpha"])
                self.screen.blit(text_surf, (dmg["x"], dmg["y"]))


def generar_codigo_partida():
    import random
    return ''.join(random.choices(ROOM_CODE_CHARS, k=5))


def create_fonts():
    return (
        pygame.font.SysFont("Arial", 80, bold=True),
        pygame.font.SysFont("Arial", 50),
        pygame.font.SysFont("Arial", 65, bold=True),
        pygame.font.SysFont("Arial", 30)
    )

def load_luigi_idle_animations():
    """Carga la animación idle de Luigi (119 frames)."""
    animations = {'left': [], 'right': []}
    for direction in ['left', 'right']:
        animations[direction] = []
        for i in range(1, 120):
            try:
                img = pygame.image.load(f"assets/luigi/idle{i}.png").convert_alpha()
                animations[direction].append(pygame.transform.scale(img, (LUIGI_BATTLE_WIDTH, LUIGI_BATTLE_HEIGHT)))
            except:
                surf = pygame.Surface((LUIGI_BATTLE_WIDTH, LUIGI_BATTLE_HEIGHT), pygame.SRCALPHA)
                surf.fill((100, 150, 255))
                animations[direction].append(surf)
    return animations

def load_mario_idle_animations():
    animations = {'left': [], 'right': []}
    for direction in ['left', 'right']:
        animations[direction] = []
        for i in range(1, 155):
            try:
                img = pygame.image.load(f"assets/mario/idle{i}.png").convert_alpha()
                animations[direction].append(pygame.transform.scale(img, (LUIGI_BATTLE_WIDTH, LUIGI_BATTLE_HEIGHT)))
            except:
                surf = pygame.Surface((LUIGI_BATTLE_WIDTH, LUIGI_BATTLE_HEIGHT), pygame.SRCALPHA)
                surf.fill((255, 100, 0))
                animations[direction].append(surf)
    return animations

def load_bowser_idle_animations():
    animations = []
    for i in range(1, 217):
        try:
            img = pygame.image.load(f"assets/bowser/idle{i}.png").convert_alpha()
            animations.append(pygame.transform.scale(img, (BOWSER_BATTLE_WIDTH, BOWSER_BATTLE_HEIGHT)))
        except:
            surf = pygame.Surface((BOWSER_BATTLE_WIDTH, BOWSER_BATTLE_HEIGHT), pygame.SRCALPHA)
            surf.fill((150, 0, 150))
            animations.append(surf)
    return animations

def draw_menu(screen, font_titulo, font_boton, boton_iniciar, boton_multijugador, boton_local_multi, selected_option):
    screen.fill((20, 20, 40))
    titulo = font_titulo.render("BOSS SLAYER ARENA", True, (255, 255, 100))
    screen.blit(titulo, (ANCHO_VENTANA//2 - titulo.get_width()//2, 80))

    if selected_option == 0:
        pygame.draw.rect(screen, (0, 255, 100), boton_iniciar, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), boton_iniciar, width=12, border_radius=12)
    else:
        pygame.draw.rect(screen, (0, 180, 0), boton_iniciar, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), boton_iniciar, width=6, border_radius=12)

    texto = font_boton.render("INICIAR", True, (255, 255, 255))
    screen.blit(texto, (boton_iniciar.centerx - texto.get_width()//2, boton_iniciar.centery - texto.get_height()//2))

    if selected_option == 1:
        pygame.draw.rect(screen, (100, 180, 255), boton_multijugador, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), boton_multijugador, width=12, border_radius=12)
    else:
        pygame.draw.rect(screen, (0, 100, 200), boton_multijugador, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), boton_multijugador, width=6, border_radius=12)

    texto_multi = font_boton.render("MULTIJUGADOR LAN", True, (255, 255, 255))
    screen.blit(texto_multi, (boton_multijugador.centerx - texto_multi.get_width()//2, boton_multijugador.centery - texto_multi.get_height()//2))

    if selected_option == 2:
        pygame.draw.rect(screen, (255, 180, 0), boton_local_multi, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), boton_local_multi, width=12, border_radius=12)
    else:
        pygame.draw.rect(screen, (200, 120, 0), boton_local_multi, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), boton_local_multi, width=6, border_radius=12)

    texto_local = font_boton.render("MULTIJUGADOR LOCAL", True, (255, 255, 255))
    screen.blit(texto_local, (boton_local_multi.centerx - texto_local.get_width()//2, boton_local_multi.centery - texto_local.get_height()//2))

def draw_level_intro(screen, font_grande, font_boton, font_pequeña):
    screen.fill((20, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (300, 280, 180, 220))
    pygame.draw.rect(screen, (150, 0, 150), (1440, 250, 220, 280))
    vs = font_grande.render("VS", True, (255, 215, 0))
    screen.blit(vs, (ANCHO_VENTANA//2 - vs.get_width()//2, 340))
    stage = font_pequeña.render("STAGE 1 - BOSQUE OSCURO", True, (200, 200, 220))
    screen.blit(stage, (ANCHO_VENTANA//2 - stage.get_width()//2, 80))

def draw_timing_bar(screen, timing_position, is_defense=False):
    red_fraction = TIMING_RED_FRACTION_DEFENSE if is_defense else TIMING_RED_FRACTION_ATTACK
    orange_fraction = TIMING_ORANGE_FRACTION_DEFENSE if is_defense else TIMING_ORANGE_FRACTION_ATTACK
    green_fraction = TIMING_GREEN_FRACTION_DEFENSE if is_defense else TIMING_GREEN_FRACTION_ATTACK

    red_width = TIMING_BAR_WIDTH * red_fraction
    orange_width = TIMING_BAR_WIDTH * orange_fraction
    green_width = TIMING_BAR_WIDTH * green_fraction

    pygame.draw.rect(screen, (50, 50, 50), (TIMING_BAR_X, TIMING_BAR_Y, TIMING_BAR_WIDTH, TIMING_BAR_HEIGHT), border_radius=10)
    pygame.draw.rect(screen, (180, 0, 0), (TIMING_BAR_X, TIMING_BAR_Y, red_width, TIMING_BAR_HEIGHT), border_radius=10)
    pygame.draw.rect(screen, (180, 0, 0), (TIMING_BAR_X + TIMING_BAR_WIDTH - red_width, TIMING_BAR_Y, red_width, TIMING_BAR_HEIGHT), border_radius=10)
    pygame.draw.rect(screen, (255, 140, 0), (TIMING_BAR_X + red_width, TIMING_BAR_Y, orange_width, TIMING_BAR_HEIGHT))
    pygame.draw.rect(screen, (255, 140, 0), (TIMING_BAR_X + TIMING_BAR_WIDTH - red_width - orange_width, TIMING_BAR_Y, orange_width, TIMING_BAR_HEIGHT))

    green_x = TIMING_BAR_X + (TIMING_BAR_WIDTH - green_width) // 2
    pygame.draw.rect(screen, (0, 200, 100), (green_x, TIMING_BAR_Y, green_width, TIMING_BAR_HEIGHT), border_radius=10)

    cursor_x = TIMING_BAR_X + timing_position
    color_cursor = (100, 255, 255) if is_defense else (255, 255, 100)
    pygame.draw.rect(screen, color_cursor, (cursor_x - 8, TIMING_BAR_Y - 10, 16, TIMING_BAR_HEIGHT + 20), border_radius=4)

def draw_battle(screen, font_boton, font_pequeña, boton_atacar_rect, player_hp, boss_hp, current_turn, boss_attack_timer,
                timing_active, timing_position, is_defense=False, timing_feedback=None,
                player_battle_x=None, boss_battle_x=None, shake_offset=(0,0), player_sprite=None, boss_sprite=None,
                local_multiplayer=False, player2_battle_x=200, player2_sprite=None):

    if player_battle_x is None: player_battle_x = PERSONAJE_X_INICIAL
    if boss_battle_x is None: boss_battle_x = JEFE_X_INICIAL
    sx, sy = shake_offset

    try:
        bg = pygame.image.load(BATTLE_BACKGROUND).convert()
        bg = pygame.transform.scale(bg, (ANCHO_VENTANA, ALTO_VENTANA))
        screen.blit(bg, (0, 0))
    except:
        screen.fill((30, 30, 50))

    if player_sprite:
        screen.blit(player_sprite, (player_battle_x + sx, PERSONAJE_Y_INICIAL + sy))

    if local_multiplayer and player2_sprite is not None:
        screen.blit(player2_sprite, (player2_battle_x + sx, PERSONAJE_Y_INICIAL + sy))

    if boss_sprite:
        screen.blit(boss_sprite, (boss_battle_x + sx, JEFE_Y_INICIAL + sy))

    pygame.draw.rect(screen, (60, 60, 60), (JUGADOR_HP_X, JUGADOR_HP_Y, ANCHO_BARRA_VIDA, ALTO_BARRA_VIDA))
    pygame.draw.rect(screen, (0, 220, 0), (JUGADOR_HP_X, JUGADOR_HP_Y, int(ANCHO_BARRA_VIDA * (player_hp / MAX_HP_JUGADOR)), ALTO_BARRA_VIDA))
    pygame.draw.rect(screen, (60, 60, 60), (JEFE_HP_X, JEFE_HP_Y, ANCHO_BARRA_VIDA, ALTO_BARRA_VIDA))
    pygame.draw.rect(screen, (220, 0, 0), (JEFE_HP_X, JEFE_HP_Y, int(ANCHO_BARRA_VIDA * (boss_hp / MAX_HP_JEFE)), ALTO_BARRA_VIDA))

    pygame.draw.rect(screen, (20, 20, 30), (0, BARRA_Y, ANCHO_BARRA, ALTO_BARRA))

    if timing_active:
        draw_timing_bar(screen, timing_position, is_defense)
    else:
        current_y, alpha = get_atacar_button_animation(current_turn, boss_attack_timer)
        boton_atacar_rect.y = current_y
        color = (180, 0, 0) if alpha > 100 else (100, 0, 0)
        pygame.draw.rect(screen, color, boton_atacar_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), boton_atacar_rect, width=8, border_radius=12)
        texto = font_boton.render("ATACAR", True, (255, 255, 255))
        texto.set_alpha(alpha)
        screen.blit(texto, (boton_atacar_rect.centerx - texto.get_width()//2, boton_atacar_rect.centery - texto.get_height()//2))

    if timing_feedback:
        font_feedback = pygame.font.SysFont("Arial", 42, bold=True)
        colors = {"PERFECT": (0, 255, 120), "GOOD": (255, 180, 0), "MISS": (200, 200, 200), "¡BIEN!": (100, 255, 100)}
        text = font_feedback.render(timing_feedback, True, colors.get(timing_feedback, (100, 255, 100)))
        screen.blit(text, (player_battle_x + 30, PERSONAJE_Y_INICIAL - 55))

    if current_turn == "player" and not timing_active:
        turno_texto = font_pequeña.render("JUGADOR 1 - Presiona ENTER", True, (255, 255, 100))
    elif current_turn == "player2" and not timing_active:
        turno_texto = font_pequeña.render("JUGADOR 2 - Presiona ENTER", True, (100, 255, 255))
    elif current_turn == "boss" and timing_active:
        turno_texto = font_pequeña.render("¡DEFIENDE!", True, (255, 100, 100))
    else:
        turno_texto = font_pequeña.render("TURNO DEL JEFE", True, (255, 100, 100))
    screen.blit(turno_texto, (ANCHO_VENTANA//2 - turno_texto.get_width()//2, 15))

def get_atacar_button_animation(current_turn, boss_attack_timer):
    current_time = pygame.time.get_ticks()
    if current_turn in ["player", "player2"]:
        return BOTON_ATACAR_Y_NORMAL, 255
    else:
        elapsed = current_time - boss_attack_timer
        progress = min(1.0, elapsed / BUTTON_ANIMATION_DURATION)
        y_offset = int(35 * progress)
        alpha = int(255 * (1 - progress))
        return BOTON_ATACAR_Y_NORMAL + y_offset, alpha

def draw_victory(screen, font_grande, victory_start_time):
    screen.fill((30, 30, 50))
    elapsed = pygame.time.get_ticks() - victory_start_time
    progress = elapsed / VICTORY_DURATION
    if progress < 0.35: alpha = int(255 * (progress / 0.35))
    elif progress > 0.65: alpha = int(255 * (1 - (progress - 0.65) / 0.35))
    else: alpha = 255
    texto = font_grande.render("JEFE DERROTADO", True, (255, 215, 80))
    texto.set_alpha(alpha)
    bar = pygame.Surface((ANCHO_VENTANA, 85), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 180))
    screen.blit(bar, (0, 195))
    screen.blit(texto, (ANCHO_VENTANA//2 - texto.get_width()//2, 200))
    return elapsed >= VICTORY_DURATION

def draw_game_over(screen, font_grande, game_over_start_time):
    screen.fill((30, 30, 50))
    elapsed = pygame.time.get_ticks() - game_over_start_time
    progress = elapsed / GAME_OVER_DURATION
    if progress < 0.35: alpha = int(255 * (progress / 0.35))
    elif progress > 0.65: alpha = int(255 * (1 - (progress - 0.65) / 0.35))
    else: alpha = 255
    texto = font_grande.render("HAS MUERTO", True, (200, 30, 30))
    texto.set_alpha(alpha)
    bar = pygame.Surface((ANCHO_VENTANA, 85), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 180))
    screen.blit(bar, (0, 195))
    screen.blit(texto, (ANCHO_VENTANA//2 - texto.get_width()//2, 200))
    return elapsed >= GAME_OVER_DURATION

def calculate_damage(timing_position, is_defense=False):
    center = TIMING_BAR_WIDTH / 2
    distance = abs(timing_position - center)
    green_fraction = TIMING_GREEN_FRACTION_DEFENSE if is_defense else TIMING_GREEN_FRACTION_ATTACK
    if distance <= TIMING_BAR_WIDTH * green_fraction:
        return 35 if not is_defense else 0
    elif distance <= TIMING_BAR_WIDTH * 0.30:
        return 22 if not is_defense else 8
    else:
        return 0 if not is_defense else 15

def player_attack(boss_hp, timing_position):
    damage = calculate_damage(timing_position, is_defense=False)
    boss_hp -= damage
    if boss_hp < 0: boss_hp = 0
    return boss_hp, damage

def boss_attack(player_hp, timing_position, is_defense_success):
    if is_defense_success:
        damage = calculate_damage(timing_position, is_defense=True)
    else:
        damage = 15
    player_hp -= damage
    if player_hp < 0: player_hp = 0
    return player_hp, damage