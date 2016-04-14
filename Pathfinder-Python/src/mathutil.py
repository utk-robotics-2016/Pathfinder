import math


# Convert degrees to radians
def d2r(self, degrees):
    return math.radians(degrees)


# Convert radians to degrees
def r2d(self, radians):
    return math.degress(radians)


# Bound an angle (in degrees) to -180 to 180 degrees.
def boundHalfDegress(self, angle_degrees):
    while angle_degrees >= 180.0:
        angle_degrees = angle_degrees - 360.0

    while angle_degrees < 180.0:
        angle_degrees = angle_degrees + 360.0
    return angle_degrees
