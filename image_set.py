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
    cwd = os.path.abspath(os.path.curdir)
    dataset_dir = os.path.join(cwd, "datasets/")
    return [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir)
            if os.path.isdir(os.path.join(dataset_dir, f))]


@pytest.fixture(params=load_folders())
def image_set(request):
    return ImageSet(request.param)
