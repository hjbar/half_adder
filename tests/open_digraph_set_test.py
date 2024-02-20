import sys
import os

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
import unittest
from modules.open_digraph import *


class OpenDigraphTest(unittest.TestCase):

    # Setup

    def setUp(self):

        # Initialisation de graph de base

        g_n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        g_n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        g_n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        g_i0 = node(3, 'i0', {}, {0: 1})
        g_i1 = node(4, 'i1', {}, {0: 1})
        g_o0 = node(5, 'o0', {1: 1}, {})
        g_o1 = node(6, 'o1', {2: 1}, {})
        g_node_list = [g_n0, g_n1, g_n2, g_i0, g_i1, g_o0, g_o1]
        self.g_g = open_digraph([3, 4], [5, 6], g_node_list)

        # Pour les tests de setters

        s_n0 = node(0, 'a', {3: 1, 4: 1, 2: 1}, {1: 2, 2: 1})
        s_n1 = node(1, 'b', {0: 2}, {2: 2, 5: 1})
        s_n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1, 0: 1})
        s_i0 = node(3, 'i0', {}, {0: 1})
        s_i1 = node(4, 'i1', {}, {0: 1})
        s_o0 = node(5, 'o0', {1: 1}, {})
        s_o1 = node(6, 'o1', {2: 1}, {})
        self.s_t1 = node(7, 't1', {2: 3}, {1: 6})
        self.s_t2 = node(8, 't2', {}, {})
        self.s_nodes_test = {
            0: s_n0,
            1: s_n1,
            2: s_n2,
            3: s_i0,
            4: s_i1,
            5: s_o0,
            6: s_o1
        }
        self.s2_nodes_test = {
            0: g_n0,
            1: g_n1,
            2: g_n2,
            3: g_i0,
            4: g_i1,
            5: g_o0,
            6: g_o1,
            7: self.s_t1,
            8: self.s_t2
        }

        s2_n0 = node(0, 'a', {3: 1, 4: 1, 7: 1}, {1: 1, 2: 1})
        s_n7 = node(7, '', {}, {0: 1})
        s_node_list = [s2_n0, g_n1, g_n2, g_i0, g_i1, s_o0, s_o1, s_n7]
        self.s_g0 = open_digraph([3, 4, 7], [5, 6], s_node_list)

        s2_n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1, 7: 1})
        s_n7 = node(7, '', {2: 1}, {})
        s2_node_list = [g_n0, g_n1, s2_n2, g_i0, g_i1, g_o0, g_o1, s_n7]
        self.s_g1 = open_digraph([3, 4], [5, 6, 7], s2_node_list)

    # Setters

    def test_set_input(self):
        self.g_g.set_input_ids([1, 1])
        self.assertEqual(self.g_g.get_input_ids(), [1, 1])

    def test_set_output(self):
        self.g_g.set_output_ids([10, 10])
        self.assertEqual(self.g_g.get_output_ids(), [10, 10])

    def test_add_input(self):
        self.g_g.add_input_id(5)
        self.assertEqual(self.g_g.get_input_ids(), [3, 4, 5])

    def test_add_output(self):
        self.g_g.add_output_id(55)
        self.assertEqual(self.g_g.get_output_ids(), [5, 6, 55])

    def test_add_edge(self):
        self.g_g.add_edge(2, 0)
        self.g_g.add_edge(0, 1)
        self.assertEqual((self.g_g.nodes), (self.s_nodes_test))
        self.g_g.is_well_formed()

        try:
            self.g_g.add_edge(3, 0)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_g.add_edge(5, 0)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_g.add_edge(0, 3)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_g.add_edge(0, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_add_edges(self):
        self.g_g.add_edges([(2, 0), (0, 1)])
        self.assertEqual((self.g_g.nodes), (self.s_nodes_test))
        self.g_g.is_well_formed()

    def test_add_node(self):
        self.g_g.add_node(label=self.s_t1.label,
                          parents=self.s_t1.parents,
                          children=self.s_t1.children)
        self.g_g.add_node(label='t2')
        self.assertEqual((self.g_g.get_id_node_map()), (self.s2_nodes_test))
        self.g_g.is_well_formed()

        try:
            self.g_g.add_node(parents={3: 1})
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_g.add_node(parents={5: 1})
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_g.add_node(children={3: 1})
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_g.add_node(children={5: 1})
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_add_input_node(self):
        self.g_g.add_input_node(0)
        self.assertEqual((self.g_g), (self.s_g0))
        self.g_g.is_well_formed()

        try:
            self.g_g.add_input_node(3)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_g.add_input_node(5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_add_output_node(self):
        self.g_g.add_output_node(2)
        self.assertEqual((self.g_g), (self.s_g1))
        self.g_g.is_well_formed()

        try:
            self.g_g.add_output_node(3)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            self.g_g.add_output_node(5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
