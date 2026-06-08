import json
import socket
import time

from game_logic import BOARD_SIZE, Board


HOST = "0.0.0.0"
PORT = 5000
SOCKET_TIMEOUT = 0.5


def send_json(conn, obj):
    data = json.dumps(obj) + "\n"
    conn.sendall(data.encode())


def recv_json(conn, buffer):
    while "\n" not in buffer[0]:
        chunk = conn.recv(4096).decode(errors="ignore")
        if not chunk:
            raise ConnectionError("closed")
        buffer[0] += chunk

    line, rest = buffer[0].split("\n", 1)
    buffer[0] = rest
    return json.loads(line)


class ClientSlot:
    def __init__(self, conn, addr, name, buffer):
        self.conn = conn
        self.addr = addr
        self.name = name
        self.buf = buffer
        self.alive = True


class GameServer:
    def __init__(self, host=HOST, port=PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(2)
        self.sock.settimeout(None)
        self.clients = []
        self.boards = {}
        self.player_order = []
        self.shutdown = False

    def accept_clients(self):
        while len(self.clients) < 2 and not self.shutdown:
            conn, addr = self.sock.accept()
            conn.settimeout(SOCKET_TIMEOUT)
            buffer = [""]

            send_json(conn, {"type": "request_handshake"})

            try:
                msg = recv_json(conn, buffer)
            except Exception:
                conn.close()
                continue

            name = msg.get("name") if isinstance(msg, dict) else None
            if not name:
                name = f"player{len(self.clients) + 1}"

            slot = ClientSlot(conn, addr, name, buffer)
            self.clients.append(slot)
            print(f"Conectado: {slot.name} desde {addr}")

        self.player_order = [client.name for client in self.clients]

    def request_fleets(self):
        for slot in self.clients:
            try:
                send_json(slot.conn, {"type": "request", "what": "place_fleet"})
            except Exception:
                slot.alive = False

        for slot in self.clients:
            if not slot.alive:
                continue

            try:
                msg = self.wait_for_fleet(slot)
            except Exception:
                slot.alive = False
                continue

            if msg is None:
                send_json(slot.conn, {"type": "error", "message": "timeout_place_fleet"})
                slot.alive = False
                continue

            if not isinstance(msg, dict) or msg.get("type") != "place_fleet":
                send_json(slot.conn, {"type": "error", "message": "expecting place_fleet"})
                slot.alive = False
                continue

            ships = msg.get("ships", [])
            board = Board()
            ok, err = board.place_fleet(ships)

            if not ok:
                send_json(slot.conn, {"type": "error", "message": f"invalid_fleet:{err}"})
                slot.alive = False
                continue

            self.boards[slot.name] = board
            send_json(slot.conn, {"type": "ack", "message": "fleet_accepted"})

    def wait_for_fleet(self, slot):
        start_time = time.time()

        while time.time() - start_time < 300:
            try:
                msg = recv_json(slot.conn, slot.buf)
            except socket.timeout:
                continue

            if isinstance(msg, dict) and msg.get("type") == "place_fleet":
                return msg

            send_json(slot.conn, {"type": "error", "message": "place_fleet_required"})

        return None

    def broadcast(self, obj):
        for slot in self.clients:
            if not slot.alive:
                continue

            try:
                send_json(slot.conn, obj)
            except Exception:
                slot.alive = False

    def run_game(self):
        current_idx = 0

        while True:
            active = [client for client in self.clients if client.alive]
            if len(active) < 2:
                self.broadcast({"type": "end", "message": "opponent_disconnected"})
                break

            current = self.player_order[current_idx]
            opponent = self.player_order[1 - current_idx]
            state_obj = {"type": "state", "your_turn": None, "boards": {}}

            for name in self.player_order:
                state_obj["boards"][name] = self.boards[name].as_public(hide_ships=True)

            for slot in self.clients:
                try:
                    send_json(slot.conn, {**state_obj, "your_turn": slot.name == current})
                except Exception:
                    slot.alive = False

            curr_slot = next((slot for slot in self.clients if slot.name == current), None)
            if curr_slot is None or not curr_slot.alive:
                current_idx = 1 - current_idx
                continue

            try:
                move_msg = self.wait_for_move(curr_slot)
            except ConnectionError:
                curr_slot.alive = False
                continue

            if move_msg is None:
                send_json(curr_slot.conn, {"type": "error", "message": "timeout_move"})
                current_idx = 1 - current_idx
                continue

            coord = tuple(move_msg.get("coord", []))
            if len(coord) != 2 or not all(isinstance(x, int) for x in coord):
                send_json(curr_slot.conn, {"type": "error", "message": "invalid_coord_format"})
                continue

            if not (0 <= coord[0] < BOARD_SIZE and 0 <= coord[1] < BOARD_SIZE):
                send_json(curr_slot.conn, {"type": "error", "message": "coord_out_of_bounds"})
                continue

            result, sunk = self.boards[opponent].receive_shot(coord)
            result_obj = {
                "type": "result",
                "from": current,
                "to": opponent,
                "coord": list(coord),
                "result": result,
            }

            if sunk:
                result_obj["sunk_coords"] = [list(item) for item in sunk]

            self.broadcast(result_obj)

            if self.boards[opponent].all_sunk():
                self.broadcast({"type": "end", "winner": current})
                break

            if result == "agua":
                current_idx = 1 - current_idx

    def wait_for_move(self, slot):
        start_time = time.time()

        while time.time() - start_time < 60:
            try:
                msg = recv_json(slot.conn, slot.buf)
            except socket.timeout:
                continue

            if not isinstance(msg, dict):
                continue

            if msg.get("type") == "move":
                return msg

            send_json(slot.conn, {"type": "error", "message": "unexpected_message"})

        return None

    def serve_forever(self):
        try:
            print(f"Servidor escuchando en {HOST}:{PORT}")
            self.accept_clients()

            if len(self.clients) < 2:
                return

            self.request_fleets()

            if len(self.boards) < 2:
                return

            self.run_game()
        finally:
            for slot in self.clients:
                try:
                    slot.conn.close()
                except Exception:
                    pass
            self.sock.close()


if __name__ == "__main__":
    GameServer().serve_forever()
