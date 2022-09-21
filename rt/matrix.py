"""
Matrix module
"""
from __future__ import annotations
import math
from rt.tuple import Tuple


class Matrix:
  """
  Matrix
  """
  def __init__(self, rows: list) -> Matrix:
    self.rows = rows
    self.row_count = len(rows)
    self.column_count = len(rows)
    self._inverse = None

  def __getitem__(self, key: int) -> list:
    return self.rows[key]

  def __eq__(self, other: Matrix) -> bool:
    if self.row_count != other.row_count or self.column_count != other.column_count:
      return False
    for i in range(0, self.row_count):
      for j in range(0, self.column_count):
        if not math.isclose(self[i][j], other[i][j], abs_tol=1e-05):
          return False
    return True

  def __mul__(self, other: Matrix|Tuple) -> Matrix|Tuple:
    if isinstance(other, Matrix):
      matrix = Matrix.by_size(self.row_count, self.column_count)
      for row in range(0, self.row_count):
        for col in range(0, self.column_count):
          matrix[row][col] = self[row][0] * other[0][col] + self[row][1] * other[1][col] + self[row][2] * other[2][col] + self[row][3] * other[3][col]
      return matrix

    if isinstance(other, Tuple):
      tuple_params = []
      for row in range(0, self.row_count):
        tuple_params.append(self[row][0] * other.x + self[row][1] * other.y + self[row][2] * other.z + self[row][3] * other.w)
      return Tuple(*tuple_params) #pylint: disable = no-value-for-parameter

    raise ValueError("Invalid type to multiply with matrix")

  def transpose(self) -> Matrix:
    """ Tranpose matrix """
    matrix = Matrix.by_size(self.row_count, self.column_count)
    for row in range(0, self.row_count):
      for col in range(0, self.column_count):
        matrix[col][row] = self[row][col]
    return matrix

  def determinant(self) -> int:
    """ Get determinant """
    if self.row_count == 2:
      return self[0][0] * self[1][1] - self[0][1] * self[1][0]

    det = 0
    for col in range(0, self.column_count):
      det += self[0][col] * self.cofactor(0, col)
    return det

  def submatrix(self, remove_row: int, remove_col: int) -> Matrix:
    """ Get submatrix """
    dest_matrix = Matrix.by_size(self.row_count - 1, self.column_count - 1)
    dest_row = 0
    dest_col = 0
    for row in range(0, self.row_count):
      if row == remove_row:
        continue
      for col in range(0, self.column_count):
        if col == remove_col:
          continue
        dest_matrix[dest_row][dest_col] = self[row][col]
        dest_col += 1
      dest_row += 1
      dest_col = 0
    return dest_matrix

  def minor(self, remove_row: int, remove_col: int) -> int:
    """ Return the minor """
    return self.submatrix(remove_row, remove_col).determinant()

  def cofactor(self, remove_row: int, remove_col: int) -> int:
    """ Return the cofactor """
    minor = self.minor(remove_row, remove_col)
    if (remove_row + remove_col) % 2 != 0:
      return -minor
    return minor

  def inverse(self) -> Matrix:
    """ Return the inverse """
    if self._inverse is not None:
      return self._inverse

    determinant = self.determinant()
    if determinant == 0:
      raise ValueError("Cannot invert matrix with determinant of 0")

    matrix = Matrix.by_size(self.row_count, self.column_count)
    for row in range(0, self.row_count):
      for col in range(0, self.column_count):
        cofactor = self.cofactor(row, col)
        matrix[col][row] = cofactor / determinant

    self._inverse = matrix
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
