class RepCounter:
    def __init__(self, down_threshold, up_threshold):
        self.down_threshold = down_threshold
        self.up_threshold = up_threshold
        self.state = "up"
        self.count = 0

    def update(self, angle):
        if angle < self.down_threshold and self.state == "up":
            self.state = "down"
        elif angle > self.up_threshold and self.state == "down":
            self.state = "up"
            self.count += 1
        return self.count