"""
Matrix module
"""
from __future__ import annotations

import math
from functools import cached_property

from rt.tuple import Tuple


class Matrix:
  """
  Matrix
  """
  def __init__(self, rows: list) -> Matrix:
    self.rows = rows
    self.size = len(rows)
    # self._inverse: Matrix
    # self._transpose: Matrix
    # self._determinant: int

  def __getitem__(self, key: int) -> list:
    return self.rows[key]

  def __eq__(self, other: Matrix) -> bool:
    if self.size != other.size:
      return False
    for i in range(0, self.size):
      for j in range(0, self.size):
        if not math.isclose(self[i][j], other[i][j], abs_tol=1e-05):
          return False
    return True

  def __mul__(self, other: Matrix|Tuple) -> Matrix|Tuple:
    if isinstance(other, Matrix):
      matrix = Matrix.by_size(self.size, self.size)
      # matrix.rows = [[sum(a * b for a, b in zip(A_row, B_col))
      #                   for B_col in zip(*other.rows)]
      #                           for A_row in self.rows]

      for i in range(0, self.size):
        for j in range(0, self.size):
          for k in range(0, self.size):
            matrix.rows[i][j] = matrix.rows[i][j] + self.rows[i][k] * other.rows[k][j]

      # for row in range(0, self.size):
      #   for col in range(0, self.size):
      #     matrix[row][col] = self[row][0] * other[0][col] + self[row][1] * other[1][col] + self[row][2] * other[2][col] + self[row][3] * other[3][col]

      return matrix

    if isinstance(other, Tuple):
      x = self.rows[0][0] * other.x + self.rows[0][1] * other.y + self.rows[0][2] * other.z + self.rows[0][3] * other.w
      y = self.rows[1][0] * other.x + self.rows[1][1] * other.y + self.rows[1][2] * other.z + self.rows[1][3] * other.w
      z = self.rows[2][0] * other.x + self.rows[2][1] * other.y + self.rows[2][2] * other.z + self.rows[2][3] * other.w
      w = self.rows[3][0] * other.x + self.rows[3][1] * other.y + self.rows[3][2] * other.z + self.rows[3][3] * other.w
      return Tuple(x, y, z, w)
      # tuple_params = []
      # for row in range(0, self.size):
      #   tuple_params.append(self.rows[row][0] * other.x + self.rows[row][1] * other.y + self.rows[row][2] * other.z + self.rows[row][3] * other.w)
      # return Tuple(*tuple_params) #pylint: disable = no-value-for-parameter

    raise ValueError("Invalid type to multiply with matrix")

  @cached_property
  def transpose(self) -> Matrix:
    """ Tranpose matrix """
    #if self._transpose is not None:
    #  return self._transpose
    matrix = Matrix.by_size(self.size, self.size)
    for row in range(0, self.size):
      for col in range(0, self.size):
        matrix[col][row] = self[row][col]
    #self._transpose = matrix
    return matrix

  @cached_property
  def determinant(self) -> int:
    """ Get determinant """
    #if self._determinant is not None:
    # return self._determinant
    if self.size == 2:
      return self[0][0] * self[1][1] - self[0][1] * self[1][0]

    det = 0
    for col in range(0, self.size):
      det += self[0][col] * self.cofactor(0, col)
    #self._determinant = det
    return det

  def submatrix(self, remove_row: int, remove_col: int) -> Matrix:
    """ Get submatrix """
    dest_matrix = Matrix.by_size(self.size - 1, self.size - 1)
    dest_row = 0
    dest_col = 0
    for row in range(0, self.size):
      if row == remove_row:
        continue
      for col in range(0, self.size):
        if col == remove_col:
          continue
        dest_matrix[dest_row][dest_col] = self[row][col]
        dest_col += 1
      dest_row += 1
      dest_col = 0
    return dest_matrix

  def minor(self, remove_row: int, remove_col: int) -> int:
    """ Return the minor """
    return self.submatrix(remove_row, remove_col).determinant

  def cofactor(self, remove_row: int, remove_col: int) -> int:
    """ Return the cofactor """
    minor = self.minor(remove_row, remove_col)
    if (remove_row + remove_col) % 2 != 0:
      return -minor
    return minor

  @cached_property
  def inverse(self) -> Matrix:
    """ Return the inverse """
    # if self._inverse is not None:
    #   return self._inverse

    determinant = self.determinant
    if determinant == 0:
      raise ValueError("Cannot invert matrix with determinant of 0")

    matrix = Matrix.by_size(self.size, self.size)
    for row in range(0, self.size):
      for col in range(0, self.size):
        cofactor = self.cofactor(row, col)
        matrix[col][row] = cofactor / determinant

    # self._inverse = matrix
    return matrix

  @classmethod
  def by_size(cls, rows: int, cols: int):
    """Helper to return empty Matrix by size"""
    if rows == 2 and cols == 2:
      return Matrix([
        [0,0],
        [0,0]
      ])
    if rows == 3 and cols == 3:
      return Matrix([
        [0,0,0],
        [0,0,0],
        [0,0,0]
      ])
    if rows == 4 and cols == 4:
      return Matrix([
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
      ])
    return Matrix([[0 for i in range(cols)] for j in range(rows)])

  @classmethod
  def identity(cls):
    """ Helper to return the identity matrix """
    return Matrix([
      [1,0,0,0],
      [0,1,0,0],
      [0,0,1,0],
      [0,0,0,1]
    ])

  @classmethod
  def translation(cls, x: float, y: float, z: float) -> Matrix:
    """ Return a translation matrix """
    return Matrix([
      [1,0,0,x],
      [0,1,0,y],
      [0,0,1,z],
      [0,0,0,1]
    ])

  @classmethod
  def scaling(cls, x: float, y: float, z: float) -> Matrix:
    """ Return a scaling matrix """
    return Matrix([
      [x,0,0,0],
      [0,y,0,0],
      [0,0,z,0],
      [0,0,0,1]
    ])

  @classmethod
  def rotation_x(cls, radians:float) -> Matrix:
    """ Return the X rotation matrix """
    cos_r = math.cos(radians)
    sin_r = math.sin(radians)
    return Matrix([
      [1,0,0,0],
      [0,cos_r,-sin_r,0],
      [0,sin_r,cos_r,0],
      [0,0,0,1]
    ])

  @classmethod
  def rotation_y(cls, radians:float) -> Matrix:
    """ Return the Y rotation matrix """
    cos_r = math.cos(radians)
    sin_r = math.sin(radians)
    return Matrix([
      [cos_r,0,sin_r,0],
      [0,1,0,0],
      [-sin_r,0,cos_r,0],
      [0,0,0,1]
    ])

  @classmethod
  def rotation_z(cls, radians:float) -> Matrix:
    """ Return the Z rotation matrix """
    cos_r = math.cos(radians)
    sin_r = math.sin(radians)
    return Matrix([
      [cos_r,-sin_r,0,0],
      [sin_r,cos_r,0,0],
      [0,0,1,0],
      [0,0,0,1]
    ])

  @classmethod
  def shearing(cls, x_y, x_z, y_x, y_z, z_x, z_y) -> Matrix:
    """ Return a scaling matrix """
    return Matrix([
      [1,x_y,x_z,0],
      [y_x,1,y_z,0],
      [z_x,z_y,1,0],
      [0,0,0,1]
    ])
