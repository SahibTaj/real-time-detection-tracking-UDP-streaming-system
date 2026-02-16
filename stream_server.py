import cv2
import socket
import struct
import time
import numpy as np
from ultralytics import YOLO
import supervision as sv

# ================= UDP =================
UDP_IP = "127.0.0.1"
UDP_PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ================= MODEL =================
model = YOLO("yolov8n.pt")
tracker = sv.ByteTrack()

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator(thickness=2, trace_length=30)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

frame_id = 0
frame_count = 0
last_detections = None

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # run detection every 3 frames (keeps FPS high)
    if frame_count % 3 == 0:
        results = model(frame, imgsz=640, conf=0.15, iou=0.5, verbose=False)[0]

        if len(results.boxes) > 0:
            xyxy = results.boxes.xyxy.cpu().numpy()
            confs = results.boxes.conf.cpu().numpy()
            cls = results.boxes.cls.cpu().numpy().astype(int)

            last_detections = sv.Detections(
                xyxy=xyxy,
                confidence=confs,
                class_id=cls
            )

    detections = last_detections

    if detections is not None:
        detections = tracker.update_with_detections(detections)

        labels = [
            f"ID:{tid} {conf:.2f}"
            for tid, conf in zip(
                detections.tracker_id,
                detections.confidence
            )
        ]

        frame = box_annotator.annotate(frame, detections)
        frame = label_annotator.annotate(frame, detections, labels)
        frame = trace_annotator.annotate(frame, detections)

    # FPS display
    fps = 1 / (time.time() - prev_time)
    prev_time = time.time()

    cv2.rectangle(frame, (5,5), (150,40), (0,0,0), -1)
    cv2.putText(frame, f"FPS: {fps:.1f}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)

    # ================= UDP SEND =================
    _, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    data = buffer.tobytes()

    max_packet = 60000
    num_packets = int(np.ceil(len(data) / max_packet))

    for i in range(num_packets):
        start = i * max_packet
        end = start + max_packet
        chunk = data[start:end]

        header = struct.pack("HHH", frame_id, i, num_packets)
        sock.sendto(header + chunk, (UDP_IP, UDP_PORT))

    frame_id += 1

    cv2.imshow("SERVER", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()