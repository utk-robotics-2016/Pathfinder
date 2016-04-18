class DistanceFollowerConfig:
    def __init(self):
        self.kp = 0.0
        self.ki = 0.0
        self.kd = 0.0
        self.kv = 0.0
        self.ka = 0.0


class DistanceFollower:
    def __init__(self, config):
        self.last_error = 0.0
        self.heading = 0.0
        self.output = 0.0
        self.segment = 0
        self.finished = 0
        self.config = config

    def follow(self, trajectory, distance):
        if(self.segment < len(trajectory)):
            s = trajectory[self.segment]
            self.finished = 0
            error = s.position - distance
            calculated_value = self.config.kp * error + self.config.kd * ((error - self.last_error) / s.dt) + (self.config.kv * s.velocity + self.config.ka * s.acceleration)

            self.last_error = error
            self.heading = s.heading
            self.output = calculated_value
            self.segment = self.segment + 1
        else:
            self.finished = 1
            self.output = 0.0
            last = trajectory[:-1]
            self.heading = last.heading
            return 0.0