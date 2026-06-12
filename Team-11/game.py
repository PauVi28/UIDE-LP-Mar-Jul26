import pygame
import sys
import os
import math
from game_logic import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    STATE_IDLE, STATE_ATTACKING, STATE_RETURNING, STATE_DEAD,
    STATE_HAMMER_ATTACK, STATE_HAMMER_FAIL, STATE_HAMMER_GOOD, STATE_HAMMER_EXCELENT,
    Mario, Luigi, Bowser,
    POS_MARIO_CENTER, POS_BOWSER_CENTER, POS_LUIGI_CENTER,
    POS_MARIO_OFFSCREEN, POS_BOWSER_OFFSCREEN, POS_LUIGI_OFFSCREEN,
    POS_MARIO_ATTACK_TARGET, POS_BOWSER_ATTACK_TARGET, POS_LUIGI_ATTACK_TARGET, POS_BOWSER_ATTACK_LUIGI_TARGET,
    ip_to_code, code_to_ip
)
from server import GameServer
from client import GameClient

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("ForgottenTale")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("arial", 80, bold=True)
font_menu = pygame.font.SysFont("arial", 50)
font_small = pygame.font.SysFont("arial", 30)

try:
    font_ds = pygame.font.SysFont("palatinolinotype", 120, italic=True)
except:
    font_ds = pygame.font.SysFont("timesnewroman", 120, italic=True)

bg_path = os.path.join("assets", "backgrounds", "battle_bg1.png")
if os.path.exists(bg_path):
    bg_image = pygame.image.load(bg_path).convert()
    bg_image = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
else:
    bg_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    bg_image.fill((40, 100, 40))

music_path = os.path.join("assets", "music", "battle_music1.flac")
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)

def draw_text(text, font, color, surface, x, y, center=False):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    return textrect

_mouse_was_pressed = False
def button(text, x, y, w, h, inactive_color, active_color, action=None):
    global _mouse_was_pressed
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    is_hover = rect.collidepoint(mouse)
    color = active_color if is_hover else inactive_color
    pygame.draw.rect(screen, color, rect, border_radius=15)
    draw_text(text, font_menu, (255, 255, 255), screen, x + w//2, y + h//2, center=True)
    if is_hover and click[0] == 1 and not _mouse_was_pressed and action != None:
        _mouse_was_pressed = True
        return action()
    if not click[0]:
        _mouse_was_pressed = False
    return None

def draw_health_bar(surface, character, x, y, width, height):
    ratio = character.hp / character.max_hp
    pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height))
    color = (0, 255, 0)
    if ratio < 0.5: color = (255, 255, 0)
    if ratio < 0.2: color = (255, 0, 0)
    pygame.draw.rect(surface, color, (x, y, int(width * ratio), height))
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 3)
    name_text = character.name.upper()
    draw_text(f"{name_text}: {character.hp}/{character.max_hp}", font_small, (255,255,255), surface, x + 10, y + 5)

def draw_action_command_bar(surface, cursor_pos):
    bar_x = WINDOW_WIDTH // 2 - 250
    bar_y = 200
    bar_w = 500
    bar_h = 40
    pygame.draw.rect(surface, (200, 0, 0), (bar_x, bar_y, bar_w * 0.20, bar_h))
    pygame.draw.rect(surface, (255, 150, 0), (bar_x + bar_w * 0.20, bar_y, bar_w * 0.25, bar_h))
    pygame.draw.rect(surface, (0, 255, 0), (bar_x + bar_w * 0.45, bar_y, bar_w * 0.10, bar_h))
    pygame.draw.rect(surface, (255, 150, 0), (bar_x + bar_w * 0.55, bar_y, bar_w * 0.25, bar_h))
    pygame.draw.rect(surface, (200, 0, 0), (bar_x + bar_w * 0.80, bar_y, bar_w * 0.20, bar_h))
    pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 4)
    cursor_x = bar_x + (bar_w * cursor_pos)
    pygame.draw.rect(surface, (255, 255, 255), (cursor_x - 4, bar_y - 10, 8, bar_h + 20))

def main_menu():
    pygame.mouse.set_visible(True)
    while True:
        screen.fill((20, 20, 40))
        draw_text("ForgottenTale", font_title, (255, 200, 0), screen, WINDOW_WIDTH//2, 200, center=True)
        if button("Singleplayer", WINDOW_WIDTH//2 - 200, 400, 400, 80, (100, 0, 0), (150, 50, 50), action=lambda: "singleplayer"):
            return "singleplayer"
        if button("Multiplayer", WINDOW_WIDTH//2 - 200, 550, 400, 80, (0, 0, 100), (50, 50, 150), action=lambda: "multiplayer"):
            return "multiplayer"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(FPS)

def singleplayer_battle():
    pygame.mouse.set_visible(False)
    mario = Mario()
    bowser = Bowser()
    if os.path.exists(music_path):
        pygame.mixer.music.play(-1)
    state = "INTRO"
    intro_start = pygame.time.get_ticks()
    button_offset_y = 150
    target_button_offset_y = 150
    hit_timer = 0
    fade_alpha = 0
    game_over_result = ""
    damage_multiplier = 1.0
    action_cursor_pos = 0.5
    while True:
        now = pygame.time.get_ticks()
        screen.blit(bg_image, (0, 0))
        current_events = pygame.event.get()
        for event in current_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if state == "INTRO":
            screen.fill((0, 0, 0))
            bowser.x, bowser.y = WINDOW_WIDTH//2 - bowser.width//2, WINDOW_HEIGHT//2 - bowser.height//2
            bowser.draw(screen)
            draw_text("JEFE APROXIMÁNDOSE", font_ds, (200, 0, 0), screen, WINDOW_WIDTH//2, 150, center=True)
            if now - intro_start > 6000:
                state = "WALKING_IN"
                mario.x = POS_MARIO_OFFSCREEN[0]
                mario.y = POS_MARIO_OFFSCREEN[1]
                bowser.x = POS_BOWSER_OFFSCREEN[0]
                bowser.y = POS_BOWSER_OFFSCREEN[1]
                mario.target_x = POS_MARIO_CENTER[0]
                bowser.target_x = POS_BOWSER_CENTER[0]
                mario.target_y = POS_MARIO_CENTER[1]
                bowser.target_y = POS_BOWSER_CENTER[1]
        else:
            if state != "PLAYER_ACTION_COMMAND":
                mario.update()
            bowser.update()
            if state in ["BOSS_ATTACK_SEQUENCE", "BOSS_RETURNING"]:
                mario.draw(screen)
                bowser.draw(screen)
            else:
                bowser.draw(screen)
                mario.draw(screen)
            if state not in ["GAME_OVER", "WALKING_IN"]:
                draw_health_bar(screen, mario, 50, 50, 400, 40)
                draw_health_bar(screen, bowser, WINDOW_WIDTH - 650, 50, 600, 40)
                debug_text = f"Game: {state} | Anim: {mario.state} | Frame: {mario.current_frame + 1} / {len(mario.frames[mario.state])}"
                draw_text(debug_text, font_small, (255, 255, 0), screen, 50, 100)
            if state == "WALKING_IN":
                if mario.x == mario.target_x and bowser.x == bowser.target_x and mario.y == mario.target_y and bowser.y == bowser.target_y:
                    state = "PLAYER_MENU"
                    target_button_offset_y = 0
            elif state == "PLAYER_MENU":
                for event in current_events:
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                        state = "PLAYER_ATTACK_SEQUENCE"
                        target_button_offset_y = 150
                        mario.set_state(STATE_HAMMER_ATTACK)
            elif state == "PLAYER_ATTACK_SEQUENCE":
                if 20 <= mario.current_frame <= 31:
                    mario.target_x = POS_MARIO_ATTACK_TARGET[0]
                    mario.target_y = POS_MARIO_ATTACK_TARGET[1]
                else:
                    mario.target_x = mario.x
                    mario.target_y = mario.y
                if mario.current_frame >= 31:
                    mario.current_frame = 31
                    state = "PLAYER_ACTION_COMMAND"
            elif state == "PLAYER_ACTION_COMMAND":
                mario.current_frame = 31
                action_cursor_pos = (math.sin(now * 0.008) + 1) / 2.0
                draw_action_command_bar(screen, action_cursor_pos)
                for event in current_events:
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                        if action_cursor_pos < 0.20 or action_cursor_pos > 0.80:
                            damage_multiplier = 0.25
                            mario.set_state(STATE_HAMMER_FAIL)
                        elif action_cursor_pos < 0.45 or action_cursor_pos > 0.55:
                            damage_multiplier = 0.50
                            mario.set_state(STATE_HAMMER_GOOD)
                        else:
                            damage_multiplier = 1.00
                            mario.set_state(STATE_HAMMER_EXCELENT)
                        mario.target_x = mario.x
                        mario.target_y = mario.y
                        state = "PLAYER_ATTACK_RESOLVE"
            elif state == "PLAYER_ATTACK_RESOLVE":
                damage_frame = -1
                if mario.state == STATE_HAMMER_FAIL:
                    damage_frame = 16
                elif mario.state == STATE_HAMMER_GOOD:
                    damage_frame = 21
                elif mario.state == STATE_HAMMER_EXCELENT:
                    damage_frame = 30
                if damage_frame != -1 and mario.current_frame >= damage_frame and not mario.damage_dealt:
                    bowser.take_damage(mario.damage * damage_multiplier)
                    mario.damage_dealt = True
                    if bowser.hp <= 0:
                        state = "BOWSER_DEATH_SEQUENCE"
                        bowser.set_state(STATE_DEAD)
                if state == "PLAYER_ATTACK_RESOLVE":
                    last_frame_idx = max(0, len(mario.frames[mario.state]) - 1)
                    if mario.current_frame >= last_frame_idx:
                        if now - mario.last_update > mario.anim_speed - 5:
                            if mario.damage_dealt:
                                mario.damage_dealt = False
                            state = "PLAYER_RETURNING"
                            mario.target_x = POS_MARIO_CENTER[0]
                            mario.target_y = POS_MARIO_CENTER[1]
                            mario.set_state(STATE_RETURNING)
            elif state == "PLAYER_RETURNING":
                if mario.x == mario.target_x and mario.y == mario.target_y:
                    mario.set_state(STATE_IDLE)
                    state = "BOSS_ATTACK_SEQUENCE"
                    bowser.set_state(STATE_ATTACKING)
                    bowser.target_x = POS_BOWSER_ATTACK_TARGET[0]
                    bowser.target_y = POS_BOWSER_ATTACK_TARGET[1]
            elif state == "BOSS_ATTACK_SEQUENCE":
                for event in current_events:
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                        mario.activate_defense(now)
                if bowser.current_frame >= 16:
                    bowser.target_x = bowser.x
                    bowser.target_y = bowser.y
                if bowser.current_frame >= 71 and not bowser.damage_dealt:
                    if not mario.is_defending:
                        mario.take_damage(bowser.damage)
                    bowser.damage_dealt = True
                    if mario.hp <= 0:
                        state = "PLAYER_DEATH_SEQUENCE"
                        mario.set_state(STATE_DEAD)
                if state == "BOSS_ATTACK_SEQUENCE":
                    last_frame_idx = max(0, len(bowser.frames[bowser.state]) - 1)
                    if bowser.current_frame >= last_frame_idx:
                        if now - bowser.last_update > bowser.anim_speed - 5:
                            if bowser.damage_dealt:
                                bowser.damage_dealt = False
                            state = "BOSS_RETURNING"
                            bowser.target_x = POS_BOWSER_CENTER[0]
                            bowser.target_y = POS_BOWSER_CENTER[1]
                            bowser.set_state(STATE_RETURNING)
            elif state == "BOSS_RETURNING":
                if bowser.x == bowser.target_x and bowser.y == bowser.target_y:
                    bowser.set_state(STATE_IDLE)
                    if mario.lockout_turns > 0: mario.lockout_turns -= 1
                    mario.defense_presses = 0
                    target_button_offset_y = 0
                    if button_offset_y <= 5:
                        state = "PLAYER_MENU"
            elif state == "BOWSER_DEATH_SEQUENCE":
                last_frame_idx = max(0, len(bowser.frames[STATE_DEAD]) - 1)
                if bowser.current_frame >= last_frame_idx:
                    state = "GAME_OVER"
                    game_over_result = "JEFE DERROTADO"
                    hit_timer = now
            elif state == "PLAYER_DEATH_SEQUENCE":
                last_frame_idx = max(0, len(mario.frames[STATE_DEAD]) - 1)
                if mario.current_frame >= last_frame_idx:
                    state = "GAME_OVER"
                    game_over_result = "HAS MUERTO"
                    hit_timer = now
            elif state == "GAME_OVER":
                time_in_game_over = now - hit_timer
                if time_in_game_over < 3000:
                    fade_alpha = min(255, fade_alpha + 2)
                elif time_in_game_over > 5000:
                    fade_alpha = max(0, fade_alpha - 2)
                if time_in_game_over > 7000:
                    pygame.mixer.music.stop()
                    return
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.set_alpha(fade_alpha // 2)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                text_color = (255, 200, 0) if "DERROTADO" in game_over_result else (200, 0, 0)
                text_surface = font_ds.render(game_over_result, True, text_color)
                text_surface.set_alpha(fade_alpha)
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                screen.blit(text_surface, text_rect)
            if button_offset_y < target_button_offset_y:
                button_offset_y += 5
            elif button_offset_y > target_button_offset_y:
                button_offset_y -= 5
            button_y = WINDOW_HEIGHT - 120 + button_offset_y
            pygame.draw.rect(screen, (150, 50, 50), (WINDOW_WIDTH//2 - 150, button_y, 300, 80), border_radius=15)
            draw_text("ATACAR", font_menu, (255, 255, 255), screen, WINDOW_WIDTH//2, button_y + 40, center=True)
            if state == "PLAYER_MENU":
                draw_text("PRESIONA ENTER", font_small, (200, 200, 200), screen, WINDOW_WIDTH//2, button_y - 20, center=True)
        pygame.display.update()
        clock.tick(FPS)

def multiplayer_menu():
    pygame.mouse.set_visible(True)
    while True:
        screen.fill((20, 20, 40))
        draw_text("MULTIJUGADOR LAN", font_title, (255, 200, 0), screen, WINDOW_WIDTH//2, 200, center=True)
        if button("Crear Partida (Host)", WINDOW_WIDTH//2 - 200, 400, 400, 80, (100, 0, 0), (150, 50, 50), action=lambda: "host"):
            return "host"
        if button("Unirse a Partida (Join)", WINDOW_WIDTH//2 - 200, 550, 400, 80, (0, 0, 100), (50, 50, 150), action=lambda: "join"):
            return "join"
        if button("Volver", WINDOW_WIDTH//2 - 200, 700, 400, 80, (50, 50, 50), (100, 100, 100), action=lambda: "back"):
            return "back"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(FPS)

def host_lobby():
    server = GameServer(port=0)
    local_ip = server.get_local_ip()
    room_code = ip_to_code(local_ip, server.port)
    while True:
        screen.fill((20, 20, 40))
        draw_text("ESPERANDO AL JUGADOR 2...", font_title, (255, 255, 255), screen, WINDOW_WIDTH//2, 200, center=True)
        alpha = int((math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127)
        text_surf = font_menu.render("TU CÓDIGO DE SALA ES:", True, (200, 200, 200))
        text_rect = text_surf.get_rect(center=(WINDOW_WIDTH//2, 400))
        screen.blit(text_surf, text_rect)
        code_surf = font_title.render(room_code, True, (255, 255, 0))
        code_surf.set_alpha(alpha + 128)
        code_rect = code_surf.get_rect(center=(WINDOW_WIDTH//2, 500))
        screen.blit(code_surf, code_rect)
        if server.connected:
            return server
        if button("Cancelar", WINDOW_WIDTH//2 - 150, 700, 300, 80, (100, 0, 0), (150, 50, 50), action=lambda: "cancel"):
            server.stop()
            return None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                server.stop()
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(FPS)

def join_lobby():
    input_text = ""
    client = None
    connecting = False
    connection_failed = False
    while True:
        screen.fill((20, 20, 40))
        draw_text("INGRESAR CÓDIGO", font_title, (255, 200, 0), screen, WINDOW_WIDTH//2, 200, center=True)
        pygame.draw.rect(screen, (255, 255, 255), (WINDOW_WIDTH//2 - 250, 400, 500, 80), border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), (WINDOW_WIDTH//2 - 250, 400, 500, 80), 4, border_radius=10)
        draw_text(input_text + "_", font_title, (0, 0, 0), screen, WINDOW_WIDTH//2, 440, center=True)
        if connecting:
            draw_text("Conectando...", font_menu, (200, 200, 200), screen, WINDOW_WIDTH//2, 550, center=True)
            if client and client.connected:
                return client
            elif client and not client.running:
                connecting = False
                connection_failed = True
                client = None
        else:
            if connection_failed:
                draw_text("Fallo al conectar. Verifica el código.", font_menu, (255, 50, 50), screen, WINDOW_WIDTH//2, 550, center=True)
            if button("Conectar", WINDOW_WIDTH//2 - 210, 650, 200, 80, (0, 100, 0), (50, 150, 50), action=lambda: "connect") == "connect":
                if input_text:
                    target_ip, target_port = code_to_ip(input_text)
                    client = GameClient(target_ip, port=target_port)
                    connecting = True
                    connection_failed = False
            if button("Volver", WINDOW_WIDTH//2 + 10, 650, 200, 80, (100, 0, 0), (150, 50, 50), action=lambda: "cancel") == "cancel":
                if client: client.stop()
                return None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if client: client.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not connecting:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN and input_text:
                    target_ip, target_port = code_to_ip(input_text)
                    client = GameClient(target_ip, port=target_port)
                    connecting = True
                    connection_failed = False
                elif len(input_text) < 8 and event.unicode.isalnum():
                    input_text += event.unicode.upper()
        pygame.display.update()
        clock.tick(FPS)

def multiplayer_battle_p1(server):
    pygame.mouse.set_visible(False)
    mario = Mario()
    luigi = Luigi()
    bowser = Bowser()
    if os.path.exists(music_path):
        pygame.mixer.music.play(-1)
    state = "INTRO"
    intro_start = pygame.time.get_ticks()
    button_offset_y = 150
    target_button_offset_y = 150
    hit_timer = 0
    fade_alpha = 0
    game_over_result = ""
    damage_multiplier = 1.0
    action_cursor_pos = 0.5
    turn_sequence = ["mario", "luigi", "bowser"]
    turn_index = 0
    current_turn = "mario"
    bowser_target = "mario"
    mario_damage_dealt = 0
    mario_damage_taken = 0
    luigi_damage_dealt = 0
    luigi_damage_taken = 0
    while True:
        now = pygame.time.get_ticks()
        client_state = server.get_client_state()
        if client_state.get("action") == "defend":
            press_id = client_state.get("press_id")
            if getattr(luigi, "last_press_id", None) != press_id:
                luigi.activate_defense(now)
                luigi.last_press_id = press_id

        screen.blit(bg_image, (0, 0))
        current_events = pygame.event.get()
        for event in current_events:
            if event.type == pygame.QUIT:
                server.stop()
                pygame.quit()
                sys.exit()
        if current_turn == "bowser" and state == "BOSS_ATTACK_SEQUENCE":
            for event in current_events:
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                    mario.activate_defense(now)
        if state == "INTRO":
            screen.fill((0, 0, 0))
            bowser.x, bowser.y = WINDOW_WIDTH//2 - bowser.width//2, WINDOW_HEIGHT//2 - bowser.height//2
            bowser.draw(screen)
            draw_text("JEFE APROXIMÁNDOSE", font_ds, (200, 0, 0), screen, WINDOW_WIDTH//2, 150, center=True)
            if now - intro_start > 6000:
                state = "WALKING_IN"
                mario.x, mario.y = POS_MARIO_OFFSCREEN
                luigi.x, luigi.y = POS_LUIGI_OFFSCREEN
                bowser.x, bowser.y = POS_BOWSER_OFFSCREEN
                mario.target_x, mario.target_y = POS_MARIO_CENTER
                luigi.target_x, luigi.target_y = POS_LUIGI_CENTER
                bowser.target_x, bowser.target_y = POS_BOWSER_CENTER
        else:
            if state not in ["PLAYER_ACTION_COMMAND", "LUIGI_ACTION_COMMAND"]:
                mario.update()
                luigi.update()
            bowser.update()
            if current_turn == "bowser":
                mario.draw(screen)
                luigi.draw(screen)
                bowser.draw(screen)
            else:
                bowser.draw(screen)
                mario.draw(screen)
                luigi.draw(screen)
            if state not in ["GAME_OVER", "WALKING_IN"]:
                draw_health_bar(screen, mario, 50, 50, 400, 40)
                draw_health_bar(screen, luigi, 50, 100, 400, 40)
                draw_health_bar(screen, bowser, WINDOW_WIDTH - 650, 50, 600, 40)
            if state == "WALKING_IN":
                if mario.x == mario.target_x and bowser.x == bowser.target_x:
                    state = "PLAYER_MENU"
                    current_turn = "mario"
                    target_button_offset_y = 0
            elif state == "PLAYER_MENU":
                if current_turn == "mario":
                    for event in current_events:
                        if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                            state = "PLAYER_ATTACK_SEQUENCE"
                            target_button_offset_y = 150
                            mario.set_state(STATE_HAMMER_ATTACK)
                elif current_turn == "luigi":
                    client_state = server.get_client_state()
                    if client_state.get("action") == "start_attack":
                        state = "LUIGI_ATTACK_SEQUENCE"
                        luigi.set_state(STATE_HAMMER_ATTACK)
            elif state == "PLAYER_ATTACK_SEQUENCE":
                if 20 <= mario.current_frame <= 31:
                    mario.target_x, mario.target_y = POS_MARIO_ATTACK_TARGET
                else:
                    mario.target_x, mario.target_y = mario.x, mario.y
                if mario.current_frame >= 31:
                    mario.current_frame = 31
                    state = "PLAYER_ACTION_COMMAND"
            elif state == "PLAYER_ACTION_COMMAND":
                mario.current_frame = 31
                action_cursor_pos = (math.sin(now * 0.008) + 1) / 2.0
                draw_action_command_bar(screen, action_cursor_pos)
                for event in current_events:
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                        if action_cursor_pos < 0.20 or action_cursor_pos > 0.80:
                            damage_multiplier = 0.25
                            mario.set_state(STATE_HAMMER_FAIL)
                        elif action_cursor_pos < 0.45 or action_cursor_pos > 0.55:
                            damage_multiplier = 0.50
                            mario.set_state(STATE_HAMMER_GOOD)
                        else:
                            damage_multiplier = 1.00
                            mario.set_state(STATE_HAMMER_EXCELENT)
                        mario.target_x, mario.target_y = mario.x, mario.y
                        state = "PLAYER_ATTACK_RESOLVE"
            elif state == "PLAYER_ATTACK_RESOLVE":
                active = mario if current_turn == "mario" else luigi
                damage_frame = -1
                if active.state == STATE_HAMMER_FAIL: damage_frame = 16
                elif active.state == STATE_HAMMER_GOOD: damage_frame = 21 if current_turn == "mario" else 16
                elif active.state == STATE_HAMMER_EXCELENT: damage_frame = 30
                if damage_frame != -1 and active.current_frame >= damage_frame and not active.damage_dealt:
                    actual_damage = active.damage * damage_multiplier
                    bowser.take_damage(actual_damage)
                    if current_turn == "mario":
                        mario_damage_dealt += actual_damage
                    else:
                        luigi_damage_dealt += actual_damage
                    active.damage_dealt = True
                    if bowser.hp <= 0:
                        state = "BOWSER_DEATH_SEQUENCE"
                        bowser.set_state(STATE_DEAD)
                if state == "PLAYER_ATTACK_RESOLVE":
                    last_frame_idx = max(0, len(active.frames[active.state]) - 1)
                    if active.current_frame >= last_frame_idx:
                        if now - active.last_update > active.anim_speed - 5:
                            if active.damage_dealt: active.damage_dealt = False
                            state = "PLAYER_RETURNING"
                            active.target_x, active.target_y = POS_MARIO_CENTER if current_turn == "mario" else POS_LUIGI_CENTER
                            active.set_state(STATE_RETURNING)
            elif state == "PLAYER_RETURNING":
                active = mario if current_turn == "mario" else luigi
                if active.x == active.target_x and active.y == active.target_y:
                    active.set_state(STATE_IDLE)
                    state = "ADVANCE_TURN"
            elif state == "LUIGI_ATTACK_SEQUENCE":
                if 20 <= luigi.current_frame <= 31:
                    luigi.target_x, luigi.target_y = POS_LUIGI_ATTACK_TARGET
                else:
                    luigi.target_x, luigi.target_y = luigi.x, luigi.y
                if luigi.current_frame >= 31:
                    luigi.current_frame = 31
                    state = "LUIGI_ACTION_COMMAND"
            elif state == "LUIGI_ACTION_COMMAND":
                luigi.current_frame = 31
                client_state = server.get_client_state()
                if client_state.get("action") == "attack_confirmed":
                    mult = client_state.get("damage_multiplier", 1.0)
                    damage_multiplier = mult
                    if mult <= 0.25:
                        luigi.set_state(STATE_HAMMER_FAIL)
                    elif mult <= 0.50:
                        luigi.set_state(STATE_HAMMER_GOOD)
                    else:
                        luigi.set_state(STATE_HAMMER_EXCELENT)
                    luigi.target_x, luigi.target_y = luigi.x, luigi.y
                    state = "PLAYER_ATTACK_RESOLVE"
            elif state == "BOSS_ATTACK_SEQUENCE":
                if bowser.current_frame >= 16:
                    bowser.target_x, bowser.target_y = bowser.x, bowser.y
                if bowser.current_frame >= 71 and not bowser.damage_dealt:
                    target_player = mario if bowser_target == "mario" else luigi
                    damage_dealt = bowser.damage
                    if not target_player.is_defending:
                        target_player.take_damage(damage_dealt)
                        if target_player == mario:
                            mario_damage_taken += damage_dealt
                        else:
                            luigi_damage_taken += damage_dealt
                    bowser.damage_dealt = True
                    if target_player.hp <= 0:
                        target_player.set_state(STATE_DEAD)
                        state = "PLAYER_DEATH_SEQUENCE"
                last_frame_idx = max(0, len(bowser.frames[bowser.state]) - 1)
                if state == "BOSS_ATTACK_SEQUENCE" and bowser.current_frame >= last_frame_idx:
                    if bowser.damage_dealt: bowser.damage_dealt = False
                    bowser.target_x, bowser.target_y = POS_BOWSER_CENTER
                    bowser.set_state(STATE_RETURNING)
                    state = "BOSS_RETURNING"
            elif state == "BOSS_RETURNING":
                if bowser.x == bowser.target_x and bowser.y == bowser.target_y:
                    bowser.set_state(STATE_IDLE)
                    if mario.lockout_turns > 0: mario.lockout_turns -= 1
                    mario.defense_presses = 0
                    if luigi.lockout_turns > 0: luigi.lockout_turns -= 1
                    luigi.defense_presses = 0
                    state = "ADVANCE_TURN"
            elif state == "BOWSER_DEATH_SEQUENCE":
                last_frame_idx = max(0, len(bowser.frames[STATE_DEAD]) - 1)
                if bowser.current_frame >= last_frame_idx:
                    state = "GAME_OVER"
                    game_over_result = "JEFE DERROTADO"
                    hit_timer = now
            elif state == "PLAYER_DEATH_SEQUENCE":
                target_player = mario if bowser_target == "mario" else luigi
                last_frame_idx = max(0, len(target_player.frames[STATE_DEAD]) - 1)
                if target_player.current_frame >= last_frame_idx:
                    if mario.hp <= 0 and luigi.hp <= 0:
                        state = "GAME_OVER"
                        game_over_result = "HAN MUERTO"
                        hit_timer = now
                    else:
                        if bowser.damage_dealt: bowser.damage_dealt = False
                        bowser.target_x, bowser.target_y = POS_BOWSER_CENTER
                        bowser.set_state(STATE_RETURNING)
                        state = "BOSS_RETURNING"
            elif state == "ADVANCE_TURN":
                while True:
                    turn_index = (turn_index + 1) % len(turn_sequence)
                    current_turn = turn_sequence[turn_index]
                    if current_turn == "mario":
                        if mario.hp > 0:
                            state = "PLAYER_MENU"
                            break
                    elif current_turn == "luigi":
                        if luigi.hp > 0:
                            state = "PLAYER_MENU"
                            break
                    elif current_turn == "bowser":
                        if bowser.hp > 0:
                            state = "BOSS_ATTACK_SEQUENCE"
                            bowser.set_state(STATE_ATTACKING)
                            alive = []
                            if mario.hp > 0: alive.append("mario")
                            if luigi.hp > 0: alive.append("luigi")
                            if len(alive) == 2:
                                bowser_target = "luigi" if bowser_target == "mario" else "mario"
                            elif alive:
                                bowser_target = alive[0]
                            else:
                                bowser_target = "mario"
                            if bowser_target == "mario":
                                bowser.target_x, bowser.target_y = POS_BOWSER_ATTACK_TARGET
                            else:
                                bowser.target_x, bowser.target_y = POS_BOWSER_ATTACK_LUIGI_TARGET
                            break
                        else:
                            break
            elif state == "GAME_OVER":
                time_in_game_over = now - hit_timer
                if time_in_game_over < 3000: fade_alpha = min(255, fade_alpha + 2)
                elif time_in_game_over > 5000: fade_alpha = max(0, fade_alpha - 2)
                if time_in_game_over > 7000:
                    state = "SCORE_SCREEN"
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.set_alpha(fade_alpha // 2)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                text_color = (255, 200, 0) if "DERROTADO" in game_over_result else (200, 0, 0)
                text_surface = font_ds.render(game_over_result, True, text_color)
                text_surface.set_alpha(fade_alpha)
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                screen.blit(text_surface, text_rect)
            elif state == "SCORE_SCREEN":
                screen.fill((20, 20, 40))
                draw_text("PUNTUACIÓN FINAL", font_title, (255, 255, 0), screen, WINDOW_WIDTH//2, 100, center=True)
                mario_score = int(mario_damage_dealt - mario_damage_taken)
                luigi_score = int(luigi_damage_dealt - luigi_damage_taken)
                m1_text = f"Jugador 1 (Mario): {mario_score}"
                l1_text = f"Jugador 2 (Luigi): {luigi_score}"
                if mario_score > luigi_score: m1_text += " - GANADOR"
                elif luigi_score > mario_score: l1_text += " - GANADOR"
                else:
                    m1_text += " - EMPATE"
                    l1_text += " - EMPATE"
                draw_text(m1_text, font_ds, (255, 100, 100), screen, WINDOW_WIDTH//2, 300, center=True)
                draw_text(l1_text, font_ds, (100, 255, 100), screen, WINDOW_WIDTH//2, 400, center=True)
                if button("Volver al menú", WINDOW_WIDTH//2 - 150, 600, 300, 80, (100, 0, 0), (150, 50, 50), action=lambda: "return") == "return":
                    pygame.mixer.music.stop()
                    server.stop()
                    return
            if current_turn == "mario" and state == "PLAYER_MENU":
                target_button_offset_y = 0
            else:
                target_button_offset_y = 150
            if button_offset_y < target_button_offset_y: button_offset_y += 5
            elif button_offset_y > target_button_offset_y: button_offset_y -= 5
            button_y = WINDOW_HEIGHT - 120 + button_offset_y
            if current_turn == "mario":
                draw_text("TU TURNO", font_title, (0, 255, 0), screen, WINDOW_WIDTH//2, 150, center=True)
            else:
                draw_text(f"Turno de: {current_turn.upper()}", font_menu, (255, 255, 0), screen, WINDOW_WIDTH//2, 150, center=True)
            pygame.draw.rect(screen, (150, 50, 50), (WINDOW_WIDTH//2 - 150, button_y, 300, 80), border_radius=15)
            draw_text("ATACAR", font_menu, (255, 255, 255), screen, WINDOW_WIDTH//2, button_y + 40, center=True)
            if state == "PLAYER_MENU" and current_turn == "mario":
                draw_text("PRESIONA ENTER", font_small, (200, 200, 200), screen, WINDOW_WIDTH//2, button_y - 20, center=True)
        out_state = {
            "game_state": state, "current_turn": current_turn, "game_over_result": game_over_result,
            "mario": {
                "x": mario.x, "y": mario.y, "hp": mario.hp, "max_hp": mario.max_hp, "anim": mario.state, "frame": mario.current_frame,
                "is_defending": getattr(mario, "is_defending", False), "has_failed_defense": getattr(mario, "has_failed_defense", False), "lockout_turns": getattr(mario, "lockout_turns", 0)
            },
            "luigi": {
                "x": luigi.x, "y": luigi.y, "hp": luigi.hp, "max_hp": luigi.max_hp, "anim": luigi.state, "frame": luigi.current_frame,
                "is_defending": getattr(luigi, "is_defending", False), "has_failed_defense": getattr(luigi, "has_failed_defense", False), "lockout_turns": getattr(luigi, "lockout_turns", 0)
            },
            "bowser": {"x": bowser.x, "y": bowser.y, "hp": bowser.hp, "max_hp": bowser.max_hp, "anim": bowser.state, "frame": bowser.current_frame},
            "mario_score": int(mario_damage_dealt - mario_damage_taken),
            "luigi_score": int(luigi_damage_dealt - luigi_damage_taken),
        }
        server.update_state(out_state)
        if not server.connected:
            print("Cliente desconectado.")
            pygame.mixer.music.stop()
            return
        pygame.display.update()
        clock.tick(FPS)
def multiplayer_battle_p2(client):
    pygame.mouse.set_visible(False)
    mario = Mario()
    luigi = Luigi()
    bowser = Bowser()
    if os.path.exists(music_path):
        pygame.mixer.music.play(-1)
    action_cursor_pos = 0.5
    client_action = {"action": "none"}
    client.update_state(client_action)
    attack_started = False
    while True:
        now = pygame.time.get_ticks()
        screen.blit(bg_image, (0, 0))
        current_events = pygame.event.get()
        for event in current_events:
            if event.type == pygame.QUIT:
                client.stop()
                pygame.quit()
                sys.exit()
        server_state = client.get_server_state()
        if not server_state:
            continue
        game_state = server_state.get("game_state", "INTRO")
        current_turn = server_state.get("current_turn", "mario")
        for char, obj in [("mario", mario), ("luigi", luigi), ("bowser", bowser)]:
            if char in server_state:
                data = server_state[char]
                obj.x, obj.y = data["x"], data["y"]
                obj.hp = data["hp"]
                obj.max_hp = data["max_hp"]
                anim = data.get("anim", STATE_IDLE)
                frame = data.get("frame", 0)
                if anim != obj.state:
                    obj.state = anim
                obj.current_frame = min(frame, max(0, len(obj.frames.get(obj.state, [obj])) - 1))
                if char in ["mario", "luigi"]:
                    obj.is_defending = data.get("is_defending", False)
                    obj.has_failed_defense = data.get("has_failed_defense", False)
                    obj.lockout_turns = data.get("lockout_turns", 0)
        if game_state == "INTRO":
            screen.fill((0, 0, 0))
            bowser.draw(screen)
            draw_text("JEFE APROXIMÁNDOSE", font_ds, (200, 0, 0), screen, WINDOW_WIDTH//2, 150, center=True)
        else:
            if current_turn == "bowser":
                mario.draw(screen)
                luigi.draw(screen)
                bowser.draw(screen)
            else:
                bowser.draw(screen)
                mario.draw(screen)
                luigi.draw(screen)
            if game_state not in ["GAME_OVER", "WALKING_IN"]:
                draw_health_bar(screen, mario, 50, 50, 400, 40)
                draw_health_bar(screen, luigi, 50, 100, 400, 40)
                draw_health_bar(screen, bowser, WINDOW_WIDTH - 650, 50, 600, 40)
                if current_turn == "luigi":
                    draw_text("TU TURNO", font_title, (0, 255, 0), screen, WINDOW_WIDTH//2, 150, center=True)
                else:
                    draw_text(f"Turno de: {current_turn.upper()}", font_menu, (255, 255, 0), screen, WINDOW_WIDTH//2, 150, center=True)
                if game_state == "BOSS_ATTACK_SEQUENCE":
                    for event in current_events:
                        if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                            if luigi.lockout_turns <= 0:
                                client.update_state({"action": "defend", "press_id": now})
                if game_state == "PLAYER_MENU" and current_turn == "luigi" and not attack_started:
                    draw_text("PRESIONA ENTER PARA ATACAR", font_menu, (255, 255, 255), screen, WINDOW_WIDTH//2, 300, center=True)
                    for event in current_events:
                        if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                            client.update_state({"action": "start_attack"})
                            attack_started = True
                elif game_state == "LUIGI_ACTION_COMMAND":
                    action_cursor_pos = (math.sin(now * 0.008) + 1) / 2.0
                    draw_action_command_bar(screen, action_cursor_pos)
                    draw_text("¡PRESIONA ENTER!", font_menu, (255, 255, 255), screen, WINDOW_WIDTH//2, 300, center=True)
                    for event in current_events:
                        if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                            if action_cursor_pos < 0.20 or action_cursor_pos > 0.80: mult = 0.25
                            elif action_cursor_pos < 0.45 or action_cursor_pos > 0.55: mult = 0.50
                            else: mult = 1.00
                            client.update_state({"action": "attack_confirmed", "damage_multiplier": mult})
        if current_turn != "luigi":
            attack_started = False
            if game_state != "BOSS_ATTACK_SEQUENCE":
                client.update_state({"action": "none"})
            if game_state == "GAME_OVER":
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                go_result = client.get_server_state().get("game_over_result", "FIN DEL JUEGO")
                if not go_result: go_result = "FIN DEL JUEGO"
                draw_text(go_result, font_ds, (255, 255, 255), screen, WINDOW_WIDTH//2, WINDOW_HEIGHT//2, center=True)
            elif game_state == "SCORE_SCREEN":
                screen.fill((20, 20, 40))
                draw_text("PUNTUACIÓN FINAL", font_title, (255, 255, 0), screen, WINDOW_WIDTH//2, 100, center=True)
                mario_score = server_state.get("mario_score", 0)
                luigi_score = server_state.get("luigi_score", 0)
                m1_text = f"Jugador 1 (Mario): {mario_score}"
                l1_text = f"Jugador 2 (Luigi): {luigi_score}"
                if mario_score > luigi_score: m1_text += " - GANADOR"
                elif luigi_score > mario_score: l1_text += " - GANADOR"
                else:
                    m1_text += " - EMPATE"
                    l1_text += " - EMPATE"
                draw_text(m1_text, font_ds, (255, 100, 100), screen, WINDOW_WIDTH//2, 300, center=True)
                draw_text(l1_text, font_ds, (100, 255, 100), screen, WINDOW_WIDTH//2, 400, center=True)
                if button("Volver al menú", WINDOW_WIDTH//2 - 150, 600, 300, 80, (100, 0, 0), (150, 50, 50), action=lambda: "return") == "return":
                    pygame.mixer.music.stop()
                    client.stop()
                    return
        if not client.connected:
            print("Desconectado del servidor.")
            pygame.mixer.music.stop()
            return
        pygame.display.update()
        clock.tick(FPS)

def main():
    while True:
        choice = main_menu()
        if choice == "singleplayer":
            singleplayer_battle()
        elif choice == "multiplayer":
            mp_choice = multiplayer_menu()
            if mp_choice == "host":
                server = host_lobby()
                if server:
                    multiplayer_battle_p1(server)
            elif mp_choice == "join":
                client = join_lobby()
                if client:
                    multiplayer_battle_p2(client)

if __name__ == "__main__":
    main()
