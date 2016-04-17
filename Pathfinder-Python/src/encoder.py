class EncoderConfig:
    def __init__(self):
        self.initial_position = 0
        self.ticks_per_revolution = 0
        self.wheel_circumference = 0.0
        self.kp = 0.0
        self.ki = 0.0
        self.kd = 0.0
        self.kv = 0.0
        self.ka = 0.0


class EncoderFollower:
    def __init__(self):
        self.last_error = 0.0
        self.heading = 0.0
        self.output = 0.0
        self.segment = 0
        self.finished = 0


def pathfinder_follow_encoder(c, follower, trajectory, trajectory_length, encoder_tick):
    segment = follower.segment
    if(segment >= trajectory_length):
        follower.finished = 1
        follower.output = 0.0
        last = trajectory[trajectory_length - 1]
        follower.heading = last.heading
        return 0.0
    else:
        return pathfinder_follow_encoder2(c, follower, trajectory[segment], trajectory_length, encoder_tick)


def pathfinder_follow_encoder2(c, follower, s, trajectory_length, encoder_tick):
    distance_covered = (float(encoder_tick) - float(c.initial_position)) / float(c.ticks_per_revolution)
    distance_covered = distance_covered * c.wheel_circumference

    if(follower.segment < trajectory_length):
        follower.finished = 0
        error = s.position - distance_covered
        calculated_value = c.kp * error + c.kd * ((error - follower.last_error) / s.dt) + (c.kv * s.velocity + c.ka * s.acceleration)
        follower.last_error = error
        follower.heading = s.heading
        follower.output = calculated_value
        follower.segment = follower.segment + 1
        return calculated_value
    else:
        follower.finished = 1
        return 0.0
