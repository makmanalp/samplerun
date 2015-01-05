import pytest
import skimage.io

import json
import os.path


class ImageSet(object):

    def __init__(self, path, extensions=(".png", ".jpg")):
        self.path = os.path.abspath(path)
        self.extensions = extensions
        data = json.loads(open(os.path.join(path, "points.json")).read())
        self.points = {k: v for k, v in data.iteritems() if k.endswith(extensions)}

    def images(self):
        for image_name, points in self.points.iteritems():
            image_path = os.path.join(self.path, image_name)
            image_array = skimage.io.imread(image_path)
            yield image_array, points


def load_folders():
    folders = ["images", "pinkball"]
    cwd = os.path.abspath(os.path.curdir)
    return [os.path.join(cwd, f) for f in folders]


@pytest.fixture(params=load_folders())
def image_set(request):
    return ImageSet(request.param)
