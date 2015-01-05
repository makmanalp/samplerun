import pytest


class Algorithm(object):

    folder = None

    def run(self, image, with_assertions=True):
        raise NotImplementedError()


class MyAlgoA(Algorithm):
    folder = "images/"

    def run(self, image, **kwargs):
        for i in image.images():
            print i


class MyAlgoB(Algorithm):
    folder = "pinkball/"

    def run(self, image, **kwargs):
        pass

ALGORITHMS = {
    "AlgoA": MyAlgoA(),
    "AlgoB": MyAlgoB()
}


@pytest.fixture(params=["AlgoA", "AlgoB"])
def algorithm(request):
    return ALGORITHMS.get(request.param)
