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
# 1. PEACE / VICTORY HAND  (v3 — compact, realistic proportions)
# ---------------------------------------------------------------------------
# Design rationale:
#   Previous version had 65mm-tall fingers on a 53mm palm (ratio 1.23:1)
#   with only a 5mm-deep V notch and 29mm gap at tips → looked like bunny ears.
#
#   This version:
#     • Palm 50mm tall, fingers only 43mm above palm (ratio 0.86:1 — palm TALLER)
#     • Each finger consistently 20mm wide (not tapering to a spike)
#     • V notch 15mm deep (y=50 down to y=35) — clearly visible in plastic
#     • Gap at tips 15mm — tight, recognizable peace sign
#     • Mild 2mm lean per finger over 43mm height (~3° from vertical)
#
#   Overall bounding box: ~80mm wide × 93mm tall
#
#   Key x-positions:
#     Palm base          x: 5 – 73  (68mm wide)
#     Index finger base  x: 12 – 32  (center x=22, leans 2mm LEFT to tip)
#     Middle finger base x: 43 – 63  (center x=53, leans 2mm RIGHT to tip)
#     V notch bottom     (37, 35)    — 15mm below finger bases

peace_hand = [
    # ── Palm base ───────────────────────────────────────────────────────────
    (  5,  0),   # bottom-left
    ( 73,  0),   # bottom-right

    # ── Right palm wall (bulges for curled ring + pinky) ────────────────────
    ( 76,  7),
    ( 78, 17),
    ( 79, 28),
    ( 78, 38),
    ( 75, 45),

    # ── Transition to middle-finger right base ───────────────────────────────
    ( 68, 49),
    ( 63, 50),   # right edge of middle finger at base

    # ── Middle finger — right side going up (leans 2mm right over 43mm) ─────
    ( 64, 62),
    ( 65, 74),
    ( 65, 82),   # right edge at start of rounded cap

    # ── Middle finger tip — semicircular cap (center x=55 at y=82) ──────────
    ( 63, 87),
    ( 59, 91),
    ( 55, 93),   # tip apex
    ( 51, 91),
    ( 47, 87),
    ( 45, 82),   # left edge at start of cap

    # ── Middle finger — left side going down ────────────────────────────────
    ( 44, 74),
    ( 43, 62),
    ( 43, 50),   # left edge of middle finger at base

    # ── V notch — 15mm deep, 11mm wide at base ──────────────────────────────
    # Goes from y=50 down to y=35 between the two finger bases.
    ( 41, 47),
    ( 40, 42),
    ( 37, 35),   # deepest point (15mm below finger bases)
    ( 34, 42),
    ( 33, 47),
    ( 32, 50),   # right edge of index finger at base

    # ── Index finger — right side going up (leans 2mm left over 43mm) ───────
    ( 31, 62),
    ( 30, 74),
    ( 30, 82),   # right edge at start of rounded cap

    # ── Index finger tip — semicircular cap (center x=20 at y=82) ───────────
    ( 28, 87),
    ( 24, 91),
    ( 20, 93),   # tip apex
    ( 16, 91),
    ( 12, 87),
    ( 10, 82),   # left edge at start of cap

    # ── Index finger — left side going down ─────────────────────────────────
    ( 10, 74),
    ( 11, 62),
    ( 12, 50),   # left edge of index finger at base

    # ── Left palm wall (thumb area, smooth curve) ───────────────────────────
    (  7, 46),
    (  3, 36),
    (  3, 26),
    (  4, 16),
    (  5,  7),
    # polygon closes back to (5, 0)
]

# ---------------------------------------------------------------------------
# 2. SNEAKER / SHOE — Vans Old Skool side profile (facing right, heel left)
# ---------------------------------------------------------------------------
# Design rationale:
#   Vans Old Skool is a flat-soled skate shoe. Key proportions:
#     • Real shoe: ~290mm long × 110mm tall → ratio ≈ 2.6:1
#     • Cookie cutter target: 130mm wide × 68mm tall → ratio ≈ 1.9:1
#     • Sole is FLAT on the bottom (skate shoe, no heel elevation)
#     • Sole thickness: 15mm at heel, tapers to 10mm at toe
#     • Toe box: slightly squared, 38mm above sole
#     • Ankle opening: distinctive dip — tongue at y=52, dips to y=46,
#       then rises to heel collar at y=68
#     • Heel back: nearly straight vertical wall
#
#   Traced CCW starting at the heel back bottom (0, 0).
#   Heel is on the LEFT (x=0), toe points RIGHT (x≈130).

sneaker = [
    # ── Heel back bottom corner (start) ────────────────────────────────────
    (  0,  0),

    # ── Sole bottom — flat, heel to toe (going right) ──────────────────────
    (  4,  0),
    ( 15,  0),
    ( 60,  0),
    (105,  0),
    (120,  0),
    (126,  3),
    (130,  8),   # toe-bottom corner

    # ── Toe front wall (going up) ──────────────────────────────────────────
    (132, 16),
    (131, 26),
    (129, 34),

    # ── Toe box top (going left) ───────────────────────────────────────────
    (125, 40),   # squared-off Vans toe box corner
    (114, 44),

    # ── Mid upper (going left, slopes gently upward toward ankle) ──────────
    ( 92, 47),
    ( 72, 50),

    # ── Tongue (front of ankle opening — slightly elevated) ─────────────────
    ( 58, 52),

    # ── Ankle opening dip (the "U" notch between tongue and heel collar) ────
    # Goes DOWN 6mm from tongue, creating a visible notch in the silhouette.
    ( 47, 46),   # bottom of ankle opening notch

    # ── Ankle rises steeply to heel collar ──────────────────────────────────
    ( 36, 58),
    ( 24, 64),
    ( 14, 68),   # heel collar peak

    # ── Heel collar curving down ────────────────────────────────────────────
    (  4, 66),
    (  0, 58),   # top of heel back wall

    # ── Heel back wall (going straight down) ───────────────────────────────
    (  0, 38),
    (  0, 18),
    # polygon closes back to (0, 0)
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
