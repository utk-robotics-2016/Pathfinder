class Waypoint:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0


class Spline:
    def __init__(self):
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0
        self.d = 0.0
        self.e = 0.0
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.angle_offset = 0.0
        self.knot_distance = 0.0
        self.arc_length = 0.0


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment:
    def __init__(self):
        self.dt = 0.0
        self.x = 0.0
        self.y = 0.0
        self.position = 0.0
        self.velocity = 0.0
        self.acceleration = 0.0
        self.jerk = 0.0
        self.heading = 0.0


class TrajectoryConfig:
    def __init__(self):
        self.dt = 0.0
        self.max_v = 0.0
        self.max_a = 0.0
        self.max_j = 0.0
        self.src_v = 0.0
        self.src_theta = 0.0
        self.dest_pos = 0.0
        self.dest_v = 0.0
        self.dest_theta = 0.0
        self.sample_count = 0


class TrajectoryInfo:
    def __init__(self, filter1, filter2, length, dt, u, v, impulse):
        self.filter1 = filter1
        self.filter2 = filter2
        self.length = length
        self.dt = dt
        self.u = u
        self.v = v
        self.impulse = impulse


class TrajectoryCandidate:
    def __init__(self):
        self.spline_list = []
        self.length_list = []
        self.total_length = 0.0
        self.length = 0
        self.path_length = 0
        self.info = TrajectoryInfo()
        self.config = TrajectoryConfig()
