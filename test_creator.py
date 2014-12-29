#!/usr/bin/env python
"""
The SpanSelector is a mouse widget to select a xmin/xmax range and plot the
detail view of the selected region in the lower axes
"""

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from collections import defaultdict
import os
import sys
import json


class ImagePicker(object):

    def __init__(self, path):

        # File stuff
        self.path = path
        assert os.path.exists(path), "Path given doesn't exist."
        self.files = sorted(set(os.listdir(path)) - set(["points.json", ".DS_Store"]))
        print self.files
        assert len(self.files) > 0, "There are no files."
        self.index = 0
        self.image = None

        # Plot
        self.fig, self.ax = plt.subplots()
        self.point_plot, = self.ax.plot([], [],
                                        linestyle="", marker="o")
        # Event handlers
        self.hook_events()
        self.fig.show()

        # Selection
        self.point_data = defaultdict(list)
        self.point_data.update(json.loads(open(self.path + "points.json").readlines()[0]))
        self.current_selection = None

        self.switch_to_image(self.index)

    def hook_events(self):
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key)

    def switch_to_image(self, index):
        self.image = mpimg.imread(self.path + self.filename())
        self.ax.set_title("Image %s of %s. (%s)" % (self.index + 1,
                                                    len(self.files),
                                                    self.filename()))
        self.draw()
        self.redraw()

    def filename(self):
        return self.files[self.index]

    def points(self):
        return self.point_data[self.filename()]

    def draw(self):
        """Draw base image and save the background to blit later."""
        self.ax.clear()
        self.ax.imshow(self.image, picker=self.image_picker)
        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

    def redraw(self):
        self.fig.canvas.restore_region(self.background)
        self.point_plot.set_xdata([x[0] for x in self.points()])
        self.point_plot.set_ydata([x[1] for x in self.points()])
        self.ax.draw_artist(self.point_plot)
        self.fig.canvas.blit(self.ax.bbox)

    def image_picker(self, artist, event):
        return True, dict(x=event.xdata, y=event.ydata, button=event.button)

    def on_pick(self, event):

        if event.x is None or event.y is None:
            return

        if event.button == 1:
            self.points().append((event.x, event.y))
        elif event.button == 3:
            if len(self.points()) != 0:
                self.points().pop()

        self.redraw()

    def on_key(self, event):

        if event.key == "right":
            if self.index < len(self.files) - 1:
                self.index += 1
            self.switch_to_image(self.index)
        elif event.key == "left":
            if self.index > 0:
                self.index -= 1
            self.switch_to_image(self.index)
        elif event.key == "escape":
            data = open(self.path + "points.json", "w+")
            data.write(json.dumps(self.point_data))
            data.close()
            sys.exit(0)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "Give me a path that contains images."
    ip = ImagePicker(sys.argv[1])
    plt.show()
