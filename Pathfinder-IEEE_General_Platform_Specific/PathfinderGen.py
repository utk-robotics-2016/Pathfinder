#includes
import argparse
import json
import os
from Structs import TrajectoryConfig
from Structs import Waypoint
from Generator import Pathfinder_Generator

# Collect command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="Path to the config file")
ap.add_argument("-o", "--output", required=False, help="Path to the output file that contains the trajectory")
args = vars(ap.parse_args())

# Set up the input and out files
fi = open(args["input"], "r")

if args['output'] is not None:
    fo = open(args["output"], "w")
else:
    dot = args["input"].find(".")
    fo_prefix = args["input"][:dot]
    if not os.path.exists(fo_prefix):
        os.makedirs(fo_prefix)
    fo = open("%s_trajectory.csv" % (fo_prefix), "w")

# Read in json
file_text = ""
for line in fi:
    file_text = file_text + line
json_data = json.loads(file_text)

trajectory_config = json_data['trajectory_config']

config = TrajectoryConfig()
config.max_v = trajectory_config['max_velocity']
config.max_a = trajectory_config['max_acceleration']
config.max_j = trajectory_config['max_jerk']
config.dt = trajectory_config['dt']
config.sample_count = trajectory_config['sample_count']

waypoints_config = json_data['waypoints']

waypoints = []

for json_item in waypoints_config:
    waypoints.append(Waypoint(json_item['x'], json_item['y'], json_item['angle']))

trajectory_segments = Pathfinder_Generator(waypoints, config)

for segment in trajectory_segments:
    fo.write("%f %f %f %f %f %f %f %f\n" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading))
