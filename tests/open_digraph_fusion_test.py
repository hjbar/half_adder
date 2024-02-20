import sys
import os

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
import unittest
from modules.bool_circ import *


class OpenDigraphTest(unittest.TestCase):

    # Setup

    def setUp(self):

        # Initialisation des graphs du TP9

        # 1er graph

        g_f0 = node(0, "x0", {}, {1: 1})
        g_f1 = node(1, "&", {0: 1, 3: 1}, {5: 1})
        g_f2 = node(2, "x1", {}, {3: 1})
        g_f3 = node(3, "&", {2: 1, 4: 1}, {1: 1})
        g_f4 = node(4, "x2", {}, {3: 1})
        g_f5 = node(5, "|", {1: 1, 7: 1}, {})
        g_f6 = node(6, "x1", {}, {7: 1})
        g_f7 = node(7, "&", {6: 1, 8: 1}, {5: 1})
        g_f8 = node(8, "~", {9: 1}, {7: 1})
        g_f9 = node(9, "x2", {}, {8: 1})

        g_f0_node_list = [
            g_f0, g_f1, g_f2, g_f3, g_f4, g_f5, g_f6, g_f7, g_f8, g_f9
        ]

        self.g_f0 = open_digraph([], [], g_f0_node_list)

        # graph intermediaire

        g_f10 = node(2, "x1", {}, {3: 1, 7: 1})
        g_f0_node_list2 = [
            g_f0, g_f1, g_f10, g_f3, g_f4, g_f5, g_f7, g_f8, g_f9
        ]

        self.g_f1 = open_digraph([], [], g_f0_node_list2)

        # 2eme graph

        g_f11 = node(4, "x2", {}, {3: 1, 8: 1})
        g_f0_node_list3 = [g_f0, g_f1, g_f10, g_f3, g_f11, g_f5, g_f7, g_f8]

        self.g_f2 = open_digraph([], [], g_f0_node_list3)

        # 3eme graph

        g_n0 = node(0, "|", {2: 1, 7: 1}, {1: 1})
        g_n1 = node(1, "", {0: 1}, {})
        g_n2 = node(2, "&", {3: 1, 4: 1}, {0: 1})
        g_n3 = node(3, "", {}, {2: 1})
        g_n4 = node(4, "&", {5: 1, 6: 1}, {2: 1})
        g_n5 = node(5, "", {}, {4: 1, 7: 1})
        g_n6 = node(6, "", {}, {4: 1, 9: 1})
        g_n7 = node(7, "&", {9: 1, 5: 1}, {0: 1})
        g_n9 = node(9, "~", {6: 1}, {7: 1})

        g_f0_node_list4 = [
            g_n0, g_n1, g_n2, g_n3, g_n4, g_n5, g_n6, g_n7, g_n9
        ]

        g_f3 = open_digraph([], [1], g_f0_node_list4)
        self.b_f1 = bool_circ(g_f3)

        # 4eme graph

        g2_n0 = node(0, "|", {2: 1, 7: 1}, {1: 1})
        g2_n1 = node(1, "", {0: 1}, {})
        g2_n2 = node(2, "&", {4: 1, 3: 1}, {0: 1})
        g2_n3 = node(3, "", {}, {2: 1, 13: 1})
        g2_n4 = node(4, "&", {5: 1, 6: 1}, {2: 1})
        g2_n5 = node(5, "", {}, {4: 1, 7: 1, 15: 1})
        g2_n6 = node(6, "", {}, {4: 1, 9: 1, 11: 1})
        g2_n7 = node(7, "&", {9: 1, 5: 1}, {0: 1})
        g2_n9 = node(9, "~", {6: 1}, {7: 1})
        g2_n11 = node(11, "|", {13: 1, 6: 1}, {12: 1})
        g2_n12 = node(12, "", {11: 1}, {})
        g2_n13 = node(13, "&", {15: 1, 3: 1}, {11: 1})
        g2_n15 = node(15, "~", {5: 1}, {13: 1})

        g_f0_node_list5 = [
            g2_n0, g2_n1, g2_n2, g2_n3, g2_n4, g2_n5, g2_n6, g2_n7, g2_n9,
            g2_n11, g2_n12, g2_n13, g2_n15
        ]

        g_f4 = open_digraph([], [1, 12], g_f0_node_list5)
        self.b_f2 = bool_circ(g_f4)

        # 5eme graph

        g3_n0 = node(0, "|", {2: 1, 6: 1}, {1: 1})
        g3_n1 = node(1, "", {0: 1}, {})
        g3_n2 = node(2, "&", {3: 1, 4: 1, 5: 1}, {0: 1})
        g3_n3 = node(3, "", {}, {2: 1})
        g3_n4 = node(4, "", {}, {2: 1, 6: 1})
        g3_n5 = node(5, "", {}, {2: 1, 8: 1})
        g3_n6 = node(6, "&", {8: 1, 4: 1}, {0: 1})
        g3_n8 = node(8, "~", {5: 1}, {6: 1})

        g_f0_node_list6 = [
            g3_n0, g3_n1, g3_n2, g3_n3, g3_n4, g3_n5, g3_n6, g3_n8
        ]

        g_f5 = open_digraph([], [1], g_f0_node_list6)
        self.b_f3 = bool_circ(g_f5)

    # Test des methodes

    def test_node_fusion(self):
        self.g_f0.node_fusion(2, 6, new_label="x1")
        self.assertEqual(self.g_f0, self.g_f1)

        self.g_f0.node_fusion(4, 9, new_label="x2")
        self.assertEqual(self.g_f0, self.g_f2)

    def test_parse_parentheses(self):
        g_test1, l_test1 = bool_circ.parse_parentheses(
            "((x0)&((x1)&(x2)))|((x1)&(~(x2)))")

        self.assertEqual(g_test1, self.b_f1)
        self.assertEqual(l_test1, ["x0", "x1", "x2"])

        g_test2, l_test2 = bool_circ.parse_parentheses(
            "((x0)&((x1)&(x2)))|((x1)&(~(x2)))", "((x0)&(~(x1)))|(x2)")

        self.assertEqual(g_test2, self.b_f2)
        self.assertEqual(l_test2, ["x0", "x1", "x2"])

        g_test3, l_test3 = bool_circ.parse_parentheses(
            "((x0)&(x1)&(x2))|((x1)&(~(x2)))")

        self.assertEqual(g_test3, self.b_f3)
        self.assertEqual(l_test3, ["x0", "x1", "x2"])


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
