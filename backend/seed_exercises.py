from database import SessionLocal
from models import Exercise

db = SessionLocal()

exercises = [
    Exercise(
        name="elbow_curl",
        display_name="Elbow Curl",
        points=[12, 14, 16],
        down_threshold=90,
        up_threshold=160,
    ),
    Exercise(
        name="squat",
        display_name="Squat",
        points=[23, 25, 27],
        down_threshold=100,
        up_threshold=160,
    ),
]

for ex in exercises:
    db.add(ex)

db.commit()
print("✅ Exercises added to database!")

db.close()