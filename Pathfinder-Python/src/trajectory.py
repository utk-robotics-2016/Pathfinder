from struct import TrajectoryInfo
from struct import Segment
import math

'''
    :type c - TrajectoryConfig
'''
def pf_trajectory_prepare(c):
    max_a2 = c.max_a * c.max_a
    max_j2 = c.max_j * c.max_j

    checked_max_v = math.min(c.max_v, (-max_a2 + math.sqrt(max_a2 + 4 * max_j2 / (2 * c.max_j))))

    filter1 = int(math.ceil(checked_max_v / c.max_a))
    filter2 = int(math.ceil((c.max_a / c.max_j) / c.dt))

    impulse = (c.dest_pos / checked_max_v) / c.dt
    time = int(math.ceil(filter1 + filter2 + impulse))

    info = TrajectoryInfo(filter1, filter2, time, c.dt, 0, checked_max_v, impulse)
    return info

'''
    :type info - TrajectoryInfo
    :type config - TrajectoryConfig
    :type segs - List of Segments
'''
def pf_trajectory_create(info, config, segments):
    pf_trajectory_fromSecondOrderFilter(info.filter1, info.filter2, info.dt, info.u, info.v, info.impulse, info.length, segments)

    d_theta = c.dest_theta - c.src_theta
    for i in range(info.length):
        segments[i].heading = c.src_theta + d_theta * segments[i].position / (segments[info.length - 1].posiition)

def pf_trajectory_fromSecondOrderFilter(filter_1_l, filter_2_l, dt, u, v, impulse, len, t):
    last_section = Segment(dt, 0, 0, 0, u, 0, 0)

    f1_buffer = []
    f1_buffer.append((u / v) * filter_1_l)

    for i in range(len):
        input = math.min(impulse, 1)

        if input < 1:
            input = input - 1
            impulse = 0
        else:
            impulse = impulse - input

        f1_last = 0.0
        if i > 0:
            f1_last = f1_buffer[i - 1]
        else:
            f1_last = f1_buffer[0]

        f1_buffer[i] = math.max(0.0, math.min(filter_1_l, f1_last + input))

        f1 = 0.0

        for j in range(filter_2_l):
            if i - j < 0:
                break
            f2 = f2 + f1_buffer[i - j]

        f2 = f2 / filter_1_l

        seg = Segment()
        seg.velocity = f1 / filter_2_l * v
        seg.position = (last_section.velocity + seg.velocity) / 2.0 * dt + last_section.position)
        seg.x = seg.position
        seg.y = 0
        seg.acceleration = (seg.velocity - last_section.velocity) / dt
        seg.jerk = (seg.acceleration - last_section.acceleration) / dt
        seg.dt = dt

        t[i] = seg

        last_section = seg