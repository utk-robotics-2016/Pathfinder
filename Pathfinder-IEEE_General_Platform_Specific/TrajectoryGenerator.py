from Structs.Trajectory import Trajectory
from Spline_Generator import Spline_Generator
from Spline_Generator import FitType
from TrajectoryPlanner import TrajectoryPlanner
from SplineUtils import SplineUtils


class TrajectoryGenerator:
    def __init__(self, path, config, fit_type=FitType.FIT_HERMITE_CUBIC):
        self.path = path
        self.config = config
        self.fit = Spline_Generator(fit_type)
        self.planner = TrajectoryPlanner(config)
        self.trajectory = Trajectory()
        self.trajectory.length = self.planner.trajectory_length
        self.spline_utils = SplineUtils()

    def prepare(self):
        if(len(self.path) < 2):
            return -1

        total_length = 0
        for i in range(len(self.path) - 1):
            s = self.fit(self.path[i], self.path[i + 1])
            dist = self.spline_utils.get_arc_length(s, self.config.sample_count)
            self.trajectory.spline_list.append(s)
            self.trajectory.length_list.append(dist)
            total_length = total_length + dist

        self.config.src_theta = self.path[0].angle
        self.config.dest_theta = self.path[0].angle

        self.trajectory.total_length = total_length
        self.trajectory.path_length = len(self.path)
        self.trajectory.config = self.config

        return 0

    def generate(self):
        trajectory_length = self.trajectory.length
        path_length = self.trajectory.path_length

        splines = self.trajectory.spline_list

        spline_lengths = self.trajectory.length_list

        segments = self.planner.create()

        spline_i = 0
        spline_pos_initial = 0.0
        spline_complete = 0.0

        for i in range(trajectory_length):
            pos = segments[i].position

            while True:
                pos_relative = pos - spline_pos_initial
                if(pos_relative <= spline_lengths[i]):
                    si = splines[spline_i]
                    percentage = self.spline_utils.get_progress_for_distance(si, pos_relative, self.config.sample_count)
                    coords = self.spline_utils.get_coords(si, percentage)
                    segments[i].heading = self.spline_utils.get_angle(si, percentage)
                    segments[i].x = coords.x
                    segments[i].y = coords.y
                    break
                elif spline_i < path_length - 2:
                    spline_complete = spline_complete + spline_lengths[spline_i]
                    spline_pos_initial = spline_complete
                    spline_i = spline_i + 1
                else:
                    si = splines[path_length - 2]
                    segments[i].heading = self.spline_utils.get_angle(si, 1.0)
                    coords = self.spline_utils.get_coords(si, 1.0)
                    segments[i].x = coords.x
                    segments[i].y = coords.y
                    break

        return segments
