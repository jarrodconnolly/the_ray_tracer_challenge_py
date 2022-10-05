""" Sphere Tests """
from math import pi, sqrt

from rt.material import Material
from rt.matrix import Matrix
from rt.ray import Ray
from rt.sphere import Sphere, UnitTestGlassSphere
from rt.tuple import Point, Vector


class TestSphere:
  """ features/spheres.feature """

  def test_sphere_intersect(self):
    """ A ray intersects a sphere at two points """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == 4.0
    assert xs[1].t == 6.0

  def test_sphere_intersect_tangent(self):
    """ A ray intersects a sphere at a tangent """
    r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
    s = Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == 5.0
    assert xs[1].t == 5.0

  def test_sphere_intersect_misses(self):
    """ A ray misses a sphere """
    r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
    s = Sphere()
    xs = s.intersect(r)
    assert len(xs) == 0

  def test_sphere_intersect_inside(self):
    """ A ray originates inside a sphere """
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    s = Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == -1.0
    assert xs[1].t == 1.0

  def test_sphere_intersect_behind(self):
    """ A sphere is behind a ray """
    r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
    s = Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == -6.0
    assert xs[1].t == -4.0

  def test_sphere_intersect_set_object(self):
    """ Intersect sets the object on the intersection """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].object == s
    assert xs[1].object == s

  def test_sphere_default_transform(self):
    """ A sphere's default transformation """
    s = Sphere()
    assert s.transform == Matrix.identity()

  def test_sphere_change_transform(self):
    """ Changing a sphere's transformation """
    s = Sphere()
    t = Matrix.translation(2, 3, 4)
    s.transform = t
    assert s.transform == t
    s2 = Sphere(t)
    assert s2.transform == t

  def test_sphere_intersect_scaled(self):
    """ Intersecting a scaled sphere with a ray """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere(Matrix.scaling(2, 2, 2))
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == 3
    assert xs[1].t == 7

  def test_sphere_intersect_translated(self):
    """ Intersecting a translated sphere with a ray """
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere(Matrix.translation(5, 0, 0))
    xs = s.intersect(r)
    assert len(xs) == 0

  def test_sphere_normal_x(self):
    """ The normal on a sphere at a point on the x axis """
    s = Sphere()
    n = s.normal_at(Point(1, 0, 0))
    assert n == Vector(1, 0, 0)

  def test_sphere_normal_y(self):
    """ The normal on a sphere at a point on the y axis """
    s = Sphere()
    n = s.normal_at(Point(0, 1, 0))
    assert n == Vector(0, 1, 0)

  def test_sphere_normal_z(self):
    """ The normal on a sphere at a point on the z axis """
    s = Sphere()
    n = s.normal_at(Point(0, 0, 1))
    assert n == Vector(0, 0, 1)

  def test_sphere_normal_nonaxial(self):
    """ The normal on a sphere at a nonaxial point """
    s = Sphere()
    n = s.normal_at(Point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3))
    assert n == Vector(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3)

  def test_sphere_normal_normalized(self):
    """ The normal is a normalized vector """
    s = Sphere()
    n = s.normal_at(Point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3))
    assert n == n.normalize()

  def test_sphere_normal_translated(self):
    """ Computing the normal on a translated sphere """
    s = Sphere(Matrix.translation(0, 1, 0))
    n = s.normal_at(Point(0, 1.70711, -0.70711))
    assert n == Vector(0, 0.70711, -0.70711)

  def test_sphere_normal_transformed(self):
    """ Computing the normal on a transformed sphere """
    s = Sphere(Matrix.scaling(1, 0.5, 1) * Matrix.rotation_z(pi / 5))
    n = s.normal_at(Point(0, sqrt(2) / 2, -sqrt(2) / 2))
    assert n == Vector(0, 0.97014, -0.24254)

  def test_sphere_default_material(self):
    """ A sphere has a default material """
    s = Sphere()
    m = s.material
    assert m == Material()

  def test_sphere_assign_material(self):
    """ A sphere may be assigned a material """
    s = Sphere()
    m = Material()
    m.ambient = 1
    s.material = m
    assert s.material == m

  def test_sphere_helper(self):
    """ A helper for producing a sphere with a glassy material """
    s = UnitTestGlassSphere()
    assert s.transform == Matrix.identity()
    assert s.material.transparency == 1.0
    assert s.material.refractive_index == 1.5
