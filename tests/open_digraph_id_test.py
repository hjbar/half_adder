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

        # Pour les tests de graph_to_dict_id

        m_n0 = node(7, 'a', {11: 1, 13: 1}, {9: 1, 8: 1})
        m_n1 = node(9, 'b', {7: 1}, {8: 2, 12: 1})
        m_n2 = node(8, 'c', {7: 1, 9: 2}, {19: 1})
        m_i0 = node(11, 'i0', {}, {7: 1})
        m_i1 = node(13, 'i1', {}, {7: 1})
        m_o0 = node(12, 'o0', {9: 1}, {})
        m_o1 = node(19, 'o1', {8: 1}, {})
        m_node_list = [m_n0, m_n1, m_n2, m_i0, m_i1, m_o0, m_o1]
        self.m_g = open_digraph([11, 13], [12, 19], m_node_list)
        self.m_dict = {
            0: m_n0,
            1: m_n1,
            2: m_n2,
            3: m_i0,
            4: m_i1,
            5: m_o0,
            6: m_o1
        }

        # Pour les tests de shift_indices

        s_n0 = node(5, 'a', {8: 1, 9: 1}, {6: 1, 7: 1})
        s_n1 = node(6, 'b', {5: 1}, {7: 2, 10: 1})
        s_n2 = node(7, 'c', {5: 1, 6: 2}, {11: 1})
        s_i0 = node(8, 'i0', {}, {5: 1})
        s_i1 = node(9, 'i1', {}, {5: 1})
        s_o0 = node(10, 'o0', {6: 1}, {})
        s_o1 = node(11, 'o1', {7: 1}, {})
        s_node_list = [s_n0, s_n1, s_n2, s_i0, s_i1, s_o0, s_o1]
        self.s_g = open_digraph([8, 9], [10, 11], s_node_list)

        s2_n0 = node(-5, 'a', {-2: 1, -1: 1}, {-4: 1, -3: 1})
        s2_n1 = node(-4, 'b', {-5: 1}, {-3: 2, 0: 1})
        s2_n2 = node(-3, 'c', {-5: 1, -4: 2}, {1: 1})
        s2_i0 = node(-2, 'i0', {}, {-5: 1})
        s2_i1 = node(-1, 'i1', {}, {-5: 1})
        s2_o0 = node(0, 'o0', {-4: 1}, {})
        s2_o1 = node(1, 'o1', {-3: 1}, {})
        s2_node_list = [s2_n0, s2_n1, s2_n2, s2_i0, s2_i1, s2_o0, s2_o1]
        self.s2_g = open_digraph([-2, -1], [0, 1], s2_node_list)

    # Test des methodes

    def test_new_id(self):
        self.assertEqual(self.g_g.new_id(), 7)

    def test_graph_to_dict_id(self):
        dict_res = self.m_g.graph_to_dict_id()
        self.assertEqual((dict_res), (self.m_dict))

    def test_min_id(self):
        res = self.g_g.min_id()
        self.assertEqual(res, 0)

    def test_max_id(self):
        res = self.g_g.max_id()
        self.assertEqual(res, 6)

    def test_shift_indices(self):
        c_g = self.g_g.copy()
        c_g.shift_indices(5)

        self.assertEqual((c_g), (self.s_g))

        c2_g = self.g_g.copy()
        c2_g.shift_indices(-5)

        self.assertEqual((c2_g), (self.s2_g))


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
