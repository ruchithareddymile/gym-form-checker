class RepCounter:
    def __init__(self, down_threshold, up_threshold):
        self.down_threshold = down_threshold
        self.up_threshold = up_threshold
        self.state = "up"
        self.count = 0
        self.min_angle = None
        self.max_angle = None

    def update(self, angle):
        if self.min_angle is None or angle < self.min_angle:
            self.min_angle = angle
        if self.max_angle is None or angle > self.max_angle:
            self.max_angle = angle

        rep_completed = False

        if angle < self.down_threshold and self.state == "up":
            self.state = "down"
        elif angle > self.up_threshold and self.state == "down":
            self.state = "up"
            self.count += 1
            rep_completed = True

        result = {
            "count": self.count,
            "rep_completed": rep_completed,
            "min_angle": self.min_angle,
            "max_angle": self.max_angle,
        }

        if rep_completed:
            # reset tracking for the next rep
            self.min_angle = None
            self.max_angle = None

        return result