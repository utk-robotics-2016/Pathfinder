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

waypoints = []

for json_item in json_data:
    waypoints.append(Waypoint(json_item['x'], json_item['y'], json_item['angle']))

candidate = TrajectoryCandidate()
pathfinder_prepare(waypoints, len(waypoints), FitType.FIT_HERMITE_CUBIC, 20, .2, 25, 10, 60, candidate)

trajectory = []

pathfinder_generate(candidate, trajectory)

leftTrajectory = []
rightTrajectory = []

wheelbase_width = 0.6

pathfinder_modify_tank(trajectory, candidate.length, leftTrajectory, rightTrajectory, wheelbase_width)

print leftTrajectory
print rightTrajectory
