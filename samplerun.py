import unittest
import math

from image_set import image_set
from algorithm_loader import algorithm


def percent_difference(self, a, b):
    """Percent difference between two values."""
    return (float(a) - b) / (a + b / 2.0)


def distance2D(a, b):
    """Distance between two 2d points"""
    return math.sqrt((b[1] - a[1])**2.0 +
                     (b[0] - a[0])**2.0)


def assertWithin(a, b, within=0.1):
    """Assert that distance between two points (2-tuples) is within x."""
    __tracebackhide__ = True
    diff = percent_difference(a, b)
    if diff < within:
        return True
    else:
        raise AssertionError("""%s is within %s of %s, expected it to be
                             within %s.""" % (a, diff, b, within))


def assertDistanceWithin(a, b, within):
    """Assert that two values are between x%."""
    __tracebackhide__ = True
    distance = distance2D(a, b)
    if distance < within:
        return True
    else:
        raise AssertionError("""%s is within %s of %s, expected it to be
                             within %s.""" % (a, distance, b, within))


def assert2DPointsWithin(a, b, within=0.1):
    __tracebackhide__ = True
    assert len(a) == len(b)
    for x, y in zip(sorted(a), sorted(b)):
        assertDistanceWithin(x, y, within)


class DetectionLocationtest(unittest.TestCase):

    def testWithin(self):
        assert2DPointsWithin([(2, 2), (3, 4)], [(2, 2), (3, 5)], 10)

    def testNotWithin(self):
        self.assertRaises(AssertionError, assert2DPointsWithin,
                          [(2, 2), (3, 4)], [(2, 2), (3, 5)], 0.1)

    def testWrongNumberOfThings(self):
        self.assertRaises(AssertionError, assert2DPointsWithin,
                          [(2, 2)], [(2, 2), (3, 5)], 10)
        self.assertRaises(AssertionError, assert2DPointsWithin,
                          [(2, 2)], [(2, 2), (3, 5)], 10)


def test_algorithms(image_set, algorithm):
    """Main entry point for py.test, parameters get filled in from fixtures in
    image_set and algorithm_loader."""
    for image, points in image_set.images():
        result = algorithm.run(image)
        assert2DPointsWithin(result, points, 5)
