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

## Configuration
### Detection

- Model: YOLOv8n (pretrained COCO)

- Runs on CPU

- Configurable confidence threshold

- Configurable resolution

### Tracking

- Algorithm: ByteTrack

- Maintains consistent IDs

- Handles occlusion

- Tracks 5+ objects simultaneously

### Streaming

- Protocol: UDP

- JPEG compression

- Packet size handling

- Frame reconstruction on client


## System Design

The goal of this project was to design a real-time perception pipeline capable of running on standard CPU hardware while maintaining low latency and stable tracking. For object detection, YOLOv8n was selected due to its strong balance between speed and accuracy on CPU. Larger models improve accuracy but significantly reduce FPS, while smaller models struggle with multi-object detection. YOLOv8n allows reliable detection of common COCO classes such as person, bottle, phone, and laptop while maintaining real-time inference.

For tracking, ByteTrack was chosen because of its robustness and ability to maintain consistent object identities across frames. Unlike simple IOU trackers, ByteTrack associates both high-confidence and low-confidence detections, allowing it to recover objects during occlusion and maintain trajectory continuity. This makes it well-suited for real-time multi-object tracking scenarios.

UDP was selected as the streaming protocol because it offers significantly lower latency than TCP, which is critical for real-time perception systems. Since UDP has a packet size limit, each frame is compressed using JPEG and fragmented into smaller packets. Each packet contains metadata including frame ID and packet index, allowing the client to reconstruct frames correctly. Old frames are dropped on the client to prevent lag buildup.

A key challenge was maintaining stable FPS while performing detection, tracking, and streaming simultaneously on CPU. This was solved by running detection periodically and using tracking between detection frames. Additional optimizations included JPEG compression tuning and packet buffering strategies. The final system consistently achieves real-time performance above the required FPS threshold.

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
