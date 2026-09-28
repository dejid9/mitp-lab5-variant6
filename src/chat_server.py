"""Многопоточный сервер локального чата на сокетах (TCP)."""

import socket
import threading
from typing import List

HOST = "127.0.0.1"
PORT = 9099


class ChatServer:
    """TCP сервер локального чата с поддержкой нескольких клиентов."""

    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        self.host = host
        self.port = port
        self.server_socket: socket.socket | None = None
        self.clients: List[socket.socket] = []
        self.running = False
        self._lock = threading.Lock()

    def start(self) -> None:
        """Запускает сервер чата."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"[СЕРВЕР ЧАТА] Запущен на {self.host}:{self.port}")

        while self.running:
            try:
                client_sock, addr = self.server_socket.accept()
                with self._lock:
                    self.clients.append(client_sock)
                print(f"[СЕРВЕР ЧАТА] Подключён клиент: {addr}")
                t = threading.Thread(
                    target=self._handle_client,
                    args=(client_sock,),
                    daemon=True
                )
                t.start()
            except OSError:
                break

    def broadcast(
        self,
        message: str,
        sender_socket: socket.socket | None = None
    ) -> None:
        """Рассылает сообщение всем активным клиентам."""
        encoded = message.encode("utf-8")
        with self._lock:
            disconnected = []
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.sendall(encoded)
                    except OSError:
                        disconnected.append(client)
            for d in disconnected:
                self.clients.remove(d)

    def _handle_client(self, client_sock: socket.socket) -> None:
        while self.running:
            try:
                data = client_sock.recv(4096)
                if not data:
                    break
                text = data.decode("utf-8")
                self.broadcast(text)
            except OSError:
                break
        with self._lock:
            if client_sock in self.clients:
                self.clients.remove(client_sock)
        client_sock.close()

    def stop(self) -> None:
        """Останавливает сервер чата."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        with self._lock:
            for c in self.clients:
                try:
                    c.close()
                except OSError:
                    pass
            self.clients.clear()


if __name__ == "__main__":
    server = ChatServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
        print("\n[СЕРВЕР ЧАТА] Остановлен.")
