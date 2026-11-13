import json
import sys

from tidewater.tides import feet_to_meters


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    as_json = "--json" in argv
    heights = [float(a) for a in argv if a != "--json"]
    if as_json:
        print(json.dumps([{"feet": h, "meters": feet_to_meters(h)} for h in heights]))
        return 0
    for h in heights:
        print(f"{h} ft = {feet_to_meters(h)} m")
    return 0
