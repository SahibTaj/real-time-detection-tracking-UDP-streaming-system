# Real-Time Object Detection, Multi-Object Tracking & UDP Video Streaming

## Project Overview

This project implements a complete real-time computer vision pipeline that performs object detection, multi-object tracking, and streams the processed video over UDP to a separate client application.

The goal of the system is to simulate a robotics/edge-AI perception pipeline where objects must be detected, tracked with persistent IDs, and transmitted across a network in real time with minimal latency.

The system runs entirely on standard CPU hardware while maintaining real-time performance.

## What We Built

The system has three main components:

1. Real-time object detection

2. Multi-object tracking with persistent IDs

3. UDP-based video streaming between server and client

The server detects and tracks objects from a webcam feed and streams the processed frames to a client application using UDP.
The client reconstructs the video stream and displays it in real time along with performance metrics.

## Why This Approach

This architecture mirrors real-world robotics and edge-AI systems where:

- detection must run on limited hardware

- objects must be tracked consistently

- video must be transmitted with low latency

- packet loss must be handled gracefully

UDP was chosen instead of TCP because real-time perception systems prioritize low latency over guaranteed delivery.

## System Architecture
    Camera → Detection → Tracking → Overlay → JPEG Compress → UDP Send → Client Receive → Display
## Server

- Captures webcam video

- Detects objects using a pretrained model

- Tracks objects with persistent IDs

- Draws bounding boxes, labels, trajectories

- Compresses frames to JPEG

- Splits frames into UDP packets

- Streams packets to client

## Client

- Receives UDP packets

- Reconstructs frames

- Decodes JPEG images

- Displays video in real time

- Shows FPS metrics

- Handles packet loss and frame drops

## Detection
### What we used

Model: YOLOv8n (pretrained COCO)

### Why

- Lightweight and fast on CPU

- Good balance between accuracy and speed

- Supports real-time inference without GPU

- Detects common real-world objects

### What it detects

- person

- chair

- laptop

- phone

- bottle

- backpack

- vehicle classes

At least 3 classes required → system detects many more.

### Performance

Runs in real time on CPU while maintaining required FPS.

## Tracking
### Algorithm used

ByteTrack

### Why

- Maintains stable IDs

- Handles occlusions well

- Lightweight and real-time capable

- Works well with YOLO detections

### What tracking provides

- Unique ID for each object

- ID persistence across frames

- Handles temporary occlusion

- Trajectory visualization

- Supports multiple objects simultaneously

System successfully tracks 5+ objects at once.

## UDP Streaming
### Why UDP

UDP is used in real-time systems because:

- lower latency than TCP

- no connection overhead

- suitable for live video

Packet loss is acceptable since new frames arrive quickly.

### Challenges

UDP has a maximum packet size of ~65KB.
Video frames are larger than this.

### Solution

Each frame is:

1. Compressed using JPEG

2. Split into smaller packets

3. Sent with metadata

4. Reconstructed on client

### Packet structure
    [frame_id | packet_id | total_packets | image_data]

This allows the client to rebuild frames correctly.

## Performance Optimizations

Several optimizations were used to maintain real-time performance on CPU:

- Lightweight YOLOv8n model

- Frame skipping for detection

- ByteTrack for fast tracking

- JPEG compression tuning

- Dropping old frames on client

- Efficient UDP packet handling

These ensure the system maintains required FPS.

## Performance Results
```
Metric	              |   Result
Server FPS	          |   ~60–90
Client FPS	          |   ~17–25
Required FPS          |   ≥15
Objects tracked	      |   5+ simultaneously
Latency	              |   Low
Tracking stability	  |   Stable
```
The system meets and exceeds the required performance threshold.

## Test Scenarios Covered

The system was tested under:

- Multiple objects in frame

- Objects entering and exiting frame

- Occlusion between objects

- Fast movement

- Slow movement

- Continuous streaming

All scenarios worked successfully.

## How to Run
### Install dependencies

    pip install -r requirements.txt
### Run server
    python stream_server.py
### Run client
    python stream_client.py

Run both simultaneously.

## Configuration Options

You can modify:

Detection:

- confidence threshold

- input resolution

- model type

Tracking:

- tracker parameters

- trajectory length

Streaming:

- JPEG quality

- UDP port

- packet size

## Design Decisions
### Model choice

YOLOv8n was selected because it provides strong performance on CPU without requiring GPU acceleration.

### Tracking choice

ByteTrack was chosen for its simplicity and strong ID persistence in real-time systems.

### UDP vs TCP

UDP provides lower latency, making it suitable for real-time video streaming. Packet loss is mitigated by sending continuous frames.

### Frame skipping

Detection does not need to run on every frame. Tracking fills gaps between detections, improving performance while keeping accuracy high.

## Future Improvements

- ROS integration

- Custom object training

- GPU acceleration

- Multi-camera support

- Web streaming interface

## Conclusion

This project demonstrates a complete real-time perception pipeline including detection, tracking, and network streaming.
The system meets all assignment requirements and performs reliably on standard hardware while maintaining real-time performance.

It reflects practical engineering decisions used in robotics and edge-AI systems.