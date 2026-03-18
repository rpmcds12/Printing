"""
Generate STL cookie cutters for:
1. Peace/Victory hand sign  (two distinct fingers with clear V gap)
2. Sneaker/shoe (Vans Old Skool side profile)
3. Circle (smiley face with lightning bolt)
4. Baseball/Trucker cap (front view)
5. Arch/Tombstone ("Good Vibes")
6. Scalloped circle / Bottle cap badge ("Hudson is ONE Happy Dude")

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
# 1. PEACE / VICTORY HAND  (completely redrawn)
# ---------------------------------------------------------------------------
# Two clearly separated fingers (index + middle) in a V shape.
# Palm/wrist below with thumb bump on left, curled ring+pinky on right.
# Overall: ~95mm wide x ~118mm tall.
# Traced CCW starting at bottom-left of palm.
#
#  Layout (approximate):
#   Index finger center  x ≈ 13  (left finger)
#   Middle finger center x ≈ 64  (right finger, V spread)
#   V notch bottom       at (42, 48)
#   Palm base            x: 5 – 85

peace_hand = [
    # ── Palm base (bottom, left to right) ──────────────────────────────────
    (  5,  0),
    ( 85,  0),
    # ── Right side of palm / wrist (going up) ──────────────────────────────
    ( 88,  6),
    ( 90, 16),
    ( 92, 26),
    # Curled ring+pinky knuckle bulge on right
    ( 93, 36),
    ( 91, 46),
    # ── Into middle-finger base (right side) ───────────────────────────────
    ( 84, 50),
    ( 78, 53),
    # ── Middle finger — right edge going up ────────────────────────────────
    ( 77, 60),
    ( 75, 74),
    ( 73, 90),
    ( 71,104),
    # ── Middle finger tip (sweeping right → left) ──────────────────────────
    ( 69,112),
    ( 65,116),
    ( 60,118),
    ( 55,116),
    ( 51,112),
    # ── Middle finger — left edge going down ───────────────────────────────
    ( 49,104),
    ( 48, 90),
    ( 48, 74),
    ( 49, 60),
    ( 50, 53),
    # ── V notch between the two fingers ────────────────────────────────────
    ( 46, 50),
    ( 42, 48),   # deepest point of the V gap
    ( 38, 50),
    # ── Index finger — right edge going up from V notch ────────────────────
    ( 37, 53),
    ( 35, 60),
    ( 31, 74),
    ( 28, 90),
    ( 25,104),
    # ── Index finger tip (sweeping right → left) ───────────────────────────
    ( 22,112),
    ( 17,116),
    ( 13,118),
    (  8,116),
    (  4,112),
    # ── Index finger — left edge going down ────────────────────────────────
    (  2,104),
    (  1, 90),
    (  1, 74),
    (  3, 60),
    (  5, 53),
    # ── Left side of palm (going down, with thumb bump) ────────────────────
    (  3, 46),
    (  3, 36),
    # Thumb knuckle bump on left
    (  4, 26),
    (  5, 16),
    (  5,  6),
]

# ---------------------------------------------------------------------------
# 2. SNEAKER / SHOE — Vans Old Skool side profile (facing right)
# ---------------------------------------------------------------------------
# Redrawn for a more accurate low-top silhouette.
# Overall: ~128mm wide x ~72mm tall.
# Key features:
#   • thick flat sole with slight curve at heel and toe
#   • squared toe box with modest height
#   • low ankle collar with a slight dip toward the tongue
#   • heel sits taller than the toe opening

sneaker = [
    # ── Sole bottom — heel (left) to toe (right) ───────────────────────────
    (  0, 14),   # heel bottom-left corner
    (  2,  6),
    (  8,  2),
    ( 20,  0),
    ( 65,  0),
    (100,  0),
    (115,  3),
    (122,  8),
    (126, 15),
    # ── Toe front wall (going up) ──────────────────────────────────────────
    (128, 22),
    (126, 30),
    # ── Toe box top (going left) ───────────────────────────────────────────
    (122, 37),
    (110, 41),
    # ── Mid upper going toward ankle ───────────────────────────────────────
    ( 90, 44),
    ( 72, 47),
    # ── Tongue / instep dip ────────────────────────────────────────────────
    ( 58, 49),
    ( 50, 54),
    ( 44, 61),
    # ── Ankle collar (top of heel) ─────────────────────────────────────────
    ( 36, 69),
    ( 22, 72),
    # ── Heel collar going down ─────────────────────────────────────────────
    (  8, 70),
    (  2, 64),
    (  0, 52),
    # ── Heel back wall going down ──────────────────────────────────────────
    (  0, 30),
]

# ---------------------------------------------------------------------------
# 3. CIRCLE (Smiley Face with lightning bolt)
# ---------------------------------------------------------------------------
# ~84mm diameter circle (radius 42mm).
# The lightning bolt / smiley decorations are painted on top — only the
# round outer shape is cut by the cutter.

_circle_angles = np.linspace(0, 2 * np.pi, 72, endpoint=False)
circle = [(42 + 42 * np.cos(a), 42 + 42 * np.sin(a)) for a in _circle_angles]

# ---------------------------------------------------------------------------
# 4. BASEBALL / TRUCKER CAP (front-facing silhouette)
# ---------------------------------------------------------------------------
# ~110mm wide x ~83mm tall.
# Wide flat brim at the bottom, rounded structured crown above.
# The brim extends slightly beyond the crown on each side.

baseball_cap = [
    (  5,  0),   # bottom-left of brim
    (105,  0),   # bottom-right of brim
    (110,  8),   # right tip of brim (angled)
    (107, 18),   # upper-right brim
    (100, 22),   # right brim-to-crown junction
    ( 97, 30),   # lower-right crown wall
    ( 96, 45),   # mid-right crown
    ( 95, 62),   # upper-right crown
    ( 90, 73),   # upper-right shoulder
    ( 80, 79),   # near top-right
    ( 65, 82),   # top-right of crown
    ( 55, 83),   # crown apex (center)
    ( 45, 82),   # top-left of crown
    ( 30, 79),   # near top-left
    ( 20, 73),   # upper-left shoulder
    ( 15, 62),   # upper-left crown
    ( 14, 45),   # mid-left crown
    ( 13, 30),   # lower-left crown wall
    ( 10, 22),   # left brim-to-crown junction
    (  3, 18),   # upper-left brim
    (  0,  8),   # left tip of brim (angled)
]

# ---------------------------------------------------------------------------
# 5. ARCH / TOMBSTONE ("Good Vibes" cookie)
# ---------------------------------------------------------------------------
# 80mm wide x ~100mm tall.
# Straight vertical sides (55mm) + semi-elliptical arch on top (45mm rise).

def _make_arch_outline(width=80, straight_h=55, arch_h=45, n_pts=24):
    cx = width / 2
    pts = []
    pts.append((0, 0))               # bottom-left
    pts.append((width, 0))           # bottom-right
    pts.append((width, straight_h))  # top-right (arch start, theta=0)
    # Semi-ellipse from right (theta=0) CCW over the top to left (theta=pi)
    for i in range(1, n_pts):        # skip theta=0 (already added)
        theta = i * np.pi / n_pts
        x = cx + cx * np.cos(theta)
        y = straight_h + arch_h * np.sin(theta)
        pts.append((x, y))
    pts.append((0, straight_h))      # top-left (arch end, theta=pi)
    # Shapely closes polygon back to (0, 0) implicitly
    return pts

arch_tombstone = _make_arch_outline()

# ---------------------------------------------------------------------------
# 6. SCALLOPED CIRCLE / BOTTLE CAP BADGE
# ---------------------------------------------------------------------------
# ("Hudson is ONE Happy Dude" cookie)
# 90mm outer diameter with 18 scallops.
# Alternates between outer tip (r=45) and inner valley (r=37).

def _make_scalloped_circle(cx=45, cy=45, outer_r=45, inner_r=37, n_scallops=18):
    pts = []
    for i in range(2 * n_scallops):
        angle = i * np.pi / n_scallops
        r = outer_r if i % 2 == 0 else inner_r
        pts.append((cx + r * np.cos(angle), cy + r * np.sin(angle)))
    return pts

scalloped_circle = _make_scalloped_circle()


if __name__ == "__main__":
    import os
    os.chdir("/home/user/Printing")

    make_cookie_cutter(
        peace_hand, WALL_THICKNESS, HEIGHT,
        filename="peace_hand_cutter.stl",
    )
    make_cookie_cutter(
        sneaker, WALL_THICKNESS, HEIGHT,
        filename="sneaker_cutter.stl",
    )
    make_cookie_cutter(
        circle, WALL_THICKNESS, HEIGHT,
        filename="circle_cutter.stl",
    )
    make_cookie_cutter(
        baseball_cap, WALL_THICKNESS, HEIGHT,
        filename="baseball_cap_cutter.stl",
    )
    make_cookie_cutter(
        arch_tombstone, WALL_THICKNESS, HEIGHT,
        filename="arch_tombstone_cutter.stl",
    )
    make_cookie_cutter(
        scalloped_circle, WALL_THICKNESS, HEIGHT,
        filename="scalloped_circle_cutter.stl",
    )

    print("\nDone! All 6 STL cookie cutter files are ready for slicing.")
