import math
import random
import tkinter as tk
from tkinter import messagebox

from game_logic import BOARD_SIZE, SHIP_SIZES, Board


CELL_SIZE = 38
BOARD_PAD = 42
BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE

COLORS = {
    "bg_top": "#071421",
    "bg_bottom": "#0d3149",
    "panel": "#10263a",
    "panel_2": "#123853",
    "line": "#2e7195",
    "water_1": "#0a6b95",
    "water_2": "#114a78",
    "water_3": "#1596bd",
    "ship": "#778894",
    "ship_dark": "#3e4b56",
    "ship_light": "#b1c1c8",
    "hit": "#ff4f5e",
    "hit_dark": "#8b1627",
    "miss": "#d4f4ff",
    "miss_ring": "#7cc8e8",
    "text": "#eef8ff",
    "muted": "#a8c4d7",
    "gold": "#ffca5c",
    "green": "#48d597",
    "danger": "#ff6b6b",
}


class BattleshipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalla Naval - Interfaz Grafica")
        self.root.geometry("1180x760")
        self.root.minsize(1050, 700)
        self.root.configure(bg=COLORS["bg_top"])

        self.player_board = Board()
        self.enemy_board = Board()
        self.player_turn = True
        self.game_active = True
        self.player_shots = 0
        self.enemy_shots = 0
        self.player_hits = 0
        self.enemy_hits = 0
        self.placement_mode = False
        self.pending_ship_sizes = []
        self.selected_start = None

        self._build_ui()
        self.new_game()

    def _build_ui(self):
        self.bg = tk.Canvas(self.root, highlightthickness=0, bg=COLORS["bg_top"])
        self.bg.pack(fill="both", expand=True)
        self.bg.bind("<Configure>", self._draw_background)

        self.shell = tk.Frame(self.bg, bg=COLORS["bg_top"])
        self.bg_window = self.bg.create_window(0, 0, anchor="nw", window=self.shell)
        self.bg.bind("<Configure>", self._position_shell)

        self.header = tk.Frame(self.shell, bg=COLORS["bg_top"])
        self.header.pack(fill="x", padx=30, pady=(22, 10))

        title_box = tk.Frame(self.header, bg=COLORS["bg_top"])
        title_box.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_box,
            text="BATALLA NAVAL",
            font=("Segoe UI", 28, "bold"),
            fg=COLORS["text"],
            bg=COLORS["bg_top"],
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="Modo visual contra la computadora",
            font=("Segoe UI", 12),
            fg=COLORS["muted"],
            bg=COLORS["bg_top"],
        ).pack(anchor="w", pady=(2, 0))

        controls = tk.Frame(self.header, bg=COLORS["bg_top"])
        controls.pack(side="right")

        self._make_button(controls, "Nueva partida", self.new_game).pack(side="left", padx=6)
        self._make_button(controls, "Salir", self.root.destroy, accent=False).pack(side="left", padx=6)

        self.main = tk.Frame(self.shell, bg=COLORS["bg_top"])
        self.main.pack(fill="both", expand=True, padx=30, pady=10)

        self.left_panel = self._make_panel(self.main)
        self.center_panel = self._make_panel(self.main)
        self.right_panel = self._make_panel(self.main)

        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self.center_panel.pack(side="left", fill="both", expand=True, padx=12)
        self.right_panel.pack(side="left", fill="y", padx=(12, 0))

        self.player_canvas = self._make_board_panel(self.left_panel, "TU FLOTA", "Barcos visibles")
        self.enemy_canvas = self._make_board_panel(self.center_panel, "RADAR ENEMIGO", "Haz clic para disparar")
        self.player_canvas.bind("<Button-1>", self.on_player_board_click)
        self.enemy_canvas.bind("<Button-1>", self.on_enemy_click)

        self._build_side_panel()

    def _make_panel(self, parent):
        panel = tk.Frame(parent, bg=COLORS["panel"], highlightthickness=1, highlightbackground="#24506b")
        return panel

    def _make_button(self, parent, text, command, accent=True):
        color = COLORS["gold"] if accent else COLORS["panel_2"]
        hover = "#ffd989" if accent else "#1b4b69"
        fg = "#15202b" if accent else COLORS["text"]

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            fg=fg,
            bg=color,
            activebackground=hover,
            activeforeground=fg,
            relief="flat",
            padx=18,
            pady=9,
            cursor="hand2",
        )
        return button

    def _make_board_panel(self, parent, title, subtitle):
        top = tk.Frame(parent, bg=COLORS["panel"])
        top.pack(fill="x", padx=18, pady=(16, 8))

        tk.Label(
            top,
            text=title,
            font=("Segoe UI", 15, "bold"),
            fg=COLORS["text"],
            bg=COLORS["panel"],
        ).pack(anchor="w")

        tk.Label(
            top,
            text=subtitle,
            font=("Segoe UI", 10),
            fg=COLORS["muted"],
            bg=COLORS["panel"],
        ).pack(anchor="w")

        canvas = tk.Canvas(
            parent,
            width=BOARD_PIXEL_SIZE + BOARD_PAD + 18,
            height=BOARD_PIXEL_SIZE + BOARD_PAD + 18,
            bg=COLORS["panel"],
            highlightthickness=0,
        )
        canvas.pack(padx=14, pady=(0, 16), expand=True)
        return canvas

    def _build_side_panel(self):
        tk.Label(
            self.right_panel,
            text="PANEL DE MANDO",
            font=("Segoe UI", 15, "bold"),
            fg=COLORS["text"],
            bg=COLORS["panel"],
        ).pack(anchor="w", padx=18, pady=(18, 4))

        self.status_label = tk.Label(
            self.right_panel,
            text="Preparando batalla...",
            font=("Segoe UI", 11, "bold"),
            fg=COLORS["gold"],
            bg=COLORS["panel"],
            wraplength=250,
            justify="left",
        )
        self.status_label.pack(anchor="w", padx=18, pady=(0, 14))

        self.stats = tk.Frame(self.right_panel, bg=COLORS["panel"])
        self.stats.pack(fill="x", padx=18, pady=8)

        self.player_stat = self._make_stat_card(self.stats, "Tus disparos", "0")
        self.hit_stat = self._make_stat_card(self.stats, "Tus impactos", "0")
        self.enemy_stat = self._make_stat_card(self.stats, "Disparos rivales", "0")

        self.player_stat.pack(fill="x", pady=5)
        self.hit_stat.pack(fill="x", pady=5)
        self.enemy_stat.pack(fill="x", pady=5)

        tk.Label(
            self.right_panel,
            text="Bitacora",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS["text"],
            bg=COLORS["panel"],
        ).pack(anchor="w", padx=18, pady=(16, 6))

        log_frame = tk.Frame(self.right_panel, bg=COLORS["panel_2"], highlightthickness=1, highlightbackground="#2b6381")
        log_frame.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.log_list = tk.Listbox(
            log_frame,
            height=12,
            borderwidth=0,
            highlightthickness=0,
            bg=COLORS["panel_2"],
            fg=COLORS["text"],
            selectbackground=COLORS["panel_2"],
            activestyle="none",
            font=("Consolas", 9),
        )
        self.log_list.pack(fill="both", expand=True, padx=8, pady=8)

        legend = tk.Frame(self.right_panel, bg=COLORS["panel"])
        legend.pack(fill="x", padx=18, pady=(0, 18))

        self._legend_item(legend, COLORS["ship"], "Barco").pack(anchor="w", pady=2)
        self._legend_item(legend, COLORS["hit"], "Impacto").pack(anchor="w", pady=2)
        self._legend_item(legend, COLORS["miss"], "Agua").pack(anchor="w", pady=2)

    def _make_stat_card(self, parent, label, value):
        card = tk.Frame(parent, bg=COLORS["panel_2"], highlightthickness=1, highlightbackground="#2b6381")
        tk.Label(card, text=label, font=("Segoe UI", 9), fg=COLORS["muted"], bg=COLORS["panel_2"]).pack(
            anchor="w", padx=12, pady=(8, 0)
        )
        value_label = tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), fg=COLORS["text"], bg=COLORS["panel_2"])
        value_label.pack(anchor="w", padx=12, pady=(0, 8))
        card.value_label = value_label
        return card

    def _legend_item(self, parent, color, text):
        item = tk.Frame(parent, bg=COLORS["panel"])
        sample = tk.Canvas(item, width=18, height=18, bg=COLORS["panel"], highlightthickness=0)
        sample.create_oval(3, 3, 15, 15, fill=color, outline="")
        sample.pack(side="left")
        tk.Label(item, text=text, font=("Segoe UI", 9), fg=COLORS["muted"], bg=COLORS["panel"]).pack(side="left", padx=8)
        return item

    def _draw_background(self, event):
        self.bg.delete("bg")
        height = max(event.height, 1)
        width = max(event.width, 1)

        for y in range(0, height, 4):
            ratio = y / height
            color = self._mix_color(COLORS["bg_top"], COLORS["bg_bottom"], ratio)
            self.bg.create_rectangle(0, y, width, y + 4, fill=color, outline="", tags="bg")

        for x in range(-80, width + 100, 190):
            y = int(height * 0.18 + math.sin(x / 80) * 15)
            self.bg.create_arc(x, y, x + 160, y + 50, start=0, extent=180, outline="#123f5b", width=2, tags="bg")

        self.bg.tag_lower("bg")

    def _position_shell(self, event):
        self.bg.coords(self.bg_window, 0, 0)
        self.bg.itemconfigure(self.bg_window, width=event.width, height=event.height)

    def _mix_color(self, a, b, ratio):
        a = a.lstrip("#")
        b = b.lstrip("#")
        ar, ag, ab = int(a[0:2], 16), int(a[2:4], 16), int(a[4:6], 16)
        br, bg, bb = int(b[0:2], 16), int(b[2:4], 16), int(b[4:6], 16)
        r = int(ar + (br - ar) * ratio)
        g = int(ag + (bg - ag) * ratio)
        blue = int(ab + (bb - ab) * ratio)
        return f"#{r:02x}{g:02x}{blue:02x}"

    def new_game(self):
        self.player_board = Board()
        self.enemy_board = Board()
        self.enemy_board.place_fleet(self.enemy_board.random_place_all())

        self.player_turn = False
        self.game_active = False
        self.player_shots = 0
        self.enemy_shots = 0
        self.player_hits = 0
        self.enemy_hits = 0
        self.placement_mode = True
        self.pending_ship_sizes = SHIP_SIZES[:]
        self.selected_start = None

        self.log_list.delete(0, tk.END)
        self.add_log("Nueva partida iniciada.")
        self.add_log("Coloca tu flota en el tablero izquierdo.")
        self.set_placement_status()
        self.refresh_all()

    def refresh_all(self):
        self.draw_board(
            self.player_canvas,
            self.player_board,
            reveal_ships=True,
            enabled=self.placement_mode,
            selected=self.selected_start,
        )
        self.draw_board(self.enemy_canvas, self.enemy_board, reveal_ships=False, enabled=self.player_turn and self.game_active)
        self.update_stats()

    def draw_board(self, canvas, board, reveal_ships, enabled, selected=None):
        canvas.delete("all")
        canvas.create_rectangle(18, 18, BOARD_PIXEL_SIZE + BOARD_PAD + 10, BOARD_PIXEL_SIZE + BOARD_PAD + 10, fill="#0b2032", outline="#295b78", width=2)

        for i in range(BOARD_SIZE):
            text_color = COLORS["muted"]
            canvas.create_text(BOARD_PAD + i * CELL_SIZE + CELL_SIZE / 2, 23, text=str(i), fill=text_color, font=("Segoe UI", 9, "bold"))
            canvas.create_text(24, BOARD_PAD + i * CELL_SIZE + CELL_SIZE / 2, text=str(i), fill=text_color, font=("Segoe UI", 9, "bold"))

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x1 = BOARD_PAD + c * CELL_SIZE
                y1 = BOARD_PAD + r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                val = board.grid[r][c]
                water = COLORS["water_1"] if (r + c) % 2 == 0 else COLORS["water_2"]

                canvas.create_rectangle(x1, y1, x2, y2, fill=water, outline=COLORS["line"], width=1)
                canvas.create_line(x1 + 4, y1 + 8, x2 - 4, y1 + 8, fill=COLORS["water_3"], width=1)

                if val == 1 and reveal_ships:
                    self.draw_ship_cell(canvas, x1, y1, x2, y2)
                elif val == 2:
                    self.draw_hit(canvas, x1, y1, x2, y2)
                elif val == 3:
                    self.draw_miss(canvas, x1, y1, x2, y2)

        if selected is not None:
            r, c = selected
            x1 = BOARD_PAD + c * CELL_SIZE
            y1 = BOARD_PAD + r * CELL_SIZE
            canvas.create_rectangle(x1 + 3, y1 + 3, x1 + CELL_SIZE - 3, y1 + CELL_SIZE - 3, outline=COLORS["gold"], width=3)

        if enabled:
            canvas.create_rectangle(BOARD_PAD, BOARD_PAD, BOARD_PAD + BOARD_PIXEL_SIZE, BOARD_PAD + BOARD_PIXEL_SIZE, outline=COLORS["gold"], width=3)

    def draw_ship_cell(self, canvas, x1, y1, x2, y2):
        canvas.create_rectangle(x1 + 5, y1 + 8, x2 - 5, y2 - 8, fill=COLORS["ship"], outline=COLORS["ship_dark"], width=2)
        canvas.create_line(x1 + 9, y1 + 12, x2 - 9, y1 + 12, fill=COLORS["ship_light"], width=2)
        canvas.create_oval(x1 + 12, y1 + 15, x1 + 20, y1 + 23, fill=COLORS["ship_dark"], outline="")
        canvas.create_oval(x2 - 20, y1 + 15, x2 - 12, y1 + 23, fill=COLORS["ship_dark"], outline="")

    def draw_hit(self, canvas, x1, y1, x2, y2):
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        points = []

        for i in range(12):
            angle = math.pi * 2 * i / 12
            radius = 15 if i % 2 == 0 else 6
            points.append(cx + math.cos(angle) * radius)
            points.append(cy + math.sin(angle) * radius)

        canvas.create_polygon(points, fill=COLORS["hit"], outline=COLORS["hit_dark"], width=2)
        canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill=COLORS["gold"], outline="")

    def draw_miss(self, canvas, x1, y1, x2, y2):
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, outline=COLORS["miss"], width=3)
        canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill=COLORS["miss_ring"], outline="")

    def on_enemy_click(self, event):
        if self.placement_mode or not self.game_active or not self.player_turn:
            return

        coord = self.event_to_coord(event)
        if coord is None:
            return

        result, sunk = self.enemy_board.receive_shot(coord)

        if result == "repetida":
            self.set_status("Ya disparaste en esa casilla. Prueba otra.", COLORS["danger"])
            return

        self.player_shots += 1
        if result in ("impacto", "hundido"):
            self.player_hits += 1

        self.add_log(f"Tu disparo {coord}: {self.translate_result(result)}")
        keeps_turn = result in ("impacto", "hundido")
        self.set_status(self.status_for_result(result, "Buen disparo."), COLORS["green"] if keeps_turn else COLORS["muted"])
        self.refresh_all()

        if self.enemy_board.all_sunk():
            self.end_game("Ganaste. Hundiste toda la flota enemiga.")
            return

        if keeps_turn:
            self.player_turn = True
            self.set_status("Acertaste. Sigues jugando hasta que falles.", COLORS["green"])
            self.refresh_all()
        else:
            self.player_turn = False
            self.refresh_all()
            self.root.after(700, self.cpu_turn)

    def cpu_turn(self):
        if not self.game_active:
            return

        coord = self.random_cpu_coord()
        result, sunk = self.player_board.receive_shot(coord)

        self.enemy_shots += 1
        if result in ("impacto", "hundido"):
            self.enemy_hits += 1

        self.add_log(f"Rival dispara {coord}: {self.translate_result(result)}")

        if self.player_board.all_sunk():
            self.refresh_all()
            self.end_game("Perdiste. Tu flota fue destruida.")
            return

        if result in ("impacto", "hundido"):
            self.set_status("El rival acerto y conserva el turno.", COLORS["danger"])
            self.refresh_all()
            self.root.after(800, self.cpu_turn)
        else:
            self.player_turn = True
            self.set_status("Tu turno: elige una casilla del radar enemigo.", COLORS["gold"])
            self.refresh_all()

    def on_player_board_click(self, event):
        if not self.placement_mode:
            return

        coord = self.event_to_coord(event)
        if coord is None:
            return

        if self.selected_start is None:
            self.selected_start = coord
            self.set_status("Ahora selecciona la casilla final del barco.", COLORS["gold"])
            self.refresh_all()
            return

        size = self.pending_ship_sizes[0]
        start = self.selected_start
        end = coord
        coords = self.player_board._coords_between(start, end)

        if coords is None or len(coords) != size:
            self.selected_start = None
            self.set_status(f"Barco invalido. Debe medir {size} casillas en linea recta.", COLORS["danger"])
            self.refresh_all()
            return

        if not self.player_board.place_ship(start, end):
            self.selected_start = None
            self.set_status("No puedes poner un barco encima de otro o fuera del tablero.", COLORS["danger"])
            self.refresh_all()
            return

        self.add_log(f"Barco de tamano {size} colocado.")
        self.pending_ship_sizes.pop(0)
        self.selected_start = None

        if not self.pending_ship_sizes:
            self.placement_mode = False
            self.game_active = True
            self.player_turn = True
            self.add_log("Flota lista. Empieza la batalla.")
            self.set_status("Tu turno: dispara en el radar enemigo.", COLORS["gold"])
        else:
            self.set_placement_status()

        self.refresh_all()

    def set_placement_status(self):
        size = self.pending_ship_sizes[0]
        self.set_status(f"Coloca un barco de {size} casillas: clic en inicio y clic en final.", COLORS["gold"])

    def random_cpu_coord(self):
        available = []

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.player_board.grid[r][c] not in (2, 3):
                    available.append((r, c))

        return random.choice(available)

    def event_to_coord(self, event):
        col = int((event.x - BOARD_PAD) // CELL_SIZE)
        row = int((event.y - BOARD_PAD) // CELL_SIZE)

        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col

        return None

    def translate_result(self, result):
        labels = {
            "agua": "agua",
            "impacto": "impacto",
            "hundido": "barco hundido",
            "repetida": "repetida",
            "invalid": "invalida",
        }
        return labels.get(result, result)

    def status_for_result(self, result, default):
        if result == "agua":
            return "Agua. El rival prepara su respuesta."
        if result == "impacto":
            return "Impacto confirmado. Sigues jugando."
        if result == "hundido":
            return "Barco enemigo hundido. Sigues jugando."
        return default

    def set_status(self, text, color):
        self.status_label.configure(text=text, fg=color)

    def add_log(self, text):
        self.log_list.insert(tk.END, text)
        self.log_list.yview_moveto(1)

    def update_stats(self):
        self.player_stat.value_label.configure(text=str(self.player_shots))
        self.hit_stat.value_label.configure(text=str(self.player_hits))
        self.enemy_stat.value_label.configure(text=str(self.enemy_shots))

    def end_game(self, message):
        self.game_active = False
        self.player_turn = False
        self.set_status(message, COLORS["gold"])
        self.add_log(message)
        self.refresh_all()
        messagebox.showinfo("Partida terminada", message)


def main():
    root = tk.Tk()
    app = BattleshipApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
