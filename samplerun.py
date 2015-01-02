import unittest
import pytest
import sys
import math
import os

import json
import os.path


class SampleRunMixin:

    @staticmethod
    def percent_difference(self, a, b):
        """Percent difference between two values."""
        return (float(a) - b) / (a + b / 2.0)

    @staticmethod
    def distance2D(a, b):
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


def load_folders():
    folders = ["images", "pinkball"]
    cwd = os.path.abspath(os.path.curdir)
    return [os.path.join(cwd, f) for f in folders]


class Algorithm(object):

    folder = None

    def run(self, image, with_assertions=True):
        raise NotImplementedError()


class MyAlgoA(Algorithm):
    folder = "images/"

    def run(self, image, **kwargs):
        pass


class MyAlgoB(Algorithm):
    folder = "pinkball/"

    def run(self, image, **kwargs):
        pass

ALGORITHMS = [MyAlgoA(), MyAlgoB()]


@pytest.fixture(params=load_folders())
def image_set(request):
    return request.param


@pytest.fixture(params=ALGORITHMS)
def algorithm(request):
    return request.param


@pytest.mark.usefixtures("image_set")
class TestsContainer(SampleRunTestCase):
    longMessage = True

    @classmethod
    def attach_method(cls, name, method):
        setattr(cls, name, method)

    @classmethod
    def make_test_function(cls, actual_points, expected_points):
        def current_test(self):
            self.assert2DPointsWithin(actual_points, expected_points, 80)
        return current_test

    @classmethod
    def add_folder(cls, folder):

        data = json.loads(open(os.path.join(folder, "points.json")).read())
        only_images = {k: v for k, v in data.iteritems() if k.endswith(".png")}

        for image_name, points in only_images.iteritems():
            test_name = "test_{0}".format(image_name.replace("-", "_").replace(".", "_"))
            cls.attach_method(test_name, cls.make_test_function([[1, 2]], points))


def test_algorithms(image_set, algorithm):
    algorithm.run(image_set, with_assertions=True)
