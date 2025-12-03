# Test Plan – Real-Time Object Tracker & Video Annotator

## 1. Introduction
This test plan describes the testing strategy for verifying the functionality, performance, and correctness of the Real-Time Object Tracker & Video Annotator project.

The main components under test:
- Input handling (webcam and video files)
- YOLO-based object detection
- Frame annotation and drawing
- Output video generation
- Command-line interface arguments

---

## 2. Test Environment
- macOS (MacBook)
- Python 3.9+
- Virtual environment `.venv`
- Required packages from `requirements.txt`
- Test videos: `test.mp4`
- Webcam: built-in FaceTime HD Camera

---

## 3. Test Cases

### **3.1 Webcam Input Test**
**Procedure:**
1. Run: `python demo_tracker.py`
2. Move objects (your hand, face, items) in front of webcam.
3. Press `q` to quit.

**Expected Result:**
- Live window opens.
- YOLO detects and labels objects.
- Annotated video is saved as `annotated_output.mp4`.

---

### **3.2 Video File Input Test**
**Procedure:**
1. Run:  
   `python demo_tracker.py --input test.mp4 --output test_annotated.mp4`
2. Let the script finish.

**Expected Result:**
- File is processed frame-by-frame.
- Output video `test_annotated.mp4` contains bounding boxes and labels.
- No display window if `--no-display` is used.

---

### **3.3 CLI Argument Test**
**Procedure:**
Run the following variations:

1. Change confidence:  
   `python demo_tracker.py --conf 0.5`
2. Change classes:  
   `python demo_tracker.py --classes person`
3. Skip frames:  
   `python demo_tracker.py --frame-skip 2`

**Expected Result:**
- Script runs without errors.
- Behavior changes according to arguments.

---

### **3.4 Output Video Integrity Test**
**Procedure:**
- After running any mode, open the generated `.mp4` file using QuickTime.

**Expected Result:**
- Video plays smoothly.
- Bounding boxes and labels appear.

---

## 4. Pass/Fail Summary

| Test Case | Status |
|----------|--------|
| Webcam detection | PASS |
| Video file detection | PASS |
| CLI arguments | PASS |
| Output video saved | PASS |

---

## 5. Conclusion
The system passes all core functionality tests.  
It successfully detects and annotates objects using YOLO, handles multiple input types, and writes output video files reliably.
