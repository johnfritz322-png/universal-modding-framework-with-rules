"""Build the Riftforged Slabblade V2 source mesh.

The project previously used a Node generator, but this machine has no Node
runtime.  This is a self-contained Python equivalent that writes only the V2
OBJ/MTL source pair outside the game directory.
"""
from pathlib import Path
from math import cos, hypot, pi, sin

OUT = Path(r"D:/Dawnwalker-Modding/Projects/DawnwalkerWeaponForge/SourceArt/Weapons")
NAME = "SM_RiftforgedSlabblade_V2"


class Obj:
    def __init__(self):
        self.lines = [f"mtllib {NAME}.mtl", f"o {NAME}", "s 1"]
        self.v = self.vt = self.vn = 0

    def vertex(self, x, y, z, u, w, nx, ny, nz):
        self.lines.extend((
            f"v {x:.4f} {y:.4f} {z:.4f}",
            f"vt {u:.4f} {w:.4f}",
            f"vn {nx:.4f} {ny:.4f} {nz:.4f}",
        ))
        self.v += 1
        self.vt += 1
        self.vn += 1
        return f"{self.v}/{self.vt}/{self.vn}"

    def face(self, *indices):
        self.lines.append("f " + " ".join(indices))

    def use(self, material):
        self.lines.append("usemtl " + material)


def prism(mesh, points, front_y, back_y, material):
    """Extrude a convex 2D X/Z outline with UVs and face normals."""
    mesh.use(material)
    min_x, max_x = min(x for x, _ in points), max(x for x, _ in points)
    min_z, max_z = min(z for _, z in points), max(z for _, z in points)
    rx, rz = max_x - min_x or 1, max_z - min_z or 1
    cx = sum(x for x, _ in points) / len(points)
    cz = sum(z for _, z in points) / len(points)
    front_center = mesh.vertex(cx, front_y, cz, .5, .5, 0, -1, 0)
    back_center = mesh.vertex(cx, back_y, cz, .5, .5, 0, 1, 0)
    front, back = [], []
    for x, z in points:
        u, w = (x - min_x) / rx, (z - min_z) / rz
        front.append(mesh.vertex(x, front_y, z, u, w, 0, -1, 0))
        back.append(mesh.vertex(x, back_y, z, u, w, 0, 1, 0))
    for i, (ax, az) in enumerate(points):
        j = (i + 1) % len(points)
        bx, bz = points[j]
        mesh.face(front_center, front[j], front[i])
        mesh.face(back_center, back[i], back[j])
        dx, dz = bx - ax, bz - az
        length = hypot(dx, dz) or 1
        nx, nz = dz / length, -dx / length
        a = mesh.vertex(ax, front_y, az, 0, 0, nx, 0, nz)
        b = mesh.vertex(bx, front_y, bz, 1, 0, nx, 0, nz)
        c = mesh.vertex(bx, back_y, bz, 1, 1, nx, 0, nz)
        d = mesh.vertex(ax, back_y, az, 0, 1, nx, 0, nz)
        mesh.face(a, b, c, d)


def cylinder(mesh, radius, half_depth, center_z, height, material, sides=16):
    mesh.use(material)
    top, bottom = [], []
    for i in range(sides):
        angle = 2 * pi * i / sides
        x, y = cos(angle) * radius, sin(angle) * half_depth
        top.append(mesh.vertex(x, y, center_z + height / 2, i / sides, 1, cos(angle), sin(angle), 0))
        bottom.append(mesh.vertex(x, y, center_z - height / 2, i / sides, 0, cos(angle), sin(angle), 0))
    for i in range(sides):
        mesh.face(bottom[i], bottom[(i + 1) % sides], top[(i + 1) % sides], top[i])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    mesh = Obj()
    blade = [(-15, 22), (-18, 31), (-18, 126), (-15, 153), (-10, 174),
             (-4, 192), (7, 184), (15, 160), (18, 131), (18, 37),
             (14, 21), (7, 13), (-6, 14)]
    core = [(-5, 28), (-7, 65), (-4, 110), (-6, 143), (0, 177), (6, 148),
            (4, 111), (7, 76), (4, 29)]
    guard = [(-39, 7), (-37, 0), (-24, -2), (-10, 7), (-6, 11), (6, 11),
             (10, 7), (24, -2), (37, 0), (39, 7), (28, 16), (9, 18),
             (0, 14), (-9, 18), (-28, 16)]
    collar = [(-8, -2), (-9, 5), (-6, 12), (6, 12), (9, 5), (8, -2),
              (4, -5), (-4, -5)]

    prism(mesh, blade, -3.6, 3.6, "RiftSteel")
    prism(mesh, core, -3.82, -3.63, "RiftGlow")
    prism(mesh, [(-15, 40), (-9, 53), (-8, 102), (-13, 118), (-16, 105)], -3.86, -3.67, "ForgePlate")
    prism(mesh, [(15, 45), (9, 58), (8, 105), (13, 124), (16, 106)], -3.86, -3.67, "ForgePlate")
    prism(mesh, guard, -4.8, 4.8, "ForgePlate")
    prism(mesh, collar, -4.0, 4.0, "Bronze")
    cylinder(mesh, 3.25, 3.25, -25, 42, "Leather")
    cylinder(mesh, 4.5, 4.5, -4, 5, "Bronze")
    cylinder(mesh, 4.7, 4.7, -47, 5, "Bronze")
    prism(mesh, [(-9, -52), (-8, -61), (-3, -69), (4, -69), (9, -61), (8, -52), (3, -47), (-3, -47)], -5.3, 5.3, "ForgePlate")
    prism(mesh, [(-2.7, -55), (-4.3, -60), (0, -66), (4.3, -60), (2.7, -55), (0, -52)], -5.55, -5.34, "RiftGlow")

    (OUT / f"{NAME}.obj").write_text("\n".join(mesh.lines) + "\n", encoding="ascii")
    (OUT / f"{NAME}.mtl").write_text("""newmtl RiftSteel
Kd 0.055 0.070 0.090
Ks 0.45 0.55 0.62
Ns 620

newmtl ForgePlate
Kd 0.11 0.12 0.14
Ks 0.30 0.34 0.40
Ns 420

newmtl RiftGlow
Kd 0.02 0.18 0.30
Ke 0.00 0.28 0.72
Ns 850

newmtl Leather
Kd 0.025 0.020 0.019
Ks 0.05 0.04 0.03
Ns 90

newmtl Bronze
Kd 0.18 0.10 0.035
Ks 0.45 0.25 0.06
Ns 300
""", encoding="ascii")
    print(f"{NAME}: vertices={mesh.v} uvs={mesh.vt} normals={mesh.vn}")


if __name__ == "__main__":
    main()
