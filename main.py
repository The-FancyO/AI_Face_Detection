import time
import cv2 as cv
import mediapipe as mp
import numpy as np

mp_face_detection = mp.solutions.face_detection
cap = cv.VideoCapture(1)
with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5
) as face_detector:
    frame_counter = 0
    fonts = cv.FONT_HERSHEY_PLAIN
    start_time = time.time()
    while True:
        frame_counter += 1
        ret, frame = cap.read()
        if ret is False:
            break
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        results = face_detector.process(rgb_frame)
        frame_height, frame_width, c = frame.shape
        if results.detections:
            for face in results.detections:
                face_react = np.multiply(
                    [
                        face.location_data.relative_bounding_box.xmin,
                        face.location_data.relative_bounding_box.ymin,
                        face.location_data.relative_bounding_box.width,
                        face.location_data.relative_bounding_box.height,
                    ],
                    [frame_width, frame_height, frame_width, frame_height],
                ).astype(int)

                cv.rectangle(frame, face_react, color=(255, 0, 255), thickness=1)
                key_points = np.array(
                    [(p.x, p.y) for p in face.location_data.relative_keypoints]
                )
                key_points_coords = np.multiply(
                    key_points, [frame_width, frame_height]
                ).astype(int)
                for p in key_points_coords:
                    cv.circle(frame, p, 4, (255, 255, 0), 1)
                    cv.circle(frame, p, 2, (0, 0, 0), -1)

        fps = frame_counter / (time.time() - start_time)
        cv.imshow("frame", frame)
        key = cv.waitKey(1)
        if key == ord("q"):
            break
    cap.release()
    cv.destroyAllWindows()
