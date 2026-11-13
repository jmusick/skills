import unittest

from tidewater.tides import feet_to_meters


class FeetToMeters(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(feet_to_meters(10), 3.05)

    def test_negative(self):
        self.assertEqual(feet_to_meters(-1.5), -0.46)
