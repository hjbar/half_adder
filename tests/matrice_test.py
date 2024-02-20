import sys
import os

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
import unittest
import numpy as np
from modules.matrice import *


class MatriceTest(unittest.TestCase):

    def test_random_int_list(self):
        list1 = random_int_list(0, 0)
        self.assertEqual(np.shape(list1), (0, ))

        list2 = random_int_list(10, 10)
        self.assertEqual(len(list2), 10)
        c1, c2 = list2[list2 > 10], list2[list2 < 0]
        self.assertEqual(len(c1), 0)
        self.assertEqual(len(c2), 0)

    def test_random_int_matrix(self):
        list1 = random_int_matrix(0, 0)
        self.assertEqual(np.shape(list1), (0, 0))

        list2 = random_int_matrix(5, 5)
        self.assertEqual(np.shape(list2)[0], 5)
        self.assertEqual(np.shape(list2)[1], 5)
        c1, c2 = list2[list2 > 5], list2[list2 < 0]
        self.assertEqual(len(c1), 0)
        self.assertEqual(len(c2), 0)
        c3 = np.diag(list2)[np.diag(list2) == 0]
        self.assertEqual(c3.size, 5)

        list3 = random_int_matrix(16, 100, null_diag=False)
        self.assertEqual(np.shape(list3)[0], 16)
        self.assertEqual(np.shape(list3)[1], 16)
        c4, c5 = list3[list3 > 100], list3[list3 < 0]
        self.assertEqual(len(c4), 0)
        self.assertEqual(len(c5), 0)
        c6 = np.diag(list3)[np.diag(list3) == 0]
        self.assertIsNot(
            c6.size, 16
        )  # Il est possible que l'on ait que des zeros sur les diagonales meme avec diag_null = False

    def test_random_symetric_int_matrix(self):
        list1 = random_symetric_int_matrix(0, 0)
        self.assertEqual(np.shape(list1), (0, 0))

        list2 = random_symetric_int_matrix(5, 5)
        self.assertEqual(np.shape(list2)[0], 5)
        self.assertEqual(np.shape(list2)[1], 5)
        c1, c2 = list2[list2 > 5], list2[list2 < 0]
        self.assertEqual(len(c1), 0)
        self.assertEqual(len(c2), 0)
        c3 = list2[list2 == list2.transpose()]
        self.assertEqual(c3.size, 25)
        c4 = np.diag(list2)[np.diag(list2) == 0]
        self.assertEqual(c4.size, 5)

        list3 = random_symetric_int_matrix(16, 100, null_diag=False)
        self.assertEqual(np.shape(list3)[0], 16)
        self.assertEqual(np.shape(list3)[1], 16)
        c5, c6 = list3[list3 > 100], list3[list3 < 0]
        self.assertEqual(len(c5), 0)
        self.assertEqual(len(c6), 0)
        c7 = list3[list3 == list3.transpose()]
        self.assertEqual(c7.size, 256)
        c8 = np.diag(list3)[np.diag(list3) == 0]
        self.assertIsNot(
            c8.size, 16
        )  # Il est possible que l'on ait que des zeros sur les diagonales meme avec diag_null = False

    def test_random_oriented_int_matrix(self):
        list1 = random_oriented_int_matrix(0, 0)
        self.assertEqual(np.shape(list1), (0, 0))

        list2 = random_oriented_int_matrix(5, 5)
        self.assertEqual(np.shape(list2)[0], 5)
        self.assertEqual(np.shape(list2)[1], 5)
        c1, c2 = list2[list2 > 5], list2[list2 < 0]
        self.assertEqual(len(c1), 0)
        self.assertEqual(len(c2), 0)
        c4 = np.diag(list2)[np.diag(list2) == 0]
        self.assertEqual(c4.size, 5)

        list3 = random_oriented_int_matrix(16, 100, null_diag=False)
        self.assertEqual(np.shape(list3)[0], 16)
        self.assertEqual(np.shape(list3)[1], 16)
        c5, c6 = list3[list3 > 100], list3[list3 < 0]
        self.assertEqual(len(c5), 0)
        self.assertEqual(len(c6), 0)
        c8 = np.diag(list3)[np.diag(list3) == 0]
        self.assertIsNot(
            c8.size, 16
        )  # Il est possible que l'on ait que des zeros sur les diagonales meme avec diag_null = False

    def test_random_triangular_int_matrix(self):
        list1 = random_triangular_int_matrix(0, 0)
        self.assertEqual(np.shape(list1), (0, 0))

        list2 = random_triangular_int_matrix(5, 5)
        self.assertEqual(np.shape(list2)[0], 5)
        self.assertEqual(np.shape(list2)[1], 5)
        c1, c2 = list2[list2 > 5], list2[list2 < 0]
        self.assertEqual(len(c1), 0)
        self.assertEqual(len(c2), 0)

        c3 = np.tril(list2)[np.tril(list2) == 0]
        self.assertEqual(c3.size, 25)
        c4 = list2[list2 == np.triu(list2)]
        self.assertEqual(c4.size, 25)
        c5 = np.triu(list2)[list2 > 0]
        self.assertIsNot(c5.size, 0)
        c6 = np.diag(list2)[np.diag(list2) == 0]
        self.assertEqual(c6.size, 5)

        list3 = random_triangular_int_matrix(16, 100, null_diag=False)
        self.assertEqual(np.shape(list3)[0], 16)
        self.assertEqual(np.shape(list3)[1], 16)
        c7, c8 = list3[list3 > 100], list3[list3 < 0]
        self.assertEqual(len(c7), 0)
        self.assertEqual(len(c8), 0)
        c9 = np.tril(list3)[np.tril(list3) == 0]
        self.assertEqual(c3.size, 25)
        c10 = list3[list3 == np.triu(list3)]
        self.assertEqual(c4.size, 25)
        c11 = np.triu(list3)[list3 > 0]
        self.assertIsNot(c5.size, 0)
        c12 = np.diag(list3)[np.diag(list3) == 0]
        self.assertIsNot(
            c12.size, 16
        )  # Il est possible que l'on ait que des zeros sur les diagonales meme avec diag_null = False


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
