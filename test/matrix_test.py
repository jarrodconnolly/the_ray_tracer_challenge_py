""" Matrix Tests """
import ray as Ray

class TestMatrix:
  """ features/matrices.feature """

  def test_matrix(self):
    """ Constructing and inspecting a 4x4 matrix """
    m = Ray.Matrix([
      [1, 2, 3, 4],
      [5.5, 6.5, 7.5, 8.5],
      [9, 10, 11, 12],
      [13.5, 14.5, 15.5, 16.5]
      ])
    assert m[0][0] == 1
    assert m[0][3] == 4
    assert m[1][0] == 5.5
    assert m[1][2] == 7.5
    assert m[2][2] == 11
    assert m[3][0] == 13.5
    assert m[3][2] == 15.5

  def test_matrix_2_2(self):
    """ A 2x2 matrix ought to be representable """
    m = Ray.Matrix([
      [-3, 5],
      [1, -2]
      ])
    assert m[0][0] == -3
    assert m[0][1] == 5
    assert m[1][0] == 1
    assert m[1][1] == -2

  def test_matrix_3_3(self):
    """ A 3x3 matrix ought to be representable """
    m = Ray.Matrix([
      [-3, 5, 0],
      [1, -2, -7],
      [0, 1, 1]
      ])
    assert m[0][0] == -3
    assert m[1][1] == -2
    assert m[2][2] == 1

  def test_matrix_eqality_identical(self):
    """ Ray.Matrix equality with identical matrices """
    m1 = Ray.Matrix([
      [1,2,3,4],
      [5,6,7,8],
      [9,8,7,6],
      [5,4,3,2]
      ])
    m2 = Ray.Matrix([
      [1,2,3,4],
      [5,6,7,8],
      [9,8,7,6],
      [5,4,3,2]
      ])
    assert m1 == m2

  def test_matrix_eqality_different(self):
    """ Ray.Matrix equality with different matrices """
    m1 = Ray.Matrix([
      [1,2,3,4],
      [5,6,7,8],
      [9,8,7,6],
      [5,4,3,2]
      ])
    m2 = Ray.Matrix([
      [2,3,4,5],
      [6,7,8,9],
      [8,7,6,5],
      [4,3,2,1]
      ])
    assert m1 != m2

  def test_matrix_multiplication(self):
    """ Multiplying two matrices """
    m1 = Ray.Matrix([
      [1,2,3,4],
      [5,6,7,8],
      [9,8,7,6],
      [5,4,3,2]
      ])
    m2 = Ray.Matrix([
      [-2,1,2,3],
      [3,2,1,-1],
      [4,3,6,5],
      [1,2,7,8]
      ])
    assert m1 * m2 == Ray.Matrix([
      [20,22,50,48],
      [44,54,114,108],
      [40,58,110,102],
      [16,26,46,42]
      ])

  def test_matrix_multiply_tuple(self):
    """ A matrix multiplied by a tuple """
    A = Ray.Matrix([
      [1,2,3,4],
      [2,4,4,2],
      [8,6,4,1],
      [0,0,0,1]
    ])
    b = Ray.Tuple(1, 2, 3, 1)
    assert A * b == Ray.Tuple(18, 24, 33, 1)

  def test_matrix_multiply_identity(self):
    """ Multiplying a matrix by the identity matrix """
    A = Ray.Matrix([
      [0,1,2,4],
      [1,2,4,8],
      [2,4,8,16],
      [4,8,16,32]
    ])
    assert A * Ray.Matrix.identity() == A

  def test_identity_matrix_multiply_tuple(self):
    """ Multiplying the identity matrix by a tuple """
    a = Ray.Tuple(1, 2, 3, 4)
    assert Ray.Matrix.identity() * a == a

  def test_transpose_matrix(self):
    """ Transposing a matrix """
    A = Ray.Matrix([
      [0,9,3,0],
      [9,8,0,8],
      [1,8,5,3],
      [0,0,5,8]
    ])
    assert A.transpose() == Ray.Matrix([
      [0,9,1,0],
      [9,8,8,0],
      [3,0,5,5],
      [0,8,3,8]
    ])

  def test_transpose_identity_matrix(self):
    """ Transposing the identity matrix """
    A = Ray.Matrix.identity().transpose()
    assert A == Ray.Matrix.identity()

  def test_determinant_2_2(self):
    """ Calculating the determinant of a 2x2 matrix """
    A = Ray.Matrix([
      [1,5],
      [-3,2]
    ])
    assert A.determinant() == 17

  def test_submatrix_3_3(self):
    """ A submatrix of a 3x3 matrix is a 2x2 matrix """
    A = Ray.Matrix([
      [1,5,0],
      [-3,2,7],
      [0,6,-3]
    ])
    assert A.submatrix(0, 2) == Ray.Matrix([
      [-3,2],
      [0,6]
    ])

  def test_submatrix_4_4(self):
    """ A submatrix of a 4x4 matrix is a 3x3 matrix """
    A = Ray.Matrix([
      [-6,1,1,6],
      [-8,5,8,6],
      [-1,0,8,2],
      [-7,1,-1,1]
    ])
    assert A.submatrix(2, 1) == Ray.Matrix([
      [-6,1,6],
      [-8,8,6],
      [-7,-1,1]
    ])

  def test_minor_3_3(self):
    """ Calculating a minor of a 3x3 matrix """
    A = Ray.Matrix([
      [3,5,0],
      [2,-1,-7],
      [6,-1,5]
    ])
    assert A.minor(1, 0) == 25

  def test_cofactor(self):
    """ Calculating a cofactor of a 3x3 matrix """
    A = Ray.Matrix([
      [3,5,0],
      [2,-1,-7],
      [6,-1,5]
    ])
    assert A.minor(0, 0) == -12
    assert A.cofactor(0, 0) == -12
    assert A.minor(1, 0) == 25
    assert A.cofactor(1, 0) == -25

  def test_determinant_3_3(self):
    """ Calculating the determinant of a 3x3 matrix """
    A = Ray.Matrix([
      [1,2,6],
      [-5,8,-4],
      [2,6,4]
    ])
    assert A.cofactor(0, 0) == 56
    assert A.cofactor(0, 1) == 12
    assert A.cofactor(0, 2) == -46
    assert A.determinant() == -196

  def test_determinant_4_4(self):
    """ Calculating the determinant of a 4x4 matrix """
    A = Ray.Matrix([
      [-2,-8,3,5],
      [-3,1,7,3],
      [1,2,-9,6],
      [-6,7,7,-9]
    ])
    assert A.cofactor(0, 0) == 690
    assert A.cofactor(0, 1) == 447
    assert A.cofactor(0, 2) == 210
    assert A.cofactor(0, 3) == 51
    assert A.determinant() == -4071

  def test_invertable_matrix(self):
    """ Testing an invertible matrix for invertibility """
    A = Ray.Matrix([
      [6,4,4,4],
      [5,5,7,6],
      [4,-9,3,-7],
      [9,1,7,-6]
    ])
    assert A.determinant() == -2120

  def test_non_invertable_matrix(self):
    """ Testing a noninvertible matrix for invertibility """
    A = Ray.Matrix([
      [-4,2,-2,-3],
      [9,6,2,6],
      [0,-5,1,-5],
      [0,0,0,0]
    ])
    assert A.determinant() == 0

  def test_matrix_inverse(self):
    """ Calculating the inverse of a matrix """
    A = Ray.Matrix([
      [-5,2,6,-8],
      [1,-5,1,8],
      [7,7,-6,-7],
      [1,-3,7,4]
    ])
    B = A.inverse()
    assert A.determinant() == 532
    assert A.cofactor(2, 3) == -160
    assert B[3][2] == -160/532
    assert A.cofactor(3, 2) == 105
    assert B[2][3] == 105/532
    assert B == Ray.Matrix([
      [0.21805, 0.45113, 0.24060, -0.04511],
      [-0.80827, -1.45677, -0.44361, 0.52068],
      [-0.07895, -0.22368, -0.05263, 0.19737],
      [-0.52256, -0.81391, -0.30075, 0.30639]
    ])

  def test_matrix_inverse_second(self):
    """ Calculating the inverse of another matrix """
    A = Ray.Matrix([
      [8,-5,9,2],
      [7,5,6,1],
      [-6,0,9,6],
      [-3,0,-9,-4]
    ])
    assert A.inverse() == Ray.Matrix([
      [-0.15385, -0.15385, -0.28205, -0.53846],
      [-0.07692, 0.12308, 0.02564, 0.03077],
      [0.35897, 0.35897, 0.43590, 0.92308],
      [-0.69231, -0.69231, -0.76923, -1.92308]
    ])


  def test_matrix_inverse_third(self):
    """ Calculating the inverse of a third matrix """
    A = Ray.Matrix([
      [9, 3, 0, 9],
      [-5, -2, -6, -3],
      [-4, 9, 6, 4],
      [-7, 6, 6, 2]
    ])
    assert A.inverse() == Ray.Matrix([
      [-0.04074, -0.07778, 0.14444, -0.22222],
      [-0.07778, 0.03333, 0.36667, -0.33333],
      [-0.02901, -0.14630, -0.10926, 0.12963],
      [0.17778, 0.06667, -0.26667, 0.33333]
    ])

  def test_matrix_multiply_product_inverse(self):
    """ Multiplying a product by its inverse """
    A = Ray.Matrix([
      [3, -9, 7, 3],
      [3, -8, 2, -9],
      [-4, 4, 4, 1],
      [-6, 5, -1, 1]
    ])
    B = Ray.Matrix([
      [8, 2, 2, 2],
      [3, -1, 7, 0],
      [7, 0, 5, 4],
      [6, -2, 0, 5]
    ])
    C = A * B
    assert C * B.inverse() == A
