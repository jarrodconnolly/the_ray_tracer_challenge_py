""" Transformation Tests """
import math

from rt.matrix import Matrix
from rt.tuple import Point, Vector


class TestTransformations:
  """ features/transformations.feature """

  def test_multiply_transform_matrix(self):
    """ Multiplying by a translation matrix """
    transform = Matrix.translation(5, -3, 2)
    p = Point(-3, 4, 5)
    assert transform * p == Point(2, 1, 7)

  def test_multiply_inverse_transform_matrix(self):
    """ Multiplying by the inverse of a translation matrix """
    transform = Matrix.translation(5, -3, 2)
    inv = transform.inverse
    p = Point(-3, 4, 5)
    assert inv * p == Point(-8, 7, 3)

  def test_translation_vectors(self):
    """ Translation does not affect vectors """
    transform = Matrix.translation(5, -3, 2)
    v = Vector(-3, 4, 5)
    assert transform * v == v

  def test_scaling_matrix_point(self):
    """ A scaling matrix applied to a point """
    transform = Matrix.scaling(2, 3, 4)
    p = Point(-4, 6, 8)
    assert transform * p == Point(-8, 18, 32)

  def test_scaling_matrix_vector(self):
    """ A scaling matrix applied to a vector """
    transform = Matrix.scaling(2, 3, 4)
    v = Vector(-4, 6, 8)
    assert transform * v == Vector(-8, 18, 32)

  def test_inverse_scaling_matrix_vector(self):
    """ Multiplying by the inverse of a scaling matrix """
    transform = Matrix.scaling(2, 3, 4)
    inv = transform.inverse
    v = Vector(-4, 6, 8)
    assert inv * v == Vector(-2, 2, 2)

  def test_reflection_scaling(self):
    """ Reflection is scaling by a negative value """
    transform = Matrix.scaling(-1, 1, 1)
    p = Point(2, 3, 4)
    assert transform * p == Point(-2, 3, 4)

  def test_rotation_point_x(self):
    """ Rotating a point around the x axis """
    p = Point(0, 1, 0)
    half_quarter = Matrix.rotation_x(math.pi / 4)
    full_quarter = Matrix.rotation_x(math.pi / 2)
    assert half_quarter * p == Point(0, math.sqrt(2) / 2, math.sqrt(2) / 2)
    assert full_quarter * p == Point(0, 0, 1)

  def test_inverse_rotation_point_x(self):
    """ The inverse of an x-rotation rotates in the opposite direction """
    p = Point(0, 1, 0)
    half_quarter = Matrix.rotation_x(math.pi / 4)
    inv = half_quarter.inverse
    assert inv * p == Point(0, math.sqrt(2) / 2, -(math.sqrt(2) / 2))

  def test_rotation_point_y(self):
    """ Rotating a point around the y axis """
    p = Point(0, 0, 1)
    half_quarter = Matrix.rotation_y(math.pi / 4)
    full_quarter = Matrix.rotation_y(math.pi / 2)
    assert half_quarter * p == Point(math.sqrt(2) / 2, 0, math.sqrt(2) / 2)
    assert full_quarter * p == Point(1, 0, 0)

  def test_rotation_point_z(self):
    """ Rotating a point around the z axis """
    p = Point(0, 1, 0)
    half_quarter = Matrix.rotation_z(math.pi / 4)
    full_quarter = Matrix.rotation_z(math.pi / 2)
    assert half_quarter * p == Point(-(math.sqrt(2) / 2), math.sqrt(2) / 2, 0)
    assert full_quarter * p == Point(-1, 0, 0)

  def test_shearing_x_y(self):
    """ A shearing transformation moves x in proportion to y """
    transform = Matrix.shearing(1, 0, 0, 0, 0, 0)
    p = Point(2, 3, 4)
    assert transform * p == Point(5, 3, 4)

  def test_shearing_x_z(self):
    """ A shearing transformation moves x in proportion to z """
    transform = Matrix.shearing(0, 1, 0, 0, 0, 0)
    p = Point(2, 3, 4)
    assert transform * p == Point(6, 3, 4)

  def test_shearing_y_x(self):
    """ A shearing transformation moves y in proportion to x """
    transform = Matrix.shearing(0, 0, 1, 0, 0, 0)
    p = Point(2, 3, 4)
    assert transform * p == Point(2, 5, 4)

  def test_shearing_y_z(self):
    """ A shearing transformation moves y in proportion to z """
    transform = Matrix.shearing(0, 0, 0, 1, 0, 0)
    p = Point(2, 3, 4)
    assert transform * p == Point(2, 7, 4)

  def test_shearing_z_x(self):
    """ A shearing transformation moves z in proportion to x """
    transform = Matrix.shearing(0, 0, 0, 0, 1, 0)
    p = Point(2, 3, 4)
    assert transform * p == Point(2, 3, 6)

  def test_shearing_z_y(self):
    """ A shearing transformation moves z in proportion to y """
    transform = Matrix.shearing(0, 0, 0, 0, 0, 1)
    p = Point(2, 3, 4)
    assert transform * p == Point(2, 3, 7)

  def test_transform_sequence(self):
    """ Individual transformations are applied in sequence """
    p = Point(1, 0, 1)
    A = Matrix.rotation_x(math.pi / 2)
    B = Matrix.scaling(5, 5, 5)
    C = Matrix.translation(10, 5, 7)

    p2 = A * p
    assert p2 == Point(1, -1, 0)

    p3 = B * p2
    assert p3 == Point(5, -5, 0)

    p4 = C * p3
    assert p4 == Point(15, 0, 7)

  def test_transform_chained(self):
    """ Chained transformations must be applied in reverse order """
    p = Point(1, 0, 1)
    A = Matrix.rotation_x(math.pi / 2)
    B = Matrix.scaling(5, 5, 5)
    C = Matrix.translation(10, 5, 7)

    T = C * B * A
    assert T * p == Point(15, 0, 7)

  def test_view_transformation_matrix_default(self):
    """ The transformation matrix for the default orientation """
    eye_from = Point(0, 0, 0)
    to = Point(0, 0, -1)
    up = Vector(0, 1, 0)
    t = eye_from.view_transform(to, up)
    assert t == Matrix.identity()

  def test_view_transformation_matrix_positive_z(self):
    """ A view transformation matrix looking in positive z direction """
    eye_from = Point(0, 0, 0)
    to = Point(0, 0, 1)
    up = Vector(0, 1, 0)
    t = eye_from.view_transform(to, up)
    assert t == Matrix.scaling(-1, 1, -1)

  def test_view_transformation_moves_world(self):
    """ The view transformation moves the world """
    eye_from = Point(0, 0, 8)
    to = Point(0, 0, 0)
    up = Vector(0, 1, 0)
    t = eye_from.view_transform(to, up)
    assert t == Matrix.translation(0, 0, -8)

  def test_view_transformation_arbitrary(self):
    """ An arbitrary view transformation """
    eye_from = Point(1, 3, 2)
    to = Point(4, -2, 8)
    up = Vector(1, 1, 0)
    t = eye_from.view_transform(to, up)
    assert t == Matrix([
      [-0.50709, 0.50709, 0.67612, -2.36643],
      [0.76772, 0.60609, 0.12122, -2.82843],
      [-0.35857, 0.59761, -0.71714, 0.00000],
      [0.00000, 0.00000, 0.00000, 1.00000]
      ])
