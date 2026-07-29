from pose_utils import calculate_angle
from rep_counter import RepCounter
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

base_options = python.BaseOptions(model_asset_path='pose_landmarker.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO
)
landmarker = vision.PoseLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
frame_timestamp = 0
counter = RepCounter(down_threshold=90, up_threshold=160)

while True:
    success, frame = cap.read()
    if not success:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    result = landmarker.detect_for_video(mp_image, frame_timestamp)
    frame_timestamp += 1

    if result.pose_landmarks:
        for landmarks in result.pose_landmarks:
            for lm in landmarks:
                x = int(lm.x * frame.shape[1])
                y = int(lm.y * frame.shape[0])
                cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

            # NEW: calculate and print the right elbow angle
            shoulder = landmarks[12]
            elbow = landmarks[14]
            wrist = landmarks[16]

            shoulder_point = (shoulder.x, shoulder.y)
            elbow_point = (elbow.x, elbow.y)
            wrist_point = (wrist.x, wrist.y)

            angle = calculate_angle(shoulder_point, elbow_point, wrist_point)
            reps = counter.update(angle)
            print(f"Elbow angle: {angle:.1f} | Reps: {reps}")
    cv2.imshow("Webcam Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()