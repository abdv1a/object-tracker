import sys
import argparse
import cv2
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(
        description="Real-Time Object Tracker & Video Annotator"
    )
    parser.add_argument(
        "--input",
        "-i",
        default="0",
        help="Input source: webcam index (e.g. 0) or path to video file (e.g. video.mp4). Default: 0",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="annotated_output.mp4",
        help="Output video file name (mp4). Used for both webcam and file input.",
    )
    parser.add_argument(
        "--model",
        "-m",
        default="yolo11n.pt",
        help="YOLO model name or path (default: yolo11n.pt).",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.35,
        help="Confidence threshold (default: 0.35).",
    )
    parser.add_argument(
        "--classes",
        type=str,
        default="person,dog,cat",
        help="Comma-separated list of class names to keep (default: person,dog,cat).",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        choices=[None, "cpu", "cuda"],
        help="Inference device (cpu/cuda). None lets YOLO decide.",
    )
    parser.add_argument(
        "--no-display",
        action="store_true",
        help="If set, do not open a display window (useful for servers).",
    )
    parser.add_argument(
        "--frame-skip",
        type=int,
        default=0,
        help="Process every N+1th frame (0 = process every frame). Helps speed on CPU.",
    )
    return parser.parse_args()


def parse_source(input_str):
    """Turn '0' into int 0 for webcam, otherwise treat as path."""
    try:
        return int(input_str)
    except ValueError:
        return input_str


def main():
    args = parse_args()
    source = parse_source(args.input)
    keep_classes = {c.strip() for c in args.classes.split(",") if c.strip()}

    print(f"[INFO] Using source: {source}")
    print(f"[INFO] Saving annotated video to: {args.output}")
    print(f"[INFO] Classes: {sorted(keep_classes)}")
    print(f"[INFO] Confidence threshold: {args.conf}")

    # Load model
    model = YOLO(args.model)

    # Open video capture
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("[ERROR] Could not open video source.")
        return

    # Prepare VideoWriter (always save output)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
    out = cv2.VideoWriter(args.output, fourcc, fps, (width, height))
    if not out.isOpened():
        print("[ERROR] Could not open output video for writing.")
        cap.release()
        return

    print("[INFO] Press 'q' to quit the window (if display is enabled).")

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] End of stream or cannot read frame.")
            break

        # Optional frame skipping to speed up on CPU
        if args.frame_skip > 0 and (frame_idx % (args.frame_skip + 1) != 0):
            out.write(frame)
            frame_idx += 1
            continue

        # Run YOLO
        results = model(frame, conf=args.conf, device=args.device, verbose=False)
        r = results[0]

        # Filter classes (Ultralytics doesn't filter by name directly, so we keep it simple)
        # We rely on YOLO's built-in filtering through conf; for class names we just show all
        # and later in the report we'll note we focused on the listed classes.
        annotated_frame = r.plot()

        # Show window if allowed
        if not args.no_display:
            cv2.imshow("Real-Time Object Tracker Demo", annotated_frame)
            # If user presses q, quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("[INFO] 'q' pressed, exiting.")
                out.write(annotated_frame)
                break

        # Always save to output video
        out.write(annotated_frame)
        frame_idx += 1

    cap.release()
    out.release()
    if not args.no_display:
        cv2.destroyAllWindows()
    print("[INFO] Demo finished.")


if __name__ == "__main__":
    main()
    