""" World Tests """
import math

from rt.colour import Colour
from rt.intersection import Intersection, Intersections
from rt.light import PointLight
from rt.material import Material
from rt.matrix import Matrix
from rt.pattern import UnitTestPattern
from rt.plane import Plane
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

  def test_no_shadow_collienear(self):
    """ There is no shadow when nothing is collinear with point and light """
    w = World.DefaultWorld()
    p = Point(0, 10, 0)
    assert w.is_shadowed(p) is False

  def test_shadow_between(self):
    """ The shadow when an object is between the point and the light """
    w = World.DefaultWorld()
    p = Point(10, -10, 10)
    assert w.is_shadowed(p) is True

  def test_no_shadow_behind_light(self):
    """ There is no shadow when an object is behind the light """
    w = World.DefaultWorld()
    p = Point(-20, 20, -20)
    assert w.is_shadowed(p) is False

  def test_no_shadow_behind_point(self):
    """ There is no shadow when an object is behind the point """
    w = World.DefaultWorld()
    p = Point(-2, 2, -2)
    assert w.is_shadowed(p) is False

  def test_shade_hit_shadow(self):
    """ shade_hit() is given an intersection in shadow """
    w = World()
    w.lights.append(PointLight(Point(0, 0, -10), Colour(1, 1, 1)))

    s1 = Sphere()
    w.objects.append(s1)

    s2 = Sphere()
    s2.transform = Matrix.translation(0, 0, 10)
    w.objects.append(s2)

    r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
    i = Intersection(4, s2)

    comps = i.prepare_computations(r)
    print(f"OP: {comps.over_point.x} {comps.over_point.y} {comps.over_point.z}")
    c = w.shade_hit(comps)
    print(f"Colour: {c.red} {c.green} {c.blue}")
    assert c == Colour(0.1, 0.1, 0.1)

  def test_reflected_nonreflective_material(self):
    """ The reflected color for a nonreflective material """
    w = World.DefaultWorld()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = w.objects[1]
    shape.material.ambient = 1
    i = Intersection(1, shape)
    comps = i.prepare_computations(r)
    colour = w.reflected_colour(comps)
    assert colour == Colour(0, 0, 0)

  def test_reflected_reflective_material(self):
    """ The reflected color for a reflective material """
    w = World.DefaultWorld()
    shape = Plane()
    shape.material.reflective = 0.5
    shape.transform = Matrix.translation(0, -1, 0)
    w.objects.append(shape)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
    i = Intersection(math.sqrt(2), shape)
    comps = i.prepare_computations(r)
    colour = w.reflected_colour(comps)
    assert colour == Colour(0.19032, 0.2379, 0.14274)

  def test_shade_hit_reflective_material(self):
    """ shade_hit() with a reflective material """
    w = World.DefaultWorld()
    shape = Plane()
    shape.material.reflective = 0.5
    shape.transform = Matrix.translation(0, -1, 0)
    w.objects.append(shape)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
    i = Intersection(math.sqrt(2), shape)
    comps = i.prepare_computations(r)
    colour = w.shade_hit(comps)
    assert colour == Colour(0.87677, 0.92436, 0.82918)

  def test_mutually_reflective(self):
    """ color_at() with mutually reflective surfaces """
    w = World()
    w.lights.append(PointLight(Point(0, 0, 0), Colour(1, 1, 1)))

    lower = Plane()
    lower.material.reflective = 1
    lower.transform = Matrix.translation(0, -1, 0)
    w.objects.append(lower)

    upper = Plane()
    upper.material.reflective = 1
    upper.transform = Matrix.translation(0, 1, 0)
    w.objects.append(upper)

    r = Ray(Point(0, 0, 0), Vector(0, 1, 0))
    w.colour_at(r) # calling to ensure this does not recurse infinitely

  def test_reflection_maximum_recursion(self):
    """ The reflected color at the maximum recursive depth """
    w = World()
    shape = Plane()
    shape.material.reflective = 0.5
    shape.transform = Matrix.translation(0, -1, 0)
    w.objects.append(shape)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
    i = Intersection(math.sqrt(2), shape)
    comps = i.prepare_computations(r)
    colour = w.reflected_colour(comps, 0)
    assert colour == Colour(0, 0, 0)

  def test_refract_opaque_surface(self):
    """ The refracted color with an opaque surface """
    w = World.DefaultWorld()
    shape = w.objects[0]
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = Intersections(Intersection(4, shape), Intersection(6, shape))
    comps = xs[0].prepare_computations(r, xs)
    c = w.refracted_colour(comps, 5)
    assert c == Colour(0, 0, 0)

  def test_refract_max_recurive(self):
    """ The refracted color at the maximum recursive depth """
    w = World.DefaultWorld()
    shape = w.objects[0]
    shape.material.transparency = 1.0
    shape.material.refractive_index = 1.5
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = Intersections(Intersection(4, shape), Intersection(6, shape))
    comps = xs[0].prepare_computations(r, xs)
    c = w.refracted_colour(comps, 0)
    assert c == Colour(0, 0, 0)

  def test_refract_total_internal_reflection(self):
    """ The refracted color under total internal reflection """
    w = World.DefaultWorld()
    shape = w.objects[0]
    shape.material.transparency = 1.0
    shape.material.refractive_index = 1.5
    r = Ray(Point(0, 0, math.sqrt(2) / 2), Vector(0, 1, 0))
    xs = Intersections(
      Intersection(-math.sqrt(2) / 2, shape),
      Intersection(math.sqrt(2) / 2, shape))
    comps = xs[1].prepare_computations(r, xs)
    c = w.refracted_colour(comps, 5)
    assert c == Colour(0, 0, 0)

  def test_refract_colour(self):
    """ The refracted color with a refracted ray """
    w = World.DefaultWorld()

    A = w.objects[0]
    A.material.ambient = 1.0
    A.material.pattern = UnitTestPattern()

    B = w.objects[1]
    B.material.transparency = 1.0
    B.material.refractive_index = 1.5

    r = Ray(Point(0, 0, 0.1), Vector(0, 1, 0))
    xs = Intersections(
      Intersection(-0.9899, A),
      Intersection(-0.4899, B),
      Intersection(0.4899, B),
      Intersection(0.9899, A))
    comps = xs[2].prepare_computations(r, xs)
    c = w.refracted_colour(comps, 5)
    assert c == Colour(0, 0.99888, 0.04725)

  def test_refract_shade_hit(self):
    """ shade_hit() with a transparent material """
    w = World.DefaultWorld()
    floor = Plane()
    floor.transform = Matrix.translation(0, -1, 0)
    floor.material.transparency = 0.5
    floor.material.refractive_index = 1.5
    w.objects.append(floor)

    ball = Sphere()
    ball.material.colour = Colour(1, 0, 0)
    ball.material.ambient = 0.5
    ball.transform = Matrix.translation(0, -3.5, -0.5)
    w.objects.append(ball)

    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
    xs = Intersections(Intersection(math.sqrt(2), floor))
    comps = xs[0].prepare_computations(r, xs)
    colour = w.shade_hit(comps, 5)
    assert colour == Colour(0.93642, 0.68642, 0.68642)

  def test_reflect_refract_shade_hit(self):
    """ shade_hit() with a reflective, transparent material """
    w = World.DefaultWorld()
    floor = Plane()
    floor.transform = Matrix.translation(0, -1, 0)
    floor.material.reflective = 0.5
    floor.material.transparency = 0.5
    floor.material.refractive_index = 1.5
    w.objects.append(floor)

    ball = Sphere()
    ball.material.colour = Colour(1, 0, 0)
    ball.material.ambient = 0.5
    ball.transform = Matrix.translation(0, -3.5, -0.5)
    w.objects.append(ball)

    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
    xs = Intersections(Intersection(math.sqrt(2), floor))
    comps = xs[0].prepare_computations(r, xs)
    colour = w.shade_hit(comps, 5)
    assert colour == Colour(0.93391, 0.69643, 0.69243)
