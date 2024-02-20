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

        # Pour les tests de adjacency_matrix

        self.m_mat = np.array([[0, 1, 1], [0, 0, 2], [0, 0, 0]])

        m2_n0 = node(0, 'a', {}, {})
        self.m2_g = open_digraph([], [], [m2_n0])
        self.m2_mat = np.array([[0]])

        m2_i0 = node(0, 'a', {}, {})
        self.m3_g = open_digraph([0], [], [m2_i0])
        self.m3_mat = np.array([])

        self.m4_g = open_digraph([], [], [])
        self.m4_mat = np.array([])

    # Test des methodes

    def test_graph_from_adjacency_matrix(self):
        mat = random_matrix(5, 3, symetric=True)
        g = open_digraph.graph_from_adjacency_matrix(mat)

        g.is_well_formed()

        self.assertEqual(g.get_input_ids(), [])
        self.assertEqual(g.get_output_ids(), [])

        mat2 = random_matrix(5, 3, oriented=True)
        g2 = open_digraph.graph_from_adjacency_matrix(mat2)

        g2.is_well_formed()

        self.assertEqual(g2.get_input_ids(), [])
        self.assertEqual(g2.get_output_ids(), [])

        mat3 = random_matrix(5, 3, triangular=True)
        g3 = open_digraph.graph_from_adjacency_matrix(mat3)

        g3.is_well_formed()

        self.assertEqual(g3.get_input_ids(), [])
        self.assertEqual(g3.get_output_ids(), [])

    def test_random(self):
        g_free = open_digraph.random(5, 3, 0, 0)
        g_free.is_well_formed()

        g2_free = open_digraph.random(2, 5, 0, 2)
        g2_free.is_well_formed()

        g3_free = open_digraph.random(3, 2, 3, 0)
        g3_free.is_well_formed()

        g4_free = open_digraph.random(1, 5, 0, 1)
        g4_free.is_well_formed()

        g5_free = open_digraph.random(1, 4, 1, 0)
        g5_free.is_well_formed()

        g6_free = open_digraph.random(0, 4, 0, 0)
        g6_free.is_well_formed()

        g7_free = open_digraph.random(5, 3, 2, 3)
        g7_free.is_well_formed()

        try:
            g8_free = open_digraph.random(5, 15, 4, 2)
            self.g8_free.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g9_free = open_digraph.random(5, 15, 2, 4)
            self.g9_free.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g10_free = open_digraph.random(5, 15, 4, 2)
            self.g10_free.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g11_free = open_digraph.random(0, 15, 1, 0)
            self.g11_free.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g12_free = open_digraph.random(0, 15, 0, 1)
            self.g12_free.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        g_dag = open_digraph.random(1, 4, 0, 0, form="DAG")
        g_dag.is_well_formed()

        g2_dag = open_digraph.random(1, 4, 1, 0, form="DAG")
        g2_dag.is_well_formed()

        g3_dag = open_digraph.random(1, 4, 0, 1, form="DAG")
        g3_dag.is_well_formed()

        g4_dag = open_digraph.random(5, 4, 3, 2, form="DAG")
        g4_dag.is_well_formed()

        g_oriented = open_digraph.random(1, 4, 0, 0, form="oriented")
        g_oriented.is_well_formed()

        g2_oriented = open_digraph.random(1, 4, 1, 0, form="oriented")
        g2_oriented.is_well_formed()

        g3_oriented = open_digraph.random(1, 4, 0, 1, form="oriented")
        g3_oriented.is_well_formed()

        g4_oriented = open_digraph.random(5, 4, 2, 3, form="oriented")
        g4_oriented.is_well_formed()

        g_loop_free = open_digraph.random(1, 4, 0, 0, form="loop-free")
        g_loop_free.is_well_formed()

        g2_loop_free = open_digraph.random(1, 4, 1, 0, form="loop-free")
        g2_loop_free.is_well_formed()

        g3_loop_free = open_digraph.random(1, 4, 0, 1, form="loop-free")
        g3_loop_free.is_well_formed()

        g4_loop_free = open_digraph.random(5, 4, 3, 2, form="loop-free")
        g4_loop_free.is_well_formed()

        g_undirected = open_digraph.random(1, 4, 0, 0, form="undirected")
        g_undirected.is_well_formed()

        g2_undirected = open_digraph.random(1, 4, 1, 0, form="undirected")
        g2_undirected.is_well_formed()

        g3_undirected = open_digraph.random(1, 4, 0, 1, form="undirected")
        g3_undirected.is_well_formed()

        g4_undirected = open_digraph.random(5, 4, 2, 3, form="undirected")
        g4_undirected.is_well_formed()

        g_loop_free_undirected = open_digraph.random(
            1, 4, 0, 0, form="loop-free-undirected")
        g_loop_free_undirected.is_well_formed()

        g2_loop_free_undirected = open_digraph.random(
            1, 4, 1, 0, form="loop-free-undirected")
        g2_loop_free_undirected.is_well_formed()

        g3_loop_free_undirected = open_digraph.random(
            1, 4, 0, 1, form="loop-free-undirected")
        g3_loop_free_undirected.is_well_formed()

        g4_loop_free_undirected = open_digraph.random(
            5, 4, 3, 2, form="loop-free-undirected")
        g4_loop_free_undirected.is_well_formed()

        try:
            g_erreur = open_digraph.random(5,
                                           2,
                                           2,
                                           1,
                                           form="loop-free undirected")
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_adjacency_matrix(self):
        mat = self.g_g.adjacency_matrix()
        self.assertEqual(np.array_equal(mat, self.m_mat), True)

        mat2 = self.m2_g.adjacency_matrix()
        self.assertEqual(np.array_equal(mat2, self.m2_mat), True)

        mat3 = self.m3_g.adjacency_matrix()
        self.assertEqual(list(mat3), list(self.m3_mat))

        mat4 = self.m4_g.adjacency_matrix()
        self.assertEqual(list(mat4), list(self.m4_mat))


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
