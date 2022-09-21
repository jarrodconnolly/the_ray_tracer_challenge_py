""" Tuple, Point, Vector Tests """
from math import sqrt
import ray as Ray

class TestTuple:
  """ features/tuples.feature """

  def test_point(self):
    """ A tuple with w=1.0 is a point """
    a = Ray.Tuple(4.3, -4.2, 3.1, 1.0)
    assert a.x == 4.3
    assert a.y == -4.2
    assert a.z == 3.1
    assert a.w == 1.0

  def test_vector(self):
    """ A tuple with w=0 is a vector """
    a = Ray.Tuple(4.3, -4.2, 3.1, 0.0)
    assert a.x == 4.3
    assert a.y == -4.2
    assert a.z == 3.1
    assert a.w == 0.0

  def test_helper_point(self):
    """ point() creates tuples with w=1 """
    p = Ray.Point(4, -4, 3)
    assert p == Ray.Tuple(4, -4, 3, 1)

  def test_helper_vector(self):
    """ vector() creates tuples with w=0 """
    v = Ray.Vector(4, -4, 3)
    assert v == Ray.Tuple(4, -4, 3, 0)

  def test_add(self):
    """ Adding two tuples """
    a1 = Ray.Tuple(3, -2, 5, 1)
    a2 = Ray.Tuple(-2, 3, 1, 0)
    assert a1 + a2 == Ray.Tuple(1, 1, 6, 1)

  def test_subtract_points(self):
    """ Subtracting two points """
    p1 = Ray.Point(3, 2, 1)
    p2 = Ray.Point(5, 6, 7)
    assert p1 - p2 == Ray.Vector(-2, -4, -6)

  def test_subtract_vector_point(self):
    """ Subtracting a vector from a point """
    p = Ray.Point(3, 2, 1)
    v = Ray.Vector(5, 6, 7)
    assert p - v == Ray.Point(-2, -4, -6)

  def test_subtract_vectors(self):
    """ Subtracting two vectors """
    v1 = Ray.Vector(3, 2, 1)
    v2 = Ray.Vector(5, 6, 7)
    assert v1 - v2 == Ray.Vector(-2, -4, -6)

  def test_subtract_zero_vector(self):
    """ Subtracting a vector from the zero vector """
    zero = Ray.Vector(0, 0, 0)
    v = Ray.Vector(1, -2, 3)
    assert zero - v == Ray.Vector(-1, 2, -3)

  def test_negate_tuple(self):
    """ Negating a tuple """
    a = Ray.Tuple(1, -2, 3, -4)
    assert -a == Ray.Tuple(-1, 2, -3, 4)

  def test_multiply_tuple_scalar(self):
    """ Multiplying a tuple by a scalar """
    a = Ray.Tuple(1, -2, 3, -4)
    assert a * 3.5 == Ray.Tuple(3.5, -7, 10.5, -14)

  def test_multiply_tuple_fraction(self):
    """ Multiplying a tuple by a fraction """
    a = Ray.Tuple(1, -2, 3, -4)
    assert a * 0.5 == Ray.Tuple(0.5, -1, 1.5, -2)

  def test_divide_tuple_scalar(self):
    """ Dividing a tuple by a scalar """
    a = Ray.Tuple(1, -2, 3, -4)
    assert a / 2 == Ray.Tuple(0.5, -1, 1.5, -2)

  def test_magnitude_vector_1_0_0(self):
    """ Computing the magnitude of vector(1, 0, 0) """
    v = Ray.Vector(1, 0, 0)
    assert v.magnitude() == 1

  def test_magnitude_vector_0_1_0(self):
    """ Computing the magnitude of vector(0, 1, 0) """
    v = Ray.Vector(0, 1, 0)
    assert v.magnitude() == 1

  def test_magnitude_vector_0_0_1(self):
    """ Computing the magnitude of vector(0, 0, 1) """
    v = Ray.Vector(0, 0, 1)
    assert v.magnitude() == 1

  def test_magnitude_vector_1_2_3(self):
    """ Computing the magnitude of vector(1, 2, 3) """
    v = Ray.Vector(1, 2, 3)
    assert v.magnitude() == sqrt(14)

  def test_magnitude_vector_n1_n2_n3(self):
    """ Computing the magnitude of vector(-1, -2, -3) """
    v = Ray.Vector(-1, -2, -3)
    assert v.magnitude() == sqrt(14)

  def test_normalize_vector_4_0_0(self):
    """ Normalizing vector(4, 0, 0) gives (1, 0, 0) """
    v = Ray.Vector(4, 0, 0)
    assert v.normalize() == Ray.Vector(1, 0, 0)

  def test_normalize_vector_1_2_3(self):
    """ Normalizing vector(1, 2, 3) """
    v = Ray.Vector(1, 2, 3)
    assert v.normalize() == Ray.Vector(1/sqrt(14), 2/sqrt(14), 3/sqrt(14))

  def test_dot_product_tuples(self):
    """ The dot product of two tuples """
    a = Ray.Vector(1, 2, 3)
    b = Ray.Vector(2, 3, 4)
    assert a.dot(b) == 20

  def test_cross_product_vectors(self):
    """ The cross product of two vectors """
    a = Ray.Vector(1, 2, 3)
    b = Ray.Vector(2, 3, 4)
    assert a.cross(b) == Ray.Vector(-1, 2, -1)
    assert b.cross(a) == Ray.Vector(1, -2, 1)

  def test_reflect_vector_45(self):
    """ Reflecting a vector approaching at 45° """
    v = Ray.Vector(1, -1, 0)
    n = Ray.Vector(0, 1, 0)
    r = v.reflect(n)
    assert r == Ray.Vector(1, 1, 0)

  def test_reflect_vector_slanted(self):
    """ Reflecting a vector off a slanted surface """
    v = Ray.Vector(0, -1, 0)
    n = Ray.Vector(sqrt(2) / 2, sqrt(2) / 2, 0)
    r = v.reflect(n)
    assert r == Ray.Vector(1, 0, 0)
