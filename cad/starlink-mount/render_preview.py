#!/usr/bin/env python3
"""Multi-view matplotlib preview of the assembled mount chain (out/*.stl)."""
import os

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from build_mount import assemble, OUT_DIR

VIEWS = [
    ("ISO", 25, -60),
    ("SIDE", 0, -90),
    ("FRONT", 0, 0),
    ("TOP", 90, -90),
    ("3/4", 20, -35),
    ("3/4 other", 20, -145),
]


def plot_mesh(ax, mesh):
    tris = mesh.vertices[mesh.faces]
    color = np.array(mesh.visual.face_colors[0][:3]) / 255.0
    coll = Poly3DCollection(tris, facecolor=color, edgecolor=(0, 0, 0, 0.15), linewidths=0.2)
    ax.add_collection3d(coll)


def main():
    parts = assemble()
    all_bounds = np.array([m.bounds for m in parts.values()])
    mins = all_bounds[:, 0, :].min(axis=0)
    maxs = all_bounds[:, 1, :].max(axis=0)
    center = (mins + maxs) / 2
    span = (maxs - mins).max() / 2 * 1.1

    fig = plt.figure(figsize=(19, 10))
    fig.suptitle(
        "POLE-BASED CHAIN v2: arm(grey, PROXY) -> pole 48mm(indigo) -> "
        "pole_clamp_v3(teal) -> polemount_v3_45deg(gold) -> tube_mount(gold) "
        "-> mini_cradle_v3(dark)",
        fontsize=11,
    )

    for i, (title, elev, azim) in enumerate(VIEWS):
        ax = fig.add_subplot(2, 3, i + 1, projection="3d")
        for mesh in parts.values():
            plot_mesh(ax, mesh)
        ax.set_xlim(center[0] - span, center[0] + span)
        ax.set_ylim(center[1] - span, center[1] + span)
        ax.set_zlim(center[2] - span, center[2] + span)
        ax.set_title(title)
        ax.view_init(elev=elev, azim=azim)

    out_path = os.path.join(OUT_DIR, "assembly_preview.png")
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
