""" Putting It Together - Chapter 7 """
from rt.camera import Camera
from rt.colour import Colour
from rt.light import PointLight
from rt.matrix import Matrix
from rt.pattern import Checker
from rt.plane import Plane
from rt.sphere import Sphere
from rt.tuple import Point, Vector
from rt.world import World


def run():
  """ main entrypoint """
  wall = Plane()
  wall.transform = Matrix.translation(0, 0, 10) * Matrix.rotation_x(1.5708)
  wall.material.pattern = Checker(Colour(0.15, 0.15, 0.15), Colour(0.85, 0.85, 0.85))
  wall.material.ambient = 0.8
  wall.material.diffuse = 0.2
  wall.material.specular = 0

  bigger = Sphere()
  bigger.material.colour = Colour(1, 1, 1)
  bigger.material.ambient = 0
  bigger.material.diffuse = 0
  bigger.material.specular = 0.9
  bigger.material.shininess = 300
  bigger.material.reflective = 0.9
  bigger.material.transparency = 0.9
  bigger.material.refractive_index = 1.5

  smaller = Sphere()
  smaller.transform = Matrix.scaling(0.5, 0.5, 0.5)
  smaller.material.colour = Colour(1, 1, 1)
  smaller.material.ambient = 0
  smaller.material.diffuse = 0
  smaller.material.specular = 0.9
  smaller.material.shininess = 300
  smaller.material.reflective = 0.9
  smaller.material.transparency = 0.9
  smaller.material.refractive_index = 1.0000034

  world = World()
  world.lights.append(PointLight(Point(2, 10, -5), Colour(0.9, 0.9, 0.9)))
  world.objects = [wall, bigger, smaller]

  camera = Camera(512, 512, 0.45)
  camera.transform = Point(0, 0, -5).view_transform(Point(0, 0, 0), Vector(0, 1, 0))

  canvas = camera.render(world)
  #camera.single_pixel(world, 125, 125)

  with open("chapter_11-Refraction.ppm", "w", encoding="utf-8") as ppm_file:
    canvas.canvas_to_ppm(ppm_file)

if __name__ == '__main__':
  run()
