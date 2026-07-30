import numpy as np

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(cosine_angle))

    return float(angle)   # CHANGED: convert numpy float64 to plain Python float
if __name__ == "__main__":
    # Straight line test: hip-knee-ankle all in a vertical line = should be ~180°
    straight = calculate_angle((0, 0), (0, 1), (0, 2))
    print(f"Straight leg angle: {straight}")  # expect ~180

    # Right-angle bend test: should be ~90°
    bent = calculate_angle((0, 0), (0, 1), (1, 1))
    print(f"Bent leg angle: {bent}")  # expect ~90