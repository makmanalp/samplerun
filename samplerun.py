import unittest
import math


class SampleRunMixin:

    def percent_difference(self, a, b):
        """Percent difference between two values."""
        return (float(a) - b) / (a + b / 2.0)

    def distance2D(self, a, b):
        """Distance between two 2d points"""
        return math.sqrt((b[1] - a[1])**2.0 +
                         (b[0] - a[0])**2.0)

    def assertWithin(self, a, b, within=0.1):
        """Assert that distance between two points (2-tuples) is within x."""
        diff = self.percent_difference(a, b)
        if diff < within:
            return True
        else:
            raise AssertionError("""%s is within %s of %s, expected it to be
                                 within %s.""" % (a, diff, b, within))

    def assertDistanceWithin(self, a, b, within):
        """Assert that two values are between x%."""
        distance = self.distance2D(a, b)
        if distance < within:
            return True
        else:
            raise AssertionError("""%s is within %s of %s, expected it to be
                                 within %s.""" % (a, distance, b, within))

    def assert2DPointsWithin(self, a, b, within=0.1):

        self.assertEquals(len(a), len(b))

        for x, y in zip(sorted(a), sorted(b)):
            self.assertDistanceWithin(x, y, within)


class SampleRunTestCase(unittest.TestCase, SampleRunMixin):
    pass


class DetectionLocationtest(SampleRunTestCase):

    def testWithin(self):
        self.assert2DPointsWithin([(2, 2), (3, 4)], [(2, 2), (3, 5)], 10)

    def testNotWithin(self):
        self.assertRaises(AssertionError, self.assert2DPointsWithin,
                          [(2, 2), (3, 4)], [(2, 2), (3, 5)], 0.1)

    def testWrongNumberOfThings(self):
        self.assertRaises(AssertionError, self.assert2DPointsWithin,
                          [(2, 2)], [(2, 2), (3, 5)], 10)
        self.assertRaises(AssertionError, self.assert2DPointsWithin,
                          [(2, 2)], [(2, 2), (3, 5)], 10)