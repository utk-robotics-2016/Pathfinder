class EncoderFollowerConfig:
    def __init__(self):
        self.initial_position = 0
        self.ticks_per_revolution = 0
        self.wheel_circumference = 0.0
        self.kp = 0.0
        self.ki = 0.0
        self.kv = 0.0
        self.ka = 0.0


class EncoderFollower:
    def __init__(self, config):
        self.last_error = 0.0
        self.heading = 0.0
        self.output = 0.0
        self.segment = 0
        self.finished = 0
        self.config = config

    def follow(self, trajectory, encoder_tick):
        if(self.segment < len(trajectory)):
            distance_covered = (float(encoder_tick) - float(self.config.initial_position)) / float(self.config.ticks_per_revolution)
            distance_covered = distance_covered * self.config.wheel_circumference

            s = trajectory[self.segment]

            self.finished = 0
            error = s.position - distance_covered
            calculated_value = self.config.kp * error + self.config.kd * ((error - self.last_error) / s.dt) + (self.config.kv * s.velocity + self.config.ka * s.acceleration)
            self.last_error = error
            self.heading = s.heading
            self.output = calculated_value
            self.segment = self.segment + 1
            return calculated_value
        else:
            self.finished = 1
            self.output = 0.0
            last = trajectory[:-1]
            self.heading = last.heading
            return 0.0
