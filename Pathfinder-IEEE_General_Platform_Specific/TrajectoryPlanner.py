from struct import TrajectoryInfo
from struct import Segment
import math


class TrajectoryPlanner:
    def __init__(self, config):
        self.config = config
        self.prepare()

    def prepare(self):
        max_a2 = self.config.max_a * self.config.max_a
        max_j2 = self.config.max_j * self.config.max_j

        checked_max_v = math.min(self.config.max_v, (-max_a2 + math.sqrt(max_a2 + 4 * max_j2 / (2 * self.config.max_j))))

        filter1 = int(math.ceil(checked_max_v / self.config.max_a))
        filter2 = int(math.ceil((self.config.max_a / self.config.max_j) / self.config.dt))

        impulse = (self.config.dest_pos / checked_max_v) / self.config.dt
        time = int(math.ceil(filter1 + filter2 + impulse))

        self.info = TrajectoryInfo(filter1, filter2, time, self.config.dt, 0, checked_max_v, impulse)

    def create(self):
        segments = self.plan_fromSecondOrderFilter()

        d_theta = self.config.dest_theta - self.config.src_theta
        for i in range(self.info.length):
            segments[i].heading = self.config.src_theta + d_theta * segments[i].position / (segments[self.info.length - 1].position)

        return segments

    def plan_fromSecondOrderFilter(self):
        last_section = Segment(self.info.dt, 0, 0, 0, self.info.u, 0, 0)

        f1_buffer = []
        f1_buffer.append((self.info.u / self.info.v) * self.info.filter_1_l)

        segments = []

        for i in range(len):
            input = math.min(self.info.impulse, 1)

            if input < 1:
                input = input - 1
                self.info.impulse = 0
            else:
                self.info.impulse = self.info.impulse - input

            f1_last = 0.0
            if i > 0:
                f1_last = f1_buffer[i - 1]
            else:
                f1_last = f1_buffer[0]

            if len(f1_buffer) > i + 1:
                f1_buffer.append(math.max(0.0, math.min(self.info.filter_1_l, f1_last + input)))
            else:
                f1_buffer[i] = math.max(0.0, math.min(self.info.filter_1_l, f1_last + input))

            f2 = 0.0

            for j in range(self.info.filter_2_l):
                if i - j < 0:
                    break
                f2 = f2 + f1_buffer[i - j]

            f2 = f2 / self.info.filter_1_l

            seg = Segment()
            seg.velocity = f2 / self.info.filter_2_l * self.info.v
            seg.position = (last_section.velocity + seg.velocity) / 2.0 * self.info.dt + last_section.position
            seg.x = seg.position
            seg.y = 0
            seg.acceleration = (seg.velocity - last_section.velocity) / self.info.dt
            seg.jerk = (seg.acceleration - last_section.acceleration) / self.info.dt
            seg.dt = self.info.dt

            segments.append(seg)

        last_section = seg

        return segments
