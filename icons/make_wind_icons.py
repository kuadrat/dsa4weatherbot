from copy import copy

import matplotlib.patches as p
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Affine2D as a2d
from matplotlib.gridspec import GridSpec
from matplotlib.path import Path

#_Parameters____________________________________________________________________

n_levels = 7
height = 1
delta_angle = 90/(n_levels-1)
linewidth = 1

#_Geometry______________________________________________________________________

windbag_length = 1.0
windbag_width = 0.2
windbag_backwidth = 0.5*windbag_width
windbag_delta = windbag_width - windbag_backwidth
fixation_length = 1.5*windbag_width

pole_height = 1.2*(windbag_length + fixation_length)
pole_base_width = 1.5*windbag_width

origin = np.array([0, 0])
front_right = origin
front_left = np.array([windbag_width, 0])
back_right = np.array([0.5*windbag_delta, windbag_length])
back_left = np.array([windbag_width - 0.5*windbag_delta, windbag_length])
fixation_point = np.array([windbag_width/2, -fixation_length])
def intermediate_point_right(r):
    return(front_right + r*(back_right - front_right))
def intermediate_point_left(r):
    return(front_left + r*(back_left - front_left))

# Base outline
windbag_outline = p.Polygon(
    [
        front_right,
        front_left,
        back_left,
        back_right,
        front_right
    ],
    facecolor="none",
    linewidth=linewidth, edgecolor="black"
)


# Fixation triangle
windbag_triangle = p.Polygon(
    [
        front_left,
        fixation_point,
        front_right
    ],
    facecolor="none",
    linewidth=linewidth, edgecolor="black",
    closed=False
)

# Red patches
red_patches = []
white_patches = []
dr = 0.2
for r in [0.2, 0.6, 1.0]:
    patch = p.Polygon(
    [
        intermediate_point_right(r-dr),
        intermediate_point_left(r-dr),
        intermediate_point_left(r),
        intermediate_point_right(r),
        intermediate_point_right(r-dr)
    ],
    facecolor="red", linewidth=0
    )
    red_patches.append(patch)

for r in [0.4, 0.8]:
    patch = p.Polygon(
    [
        intermediate_point_right(r-dr),
        intermediate_point_left(r-dr),
        intermediate_point_left(r),
        intermediate_point_right(r),
        intermediate_point_right(r-dr)
    ],
    facecolor="white", linewidth=0
    )
    white_patches.append(patch)

windbag = red_patches + white_patches + [windbag_triangle, windbag_outline]

# Pole
vertcodes = [
    (Path.MOVETO, origin),
    (Path.LINETO, np.array([0, -pole_height])),
    (Path.MOVETO, np.array([-0.5*pole_base_width, -pole_height])),
    (Path.LINETO, np.array([0.5*pole_base_width, -pole_height]))
]
verts = [v[1] for v in vertcodes]
codes = [v[0] for v in vertcodes]
pole_path = Path(verts, codes)
pole = p.PathPatch(pole_path, lw=linewidth, edgecolor="black", zorder=-1)

# Move the windbag's fixpoint to the center
to_center = a2d().translate(-windbag_width/2, fixation_length)

# Move windbag from origin to it's final location
to_fixpoint = a2d().translate(-0.5, 0.75)

#_Plotting______________________________________________________________________

fig = plt.figure(figsize=(n_levels*height, height), layout="constrained")
gs = GridSpec(nrows=1, ncols=n_levels, figure=fig)

for i in range(n_levels):
    angle = 180 + i*delta_angle
    rotate = a2d().rotate_deg(angle)

    ax = fig.add_subplot(gs[i], frameon=False)

    ## Windbag
    for original_shape in windbag:
        shape = copy(original_shape)
        shape.set_transform(to_center + rotate + to_fixpoint + ax.transData)

        ax.add_patch(shape)

    ## Pole
    my_pole = copy(pole)
    my_pole.set_transform(to_fixpoint + ax.transData)
    ax.add_patch(my_pole)

    ax.set_aspect("equal")
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_xticks([])
    ax.set_yticks([])

fig.savefig("windbags.pdf")
fig.savefig("windbags.png", dpi=150)

#_Cut_into_separate_icons_______________________________________________________

from PIL import Image
image = Image.open("windbags.png")
nx, ny = image.width, image.height
dx = nx//n_levels

for i in range(n_levels):
    i0 = i*dx
    i1 = (i+1)*dx
    sub = image.crop((i0, 0, i1, ny))
    name = "wind{}.png".format(i)
    sub.save(name, "PNG")

