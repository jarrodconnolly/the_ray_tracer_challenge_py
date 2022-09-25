""" Shape Tests """

from math import pi, sqrt

from rt.material import Material
from rt.matrix import Matrix
from rt.ray import Ray
from rt.shape import UnitTestShape
from rt.tuple import Point, Vector


class TestShape:
  """ features/shapes.feature """

  def test_default_transform(self):
    """ The default transformation """
    s = UnitTestShape()
    assert s.transform == Matrix.identity()

  def test_assign_transform(self):
    """ Assigning a transformation """
    s = UnitTestShape()
    s.transform = Matrix.translation(2, 3, 4)
    assert s.transform == Matrix.translation(2, 3, 4)

  def test_default_material(self):
    """ The default material """
    s = UnitTestShape()
    assert s.material == Material()

  def test_assign_material(self):
    """ Assigning a material """
    s = UnitTestShape()
    m = Material()
    m.ambient = 1

    s.material = m
    assert s.material == m

  def test_intersect_scaled_shape_ray(self):
    """ Intersecting a scaled shape with a ray """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = UnitTestShape()
    s.transform = Matrix.scaling(2, 2, 2)
    s.intersect(r)
    assert s.saved_ray.origin == Point(0, 0, -2.5)
    assert s.saved_ray.direction == Vector(0, 0, 0.5)

  def test_intersect_translate_shape_ray(self):
    """ Intersecting a translated shape with a ray """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = UnitTestShape()
    s.transform = Matrix.translation(5, 0, 0)
    s.intersect(r)
    assert s.saved_ray.origin == Point(-5, 0, -5)
    assert s.saved_ray.direction == Vector(0, 0, 1)

  def test_sphere_normal_translated(self):
    """ Computing the normal on a translated shape """
    s = UnitTestShape()
    s.transform = Matrix.translation(0, 1, 0)
    n = s.normal_at(Point(0, 1.70711, -0.70711))
    assert n == Vector(0, 0.70711, -0.70711)

  def test_sphere_normal_transformed(self):
    """ Computing the normal on a transformed shape """
    s = UnitTestShape()
    s.transform = Matrix.scaling(1, 0.5, 1) * Matrix.rotation_z(pi / 5)
    n = s.normal_at(Point(0, sqrt(2) / 2, -sqrt(2) / 2))
    assert n == Vector(0, 0.97014, -0.24254)
