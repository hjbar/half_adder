import sys
import os

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
import unittest
from modules.open_digraph import *


class InitTest(unittest.TestCase):

    # Open_digraph

    def test_init_digraph(self):
        g = open_digraph.empty()
        self.assertEqual(g.inputs, [])
        self.assertEqual(g.outputs, [])
        self.assertEqual(g.nodes, {})
        self.assertIsInstance(g, open_digraph)
        self.assertIsNot(g.copy(), g)


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

        # Pour les tests de is_well_formed

        n3 = node(9, 'z', {5: 1}, {})
        node_bad_list_1 = g_node_list + [n3]
        self.g_bad1 = open_digraph([3, 4], [5, 6], node_bad_list_1)
        self.g_bad2 = open_digraph([11, 4], [5, 6], g_node_list)
        self.g_bad3 = open_digraph([3, 4], [11, 6], g_node_list)
        i0 = node(3, 'i0', {1: 1}, {6: 1})
        self.g_bad4 = open_digraph([3, 4], [5, 6], g_node_list)
        i0 = node(3, 'i0', {}, {6: 1, 1: 1})
        self.g_bad5 = open_digraph([3, 4], [5, 6], g_node_list)
        i0 = node(3, 'i0', {}, {0: 1})
        o0 = node(5, 'o0', {1: 1}, {1: 1})
        self.g_bad6 = open_digraph([3, 4], [5, 6], g_node_list)
        o0 = node(5, 'o0', {1: 1, 2: 2}, {})
        self.g_bad7 = open_digraph([3, 4], [5, 6], g_node_list)
        o0 = node(5, 'o0', {1: 1}, {})

    # Test des methodes

    def test_copy_graph(self):
        graph = self.g_g.copy()
        self.assertEqual((graph), (self.g_g))

        graph.set_input_ids({})
        graph.set_output_ids({})
        graph.add_edge(0, 1)
        self.assertIsNot(
            (graph),
            (self.g_g
             ))  # On test si modifier une copie, modifie aussi l'original

    def test_well_formed(self):
        self.g_g.is_well_formed()

        try:
            self.g_bad1.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_bad2.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_bad3.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_bad4.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_bad5.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_bad6.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_bad7.is_well_formed()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
