from struct import *
from trajectory import *


def pathfinder_prepare(path, path_length, fit_type, sample_count, dt, max_velocity, max_acceleration, max_jerk, candidate):

    if(path_length < 2):
        return -1

    total_length = 0
    for i in range(path_length - 1):
        s = Spline()
        if fit_type == FitType.FIT_HERMITE_CUBIC:
            pf_fit_hermite_cubic(path[i], path[i+1], s)
        elif fit_type == FitType.FIT_HERMITE_QUINTIC:
            pf_fit_hermite_quintic(path[i], path[i+1], s)
        dist = pf_spline_distance(s, sample_count)
        candidate.spline_list[i] = s
        candidate.length_list[i] = dist
        total_length = tota_length + dist

    config = TrajectoryConfig()
    config.dt = dt
    config.max_velocity = max_velocity
    config.max_acceleration = max_acceleration
    config.max_jerk = max_jerk
    config.src_theta = path[0].angle
    config.dest_theta = path[0].angle
    config.sample_count = sample_count
    trajectory_length = info.length

    candidate.total_length = total_length
    candidate.length = trajectory_length
    candidate.path_length = path_length
    candidate.info = info
    candidate.config = config

    return 0


def pathfinder_generate(candidate, segments):
    trajectory_length = candidate.length
    path_length = candidate.path_length

    splines = candidate.spline_list

    spline_lengths = candidate.length_list

    pf_trajectory_create(candidate.info, candidate.config, segments)

    spline_i = 0
    spline_pos_initial = 0.0
    spline_complete = 0.0

    for i in range(trajectory_length):
        pos = segments[i].position

        found = 0
        while not found:
            pos_relative = pos - spline_pos_initial
            if(pos_relative <= spline_lengths[i]):
                si = splines[spline_i]
                percentage = pf_spline_progress_for_distance(si, pos_relative, candidate.config.sample_count)
                coords = pf_spline_coords(si, percentage)
                segments[i].heading = pf_spline_angle(si, percentage)
                segments[i].x = coords.x
                segments[i].y = coords.y
                found = 1
            elif spline_i < path_length - 2:
                spline_complete = spline_complete + spline_lengths[spline_i]
                spline_pos_initial = spline_complete
                spline_i = spline_i + 1
            else:
                si = splines[path_length - 2]
                segments[i].heading = pf_spline_angle(si, 1.0)
                coords = pf_spline_coords(si, 1.0)
                segments[i].x = coords.x
                segments[i].y = coords.y
                found = 1

    return trajectory_length
