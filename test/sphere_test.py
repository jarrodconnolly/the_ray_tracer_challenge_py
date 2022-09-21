""" Sphere Tests """
from math import sqrt, pi
import ray as Ray

class TestSphere:
  """ features/spheres.feature """

  def test_sphere_intersect(self):
    """ A ray intersects a sphere at two points """
    r = Ray.Ray(Ray.Point(0, 0, -5), Ray.Vector(0, 0, 1))
    s = Ray.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == 4.0
    assert xs[1].t == 6.0

  def test_sphere_intersect_tangent(self):
    """ A ray intersects a sphere at a tangent """
    r = Ray.Ray(Ray.Point(0, 1, -5), Ray.Vector(0, 0, 1))
    s = Ray.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == 5.0
    assert xs[1].t == 5.0

  def test_sphere_intersect_misses(self):
    """ A ray misses a sphere """
    r = Ray.Ray(Ray.Point(0, 2, -5), Ray.Vector(0, 0, 1))
    s = Ray.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 0

  def test_sphere_intersect_inside(self):
    """ A ray originates inside a sphere """
    r = Ray.Ray(Ray.Point(0, 0, 0), Ray.Vector(0, 0, 1))
    s = Ray.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == -1.0
    assert xs[1].t == 1.0

  def test_sphere_intersect_behind(self):
    """ A sphere is behind a ray """
    r = Ray.Ray(Ray.Point(0, 0, 5), Ray.Vector(0, 0, 1))
    s = Ray.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == -6.0
    assert xs[1].t == -4.0

  def test_sphere_intersect_set_object(self):
    """ Intersect sets the object on the intersection """
    r = Ray.Ray(Ray.Point(0, 0, -5), Ray.Vector(0, 0, 1))
    s = Ray.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].object == s
    assert xs[1].object == s

  def test_sphere_default_transform(self):
    """ A sphere's default transformation """
    s = Ray.Sphere()
    assert s.transform == Ray.Matrix.identity()

  def test_sphere_change_transform(self):
    """ Changing a sphere's transformation """
    s = Ray.Sphere()
    t = Ray.Matrix.translation(2, 3, 4)
    s.transform = t
    assert s.transform == t
    s2 = Ray.Sphere(t)
    assert s2.transform == t

  def test_sphere_intersect_scaled(self):
    """ Intersecting a scaled sphere with a ray """
    r = Ray.Ray(Ray.Point(0, 0, -5), Ray.Vector(0, 0, 1))
    s = Ray.Sphere(Ray.Matrix.scaling(2, 2, 2))
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].t == 3
    assert xs[1].t == 7

  def test_sphere_intersect_translated(self):
    """ Intersecting a translated sphere with a ray """
    r = Ray.Ray(Ray.Point(0, 0, -5), Ray.Vector(0, 0, 1))
    s = Ray.Sphere(Ray.Matrix.translation(5, 0, 0))
    xs = s.intersect(r)
    assert len(xs) == 0

  def test_sphere_normal_x(self):
    """ The normal on a sphere at a point on the x axis """
    s = Ray.Sphere()
    n = s.normal_at(Ray.Point(1, 0, 0))
    assert n == Ray.Vector(1, 0, 0)

  def test_sphere_normal_y(self):
    """ The normal on a sphere at a point on the y axis """
    s = Ray.Sphere()
    n = s.normal_at(Ray.Point(0, 1, 0))
    assert n == Ray.Vector(0, 1, 0)

  def test_sphere_normal_z(self):
    """ The normal on a sphere at a point on the z axis """
    s = Ray.Sphere()
    n = s.normal_at(Ray.Point(0, 0, 1))
    assert n == Ray.Vector(0, 0, 1)

  def test_sphere_normal_nonaxial(self):
    """ The normal on a sphere at a nonaxial point """
    s = Ray.Sphere()
    n = s.normal_at(Ray.Point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3))
    assert n == Ray.Vector(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3)

  def test_sphere_normal_normalized(self):
    """ The normal is a normalized vector """
    s = Ray.Sphere()
    n = s.normal_at(Ray.Point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3))
    assert n == n.normalize()

  def test_sphere_normal_translated(self):
    """ Computing the normal on a translated sphere """
    s = Ray.Sphere(Ray.Matrix.translation(0, 1, 0))
    n = s.normal_at(Ray.Point(0, 1.70711, -0.70711))
    assert n == Ray.Vector(0, 0.70711, -0.70711)

  def test_sphere_normal_transformed(self):
    """ Computing the normal on a transformed sphere """
    s = Ray.Sphere(Ray.Matrix.scaling(1, 0.5, 1) * Ray.Matrix.rotation_z(pi / 5))
    n = s.normal_at(Ray.Point(0, sqrt(2) / 2, -sqrt(2) / 2))
    assert n == Ray.Vector(0, 0.97014, -0.24254)

  def test_sphere_default_material(self):
    """ A sphere has a default material """
    s = Ray.Sphere()
    m = s.material
    assert m == Ray.Material()

  def test_sphere_assign_material(self):
    """ A sphere may be assigned a material """
    s = Ray.Sphere()
    m = Ray.Material()
    m.ambient = 1
    s.material = m
    assert s.material == m
