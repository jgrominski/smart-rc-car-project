import socket
import sys

import cv2
import pygame
from pygame.locals import *

RTSP_URL = "rtsp://192.168.1.103:8000/stream"


class App:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("RC Car Control App")
        self.screen = pygame.display.set_mode((960, 720))
        self.clock = pygame.time.Clock()
        self.fps = 30

        self.main_loop()

    def main_loop(self):
        cap = cv2.VideoCapture(RTSP_URL)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    break

            drive_motor = 0
            turn_motor = 90

            keys = pygame.key.get_pressed()

            if keys[K_UP]:
                drive_motor += 255
            if keys[K_DOWN]:
                drive_motor -= 255
            if keys[K_RIGHT]:
                turn_motor += 30
            if keys[K_LEFT]:
                turn_motor -= 30

            drive_cmd = ("F" if drive_motor > 0 else "B") + str(-drive_motor)
            turn_cmd = "T" + str(turn_motor)
            cmd = drive_cmd + " " + turn_cmd

            sock.sendto(cmd.encode("utf-8"), ("192.168.1.103", 8080))

            ret, frame = cap.read()
            if not ret:
                print("Error: No frame found")
                break

            frame_to_surface = pygame.surfarray.make_surface(frame)
            pygame.transform.scale(frame_to_surface, (960, 720), self.screen)

            pygame.display.flip()
            self.clock.tick(self.fps)

        sock.sendto("S".encode("utf-8"), ("192.168.1.103", 8080))
        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    print("Client: Starting RTSP stream reception...")
    app = App()
    print("Client: RTSP stream reception ended.")
