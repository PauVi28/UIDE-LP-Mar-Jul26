import json
import queue
import random
import socket
import threading
import tkinter as tk
from tkinter import messagebox

from game_logic import BOARD_SIZE, SHIP_SIZES, Board
from gui_game import BOARD_PAD, BOARD_PIXEL_SIZE, CELL_SIZE, COLORS


SERVER_TIMEOUT = 0.5


def send_json(conn, obj):
    conn.sendall((json.dumps(obj) + "\n").encode())


def recv_json(conn, buffer):
    while "\n" not in buffer[0]:
        chunk = conn.recv(4096).decode(errors="ignore")
        if not chunk:
            raise ConnectionError("closed")
        buffer[0] += chunk

    line, rest = buffer[0].split("\n", 1)
    buffer[0] = rest
    return json.loads(line)


class MultiplayerClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalla Naval - Cliente Multijugador")
        self.root.geometry("1160x740")
        self.root.minsize(1050, 700)
        self.root.configure(bg=COLORS["bg_top"])

        self.sock = None
        self.send_lock = threading.Lock()
        self.inbox = queue.Queue()
        self.connected = False
        self.game_active = False
        self.my_turn = False
        self.name = f"jugador{random.randint(100, 999)}"
        self.enemy_name = "rival"
        self.player_board = Board()
        self.enemy_radar = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.my_shots = 0
        self.my_hits = 0
        self.enemy_shots = 0
        self.placement_mode = False
        self.pending_ship_sizes = []
        self.selected_start = None
        self.placed_ships = []

        self._build_ui()
        self.refresh_boards()
        self.root.after(100, self.process_inbox)

    def _build_ui(self):
        self.header = tk.Frame(self.root, bg=COLORS["bg_top"])
        self.header.pack(fill="x", padx=28, pady=(18, 10))

        title_box = tk.Frame(self.header, bg=COLORS["bg_top"])
        title_box.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_box,
            text="MULTIJUGADOR",
            font=("Segoe UI", 27, "bold"),
            fg=COLORS["text"],
            bg=COLORS["bg_top"],
        ).pack(anchor="w")
        tk.Label(
            title_box,
            text="Conectate al servidor y dispara desde el radar",
            font=("Segoe UI", 11),
            fg=COLORS["muted"],
            bg=COLORS["bg_top"],
        ).pack(anchor="w")

        form = tk.Frame(self.header, bg=COLORS["bg_top"])
        form.pack(side="right")

        self.host_entry = self._entry(form, "127.0.0.1", 13)
        self.port_entry = self._entry(form, "5000", 6)
        self.name_entry = self._entry(form, self.name, 10)
        self.connect_button = self._button(form, "Conectar", self.connect_to_server)

        self.host_entry.pack(side="left", padx=4)
        self.port_entry.pack(side="left", padx=4)
        self.name_entry.pack(side="left", padx=4)
        self.connect_button.pack(side="left", padx=4)

        self.body = tk.Frame(self.root, bg=COLORS["bg_top"])
        self.body.pack(fill="both", expand=True, padx=28, pady=10)

        self.left = self._panel(self.body)
        self.middle = self._panel(self.body)
        self.right = self._panel(self.body)

        self.left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.middle.pack(side="left", fill="both", expand=True, padx=10)
        self.right.pack(side="left", fill="y", padx=(10, 0))

        self.player_canvas = self._board_panel(self.left, "TU FLOTA", "Tu tablero local")
        self.enemy_canvas = self._board_panel(self.middle, "RADAR DEL RIVAL", "Clic para enviar jugada")
        self.player_canvas.bind("<Button-1>", self.on_player_board_click)
        self.enemy_canvas.bind("<Button-1>", self.on_radar_click)

        self.status = tk.Label(
            self.right,
            text="Conectate para iniciar.",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS["gold"],
            bg=COLORS["panel"],
            wraplength=245,
            justify="left",
        )
        self.status.pack(anchor="w", padx=18, pady=(18, 10))

        self.stats_label = tk.Label(
            self.right,
            text="Disparos: 0\nImpactos: 0\nDisparos rivales: 0",
            font=("Segoe UI", 11),
            fg=COLORS["text"],
            bg=COLORS["panel"],
            justify="left",
        )
        self.stats_label.pack(anchor="w", padx=18, pady=(0, 16))

        tk.Label(
            self.right,
            text="Bitacora de red",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS["text"],
            bg=COLORS["panel"],
        ).pack(anchor="w", padx=18, pady=(4, 6))

        self.log = tk.Listbox(
            self.right,
            width=34,
            height=24,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#2b6381",
            bg=COLORS["panel_2"],
            fg=COLORS["text"],
            selectbackground=COLORS["panel_2"],
            font=("Consolas", 9),
        )
        self.log.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _entry(self, parent, value, width):
        entry = tk.Entry(
            parent,
            width=width,
            font=("Segoe UI", 10),
            bg="#eaf6fb",
            fg="#10263a",
            relief="flat",
            insertbackground="#10263a",
        )
        entry.insert(0, value)
        return entry

    def _button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            fg="#15202b",
            bg=COLORS["gold"],
            activebackground="#ffd989",
            relief="flat",
            padx=14,
            pady=8,
            cursor="hand2",
        )

    def _panel(self, parent):
        return tk.Frame(parent, bg=COLORS["panel"], highlightthickness=1, highlightbackground="#24506b")

    def _board_panel(self, parent, title, subtitle):
        top = tk.Frame(parent, bg=COLORS["panel"])
        top.pack(fill="x", padx=18, pady=(16, 8))

        tk.Label(top, text=title, font=("Segoe UI", 15, "bold"), fg=COLORS["text"], bg=COLORS["panel"]).pack(anchor="w")
        tk.Label(top, text=subtitle, font=("Segoe UI", 10), fg=COLORS["muted"], bg=COLORS["panel"]).pack(anchor="w")

        canvas = tk.Canvas(
            parent,
            width=BOARD_PIXEL_SIZE + BOARD_PAD + 18,
            height=BOARD_PIXEL_SIZE + BOARD_PAD + 18,
            bg=COLORS["panel"],
            highlightthickness=0,
        )
        canvas.pack(padx=14, pady=(0, 16), expand=True)
        return canvas

    def connect_to_server(self):
        if self.connected:
            return

        host = self.host_entry.get().strip() or "127.0.0.1"
        name = self.name_entry.get().strip() or "jugador"

        try:
            port = int(self.port_entry.get().strip())
        except ValueError:
            messagebox.showerror("Puerto invalido", "El puerto debe ser un numero.")
            return

        self.name = name
        self.set_status("Conectando al servidor...", COLORS["gold"])
        self.connect_button.configure(state="disabled")

        thread = threading.Thread(target=self.network_loop, args=(host, port, name), daemon=True)
        thread.start()

    def network_loop(self, host, port, name):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((host, port))
            self.sock.settimeout(SERVER_TIMEOUT)
            buffer = [""]
            self.inbox.put(("connected", None))

            while True:
                try:
                    msg = recv_json(self.sock, buffer)
                except socket.timeout:
                    continue

                if msg.get("type") == "request_handshake":
                    self.send({"type": "handshake", "name": name})
                elif msg.get("type") == "request" and msg.get("what") == "place_fleet":
                    self.inbox.put(("place_request", None))
                else:
                    self.inbox.put(("message", msg))
        except Exception as exc:
            self.inbox.put(("error", str(exc)))

    def send(self, obj):
        if not self.sock:
            return

        with self.send_lock:
            send_json(self.sock, obj)

    def start_manual_placement(self):
        self.player_board = Board()
        self.enemy_radar = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.my_shots = 0
        self.my_hits = 0
        self.enemy_shots = 0
        self.game_active = False
        self.my_turn = False
        self.placement_mode = True
        self.pending_ship_sizes = SHIP_SIZES[:]
        self.selected_start = None
        self.placed_ships = []
        self.add_log("El servidor pide colocar la flota.")
        self.set_placement_status()
        self.refresh_boards()

    def process_inbox(self):
        while not self.inbox.empty():
            kind, data = self.inbox.get()

            if kind == "connected":
                self.connected = True
                self.add_log("Conexion realizada.")
                self.set_status("Esperando al segundo jugador...", COLORS["gold"])
            elif kind == "place_request":
                self.start_manual_placement()
            elif kind == "message":
                self.handle_message(data)
            elif kind == "error":
                self.connected = False
                self.game_active = False
                self.connect_button.configure(state="normal")
                self.set_status("Conexion finalizada.", COLORS["danger"])
                self.add_log(f"Error/red: {data}")

        self.root.after(100, self.process_inbox)

    def handle_message(self, msg):
        msg_type = msg.get("type")

        if msg_type == "ack":
            self.add_log("Servidor acepto tu flota.")
            self.placement_mode = False
            self.game_active = True
            self.set_status("Flota aceptada. Esperando inicio de turnos...", COLORS["gold"])
            self.refresh_boards()
        elif msg_type == "state":
            self.my_turn = bool(msg.get("your_turn"))
            names = list(msg.get("boards", {}).keys())
            rivals = [item for item in names if item != self.name]
            if rivals:
                self.enemy_name = rivals[0]
            if self.my_turn:
                self.set_status("Tu turno: haz clic en el radar enemigo.", COLORS["gold"])
            else:
                self.set_status("Turno del rival. Esperando jugada...", COLORS["muted"])
            self.refresh_boards()
        elif msg_type == "result":
            self.apply_result(msg)
        elif msg_type == "end":
            self.game_active = False
            self.my_turn = False
            winner = msg.get("winner")
            if winner:
                message = "Ganaste la partida." if winner == self.name else f"Gano {winner}."
            else:
                message = msg.get("message", "Partida terminada.")
            self.set_status(message, COLORS["gold"])
            self.add_log(message)
            self.refresh_boards()
            messagebox.showinfo("Partida terminada", message)
        elif msg_type == "error":
            self.add_log("Servidor: " + str(msg.get("message")))
        else:
            self.add_log("Servidor: " + str(msg))

    def apply_result(self, msg):
        coord = tuple(msg.get("coord", []))
        result = msg.get("result")

        if len(coord) != 2:
            return

        r, c = coord
        was_hit = result in ("impacto", "hundido")

        if msg.get("from") == self.name:
            self.my_shots += 1
            if was_hit:
                self.my_hits += 1
            self.enemy_radar[r][c] = 2 if was_hit else 3
            self.add_log(f"Tu disparo {coord}: {self.label_result(result)}")
            if was_hit:
                self.set_status("Acertaste. Sigues jugando cuando el servidor confirme tu turno.", COLORS["green"])
        elif msg.get("to") == self.name:
            self.enemy_shots += 1
            self.player_board.grid[r][c] = 2 if was_hit else 3
            self.add_log(f"Rival dispara {coord}: {self.label_result(result)}")
            if was_hit:
                self.set_status("El rival acerto y conserva el turno.", COLORS["danger"])

        self.refresh_boards()

    def on_radar_click(self, event):
        if self.placement_mode or not self.connected or not self.game_active or not self.my_turn:
            return

        coord = self.event_to_coord(event)
        if coord is None:
            return

        r, c = coord
        if self.enemy_radar[r][c] in (2, 3):
            self.set_status("Esa casilla ya fue usada. Elige otra.", COLORS["danger"])
            return

        self.my_turn = False
        self.set_status("Jugada enviada. Esperando resultado...", COLORS["muted"])
        self.send({"type": "move", "coord": [r, c]})
        self.refresh_boards()

    def event_to_coord(self, event):
        col = int((event.x - BOARD_PAD) // CELL_SIZE)
        row = int((event.y - BOARD_PAD) // CELL_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None

    def refresh_boards(self):
        self.draw_board(
            self.player_canvas,
            self.player_board.grid,
            reveal_ships=True,
            enabled=self.placement_mode,
            selected=self.selected_start,
        )
        self.draw_board(self.enemy_canvas, self.enemy_radar, reveal_ships=False, enabled=self.my_turn and self.game_active)
        self.stats_label.configure(
            text=f"Disparos: {self.my_shots}\nImpactos: {self.my_hits}\nDisparos rivales: {self.enemy_shots}"
        )

    def draw_board(self, canvas, grid, reveal_ships, enabled, selected=None):
        canvas.delete("all")
        canvas.create_rectangle(
            18,
            18,
            BOARD_PIXEL_SIZE + BOARD_PAD + 10,
            BOARD_PIXEL_SIZE + BOARD_PAD + 10,
            fill="#0b2032",
            outline="#295b78",
            width=2,
        )

        for i in range(BOARD_SIZE):
            canvas.create_text(
                BOARD_PAD + i * CELL_SIZE + CELL_SIZE / 2,
                23,
                text=str(i),
                fill=COLORS["muted"],
                font=("Segoe UI", 9, "bold"),
            )
            canvas.create_text(
                24,
                BOARD_PAD + i * CELL_SIZE + CELL_SIZE / 2,
                text=str(i),
                fill=COLORS["muted"],
                font=("Segoe UI", 9, "bold"),
            )

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x1 = BOARD_PAD + c * CELL_SIZE
                y1 = BOARD_PAD + r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                value = grid[r][c]
                water = COLORS["water_1"] if (r + c) % 2 == 0 else COLORS["water_2"]
                canvas.create_rectangle(x1, y1, x2, y2, fill=water, outline=COLORS["line"], width=1)

                if value == 1 and reveal_ships:
                    canvas.create_rectangle(x1 + 5, y1 + 8, x2 - 5, y2 - 8, fill=COLORS["ship"], outline=COLORS["ship_dark"], width=2)
                    canvas.create_line(x1 + 9, y1 + 12, x2 - 9, y1 + 12, fill=COLORS["ship_light"], width=2)
                elif value == 2:
                    canvas.create_oval(x1 + 7, y1 + 7, x2 - 7, y2 - 7, fill=COLORS["hit"], outline=COLORS["hit_dark"], width=2)
                    canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="X", fill=COLORS["gold"], font=("Segoe UI", 12, "bold"))
                elif value == 3:
                    canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, outline=COLORS["miss"], width=3)

        if selected is not None:
            r, c = selected
            x1 = BOARD_PAD + c * CELL_SIZE
            y1 = BOARD_PAD + r * CELL_SIZE
            canvas.create_rectangle(x1 + 3, y1 + 3, x1 + CELL_SIZE - 3, y1 + CELL_SIZE - 3, outline=COLORS["gold"], width=3)

        if enabled:
            canvas.create_rectangle(
                BOARD_PAD,
                BOARD_PAD,
                BOARD_PAD + BOARD_PIXEL_SIZE,
                BOARD_PAD + BOARD_PIXEL_SIZE,
                outline=COLORS["gold"],
                width=3,
            )

    def on_player_board_click(self, event):
        if not self.placement_mode:
            return

        coord = self.event_to_coord(event)
        if coord is None:
            return

        if self.selected_start is None:
            self.selected_start = coord
            self.set_status("Ahora selecciona la casilla final del barco.", COLORS["gold"])
            self.refresh_boards()
            return

        size = self.pending_ship_sizes[0]
        start = self.selected_start
        end = coord
        coords = self.player_board._coords_between(start, end)

        if coords is None or len(coords) != size:
            self.selected_start = None
            self.set_status(f"Barco invalido. Debe medir {size} casillas en linea recta.", COLORS["danger"])
            self.refresh_boards()
            return

        if not self.player_board.place_ship(start, end):
            self.selected_start = None
            self.set_status("No puedes poner un barco encima de otro o fuera del tablero.", COLORS["danger"])
            self.refresh_boards()
            return

        self.placed_ships.append([list(start), list(end)])
        self.pending_ship_sizes.pop(0)
        self.selected_start = None
        self.add_log(f"Barco de tamano {size} colocado.")

        if not self.pending_ship_sizes:
            self.placement_mode = False
            self.set_status("Flota lista. Enviando al servidor...", COLORS["gold"])
            self.send({"type": "place_fleet", "ships": self.placed_ships})
        else:
            self.set_placement_status()

        self.refresh_boards()

    def set_placement_status(self):
        size = self.pending_ship_sizes[0]
        self.set_status(f"Coloca un barco de {size} casillas: clic en inicio y clic en final.", COLORS["gold"])

    def set_status(self, text, color):
        self.status.configure(text=text, fg=color)

    def add_log(self, text):
        self.log.insert(tk.END, text)
        self.log.yview_moveto(1)

    def label_result(self, result):
        labels = {
            "agua": "agua",
            "impacto": "impacto",
            "hundido": "hundido",
            "repetida": "repetida",
            "invalid": "invalida",
        }
        return labels.get(result, str(result))


def main():
    root = tk.Tk()
    MultiplayerClientApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
