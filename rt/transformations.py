"""
Transformations module
"""
from __future__ import annotations

from rt.matrix import Matrix
from rt.tuple import Point, Vector


class Transformations:
  """
  Transformations
  """
  @classmethod
  def view_transform(cls, from_p: Point, to: Point, up: Vector) -> Matrix:
    """ compute the view transform """
    forward = (to - from_p).normalize()
    upn = up.normalize()
    left = forward.cross(upn)
    true_up = left.cross(forward)
    orientation = Matrix([
      [left.x, left.y, left.z, 0],
      [true_up.x, true_up.y, true_up.z, 0],
      [-forward.x, -forward.y, -forward.z, 0],
      [0, 0, 0, 1]
      ])
    return orientation * Matrix.translation(-from_p.x, -from_p.y, -from_p.z)
