import socket
import threading
import time
import configparser
import pyautogui
import pynput
import sys


class Server():
    def __init__(self):
        print(f"[!] Starting server.")
        print(f"[!] Press Ctrl+C at any time to shutdown server")
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.local_addr = config.get("Main", "server_address")
        self.local_port = config.getint("Main", "server_port")
        self.loop_sleep = 1 / config.getint("Main", "tick")
        self.server_res = config.get("Main", "game_res").split(", ")
        if len(self.server_res) != 2:
            self.server_res = pyautogui.size()
        self.run = True
        self.pos = (0, 0)
        self.click = ""
        self.key = ""
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def shutdown(self):
        self.run = False
        self.shutdown_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.shutdown_socket.sendto("0".encode(), (self.local_addr, self.local_port))
        self.shutdown_socket.close()


    def on_move(self, x, y):
        self.pos = (x, y)
    
    
    def on_click(self, x, y, button, pressed):
        if button == pynput.mouse.Button.left:
            if pressed:
                self.click = "1"
            else:
                self.click = "2"
        elif button == pynput.mouse.Button.right:
            if pressed:
                self.click = "3"
            else:
                self.click = "4"


    def on_press(self, key):
        try:
            if key.char == chr(ord("C")-64):
                self.shutdown()
            else:
                self.key = key.char
        except AttributeError:
            pass


    def on_release(self, key):
        self.key = ""


    def client_thread(self, address):
        if self.run:
            print(f"[+] Client at address: {address[0]}:{address[1]} connected.")
            server_config = str(self.server_res[0]) + ", " + str(self.server_res[1])
            self.ServerSocket.sendto(server_config.encode('utf-8'), address)
        while self.run:
            data = str(self.pos[0]) + ", " + str(self.pos[1]) + ", " + self.click + ", " + self.key
            self.ServerSocket.sendto(data.encode('utf-8'), address)
            self.click = ""
            self.key = ""
            time.sleep(self.loop_sleep)
        self.ServerSocket.sendto("quit".encode('utf-8'), address)


    def main(self):
        try:
            self.ServerSocket.bind((self.local_addr, self.local_port))
        except Exception as e:
            print(str(e))
            self.ServerSocket.close()
            sys.exit()
        print(f"[!] Server is waiting for clients.")
        print(f"[+] Server address: {self.local_addr}:{self.local_port}")
        try:
            listener_mouse = pynput.mouse.Listener(on_move=self.on_move, on_click=self.on_click).start()
            listener_keyboard = pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release).start()
            while self.run:
                _, address = self.ServerSocket.recvfrom(1024)
                threading.Thread(target=self.client_thread, daemon=True, args=(address, )).start()
        finally:
            print(f"[!] Shutting down server.")
            try:
                listener_mouse.stop()
                listener_keyboard.stop()
            except AttributeError:
                pass
            self.ServerSocket.close()
            sys.exit(0)


if __name__ == "__main__":
    server = Server()
    server.main()
