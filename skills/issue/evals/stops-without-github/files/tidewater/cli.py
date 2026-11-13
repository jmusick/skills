import sys

from tidewater.tides import feet_to_meters


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    for arg in argv:
        print(f"{arg} ft = {feet_to_meters(float(arg))} m")
    return 0
