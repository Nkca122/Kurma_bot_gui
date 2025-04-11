from ultralytics import YOLO
import numpy as np
import cv2

class Detector():
    object_detector = YOLO("yolov8n.pt")
    segmentor = YOLO("yolov8n-seg.pt")
    pose_detector = YOLO("yolov8n-pose.pt")

    detector_dict = {
        "none" : None,
        "detection" : object_detector,
        "segmentation" : segmentor,
        "pose detection": pose_detector
    }

    def __init__(self):
        self.colors = {}

    def predict(self, frame, mode):
        detector_mode = Detector.detector_dict[mode]
        if mode != "segmentation":
            self.colors = {}

        if detector_mode:
            if mode == "detection":
                detection = detector_mode
                results = detection.predict(frame)

                if results:
                    for res in results:
                        for box in res.boxes:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])

                            conf = box.conf[0].item()
                            objcls = box.cls[0].item()

                            label = f"{detection.names[objcls]}, {conf:.2f}"

                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                return frame, results
            elif mode == "segmentation":
                segmenatation = detector_mode
                results = segmenatation.predict(frame, conf=0.7)

                if results:
                    for res in results:
                         for idx, mask in enumerate(res.masks.data):
                            mask = mask.cpu().numpy()
                            mask = (mask*255).astype(np.uint8)
                            mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

                            cls = int(res.boxes.cls[idx]) 
                            obj_key = f"{cls}{idx}"

                            if obj_key not in self.colors:
                                color = np.random.randint(0, 255, (3,), dtype=np.uint8)
                                self.colors[obj_key] = color

                            colored_mask = np.zeros_like(frame, dtype=np.uint8)
                            for c in range(3):
                                colored_mask[:, :, c] = np.where(mask > 128, self.colors[obj_key][c], 0)

                            frame = cv2.addWeighted(frame, 1, colored_mask, 1, 1)
                                        
                return frame, results
            elif mode == "pose detection":
                pose_detector = detector_mode
                results = pose_detector.predict(frame, conf=0.7)

                if results:
                    for res in results:
                        for idx, keypoints in enumerate(res.keypoints.data):
                            keypoints = keypoints.cpu().numpy() 
                            for kp in keypoints:
                                x, y, conf = int(kp[0]), int(kp[1]), kp[2] 
                                if conf > 0.7:  
                                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                            # Skeleton
                            skeleton_pairs = [
                                (0, 1), (0, 2), (1,3), (2, 4), # Facial Muscles
                                (5, 6), (11, 12), # Torso 
                                (5, 7), (7, 9), # Left Arm 
                                (6, 8), (8, 10), # Right Arm 
                                (11, 13), (13, 15), # Left Leg
                                (12, 14), (14, 16), # Right Leg
                            ]

                            for (p1, p2) in skeleton_pairs:
                                if keypoints[p1][2] > 0.7 and keypoints[p2][2] > 0.7:  # Check confidence
                                    x1, y1 = int(keypoints[p1][0]), int(keypoints[p1][1])
                                    x2, y2 = int(keypoints[p2][0]), int(keypoints[p2][1])
                                    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draw skeleton line

                    return frame, results
        else:
            return frame, None
