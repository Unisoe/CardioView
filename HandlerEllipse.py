import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerPatch

class HandlerEllipse(HandlerPatch):
    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        center = 0.5 * width - 0.5, 0.5 * height - 0.5
        p = mpatches.Ellipse(xy=center, width=width * 0.35,
                             height=height)
        self.update_prop(p, orig_handle, legend)
        p.set_transform(trans)
        return [p]