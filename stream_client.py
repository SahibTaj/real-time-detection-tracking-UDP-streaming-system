import socket
import struct
import cv2
import numpy as np
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

frame_buffer = {}
last_displayed_frame = -1

fps_time = time.time()
frame_counter = 0
display_fps = 0

while True:
    packet, _ = sock.recvfrom(65535)

    header = packet[:6]
    frame_id, packet_id, total_packets = struct.unpack("HHH", header)
    data = packet[6:]

    if frame_id not in frame_buffer:
        frame_buffer[frame_id] = [None] * total_packets

    frame_buffer[frame_id][packet_id] = data

    # If full frame received
    if all(p is not None for p in frame_buffer[frame_id]):

        frame_data = b''.join(frame_buffer[frame_id])
        del frame_buffer[frame_id]

        # Drop old frames (avoid lag buildup)
        if frame_id < last_displayed_frame:
            continue
        last_displayed_frame = frame_id

        img = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), 1)
        if img is None:
            continue

        display = img.copy()

        # FPS calculation (stable)
        frame_counter += 1
        if frame_counter >= 10:
            now = time.time()
            display_fps = frame_counter / (now - fps_time)
            fps_time = now
            frame_counter = 0

        # Clean text background
        cv2.rectangle(display, (5, 5), (220, 40), (0, 0, 0), -1)

        cv2.putText(
            display,
            f"Client FPS: {display_fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

        cv2.imshow("CLIENT", display)

        if cv2.waitKey(1) == 27:
            break