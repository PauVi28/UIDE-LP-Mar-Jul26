import socket
import threading
import json
import time

class GameServer:
    def __init__(self, port=0):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if port == 0:
            import random
            while True:
                port = random.randint(50000, 50999)
                try:
                    self.server_socket.bind(('0.0.0.0', port))
                    break
                except OSError:
                    continue
        else:
            self.server_socket.bind(('0.0.0.0', port))
        self.port = self.server_socket.getsockname()[1]
        self.server_socket.listen(1)
        self.client_socket = None
        self.state_to_send = {}
        self.state_received = {}
        self.buffer = ""
        self.running = True
        self.connected = False
        self.thread = threading.Thread(target=self._server_loop, daemon=True)
        self.thread.start()

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def update_state(self, state_dict):
        self.state_to_send = state_dict

    def get_client_state(self):
        return self.state_received

    def _server_loop(self):
        self.server_socket.settimeout(1.0)
        while self.running and not self.client_socket:
            try:
                conn, addr = self.server_socket.accept()
                self.client_socket = conn
                self.client_socket.settimeout(0.1)
                self.connected = True
                print(f"[SERVER] Client connected from {addr}")
            except socket.timeout:
                pass
            except Exception as e:
                print(f"[SERVER] Error accepting: {e}")

        while self.running and self.client_socket:
            try:
                data = json.dumps(self.state_to_send).encode('utf-8')
                self.client_socket.sendall(data + b"\\n")
                recv_data = self.client_socket.recv(4096)
                if recv_data:
                    self.buffer += recv_data.decode('utf-8')
                    if '\\n' in self.buffer:
                        parts = self.buffer.split('\\n')
                        self.buffer = parts[-1]
                        for msg in reversed(parts[:-1]):
                            if msg.strip():
                                try:
                                    self.state_received = json.loads(msg.strip())
                                    break
                                except json.JSONDecodeError:
                                    pass
                else:
                    self.connected = False
                    self.client_socket.close()
                    self.client_socket = None
            except socket.timeout:
                pass
            except Exception as e:
                print(f"[SERVER] Error: {e}")
                self.connected = False
                self.client_socket.close()
                self.client_socket = None
            time.sleep(0.016)

    def stop(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        self.server_socket.close()
