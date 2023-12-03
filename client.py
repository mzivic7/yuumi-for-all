import socket
import threading
import time
import configparser
import pyautogui
import pynput
import sys
import keyboard


pyautogui.PAUSE = 1e-9
pyautogui.FAILSAFE = False   # don't worry, there is failsafe key (Ctrl+C)


class Client():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.server_addr = config.get("Main", "server_address")
        self.server_port = config.getint("Main", "server_port")
        self.client_res = config.get("Main", "game_res").split(", ")
        if len(self.client_res) != 2:
            self.client_res = pyautogui.size()
        print(f"[!] Trying to connect to server at: {self.server_addr}:{self.server_port}")
        self.ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.ClientSocket.sendto("0".encode(), (self.server_addr, self.server_port))
        self.run = True
        self.enable = True
        self.data = [100 , 100, "", ""]


    def shutdown(self):
        self.run = False
        try:
            self.listener_keyboard.stop()
        except AttributeError:
            pass
        self.ClientSocket.close()
        print(f"[+] Disconnected.")
        sys.exit(0)


    def on_press(self, key):
        try:
            if key.char == chr(ord("C")-64):
                self.shutdown()
            if key.char == chr(ord("R")-64):
                self.enable = not self.enable
                if self.enable:
                    print(f"[+] Control enabled.")
                else:
                    print(f"[+] Control disabled.")
        except AttributeError:
            pass


    def receiver(self):
        while self.run:
            data_raw, address = self.ClientSocket.recvfrom(4096)
            self.data = data_raw.decode().split(", ")
            if not self.data:
                self.self.run = False
            if self.data == "quit":
                self.run = False


    def main(self):
        self.listener_keyboard = pynput.keyboard.Listener(on_press=self.on_press).start()
        data_raw, address = self.ClientSocket.recvfrom(4096)
        server_config = data_raw.decode().split(", ")
        res_mult_x = self.client_res[0] / int(server_config[0])
        res_mult_y = self.client_res[1] / int(server_config[1])
        receiver = threading.Thread(target=self.receiver, daemon=True).start()
        print(f"[+] Client connected to server at: {self.server_addr}:{self.server_port}")
        print(f"[!] Press Ctrl+C at any time to stop client and release controls.")
        print(f"[!] Press Ctrl+R at any time to toggle control.")
        while self.run:
            if self.enable:

                # MOUSE MOVE
                client_mouse_x = int(int(self.data[0]) * res_mult_x)
                client_mouse_y = int(int(self.data[1]) * res_mult_y)
                pyautogui.moveTo(client_mouse_x, client_mouse_y)

                # MOUSE CLICK
                click = self.data[2]
                if click:
                    if click == "1":
                        pyautogui.mouseDown()
                    if click == "2":
                        pyautogui.mouseUp()
                    if click == "3":
                        pyautogui.mouseDown(button='right')
                    if click == "4":
                        pyautogui.mouseUp(button='right')

                # KEYBOARD
                key = self.data[3]
                if key:
                    keyboard.press(key)
                    time.sleep(0.01)
                    keyboard.release(key)


if __name__ == "__main__":
    client = Client()
    client.main()
