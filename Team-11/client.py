import socket
import threading
import json
import time

class GameClient:
    def __init__(self, ip, port=5555):
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.state_to_send = {}
        self.state_received = {}
        self.buffer = ""
        self.running = True
        self.connected = False
        self.thread = threading.Thread(target=self._client_loop, daemon=True)
        self.thread.start()

    def update_state(self, state_dict):
        self.state_to_send = state_dict

    def get_server_state(self):
        return self.state_received

    def _client_loop(self):
        try:
            self.client_socket.connect((self.ip, self.port))
            self.client_socket.settimeout(0.1)
            self.connected = True
            print(f"[CLIENT] Connected to server {self.ip}:{self.port}")
        except Exception as e:
            print(f"[CLIENT] Failed to connect: {e}")
            self.running = False
            return

        while self.running:
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
                    self.running = False
            except socket.timeout:
                pass
            except Exception as e:
                print(f"[CLIENT] Error: {e}")
                self.connected = False
                self.running = False
            time.sleep(0.016)

    def stop(self):
        self.running = False
        self.client_socket.close()
