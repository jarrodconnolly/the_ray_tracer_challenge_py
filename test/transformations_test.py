""" Transformation Tests """
import math
import ray as Ray

class TestTransformations:
  """ features/transformations.feature """

  def test_multiply_transform_matrix(self):
    """ Multiplying by a translation matrix """
    transform = Ray.Matrix.translation(5, -3, 2)
    p = Ray.Point(-3, 4, 5)
    assert transform * p == Ray.Point(2, 1, 7)

  def test_multiply_inverse_transform_matrix(self):
    """ Multiplying by the inverse of a translation matrix """
    transform = Ray.Matrix.translation(5, -3, 2)
    inv = transform.inverse()
    p = Ray.Point(-3, 4, 5)
    assert inv * p == Ray.Point(-8, 7, 3)

  def test_translation_vectors(self):
    """ Translation does not affect vectors """
    transform = Ray.Matrix.translation(5, -3, 2)
    v = Ray.Vector(-3, 4, 5)
    assert transform * v == v

  def test_scaling_matrix_point(self):
    """ A scaling matrix applied to a point """
    transform = Ray.Matrix.scaling(2, 3, 4)
    p = Ray.Point(-4, 6, 8)
    assert transform * p == Ray.Point(-8, 18, 32)

  def test_scaling_matrix_vector(self):
    """ A scaling matrix applied to a vector """
    transform = Ray.Matrix.scaling(2, 3, 4)
    v = Ray.Vector(-4, 6, 8)
    assert transform * v == Ray.Vector(-8, 18, 32)

  def test_inverse_scaling_matrix_vector(self):
    """ Multiplying by the inverse of a scaling matrix """
    transform = Ray.Matrix.scaling(2, 3, 4)
    inv = transform.inverse()
    v = Ray.Vector(-4, 6, 8)
    assert inv * v == Ray.Vector(-2, 2, 2)

  def test_reflection_scaling(self):
    """ Reflection is scaling by a negative value """
    transform = Ray.Matrix.scaling(-1, 1, 1)
    p = Ray.Point(2, 3, 4)
    assert transform * p == Ray.Point(-2, 3, 4)

  def test_rotation_point_x(self):
    """ Rotating a point around the x axis """
    p = Ray.Point(0, 1, 0)
    half_quarter = Ray.Matrix.rotation_x(math.pi / 4)
    full_quarter = Ray.Matrix.rotation_x(math.pi / 2)
    assert half_quarter * p == Ray.Point(0, math.sqrt(2) / 2, math.sqrt(2) / 2)
    assert full_quarter * p == Ray.Point(0, 0, 1)

  def test_inverse_rotation_point_x(self):
    """ The inverse of an x-rotation rotates in the opposite direction """
    p = Ray.Point(0, 1, 0)
    half_quarter = Ray.Matrix.rotation_x(math.pi / 4)
    inv = half_quarter.inverse()
    assert inv * p == Ray.Point(0, math.sqrt(2) / 2, -(math.sqrt(2) / 2))

  def test_rotation_point_y(self):
    """ Rotating a point around the y axis """
    p = Ray.Point(0, 0, 1)
    half_quarter = Ray.Matrix.rotation_y(math.pi / 4)
    full_quarter = Ray.Matrix.rotation_y(math.pi / 2)
    assert half_quarter * p == Ray.Point(math.sqrt(2) / 2, 0, math.sqrt(2) / 2)
    assert full_quarter * p == Ray.Point(1, 0, 0)

  def test_rotation_point_z(self):
    """ Rotating a point around the z axis """
    p = Ray.Point(0, 1, 0)
    half_quarter = Ray.Matrix.rotation_z(math.pi / 4)
    full_quarter = Ray.Matrix.rotation_z(math.pi / 2)
    assert half_quarter * p == Ray.Point(-(math.sqrt(2) / 2), math.sqrt(2) / 2, 0)
    assert full_quarter * p == Ray.Point(-1, 0, 0)

  def test_shearing_x_y(self):
    """ A shearing transformation moves x in proportion to y """
    transform = Ray.Matrix.shearing(1, 0, 0, 0, 0, 0)
    p = Ray.Point(2, 3, 4)
    assert transform * p == Ray.Point(5, 3, 4)

  def test_shearing_x_z(self):
    """ A shearing transformation moves x in proportion to z """
    transform = Ray.Matrix.shearing(0, 1, 0, 0, 0, 0)
    p = Ray.Point(2, 3, 4)
    assert transform * p == Ray.Point(6, 3, 4)

  def test_shearing_y_x(self):
    """ A shearing transformation moves y in proportion to x """
    transform = Ray.Matrix.shearing(0, 0, 1, 0, 0, 0)
    p = Ray.Point(2, 3, 4)
    assert transform * p == Ray.Point(2, 5, 4)

  def test_shearing_y_z(self):
    """ A shearing transformation moves y in proportion to z """
    transform = Ray.Matrix.shearing(0, 0, 0, 1, 0, 0)
    p = Ray.Point(2, 3, 4)
    assert transform * p == Ray.Point(2, 7, 4)

  def test_shearing_z_x(self):
    """ A shearing transformation moves z in proportion to x """
    transform = Ray.Matrix.shearing(0, 0, 0, 0, 1, 0)
    p = Ray.Point(2, 3, 4)
    assert transform * p == Ray.Point(2, 3, 6)

  def test_shearing_z_y(self):
    """ A shearing transformation moves z in proportion to y """
    transform = Ray.Matrix.shearing(0, 0, 0, 0, 0, 1)
    p = Ray.Point(2, 3, 4)
    assert transform * p == Ray.Point(2, 3, 7)

  def test_transform_sequence(self):
    """ Individual transformations are applied in sequence """
    p = Ray.Point(1, 0, 1)
    A = Ray.Matrix.rotation_x(math.pi / 2)
    B = Ray.Matrix.scaling(5, 5, 5)
    C = Ray.Matrix.translation(10, 5, 7)

    p2 = A * p
    assert p2 == Ray.Point(1, -1, 0)

    p3 = B * p2
    assert p3 == Ray.Point(5, -5, 0)

    p4 = C * p3
    assert p4 == Ray.Point(15, 0, 7)

  def test_transform_chained(self):
    """ Chained transformations must be applied in reverse order """
    p = Ray.Point(1, 0, 1)
    A = Ray.Matrix.rotation_x(math.pi / 2)
    B = Ray.Matrix.scaling(5, 5, 5)
    C = Ray.Matrix.translation(10, 5, 7)

    T = C * B * A
    assert T * p == Ray.Point(15, 0, 7)
