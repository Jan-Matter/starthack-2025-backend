from typing import Dict
import socket
import time
import threading

from logging import Logger
from controllers.transcriber import Transcriber
from api.constants import LoggingMessages


class AudioRecv:

    def __init__(self,
            transcriber: Transcriber,
            logger: Logger,
            transcription_buffer: Dict,
            config : Dict
        ) -> None:
        self._transcriber = transcriber
        self._logger = logger
        self._audio_buffer = b""
        self._buffer_time = config["buffer_time"]
        self._transcription_buffer = transcription_buffer


    def add_socket_port(self, port) -> None:
        self._socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket_connection.bind(("0.0.0.0", port))
        self._socket_connection.listen(1)
        self._logger.info(LoggingMessages.SOCKET_LISTENING.value + str(port))

        

        # Start a thread to handle the client connection
        threading.Thread(target=self.handle_client_connection, daemon=True).start()
    
    def handle_client_connection(self):
            conn, addr = self._socket_connection.accept()
            self._logger.info(f"Connection established with {addr}")
            timer = time.time()
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                self._audio_buffer += data
                if time.time() - timer > self._buffer_time:
                    self._transcription_buffer["audio"] = self._audio_buffer
                    self._audio_buffer = b""
                    timer = time.time()
