""" Transformation Tests """
import math
import rt as RT

class TestTransformations:
  """ features/transformations.feature """

  def test_multiply_transform_matrix(self):
    """ Multiplying by a translation matrix """
    transform = RT.Matrix.translation(5, -3, 2)
    p = RT.Point(-3, 4, 5)
    assert transform * p == RT.Point(2, 1, 7)

  def test_multiply_inverse_transform_matrix(self):
    """ Multiplying by the inverse of a translation matrix """
    transform = RT.Matrix.translation(5, -3, 2)
    inv = transform.inverse()
    p = RT.Point(-3, 4, 5)
    assert inv * p == RT.Point(-8, 7, 3)

  def test_translation_vectors(self):
    """ Translation does not affect vectors """
    transform = RT.Matrix.translation(5, -3, 2)
    v = RT.Vector(-3, 4, 5)
    assert transform * v == v

  def test_scaling_matrix_point(self):
    """ A scaling matrix applied to a point """
    transform = RT.Matrix.scaling(2, 3, 4)
    p = RT.Point(-4, 6, 8)
    assert transform * p == RT.Point(-8, 18, 32)

  def test_scaling_matrix_vector(self):
    """ A scaling matrix applied to a vector """
    transform = RT.Matrix.scaling(2, 3, 4)
    v = RT.Vector(-4, 6, 8)
    assert transform * v == RT.Vector(-8, 18, 32)

  def test_inverse_scaling_matrix_vector(self):
    """ Multiplying by the inverse of a scaling matrix """
    transform = RT.Matrix.scaling(2, 3, 4)
    inv = transform.inverse()
    v = RT.Vector(-4, 6, 8)
    assert inv * v == RT.Vector(-2, 2, 2)

  def test_reflection_scaling(self):
    """ Reflection is scaling by a negative value """
    transform = RT.Matrix.scaling(-1, 1, 1)
    p = RT.Point(2, 3, 4)
    assert transform * p == RT.Point(-2, 3, 4)

  def test_rotation_point_x(self):
    """ Rotating a point around the x axis """
    p = RT.Point(0, 1, 0)
    half_quarter = RT.Matrix.rotation_x(math.pi / 4)
    full_quarter = RT.Matrix.rotation_x(math.pi / 2)
    assert half_quarter * p == RT.Point(0, math.sqrt(2) / 2, math.sqrt(2) / 2)
    assert full_quarter * p == RT.Point(0, 0, 1)

  def test_inverse_rotation_point_x(self):
    """ The inverse of an x-rotation rotates in the opposite direction """
    p = RT.Point(0, 1, 0)
    half_quarter = RT.Matrix.rotation_x(math.pi / 4)
    inv = half_quarter.inverse()
    assert inv * p == RT.Point(0, math.sqrt(2) / 2, -(math.sqrt(2) / 2))

  def test_rotation_point_y(self):
    """ Rotating a point around the y axis """
    p = RT.Point(0, 0, 1)
    half_quarter = RT.Matrix.rotation_y(math.pi / 4)
    full_quarter = RT.Matrix.rotation_y(math.pi / 2)
    assert half_quarter * p == RT.Point(math.sqrt(2) / 2, 0, math.sqrt(2) / 2)
    assert full_quarter * p == RT.Point(1, 0, 0)

  def test_rotation_point_z(self):
    """ Rotating a point around the z axis """
    p = RT.Point(0, 1, 0)
    half_quarter = RT.Matrix.rotation_z(math.pi / 4)
    full_quarter = RT.Matrix.rotation_z(math.pi / 2)
    assert half_quarter * p == RT.Point(-(math.sqrt(2) / 2), math.sqrt(2) / 2, 0)
    assert full_quarter * p == RT.Point(-1, 0, 0)

  def test_shearing_x_y(self):
    """ A shearing transformation moves x in proportion to y """
    transform = RT.Matrix.shearing(1, 0, 0, 0, 0, 0)
    p = RT.Point(2, 3, 4)
    assert transform * p == RT.Point(5, 3, 4)

  def test_shearing_x_z(self):
    """ A shearing transformation moves x in proportion to z """
    transform = RT.Matrix.shearing(0, 1, 0, 0, 0, 0)
    p = RT.Point(2, 3, 4)
    assert transform * p == RT.Point(6, 3, 4)

  def test_shearing_y_x(self):
    """ A shearing transformation moves y in proportion to x """
    transform = RT.Matrix.shearing(0, 0, 1, 0, 0, 0)
    p = RT.Point(2, 3, 4)
    assert transform * p == RT.Point(2, 5, 4)

  def test_shearing_y_z(self):
    """ A shearing transformation moves y in proportion to z """
    transform = RT.Matrix.shearing(0, 0, 0, 1, 0, 0)
    p = RT.Point(2, 3, 4)
    assert transform * p == RT.Point(2, 7, 4)

  def test_shearing_z_x(self):
    """ A shearing transformation moves z in proportion to x """
    transform = RT.Matrix.shearing(0, 0, 0, 0, 1, 0)
    p = RT.Point(2, 3, 4)
    assert transform * p == RT.Point(2, 3, 6)

  def test_shearing_z_y(self):
    """ A shearing transformation moves z in proportion to y """
    transform = RT.Matrix.shearing(0, 0, 0, 0, 0, 1)
    p = RT.Point(2, 3, 4)
    assert transform * p == RT.Point(2, 3, 7)

  def test_transform_sequence(self):
    """ Individual transformations are applied in sequence """
    p = RT.Point(1, 0, 1)
    A = RT.Matrix.rotation_x(math.pi / 2)
    B = RT.Matrix.scaling(5, 5, 5)
    C = RT.Matrix.translation(10, 5, 7)

    p2 = A * p
    assert p2 == RT.Point(1, -1, 0)

    p3 = B * p2
    assert p3 == RT.Point(5, -5, 0)

    p4 = C * p3
    assert p4 == RT.Point(15, 0, 7)

  def test_transform_chained(self):
    """ Chained transformations must be applied in reverse order """
    p = RT.Point(1, 0, 1)
    A = RT.Matrix.rotation_x(math.pi / 2)
    B = RT.Matrix.scaling(5, 5, 5)
    C = RT.Matrix.translation(10, 5, 7)

    T = C * B * A
    assert T * p == RT.Point(15, 0, 7)
