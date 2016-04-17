class FollowerConfig:
    def __init__(self):
        self.kp = 0.0
        self.ki = 0.0
        self.kd = 0.0
        self.kv = 0.0
        self.ka = 0.0


class DistanceFollower:
    def __init__(self):
        self.last_error = 0.0
        self.heading = 0.0
        self.output = 0.0
        self.segment = 0
        self.finished = 0


def path_finder_follow_distance(c, follower, trajectory, trajectory_length, distance):
    segment = follower.segment
    if(segment >= trajectory_length):
        follower.finished = 1
        follower.output = 0.0
        last = trajectory[trajectory_length - 1]
        follower.heading = last.heading
        return 0.0
    else:
        return path_finder_follow_distance2(c, follower, trajectory[segment], trajectory_length, distance)


def path_finder_follow_distance2(c, follower, s, trajectory_length, distance):
    if(follower.segment < trajectory_length):
        follower.finished = 0
        error = s.position - distance
        calculated_value = c.kp * error + c.kd * ((error - follower.last_error) / s.dt) + (c.kv * s.velocity + c.ka * s.acceleration)

        follower.last_error = error
        follower.heading = s.heading
        follower.output = calculated_value
        follower.segement = follower.segment + 1
        return calculated_value
    else:
        follower.finished = 1
        return 0.0
