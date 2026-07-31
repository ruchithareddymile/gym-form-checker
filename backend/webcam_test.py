from pose_utils import calculate_angle
from rep_counter import RepCounter
from database import SessionLocal
from models import WorkoutSession, RepLog
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

EXERCISES = {
    "elbow_curl": {
        "points": (12, 14, 16),   # shoulder, elbow, wrist
        "down_threshold": 90,
        "up_threshold": 160,
    },
    "squat": {
        "points": (23, 25, 27),   # left hip, left knee, left ankle
        "down_threshold": 100,
        "up_threshold": 160,
    },
}

exercise = EXERCISES["squat"]   # change this to "squat" to switch exercises
db = SessionLocal()

# Look up the matching Exercise row in the database by name
from models import Exercise
exercise_name = "squat"  # keep this in sync with EXERCISES key above
db_exercise = db.query(Exercise).filter(Exercise.name == exercise_name).first()

session = WorkoutSession(exercise_id=db_exercise.id)
db.add(session)
db.commit()
db.refresh(session)
print(f"Started workout session #{session.id}")

base_options = python.BaseOptions(model_asset_path='pose_landmarker.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO
)
landmarker = vision.PoseLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
frame_timestamp = 0
counter = RepCounter(down_threshold=exercise["down_threshold"], up_threshold=exercise["up_threshold"])

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

            p1_idx, p2_idx, p3_idx = exercise["points"]
            point_a = (landmarks[p1_idx].x, landmarks[p1_idx].y)
            point_b = (landmarks[p2_idx].x, landmarks[p2_idx].y)
            point_c = (landmarks[p3_idx].x, landmarks[p3_idx].y)

            angle = calculate_angle(point_a, point_b, point_c)
            result = counter.update(angle)
            print(f"Angle: {angle:.1f} | Reps: {result['count']}")

            if result["rep_completed"]:
                rep = RepLog(
                    session_id=session.id,
                    rep_number=result["count"],
                    min_angle=result["min_angle"],
                    max_angle=result["max_angle"],
                )
                db.add(rep)
                db.commit()
                print(f"  → Saved rep #{result['count']} to database")
    cv2.imshow("Webcam Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
db.close()