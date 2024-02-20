import sys
import os

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
import unittest
from modules.open_digraph import *


class OpenDigraphTest(unittest.TestCase):

    # Setup

    def setUp(self):

        # Pour les tests de getters

        self.g_n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        g_n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        g_n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        g_i0 = node(3, 'i0', {}, {0: 1})
        g_i1 = node(4, 'i1', {}, {0: 1})
        g_o0 = node(5, 'o0', {1: 1}, {})
        g_o1 = node(6, 'o1', {2: 1}, {})
        self.g_nodes_test = {
            0: self.g_n0,
            1: g_n1,
            2: g_n2,
            3: g_i0,
            4: g_i1,
            5: g_o0,
            6: g_o1
        }
        self.g_node_list = [self.g_n0, g_n1, g_n2, g_i0, g_i1, g_o0, g_o1]
        self.g_g = open_digraph([3, 4], [5, 6], self.g_node_list)
        self.rc_g = self.g_g.copy()
        self.rc2_g = self.g_g.copy()

    # Getters

    def get_input(self):
        self.assertEqual(self.g_g.get_input_ids(), [3, 4])

    def get_output(self):
        self.assertEqual(self.g_g.get_output_ids(), [5, 6])

    def get_id_node_map(self):
        self.assertEqual(self.g_g.get_id_node_map(), self.g_nodes_test)

    def get_nodes(self):
        self.assertEqual(self.g_g.get_nodes(), list(self.g_nodes_test.keys()))

    def get_nodes_ids(self):
        self.assertEqual(self.g_g.get_nodes_ids(),
                         list(self.g_nodes_test.values()))

    def get_item(self):
        self.assertEqual(self.g_g[0], self.g_n0)

    def get_node_by_ids(self, ids):
        self.assertEqual(self.g_g.get_node_by_ids([0, 1, 2, 3, 4, 5, 6]),
                         self.g_node_list)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
