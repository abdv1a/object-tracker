[![Python CI](https://github.com/abdv1a/object-tracker/actions/workflows/python-tests.yml/badge.svg)](https://github.com/abdv1a/object-tracker/actions/workflows/python-tests.yml)

# Real-Time Object Tracker & Video Annotator

## Project Overview
This project implements a real-time object tracking and video annotation system using a pretrained YOLO model, OpenCV, and Python.

The program:

- Accepts webcam or video file input.  
- Runs object detection on each frame.  
- Draws bounding boxes and labels.  
- Saves an annotated `.mp4` video.  
- (Optional) Shows the detection window live.


---

## Requirements
Python packages (also in `requirements.txt`):

ultralytics==8.3.0
opencv-python==4.10.0.84
numpy<2


---

## Installation
```bash
cd object-tracker
python3 -m venv .venv
source .venv/bin/activate   # macOS
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
