import math
import argparse

parser = argparse.ArgumentParser(description='Calculate volumn of a cylinder')
parser.add_argument('-r', '--radius', type=int, metavar='', required=True, help='Radius of a Cylinder')
parser.add_argument('-H', '--height', type=int, metavar='', required=True, help='Height of a Cylinder')
args = parser.parse_args()

def cylinder_volume(radius, height):
    return ((math.pi) * (radius ** 2) * (height))

if __name__ == '__main__':
    print(cylinder_volume(args.radius, args.height))