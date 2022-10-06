""" Putting It Together - Chapter 10 """

import math

from rt.camera import Camera
from rt.colour import Colour
from rt.light import PointLight
from rt.matrix import Matrix
from rt.pattern import Checker, Gradient, Ring, Stripe
from rt.plane import Plane
from rt.sphere import Sphere
from rt.tuple import Point, Vector
from rt.world import World


def run():
  """ main entrypoint """
  floor = Plane()
  floor.material.pattern = Ring(Colour.White(), Colour.Black())
  floor.material.pattern.transform = Matrix.scaling(0.25, 1, 0.25)
  floor.material.specular = 0

  wall = Plane()
  wall.transform = Matrix.translation(0, 0, 2) * Matrix.rotation_x(math.pi / 2)
  wall.material.pattern = Gradient(Colour(0.2, 0.2, 1), Colour(0, 0, 0))
  wall.material.pattern.transform = Matrix.scaling(1, 1, 5) * Matrix.rotation_y(math.pi / 2)
  wall.material.specular = 0

  middle = Sphere()
  middle.transform = Matrix.translation(-0.5, 1, 0.5) * Matrix.rotation_z(math.pi / 3)
  middle.material.pattern = Stripe(Colour(1, 0.08, 0.58), Colour(0.54, 0.17, 0.89))
  middle.material.pattern.transform = Matrix.scaling(0.125, 1, 1)
  middle.material.diffuse = 0.9
  middle.material.specular = 0.75

  right = Sphere()
  right.transform = Matrix.translation(1.5, 1.5, -1) * Matrix.scaling(0.5, 1.5, 0.5)
  right.material.pattern = Gradient(Colour(1, 0, 0), Colour(0, 1, 0))
  right.material.pattern.transform = Matrix.rotation_z(math.pi / 2) * Matrix.scaling(2, 1, 1) * Matrix.translation(-0.5, 0, 0)
  right.material.diffuse = 0.7
  right.material.specular = 0.3

  left = Sphere()
  left.transform = Matrix.translation(-1.5, 0.25, -0.75) * Matrix.scaling(0.75, 0.75, 0.75)
  left.material.pattern = Checker(Colour(1, 0, 0), Colour(0, 1, 0), True)
  left.material.pattern.transform = Matrix.scaling(0.25, 0.25, 0.25)
  left.material.diffuse = 0.9
  left.material.specular = 0.1

  world = World()
  world.lights.append(PointLight(Point(-10, 10, -10), Colour(1, 1, 1)))
  world.objects = [floor, wall, middle, right, left]

  camera = Camera(512, 512, math.pi / 3)
  camera.transform = Point(0, 1.5, -5).view_transform(Point(0, 1, 0), Vector(0, 1, 0))

  canvas = camera.render(world)

  with open("chapter_10.ppm", "w", encoding="utf-8") as ppm_file:
    canvas.canvas_to_ppm(ppm_file)

if __name__ == '__main__':
  run()
