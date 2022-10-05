""" Intersection Tests """
import math

from rt.helpers import EPSILON
from rt.intersection import Intersection, Intersections
from rt.matrix import Matrix
from rt.plane import Plane
from rt.ray import Ray
from rt.sphere import Sphere, UnitTestGlassSphere
from rt.tuple import Point, Vector


class TestIntersection:
  """ features/intersections.feature """

  def test_intersection(self):
    """ An intersection encapsulates t and object """
    s = Sphere()
    i = Intersection(3.5, s)
    assert i.t == 3.5
    assert i.object == s

  def test_intersections(self):
    """ Aggregating intersections """
    s = Sphere()
    i1 = Intersection(1, s)
    i2 = Intersection(2, s)
    xs = Intersections(i1, i2)
    assert len(xs) == 2
    assert xs[0].t  == 1
    assert xs[1].t == 2

  def test_hit_intersections_positive(self):
    """ The hit, when all intersections have positive t """
    s = Sphere()
    i1 = Intersection(1, s)
    i2 = Intersection(2, s)
    xs = Intersections(i2, i1)
    i = xs.hit()
    assert i == i1

  def test_hit_intersections_some_negative(self):
    """ The hit, when some intersections have negative t """
    s = Sphere()
    i1 = Intersection(-1, s)
    i2 = Intersection(2, s)
    xs = Intersections(i2, i1)
    i = xs.hit()
    assert i == i2

  def test_hit_intersections_all_negative(self):
    """ The hit, when all intersections have negative t """
    s = Sphere()
    i1 = Intersection(-2, s)
    i2 = Intersection(-1, s)
    xs = Intersections(i2, i1)
    i = xs.hit()
    assert i is None

  def test_hit_intersections_lowest_non_negative(self):
    """ The hit is always the lowest nonnegative intersection """
    s = Sphere()
    i1 = Intersection(5, s)
    i2 = Intersection(7, s)
    i3 = Intersection(-3, s)
    i4 = Intersection(2, s)
    xs = Intersections(i1, i2, i3, i4)
    i = xs.hit()
    assert i == i4

  def test_precompute_intersection(self):
    """ Precomputing the state of an intersection """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = i.prepare_computations(r)
    assert comps.t == i.t
    assert comps.object == i.object
    assert comps.point == Point(0, 0, -1)
    assert comps.eyev == Vector(0, 0, -1)
    assert comps.normalv == Vector(0, 0, -1)

  def test_hit_intersection_outside(self):
    """ The hit, when an intersection occurs on the outside """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = i.prepare_computations(r)
    assert comps.inside is False

  def test_hit_intersection_inside(self):
    """ The hit, when an intersection occurs on the inside """
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(1, shape)
    comps = i.prepare_computations(r)
    assert comps.point == Point(0, 0, 1)
    assert comps.eyev == Vector(0, 0, -1)
    assert comps.inside is True
    assert comps.normalv == Vector(0, 0, -1)

  def test_hit_offset_point(self):
    """ The hit should offset the point """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    shape.transform = Matrix.translation(0, 0, 1)
    i = Intersection(5, shape)
    comps = i.prepare_computations(r)
    assert comps.over_point.z < -EPSILON / 2
    assert comps.point.z > comps.over_point.z

  def test_precompute_reflection_vector(self):
    """ Precomputing the reflection vector """
    shape = Plane()
    r = Ray(Point(0, 1, -1), Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))
    i = Intersection(math.sqrt(2), shape)
    comps = i.prepare_computations(r)
    assert comps.reflectv == Vector(0, math.sqrt(2) / 2, math.sqrt(2) / 2)

  def test_n1_n2_intersections(self):
    """ Finding n1 and n2 at various intersections """
    a = UnitTestGlassSphere()
    a.transform = Matrix.scaling(2, 2, 2)
    a.material.refractive_index = 1.5

    b = UnitTestGlassSphere()
    b.transform = Matrix.translation(0, 0, -0.25)
    b.material.refractive_index = 2.0

    c = UnitTestGlassSphere()
    c.transform = Matrix.translation(0, 0, 0.25)
    c.material.refractive_index = 2.5

    r = Ray(Point(0, 0, -4), Vector(0, 0, 1))
    xs = Intersections(
      Intersection(2, a),
      Intersection(2.75, b),
      Intersection(3.25, c),
      Intersection(4.75, b),
      Intersection(5.25, c),
      Intersection(6, a)
    )

    testValues = [
        [1.0, 1.5],
        [1.5, 2.0],
        [2.0, 2.5],
        [2.5, 2.5],
        [2.5, 1.5],
        [1.5, 1.0],
      ]

    for idx, test in enumerate(testValues):
      comps = xs[idx].prepare_computations(r, xs)
      assert comps.n1 == test[0]
      assert comps.n2 == test[1]

  def test_hit_offset_under_point(self):
    """ The under point is offset below the surface """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    shape.transform = Matrix.translation(0, 0, 1)
    i = Intersection(5, shape)
    comps = i.prepare_computations(r)
    assert comps.under_point.z > -EPSILON / 2
    assert comps.point.z < comps.under_point.z

  def test_schlick_total_internal_reflection(self):
    """ The Schlick approximation under total internal reflection """
    shape = UnitTestGlassSphere()
    r = Ray(Point(0, 0, math.sqrt(2) / 2), Vector(0, 1, 0))
    xs = Intersections(
      Intersection(-math.sqrt(2) / 2, shape),
      Intersection(math.sqrt(2) / 2, shape)
    )
    comps = xs[1].prepare_computations(r, xs)
    reflectance = comps.schlick()
    assert reflectance == 1.0

  def test_schlick_perpendicular(self):
    """ The Schlick approximation with a perpendicular viewing angle """
    shape = UnitTestGlassSphere()
    r = Ray(Point(0, 0, 0), Vector(0, 1, 0))
    xs = Intersections(
      Intersection(-1, shape),
      Intersection(1, shape)
    )
    comps = xs[1].prepare_computations(r, xs)
    reflectance = comps.schlick()
    assert math.isclose(reflectance, 0.04)

  def test_schlick_small_angle(self):
    """ The Schlick approximation with small angle and n2 > n1 """
    shape = UnitTestGlassSphere()
    r = Ray(Point(0, 0.99, -2), Vector(0, 0, 1))
    xs = Intersections(
      Intersection(1.8589, shape)
    )
    comps = xs[0].prepare_computations(r, xs)
    reflectance = comps.schlick()
    assert math.isclose(reflectance, 0.48873, abs_tol=0.00001)
