#includes
import argparse
import json
import os
from struct import *
from enums import *

# Collect command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="Path to the config file for the waypoints")
ap.add_argument("-o", "--output", required=False, help="Path to the output file that is the config for the trajectory")
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
    fo = open("%s_trajectory.json" % (fo_prefix), "w")

# Read in json
file_text = ""
for line in fi:
    file_text = file_text + line
json_data = json.loads(file_text)

json_config = json_data['Trajectory_Config']

config = TrajectoryConfig()
config.max_v = json_config['max_velocity']
config.max_a = json_config['max_acceleration']
config.max_j = json_config['max_jerk']
config.dt = json_config['dt']
config.sample_count = json_config['sample_count']

waypoints = []

for json_item in json_data:
    waypoints.append(Waypoint(json_item['x'], json_item['y'], json_item['angle']))

trajectory = Pathfinder_Generator(waypoints, config)
