""" Putting It Together - Chapter 11-Reflection """

import math

from rt.camera import Camera
from rt.colour import Colour
from rt.light import PointLight
from rt.material import Material
from rt.matrix import Matrix
from rt.plane import Plane
from rt.sphere import Sphere
from rt.tuple import Point, Vector
from rt.world import World


def run():
  """ main entrypoint """
  floor = Plane()
  floor.transform = Matrix.translation(0, 0, 0)
  floor.material = Material()
  floor.material.colour = Colour(1, 0.9, 0.9)
  floor.material.specular = 0

  middle = Sphere()
  middle.transform = Matrix.translation(-0.5, 1, 0.5)
  middle.material = Material()
  middle.material.colour = Colour(0, 0, 1)
  middle.material.diffuse = 0.5
  middle.material.specular = 0.75
  middle.material.reflective = 0.75

  right = Sphere()
  right.transform = Matrix.translation(1.5, 0.5, -0.5) * Matrix.scaling(0.5, 0.5, 0.5)
  right.material = Material()
  right.material.colour = Colour(0, 1, 0)
  right.material.diffuse = 0.8
  right.material.specular = 0.25

  left = Sphere()
  left.transform = Matrix.translation(1, 0.33, -0.75) * Matrix.scaling(0.33, 0.33, 0.33)
  left.material = Material()
  left.material.colour = Colour(1, 0, 0)
  left.material.diffuse = 0.8
  left.material.specular = 0.25

  world = World()
  world.lights.append(PointLight(Point(-10, 10, -10), Colour(1, 1, 1)))
  world.objects = [floor, middle, right, left]

  camera = Camera(512, 512, math.pi / 3)
  camera.transform = Point(0, 1.5, -5).view_transform(Point(0, 1, 0), Vector(0, 1, 0))

  canvas = camera.render(world)

  with open("chapter_11-Reflection.ppm", "w", encoding="utf-8") as ppm_file:
    canvas.canvas_to_ppm(ppm_file)

if __name__ == '__main__':
  run()
