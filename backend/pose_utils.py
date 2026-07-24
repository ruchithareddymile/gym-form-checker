import numpy as np

def calculate_angle(a, b, c):
    a = np.array(a)  # first point
    b = np.array(b)  # middle point (the vertex - where we measure the angle)
    c = np.array(c)  # third point

    ba = a - b  # vector from b to a
    bc = c - b  # vector from b to c

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(cosine_angle))

    return angle
if __name__ == "__main__":
    # Straight line test: hip-knee-ankle all in a vertical line = should be ~180°
    straight = calculate_angle((0, 0), (0, 1), (0, 2))
    print(f"Straight leg angle: {straight}")  # expect ~180

    # Right-angle bend test: should be ~90°
    bent = calculate_angle((0, 0), (0, 1), (1, 1))
    print(f"Bent leg angle: {bent}")  # expect ~90