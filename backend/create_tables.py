from database import Base, engine
import models  # needed so the table classes register with Base, even though we don't call anything from it directly

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")