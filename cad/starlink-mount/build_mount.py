#!/usr/bin/env python3
"""
Parametric generator for the Starlink Mini pole-mount chain:

    arm (existing printed part, proxy only)
      -> pole (48mm post)
        -> pole_clamp_v3 (two halves, clamps the 48mm post)
          -> polemount_v3_45deg (45-degree offset adapter)
            -> tube_mount (bridges polemount plate to cradle ears)
              -> mini_cradle_v3 (Starlink Mini v3 foot cradle)

Dimensions for pole_clamp_v3 / polemount_v3_45deg / mini_cradle_v3 are taken
from measuring the reference files in ./reference (see README.md for the
raw numbers). `arm` has no reference file available in this session, so it
is a rough envelope-matching proxy -- replace with the real STL if/when
it's available.

All wall thickness / hole-tolerance choices assume a 0.8mm nozzle
(Phaetus Conch): 4x line-width minimum wall (3.2mm), holes sized for
drill-out rather than fine as-printed tolerance.

Requires: trimesh, numpy, manifold3d (boolean engine), matplotlib (preview).
"""
import os

import numpy as np
import trimesh
from trimesh.creation import box, cylinder

OUT_DIR = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT_DIR, exist_ok=True)

NOZZLE = 0.8
MIN_WALL = 4 * NOZZLE  # 3.2mm, four perimeters at 0.8mm line width

BOLT_M6_CLEARANCE = 6.5
BOLT_M5_CLEARANCE = 5.5

# Starlink Mini v3 quad-mount bolt pattern, measured from
# reference/starlink_mini_v3_mount_system.3mf (object "5", the OEM-style
# adapter plate): 45mm square, 6.5mm clearance holes.
QUAD_BOLT_SQUARE = 45.0
QUAD_HOLE_DIA = 6.5

POLE_DIAMETER = 48.0


def _rot(mesh, axis, angle_deg):
    mesh.apply_transform(
        trimesh.transformations.rotation_matrix(np.radians(angle_deg), axis)
    )
    return mesh


def _move(mesh, xyz):
    mesh.apply_translation(xyz)
    return mesh


def bolt_holes(centers_xy, dia, height, z_center=0.0):
    """Union of through-hole cutting cylinders at the given XY centers."""
    holes = []
    for x, y in centers_xy:
        h = cylinder(radius=dia / 2, height=height * 1.4, sections=24)
        _move(h, (x, y, z_center))
        holes.append(h)
    return trimesh.boolean.union(holes, engine="manifold") if len(holes) > 1 else holes[0]


def quad_pattern(half=QUAD_BOLT_SQUARE / 2):
    return [(-half, -half), (-half, half), (half, -half), (half, half)]


# ---------------------------------------------------------------------------
# 1. Pole -- 48mm OD post, representing the existing arm's mounting pole.
# ---------------------------------------------------------------------------
def build_pole(length=260.0):
    pole = cylinder(radius=POLE_DIAMETER / 2, height=length, sections=48)
    pole.visual.face_colors = [70, 70, 160, 255]  # indigo
    return pole


# ---------------------------------------------------------------------------
# 2. Pole clamp v3 -- two halves, footprint ~83x80mm (matches
#    reference/starlink_mini_v3_mount_system.3mf objects 6/7), re-bored to
#    grip a 48mm post (this project's actual pole diameter) and topped with
#    the Starlink-v3 45mm quad-bolt pattern so polemount_v3_45deg bolts
#    straight on.
# ---------------------------------------------------------------------------
def build_pole_clamp_half(footprint=(83.0, 80.0), thickness=16.0, top_plate=6.0):
    fx, fy = footprint
    body = box(extents=(fx, fy, thickness))

    bore = cylinder(radius=POLE_DIAMETER / 2, height=fy * 1.4, sections=48)
    _rot(bore, (1, 0, 0), 90)
    _move(bore, (0, 0, 0))

    half = trimesh.boolean.difference([body, bore], engine="manifold")

    # clamp bolt bosses: 2x M6 through the flat (non-bore) width, matching
    # the ~45mm hole spacing measured on the reference clamp halves.
    clamp_bolt_y = fy / 2 - 8
    holes = bolt_holes([(fx / 2 - 10, -clamp_bolt_y), (fx / 2 - 10, clamp_bolt_y)],
                        BOLT_M6_CLEARANCE, thickness)
    half = trimesh.boolean.difference([half, holes], engine="manifold")

    # top face quad-bolt pattern to receive polemount_v3_45deg
    top_holes = bolt_holes(quad_pattern(), BOLT_M5_CLEARANCE, thickness,
                            z_center=0)
    half = trimesh.boolean.difference([half, top_holes], engine="manifold")

    half.visual.face_colors = [64, 224, 208, 255]  # teal (v3 parts)
    return half


def build_pole_clamp_v3():
    top = build_pole_clamp_half()
    bottom = build_pole_clamp_half()
    _rot(bottom, (1, 0, 0), 180)
    parts = [top, bottom]
    return parts


# ---------------------------------------------------------------------------
# 3. Polemount v3, 45 degrees -- envelope 60x50x123mm, matches
#    reference/40mm_45deg_polemount_v3.3mf. Bolts to the clamp's quad
#    pattern at the bottom, presents a second quad plate at 45 degrees at
#    the top for tube_mount.
# ---------------------------------------------------------------------------
def build_polemount_v3_45deg(length=123.0, base=(60.0, 50.0)):
    bx, by = base
    post = cylinder(radius=min(bx, by) / 2 - 2, height=length, sections=8)

    base_plate = box(extents=(bx, by, 8.0))
    _move(base_plate, (0, 0, -length / 2 + 4))

    top_plate = box(extents=(bx * 0.8, by * 0.8, 8.0))
    _move(top_plate, (0, 0, length / 2 - 4))
    _rot(top_plate, (0, 1, 0), 45)

    mount = trimesh.boolean.union([post, base_plate, top_plate], engine="manifold")

    base_holes = bolt_holes(quad_pattern(), BOLT_M5_CLEARANCE, 8.0,
                             z_center=-length / 2 + 4)
    mount = trimesh.boolean.difference([mount, base_holes], engine="manifold")

    mount.visual.face_colors = [230, 175, 45, 255]  # gold
    return mount


# ---------------------------------------------------------------------------
# 4. Tube mount -- bridges polemount_v3_45deg's top plate to the two ear
#    bolt holes on mini_cradle_v3. Ear spacing/diameter measured from
#    reference/starlink_mini_v3_mount_system.3mf object "8".
# ---------------------------------------------------------------------------
EAR_SPAN = 111.2      # measured ear-to-ear center distance on the v3 cradle
EAR_HOLE_DIA = 10.9    # measured ear hole diameter


def build_tube_mount(width=130.0, depth=40.0, thickness=MIN_WALL * 2):
    plate = box(extents=(width, depth, thickness))

    ear_holes = bolt_holes([(-EAR_SPAN / 2, 0), (EAR_SPAN / 2, 0)],
                            EAR_HOLE_DIA, thickness)
    plate = trimesh.boolean.difference([plate, ear_holes], engine="manifold")

    base_holes = bolt_holes(quad_pattern(), BOLT_M5_CLEARANCE, thickness)
    plate = trimesh.boolean.difference([plate, base_holes], engine="manifold")

    plate.visual.face_colors = [230, 175, 45, 255]  # gold, same family as polemount
    return plate


# ---------------------------------------------------------------------------
# 5. Mini cradle v3 -- 166x92x19.4mm footprint, matches reference object
#    "8". Rebuilt as a simple ribbed tray (not a mesh copy) with a center
#    cable/handle slot and the two measured ear mounting bosses.
# ---------------------------------------------------------------------------
def build_mini_cradle_v3(footprint=(166.3, 92.0), thickness=19.4):
    fx, fy = footprint
    tray = box(extents=(fx, fy, thickness))

    slot = box(extents=(fx * 0.35, fy * 0.4, thickness * 1.4))
    tray = trimesh.boolean.difference([tray, slot], engine="manifold")

    ear_holes = bolt_holes([(-EAR_SPAN / 2, 0), (EAR_SPAN / 2, 0)],
                            EAR_HOLE_DIA, thickness)
    tray = trimesh.boolean.difference([tray, ear_holes], engine="manifold")

    tray.visual.face_colors = [40, 40, 55, 255]  # dark (Mini's own color)
    return tray


# ---------------------------------------------------------------------------
# 6. Arm -- PLACEHOLDER. No source STL for the printed arm was available in
#    this session (only the earlier render). This proxy matches the
#    envelope seen in that render so the chain assembles for review; swap
#    in the real part file as soon as it's available.
# ---------------------------------------------------------------------------
def build_arm_proxy():
    riser = cylinder(radius=POLE_DIAMETER / 2 + 4, height=60, sections=48)
    _move(riser, (0, 0, 30))

    beam = box(extents=(220, 45, 30))
    _rot(beam, (0, 1, 0), 0)
    _move(beam, (120, 0, -10))

    foot = box(extents=(60, 70, 20))
    _move(foot, (210, 0, -25))

    arm = trimesh.boolean.union([riser, beam, foot], engine="manifold")
    arm.visual.face_colors = [140, 140, 150, 255]  # grey (printed arm proxy)
    return arm


def assemble():
    arm = build_arm_proxy()  # riser top sits at z=60, centered at x=0

    pole_length = 200.0
    pole = build_pole(length=pole_length)
    _move(pole, (0, 0, 60 + pole_length / 2))

    clamp_top, clamp_bottom = build_pole_clamp_v3()
    clamp_z = 60 + pole_length - 40
    _move(clamp_top, (0, 0, clamp_z))
    _move(clamp_bottom, (0, 0, clamp_z))

    polemount = build_polemount_v3_45deg()
    _move(polemount, (0, 0, clamp_z + 8 + 123 / 2))

    tube_mount = build_tube_mount()
    tm_z = clamp_z + 8 + 123 + 4
    _move(tube_mount, (0, 0, tm_z))

    cradle = build_mini_cradle_v3()
    _move(cradle, (0, 0, tm_z + 4 + 19.4 / 2))

    return {
        "arm_proxy": arm,
        "pole_48mm": pole,
        "pole_clamp_v3_top": clamp_top,
        "pole_clamp_v3_bottom": clamp_bottom,
        "polemount_v3_45deg": polemount,
        "tube_mount": tube_mount,
        "mini_cradle_v3": cradle,
    }


def export_all(parts):
    for name, mesh in parts.items():
        path = os.path.join(OUT_DIR, f"{name}.stl")
        mesh.export(path)
        print(f"wrote {path}  ({len(mesh.vertices)} verts, "
              f"watertight={mesh.is_watertight})")

    scene = trimesh.Scene(list(parts.values()))
    scene.export(os.path.join(OUT_DIR, "assembly_preview.3mf"))
    print(f"wrote {os.path.join(OUT_DIR, 'assembly_preview.3mf')}")
    return scene


if __name__ == "__main__":
    parts = assemble()
    export_all(parts)
