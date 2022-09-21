""" World Tests """
from rt.colour import Colour
from rt.light import PointLight
from rt.material import Material
from rt.matrix import Matrix
from rt.ray import Ray
from rt.sphere import Sphere
from rt.tuple import Point, Vector
from rt.world import World


class TestWorld:
  """ features/world.feature """

  def test_create_world(self):
    """ Creating a world """
    w = World()
    assert len(w.objects) == 0
    assert len(w.lights) == 0

  def test_default_world(self):
    """ The default world """
    w = World.DefaultWorld()
    assert w.lights[0] == PointLight(Point(-10, 10, -10), Colour(1, 1, 1))

    assert w.objects[0] == Sphere(material=Material(
      colour=Colour(0.8, 1.0, 0.6),
      diffuse=0.7,
      specular=0.2))

    assert w.objects[1] == Sphere(transform=Matrix.scaling(0.5, 0.5, 0.5))

  def test_intersect_world_ray(self):
    """ Intersect a world with a ray """
    w = World.DefaultWorld()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = w.intersect(r)

    assert len(xs) == 4
    assert xs[0].t == 4
    assert xs[1].t == 4.5
    assert xs[2].t == 5.5
    assert xs[3].t == 6
