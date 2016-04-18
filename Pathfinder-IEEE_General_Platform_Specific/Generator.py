from Structs.TrajectoryCandidate import TrajectoryCandidate
from Spline_Generator import Spline_Generator
from Spline_Generator import FitType
from TrajectoryPlanner import TrajectoryPlanner
from SplineUtils import SplineUtils


class Pathfinder_Generator:
    def __init__(self, path, config, fit_type=FitType.FIT_HERMITE_CUBIC):
        self.path = path
        self.config = config
        self.fit = Spline_Generator(fit_type)
        self.planner = TrajectoryPlanner(config)
        self.candidate = TrajectoryCandidate()
        self.candidate.length = self.planner.trajectory_length
        self.spline_utils = SplineUtils()

    def prepare(self):
        if(len(self.path) < 2):
            return -1

        total_length = 0
        for i in range(len(self.path) - 1):
            s = self.fit(self.path[i], self.path[i + 1])
            dist = self.spline_utils.get_arc_length(s, self.config.sample_count)
            self.candidate.spline_list.append(s)
            self.candidate.length_list.append(dist)
            total_length = total_length + dist

        self.config.src_theta = self.path[0].angle
        self.config.dest_theta = self.path[0].angle

        self.candidate.total_length = total_length
        self.candidate.path_length = len(self.path)
        self.candidate.config = self.config

        return 0

    def generate(self):
        trajectory_length = self.candidate.length
        path_length = self.candidate.path_length

        splines = self.candidate.spline_list

        spline_lengths = self.candidate.length_list

        segments = self.planner.create()

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
                    percentage = self.spline_utils.get_progress_for_distance(si, pos_relative, self.config.sample_count)
                    coords = self.spline_utils.get_coords(si, percentage)
                    segments[i].heading = self.spline_utils.get_angle(si, percentage)
                    segments[i].x = coords.x
                    segments[i].y = coords.y
                    found = 1
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
                    found = 1

        return segments
