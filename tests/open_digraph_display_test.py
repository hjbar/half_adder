import sys
import os

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
import unittest
from modules.open_digraph import *


class OpenDigraphTest(unittest.TestCase):

    # Setup

    def setUp(self):

        # Initialisation du graph de base

        g_n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        g_n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        g_n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        g_i0 = node(3, 'i0', {}, {0: 1})
        g_i1 = node(4, 'i1', {}, {0: 1})
        g_o0 = node(5, 'o0', {1: 1}, {})
        g_o1 = node(6, 'o1', {2: 1}, {})
        g_node_list = [g_n0, g_n1, g_n2, g_i0, g_i1, g_o0, g_o1]
        self.g_g = open_digraph([3, 4], [5, 6], g_node_list)

    # Test des methodes

    def test_save_as_dot_file(self):
        # Test avec verbose=False
        self.g_g.save_as_dot_file("tmp.dot")

        f_cree = open("tmp.dot", "r")
        f_test = open("tests/fichiers_annexes/test1_dot.dot", "r")

        l_cree = f_cree.readlines()
        l_test = f_test.readlines()

        f_cree.close()
        f_test.close()

        self.assertEqual(l_cree, l_test)
        os.system("rm tmp.dot")

        # Test avec verbose=True
        self.g_g.save_as_dot_file("tmp.dot", verbose=True)

        f_cree2 = open("tmp.dot", "r")
        f_test2 = open("tests/fichiers_annexes/test2_dot.dot", "r")

        l_cree2 = f_cree2.readlines()
        l_test2 = f_test2.readlines()

        f_cree2.close()
        f_test2.close()

        self.assertEqual(l_cree, l_test)
        os.system("rm tmp.dot")

    def test_from_dot_file(self):
        # Test avec verbose=False
        g1 = open_digraph.from_dot_file("tests/fichiers_annexes/test1_dot.dot")
        self.assertEqual((g1), (self.g_g))

        # Test avec verbose=True
        g2 = open_digraph.from_dot_file("tests/fichiers_annexes/test2_dot.dot")
        self.assertEqual((g2), (self.g_g))

    # Les tests de la methode display sont effectués dans le worksheet_graph


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
