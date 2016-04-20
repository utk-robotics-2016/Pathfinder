#includes
import argparse
import json
import sys
from Structs import TrajectoryConfig
from Structs import Waypoint
from TrajectoryGenerator import TrajectoryGenerator
from SwerveModifier import SwerveModifier
from TankModifier import TankModifier

# Collect command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=False, help="Path to the config file")
ap.add_argument("-w", "--waypoints", required=False, help="Path to the waypoints file")
ap.add_argument("-o", "--output", required=False, help="Path to the output file that contains the trajectory")
args = vars(ap.parse_args())

# Set up the input and out files
if args['config'] is not None:
    try:
        config_file = open(args['config'], "r")
    except:
        print "Config file: %s does not exist" % args['config']
        sys.exit()
else:
    try:
        config_file = open("pathplanning_robot_config.json", "r")
    except:
        print "Config file: pathplanning_robot_config.json does not exist"
        sys.exit()

if args['waypoints'] is not None:
    try:
        waypoints_file = open(args['waypoints'], "r")
    except:
        print "Waypoints file: %s does not exist" % args['waypoints']
        sys.exit()
else:
    try:
        waypoints_file = open("waypoints.json", "r")
    except:
        print "Waypoints file: waypoints.json does not exist"
        sys.exit()

if args['output'] is not None:
    output_file = open(args['output'], "w")
else:
    output_file = open("trajectory.json", "w")

# Read in json
file_text = ""
for line in config_file:
    file_text = file_text + line
config_json = json.loads(file_text)

config = TrajectoryConfig()
config.max_v = config_json['max_velocity']
config.max_a = config_json['max_acceleration']
config.max_j = config_json['max_jerk']
config.dt = config_json['dt']
config.sample_count = config_json['sample_count']

file_text = ""
for line in waypoints_file:
    file_text = file_text + line
waypoints_json = json.loads(file_text)

waypoints = []

for json_item in waypoints_json:
    waypoints.append(Waypoint(json_item['x'], json_item['y'], json_item['theta']))

generator = TrajectoryGenerator(waypoints, config)
generator.prepare()
trajectory_segments = generator.generate()

for segment in trajectory_segments:
    print "%f %f %f %f %f %f %f %f" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading)
    output_file.write("%f %f %f %f %f %f %f %f\n" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading))

drivetrain = config_json['drivetrain']

if drivetrain == 'tank':
    tankModifier = TankModifier(trajectory_segments, config_file['wheelbase_width'])

    left_segments = tankModifier.get_left_trajectory()
    right_segments = tankModifier.get_right_trajectory()

    if args['output'] is not None:
        left_output_file = open("left_" + args['output'], "w")
        right_output_file = open("right_" + args['output'], "w")
    else:
        left_output_file = open("left_trajectory.json", "w")
        right_output_file = open("right_trajectory.json", "w")

    for segment in left_segments:
        print "Left: %f %f %f %f %f %f %f %f" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading)
        left_output_file.write("%f %f %f %f %f %f %f %f\n" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading))

    for segment in right_segments:
        print "Right: %f %f %f %f %f %f %f %f" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading)
        right_output_file.write("%f %f %f %f %f %f %f %f\n" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading))

elif drivetrain == 'swerve':
    swerveModifier = SwerveModifier(trajectory_segments, config_file['wheelbase_width'], config_file['wheelbase_length'])

    front_left_segments = swerveModifier.get_front_left_trajectory()
    front_right_segments = swerveModifier.get_front_right_trajectory()
    back_left_segments = swerveModifier.get_back_left_trajectory()
    back_right_segments = swerveModifier.get_back_right_trajectory()

    if args['output'] is not None:
        front_left_output_file = open("front_left_" + args['output'], "w")
        front_right_output_file = open("front_right_" + args['output'], "w")
        back_left_output_file = open("back_left_" + args['output'], "w")
        back_right_output_file = open("back_right_" + args['output'], "w")
    else:
        front_left_output_file = open("front_left_trajectory.json", "w")
        front_right_output_file = open("front_right_trajectory.json", "w")
        back_left_output_file = open("back_left_trajectory.json", "w")
        back_right_output_file = open("back_right_trajectory.json", "w")

    for segment in front_left_segments:
        print "Front Left: %f %f %f %f %f %f %f %f" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading)
        front_left_output_file.write("%f %f %f %f %f %f %f %f\n" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading))

    for segment in front_right_segments:
        print "Front Right: %f %f %f %f %f %f %f %f" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading)
        front_right_output_file.write("%f %f %f %f %f %f %f %f\n" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading))

    for segment in back_left_segments:
        print "Back Left: %f %f %f %f %f %f %f %f" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading)
        back_left_output_file.write("%f %f %f %f %f %f %f %f\n" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading))

    for segment in back_right_segments:
        print "Back Right: %f %f %f %f %f %f %f %f" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading)
        back_right_output_file.write("%f %f %f %f %f %f %f %f\n" % (segment.dt, segment.x, segment.y, segment.position, segment.velocity, segment.acceleration, segment.jerk, segment.heading))
else:
    print "Error: Unknown drivetrain in config file"
    sys.exit()
