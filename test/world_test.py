""" World Tests """
from rt.colour import Colour
from rt.intersection import Intersection
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

  def test_shading_intersection(self):
    """ Shading an intersection """
    w = World.DefaultWorld()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = w.objects[0]
    i = Intersection(4, shape)
    comps = i.prepare_computations(r)
    c = w.shade_hit(comps)
    assert c == Colour(0.38066, 0.47583, 0.2855)

  def test_shading_intersection_inside(self):
    """ Shading an intersection from the inside """
    w = World.DefaultWorld()
    w.lights[0] = PointLight(Point(0, 0.25, 0), Colour(1, 1, 1))
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = w.objects[1]
    i = Intersection(0.5, shape)
    comps = i.prepare_computations(r)
    c = w.shade_hit(comps)
    assert c == Colour(0.90498, 0.90498, 0.90498)

  def test_colour_ray_miss(self):
    """ The color when a ray misses """
    w = World.DefaultWorld()
    r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
    c = w.colour_at(r)
    assert c == Colour(0, 0, 0)

  def test_colour_ray_hit(self):
    """ The color when a ray hits """
    w = World.DefaultWorld()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    c = w.colour_at(r)
    assert c == Colour(0.38066, 0.47583, 0.2855)

  def test_intersection_behind_ray(self):
    """ The color with an intersection behind the ray """
    w = World.DefaultWorld()
    outer = w.objects[0]
    outer.material.ambient = 1
    inner = w.objects[1]
    inner.material.ambient = 1
    r = Ray(Point(0, 0, 0.75), Vector(0, 0, -1))
    c = w.colour_at(r)
    assert c == inner.material.colour
