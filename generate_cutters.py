"""
Generate STL cookie cutters for:
1. Peace/Victory hand sign
2. Sneaker/shoe

Each cutter is just the outline wall (no internal detail cutouts).
Wall thickness: 2mm, Height: 20mm
"""

import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union

WALL_THICKNESS = 2.0   # mm
HEIGHT = 20.0           # mm


def make_cookie_cutter(outline_pts, wall_thickness, height, filename):
    """
    Given a 2D outline polygon, create a cookie cutter STL.
    The cutter has:
      - vertical outer wall
      - vertical inner wall (offset inward by wall_thickness)
      - closed top face
      - open bottom (the cutting edge)
    """
    outer = Polygon(outline_pts)
    if not outer.is_valid:
        outer = outer.buffer(0)
    # Ensure CCW orientation
    if not outer.exterior.is_ccw:
        outer = Polygon(list(reversed(list(outer.exterior.coords))))

    inner = outer.buffer(-wall_thickness)
    if inner.is_empty:
        raise ValueError("Wall thickness too large for this shape")

    # Ring polygon: outer minus inner
    ring = outer.difference(inner)

    # Extrude the ring polygon to get the 3D cookie cutter
    cutter = trimesh.creation.extrude_polygon(ring, height=height)

    cutter.export(filename)
    print(f"Saved: {filename}  (vertices={len(cutter.vertices)}, faces={len(cutter.faces)})")
    return cutter


# ---------------------------------------------------------------------------
# 1. PEACE / VICTORY HAND
# ---------------------------------------------------------------------------
# Outline traced approximately from the photo.
# Coordinates in mm, origin at bottom-left of bounding box.
# Shape is ~80 wide x ~100 tall.
# Points go counter-clockwise (shapely convention).

peace_hand = [
    # --- bottom handle bar ---
    (10,  0),
    (70,  0),
    # right side of wrist/palm going up
    (70,  8),
    (72, 15),
    # right bulge of palm (ring/pinky knuckle area)
    (74, 28),
    (72, 38),
    # right side going up toward middle finger base
    (66, 42),
    # --- middle finger (right of V) ---
    (62, 44),
    (64, 48),
    (66, 55),
    (65, 75),
    (62, 88),
    (58, 96),
    (54, 100),
    (50, 101),
    (46, 100),
    (42, 96),
    (38, 88),
    (35, 75),
    (34, 55),
    (36, 48),
    (38, 44),
    # --- index finger (left of V) ---
    (34, 42),
    (28, 40),
    # left side of palm going down
    (24, 36),
    (22, 28),
    # thumb bump on left side
    (18, 24),
    (14, 20),
    (12, 16),
    # back down to base
    (10,  8),
]

# ---------------------------------------------------------------------------
# 2. SNEAKER / SHOE (side profile, facing right)
# ---------------------------------------------------------------------------
# Shape is ~120 wide x ~70 tall.

sneaker = [
    # --- sole bottom, left (heel) to right (toe) ---
    ( 0, 10),
    ( 5,  5),
    (10,  2),
    (25,  0),
    (60,  0),
    (90,  2),
    (110,  5),
    (120, 10),
    (118, 15),
    # toe front wall
    (120, 22),
    (118, 28),
    # toe-box top curving back
    (115, 32),
    (105, 36),
    # mid-upper
    ( 85, 40),
    ( 70, 44),
    # ankle opening notch (front)
    ( 55, 46),
    ( 48, 50),
    ( 42, 58),
    # ankle opening (top of collar)
    ( 35, 65),
    ( 22, 68),
    # heel collar
    (  8, 65),
    (  2, 58),
    (  0, 48),
    # heel back wall
    (  0, 28),
    (  2, 18),
]

if __name__ == "__main__":
    import os
    os.chdir("/home/user/Printing")

    make_cookie_cutter(
        peace_hand,
        wall_thickness=WALL_THICKNESS,
        height=HEIGHT,
        filename="peace_hand_cutter.stl",
    )

    make_cookie_cutter(
        sneaker,
        wall_thickness=WALL_THICKNESS,
        height=HEIGHT,
        filename="sneaker_cutter.stl",
    )

    print("Done! Both STL files are ready for slicing.")
