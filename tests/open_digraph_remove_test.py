import sys
import os

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
import unittest
from modules.open_digraph import *


class OpenDigraphTest(unittest.TestCase):

    # Setup

    def setUp(self):

        # Initalisation du graph de base

        g_n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        g_n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        g_n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        g_i0 = node(3, 'i0', {}, {0: 1})
        g_i1 = node(4, 'i1', {}, {0: 1})
        g_o0 = node(5, 'o0', {1: 1}, {})
        g_o1 = node(6, 'o1', {2: 1}, {})
        g_node_list = [g_n0, g_n1, g_n2, g_i0, g_i1, g_o0, g_o1]
        self.g_g = open_digraph([3, 4], [5, 6], g_node_list)
        self.rc_g = self.g_g.copy()
        self.rc2_g = self.g_g.copy()

        # Pour les tests de removers

        r_n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        r2_n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        r2_n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        r_i0 = node(3, 'i0', {}, {0: 1})
        r_i1 = node(4, 'i1', {}, {0: 1})
        r_o0 = node(5, 'o0', {1: 1}, {})
        r_o1 = node(6, 'o1', {2: 1}, {})

        r_n1 = node(1, 'b', {0: 1}, {2: 1, 5: 1})
        r_n2 = node(2, 'c', {0: 1, 1: 1}, {6: 1})
        r_node_list = [r_n0, r_n1, r_n2, r_i0, r_i1, r_o0, r_o1]
        self.r_g0 = open_digraph([3, 4], [5, 6], r_node_list)

        r2_n1 = node(1, 'b', {0: 1}, {5: 1})
        r2_n2 = node(2, 'c', {0: 1}, {6: 1})
        r2_node_list = [r_n0, r2_n1, r2_n2, r_i0, r_i1, r_o0, r_o1]
        self.r_g1 = open_digraph([3, 4], [5, 6], r2_node_list)

        r_n0 = node(0, 'a', {3: 1, 4: 1}, {2: 1})
        r2_n1 = node(1, 'b', {}, {5: 1})
        r2_n2 = node(2, 'c', {0: 1}, {6: 1})
        r3_node_list = [r_n0, r2_n1, r2_n2, r_i0, r_i1, r_o0, r_o1]
        self.r_g2 = open_digraph([3, 4], [5, 6], r3_node_list)

        r1_n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1})
        r3_n1 = node(1, 'b', {0: 1}, {5: 1})
        r3_n2 = node(2, 'c', {}, {6: 1})
        r4_node_list = [r1_n0, r3_n1, r3_n2, r_i0, r_i1, r_o0, r_o1]
        self.r_g3 = open_digraph([3, 4], [5, 6], r4_node_list)

        r5_n0 = node(0, 'a', {4: 1}, {1: 1, 2: 1})
        r5_node_list = [r5_n0, g_n1, g_n2, g_i1, g_o0, g_o1]
        self.r_g4 = open_digraph([4], [5, 6], r5_node_list)

        r6_n2 = node(2, 'c', {0: 1, 1: 2}, {})
        r6_node_list = [g_n0, g_n1, r6_n2, g_i1, g_o0]
        self.r_g5 = open_digraph([4], [5], r6_node_list)

        r3_n1 = node(1, 'b', {}, {2: 2, 5: 1})
        r3_n2 = node(2, 'c', {1: 2}, {6: 1})
        r3_i0 = node(3, 'i0', {}, {})
        r3_i1 = node(4, 'i1', {}, {})
        r7_node_list = [r3_n1, r3_n2, r3_i0, r3_i1, r_o0, r_o1]
        self.r_g6 = open_digraph([], [5, 6], r7_node_list)

        r2_n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1})
        r7_n1 = node(1, 'b', {0: 1}, {5: 1})
        r2_o1 = node(6, 'o1', {}, {})
        r8_node_list = [r2_n0, r7_n1, r_i0, r_i1, r_o0, r2_o1]
        self.r_g7 = open_digraph([3, 4], [5], r8_node_list)

        r8_n1 = node(1, 'b', {}, {5: 1})
        r9_node_list = [r8_n1, r3_i0, r3_i1, r_o0, r2_o1]
        self.r_g8 = open_digraph([], [5], r9_node_list)

    # Removers

    def test_remove_edge(self):
        self.g_g.remove_edge(1, 2)
        self.assertEqual((self.g_g), (self.r_g0))
        self.g_g.is_well_formed()

    def test_remove_parallel_edge(self):
        self.g_g.remove_parallel_edges(1, 2)
        self.assertEqual((self.g_g), (self.r_g1))
        self.g_g.is_well_formed()

    def test_remove_edges(self):
        self.g_g.remove_edges([(1, 2), (1, 2), (0, 1)])
        self.assertEqual((self.g_g), (self.r_g2))
        self.g_g.is_well_formed()

    def test_remove_several_parallel_edges(self):
        self.g_g.remove_several_parallel_edges([(0, 2), (1, 2)])
        self.assertEqual((self.g_g), (self.r_g3))
        self.g_g.is_well_formed()

    def test_remove_node_by_id(self):
        del self.g_g[3]
        self.assertEqual((self.g_g), (self.r_g4))
        self.g_g.is_well_formed()

        del self.g_g[6]
        self.assertEqual((self.g_g), (self.r_g5))
        self.g_g.is_well_formed()

        del self.rc_g[0]
        self.assertEqual((self.rc_g), (self.r_g6))
        self.rc_g.is_well_formed()

        del self.rc2_g[2]
        self.assertEqual((self.rc2_g), (self.r_g7))
        self.rc2_g.is_well_formed()

    def test_remove_nodes_by_id(self):
        del self.g_g[[3, 6]]
        self.assertEqual((self.g_g), (self.r_g5))
        self.g_g.is_well_formed()

        del self.rc_g[[0, 2]]
        self.assertEqual((self.rc_g), (self.r_g8))
        self.rc_g.is_well_formed()


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
