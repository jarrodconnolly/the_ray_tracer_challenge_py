""" Putting It Together - Chapter 12 """

import math

from rt.camera import Camera
from rt.colour import Colour
from rt.cube import Cube
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
  floor.transform = Matrix.translation(0, -1, 0)
  floor.material = Material()
  floor.material.colour = Colour(1, 0.9, 0.9)

  world = World()
  world.lights.append(PointLight(Point(-10, 10, -10), Colour(1, 1, 1)))
  world.objects = [floor]

  s1 = Sphere()
  s1.transform = Matrix.scaling(4, 4, 4) * Matrix.translation(0, 0, 0)
  s1.material.colour = Colour(0, 0, 0.6)
  s1.material.diffuse = 0.1
  s1.material.specular = 0.9
  s1.material.shininess = 300
  s1.material.reflective = 0.9

  s1.material.transparency = 0.9
  s1.material.refractive_index = 1.0000034

  world.objects.append(s1)

  for i in range(0, 12):
    cube1 = Cube()
    cube1.transform =  Matrix.rotation_y((math.pi / 6) * i) * Matrix.translation(5, 0, 0)
    c = (1 / 16) * (i + 1)
    cube1.material.colour = Colour(0.2, 0, c)
    cube1.material.diffuse = 0.9
    cube1.material.ambient = 0.25
    cube1.material.specular = 0.35
    world.objects.append(cube1)

  camera = Camera(512, 512, math.pi / 3)
  camera.transform = Point(0, 6, -10).view_transform(Point(0, 1, 0), Vector(0, 1, 0))

  canvas = camera.render(world)

  with open("chapter_12.ppm", "w", encoding="utf-8") as ppm_file:
    canvas.canvas_to_ppm(ppm_file)

if __name__ == '__main__':
  run()
