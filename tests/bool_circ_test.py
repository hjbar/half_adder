import numpy as np
import sys
import os

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
import unittest
from modules.bool_circ import *


class InitTest(unittest.TestCase):

    # Bool_circ

    def test_init_digraph(self):
        g = open_digraph.empty()
        b_g = bool_circ(g)
        self.assertEqual(b_g.inputs, [])
        self.assertEqual(b_g.outputs, [])
        self.assertEqual(b_g.nodes, {})
        self.assertIsInstance(b_g, bool_circ)
        self.assertIsNot(b_g.copy(), b_g)


class OpenDigraphTest(unittest.TestCase):

    # Setup

    def setUp(self):

        # Pour les methodes

        i1 = node(0, '0', {}, {5: 1})
        i2 = node(1, '1', {}, {3: 1})
        i3 = node(2, '0', {}, {6: 1})

        n1 = node(3, '~', {1: 1}, {4: 1})
        n2 = node(4, '&', {3: 1, 5: 1, 6: 1}, {7: 1})
        n3 = node(5, '|', {0: 1}, {4: 1})
        n4 = node(6, '^', {2: 1}, {4: 1})

        o0 = node(7, '', {4: 1}, {})

        node_list = [n1, n2, n3, n4, i1, i2, i3, o0]
        g = open_digraph([0, 1], [7], node_list)

        self.b_g = bool_circ(g)

        # Graph pour Adder et Half_Adder

        a_i0 = node(9, "", {}, {0: 1})
        a_i1 = node(10, "", {}, {1: 1})
        a_i2 = node(11, "", {}, {4: 1})

        a_c0 = node(0, "", {9: 1}, {2: 1, 5: 1})
        a_c1 = node(1, "", {10: 1}, {2: 1, 5: 1})
        a_c3 = node(3, "", {2: 1}, {6: 1, 7: 1})
        a_c4 = node(4, "", {11: 1}, {6: 1, 7: 1})

        a_n2 = node(2, "^", {0: 1, 1: 1}, {3: 1})
        a_n5 = node(5, "&", {0: 1, 1: 1}, {8: 1})
        a_n6 = node(6, "&", {3: 1, 4: 1}, {8: 1})
        a_n7 = node(7, "^", {3: 1, 4: 1}, {13: 1})
        a_n8 = node(8, "|", {5: 1, 6: 1}, {12: 1})

        a_o0 = node(12, "", {8: 1}, {})
        a_o1 = node(13, "", {7: 1}, {})

        a_node_list = [
            a_c0, a_c1, a_n2, a_c3, a_c4, a_n5, a_n6, a_n7, a_n8, a_i0, a_i1,
            a_i2, a_o0, a_o1
        ]

        g_a = open_digraph([9, 10, 11], [12, 13], a_node_list)

        self.b_a = bool_circ(g_a)

        g_ha = open_digraph([9, 10], [12, 13], a_node_list)
        self.b_ha = bool_circ(g_ha)
        self.b_ha[11].set_label("0")

        # Pour Registre

        r0_n0 = node(0, "0", {}, {1: 1})
        r0_n1 = node(2, "0", {}, {3: 1})
        r0_n2 = node(4, "0", {}, {5: 1})
        r0_o0 = node(1, "", {0: 1}, {})
        r0_o1 = node(3, "", {2: 1}, {})
        r0_o2 = node(5, "", {4: 1}, {})

        r0_node_list = [r0_n0, r0_o0, r0_n1, r0_o1, r0_n2, r0_o2]

        r0_g = open_digraph([], [1, 3, 5], r0_node_list)

        self.r0_g = bool_circ(r0_g)

        r1_n0 = node(0, "1", {}, {1: 1})
        r1_n1 = node(2, "0", {}, {3: 1})
        r1_n2 = node(4, "1", {}, {5: 1})
        r1_n3 = node(6, "1", {}, {7: 1})
        r1_o0 = node(1, "", {0: 1}, {})
        r1_o1 = node(3, "", {2: 1}, {})
        r1_o2 = node(5, "", {4: 1}, {})
        r1_o3 = node(7, "", {6: 1}, {})

        r1_node_list = [r1_n0, r1_o0, r1_n1, r1_o1, r1_n2, r1_o2, r1_n3, r1_o3]

        r1_g = open_digraph([], [1, 3, 5, 7], r1_node_list)

        self.r1_g = bool_circ(r1_g)

        # Pour les transformations

        #COPIE GATE
        t4_i0 = node(4, "", {}, {0: 1})
        t4_c0 = node(0, "0", {4: 1}, {1: 1})
        t4_c1 = node(1, "", {0: 1}, {2: 1, 3: 1})
        t4_n0 = node(2, "", {1: 1}, {})
        t4_n1 = node(3, "", {1: 1}, {})
        t4_node_list = [t4_i0, t4_c0, t4_c1, t4_n0, t4_n1]

        t4_g = open_digraph([4], [], t4_node_list)
        self.t4_b = bool_circ(t4_g)

        t4_c2 = node(0, "0", {}, {2: 1})
        t4_c3 = node(1, "0", {}, {3: 1})
        t4_n2 = node(2, "", {0: 1}, {})
        t4_n3 = node(3, "", {1: 1}, {})
        t4_node_res = [t4_c2, t4_c3, t4_n2, t4_n3]

        t4_res = open_digraph([4], [], t4_node_res)
        self.t4_res = bool_circ(t4_res)

        t4b_i0 = node(4, "", {}, {0: 1})
        t4b_c0 = node(0, "1", {4: 1}, {1: 1})
        t4b_c1 = node(1, "", {0: 1}, {2: 1, 3: 1})
        t4b_n0 = node(2, "", {1: 1}, {})
        t4b_n1 = node(3, "", {1: 1}, {})
        t4b_node_list = [t4b_i0, t4b_c0, t4b_c1, t4b_n0, t4b_n1]

        t4_g2 = open_digraph([4], [], t4b_node_list)
        self.t4_b2 = bool_circ(t4_g2)

        t4b_c2 = node(0, "1", {}, {2: 1})
        t4b_c3 = node(1, "1", {}, {3: 1})
        t4b_n2 = node(2, "", {0: 1}, {})
        t4b_n3 = node(3, "", {1: 1}, {})
        t4b_node_res = [t4b_c2, t4b_c3, t4b_n2, t4b_n3]

        t4_res2 = open_digraph([4], [], t4b_node_res)
        self.t4_res2 = bool_circ(t4_res2)

        # NEG GATE
        t2_i0 = node(3, "", {}, {0: 1})
        t2_c0 = node(0, "0", {3: 1}, {1: 1})
        t2_g0 = node(1, "~", {0: 1}, {2: 1})
        t2_n0 = node(2, "", {1: 1}, {})
        t2_node_list = [t2_i0, t2_c0, t2_g0, t2_n0]

        t2_g = open_digraph([], [], t2_node_list)
        self.t2_b = bool_circ(t2_g)

        t2_g0bis = node(1, "1", {}, {2: 1})
        t2_node_res = [t2_g0bis, t2_n0]

        t2_res = open_digraph([], [], t2_node_res)
        self.t2_res = bool_circ(t2_res)

        # AND GATE

        t5_i0 = node(4, "", {}, {0: 1})
        t5_i1 = node(3, "", {}, {1: 1})
        t5_n0 = node(0, "1", {4: 1}, {1: 1})
        t5_n1 = node(1, "&", {0: 1, 3: 1, 5: 1}, {2: 1})
        t5_a0 = node(2, "", {1: 1}, {})
        t5_a1 = node(5, "", {}, {1: 1})

        t5_node_list = [t5_i0, t5_i1, t5_n0, t5_n1, t5_a0, t5_a1]

        t5_g = open_digraph([3, 4], [], t5_node_list)
        self.t5_b = bool_circ(t5_g)

        t5_i1_res = node(3, "", {}, {1: 1})
        t5_n1_res = node(1, "&", {3: 1, 5: 1}, {2: 1})
        t5_a0_res = node(2, "", {1: 1}, {})
        t5_a1_res = node(5, "", {}, {1: 1})

        t5_node_list_res = [t5_i1_res, t5_n1_res, t5_a0_res, t5_a1_res]

        t5_g_res = open_digraph([3, 4], [], t5_node_list_res)
        self.t5_b_res = bool_circ(t5_g_res)

        t6_i0 = node(4, "", {}, {0: 1})
        t6_i1 = node(3, "", {}, {1: 1, 6: 1})
        t6_n0 = node(0, "0", {4: 1}, {1: 1})
        t6_n1 = node(1, "&", {0: 1, 3: 1, 5: 1}, {2: 1})
        t6_a0 = node(2, "", {1: 1}, {})
        t6_a1 = node(5, "", {6: 1}, {1: 1})
        t6_l1 = node(6, "", {3: 1}, {5: 1})

        t6_node_list = [t6_i0, t6_i1, t6_n0, t6_n1, t6_a0, t6_a1, t6_l1]

        t6_g = open_digraph([4], [], t6_node_list)
        self.t6_b = bool_circ(t6_g)

        t6_i1_res = node(3, "", {}, {0: 1, 6: 1})
        t6_c0_res = node(0, "", {3: 1}, {})
        t6_c1_res = node(4, "", {5: 1}, {})
        t6_n1_res = node(1, "0", {}, {2: 1})
        t6_a0_res = node(2, "", {1: 1}, {})
        t6_a1_res = node(5, "", {6: 1}, {4: 1})
        t6_l1_res = node(6, "", {3: 1}, {5: 1})

        t6_node_list_res = [
            t6_i1_res, t6_n1_res, t6_a0_res, t6_a1_res, t6_c0_res, t6_c1_res,
            t6_l1_res
        ]

        t6_g_res = open_digraph([4], [], t6_node_list_res)
        self.t6_b_res = bool_circ(t6_g_res)

        # OR GATE

        t7_i0 = node(4, "", {}, {0: 1})
        t7_i1 = node(3, "", {}, {1: 1})
        t7_n0 = node(0, "0", {4: 1}, {1: 1})
        t7_n1 = node(1, "|", {0: 1, 3: 1, 5: 1}, {2: 1})
        t7_a0 = node(2, "", {1: 1}, {})
        t7_a1 = node(5, "", {}, {1: 1})

        t7_node_list = [t7_i0, t7_i1, t7_n0, t7_n1, t7_a0, t7_a1]

        t7_g = open_digraph([3, 4], [], t7_node_list)
        self.t7_b = bool_circ(t7_g)

        t7_i1_res = node(3, "", {}, {1: 1})
        t7_n1_res = node(1, "|", {3: 1, 5: 1}, {2: 1})
        t7_a0_res = node(2, "", {1: 1}, {})
        t7_a1_res = node(5, "", {}, {1: 1})

        t7_node_list_res = [t7_i1_res, t7_n1_res, t7_a0_res, t7_a1_res]

        t7_g_res = open_digraph([3], [], t7_node_list_res)
        self.t7_b_res = bool_circ(t7_g_res)

        t8_i0 = node(4, "", {}, {0: 1})
        t8_i1 = node(3, "", {}, {1: 1, 6: 1})
        t8_n0 = node(0, "1", {4: 1}, {1: 1})
        t8_n1 = node(1, "|", {0: 1, 3: 1, 5: 1}, {2: 1})
        t8_a0 = node(2, "", {1: 1}, {})
        t8_a1 = node(5, "", {6: 1}, {1: 1})
        t8_l1 = node(6, "", {3: 1}, {5: 1})

        t8_node_list = [t8_i0, t8_i1, t8_n0, t8_n1, t8_a0, t8_a1, t8_l1]

        t8_g = open_digraph([4], [], t8_node_list)
        self.t8_b = bool_circ(t8_g)

        t8_i1_res = node(3, "", {}, {0: 1, 6: 1})
        t8_c0_res = node(0, "", {3: 1}, {})
        t8_c1_res = node(4, "", {5: 1}, {})
        t8_n1_res = node(1, "1", {}, {2: 1})
        t8_a0_res = node(2, "", {1: 1}, {})
        t8_a1_res = node(5, "", {6: 1}, {4: 1})
        t8_l1_res = node(6, "", {3: 1}, {5: 1})

        t8_node_list_res = [
            t8_i1_res, t8_n1_res, t8_a0_res, t8_a1_res, t8_c0_res, t8_c1_res,
            t8_l1_res
        ]

        t8_g_res = open_digraph([], [], t8_node_list_res)
        self.t8_b_res = bool_circ(t8_g_res)

        # XOR GATE
        t_i0 = node(4, "", {}, {0: 1})
        t_a1 = node(3, "", {}, {1: 1})
        t_n0 = node(0, "1", {4: 1}, {1: 1})
        t_n1 = node(1, "^", {0: 1, 3: 1}, {2: 1})
        t_a0 = node(2, "", {1: 1}, {})
        t_node_list = [t_i0, t_a1, t_n0, t_n1, t_a0]

        t_g = open_digraph([4], [], t_node_list)
        self.t_b = bool_circ(t_g)

        t_n2 = node(0, "~", {1: 1}, {2: 1})
        t_n1bis = node(1, "^", {3: 1}, {0: 1})
        t_a0bis = node(2, "", {0: 1}, {})
        t_node_res = [t_a1, t_n1bis, t_n2, t_a0bis]

        t_res = open_digraph([], [], t_node_res)
        self.t_res = bool_circ(t_res)

        tb_i0 = node(4, "", {}, {0: 1})
        tb_a1 = node(3, "", {}, {1: 1})
        tb_n0 = node(0, "0", {4: 1}, {1: 1})
        tb_n1 = node(1, "^", {0: 1, 3: 1}, {2: 1})
        tb_a0 = node(2, "", {1: 1}, {})
        tb_node_list = [tb_i0, tb_a1, tb_n0, tb_n1, tb_a0]

        t_g2 = open_digraph([4], [], tb_node_list)
        self.t_b2 = bool_circ(t_g2)

        tb_n1bis = node(1, "^", {3: 1}, {2: 1})
        tb_a0bis = node(2, "", {1: 1}, {})
        tb_node_res = [tb_a1, tb_n1bis, tb_a0bis]

        t_res2 = open_digraph([], [], tb_node_res)
        self.t_res2 = bool_circ(t_res2)

        #NEUTRAL GATE
        t3_c0 = node(0, "|", {}, {1: 1})
        t3_n0 = node(1, "", {0: 1}, {})
        t3_node_list = [t3_c0, t3_n0]

        t3_g = open_digraph([], [], t3_node_list)
        self.t3_b = bool_circ(t3_g)

        t3_c1 = node(0, "^", {}, {1: 1})
        t3_n1 = t3_n0.copy()
        t3_node_list2 = [t3_c1, t3_n1]

        t3_g2 = open_digraph([], [], t3_node_list2)
        self.t3_b2 = bool_circ(t3_g2)

        t3_c2 = node(0, "&", {}, {1: 1})
        t3_n2 = t3_n0.copy()
        t3_node_list3 = [t3_c2, t3_n2]

        t3_g3 = open_digraph([], [], t3_node_list3)
        self.t3_b3 = bool_circ(t3_g3)

        t3_c3 = node(0, "0", {}, {1: 1})
        t3_n3 = t3_n0.copy()
        t3_node_res = [t3_c3, t3_n3]

        t3_res = open_digraph([], [], t3_node_res)
        self.t3_res = bool_circ(t3_res)

        t3_c4 = node(0, "1", {}, {1: 1})
        t3_n4 = t3_n0.copy()
        t3_node_res2 = [t3_c4, t3_n4]

        t3_res2 = open_digraph([], [], t3_node_res2)
        self.t3_res2 = bool_circ(t3_res2)

        # test evaluate sur un graph

        e2_i0 = node(9, "", {}, {0: 1})
        e2_i1 = node(10, "", {}, {1: 1})
        e2_i2 = node(14, "", {}, {7: 1})
        e2_i3 = node(18, "", {}, {17: 1})
        e2_i4 = node(19, "", {}, {17: 1})
        e2_i5 = node(20, "", {}, {21: 1})
        e2_n0 = node(0, "", {9: 1}, {2: 1, 5: 1})
        e2_n1 = node(1, "", {10: 1}, {2: 2, 5: 1})
        e2_n2 = node(2, "^", {0: 1, 1: 2, 6: 1, 17: 1}, {3: 1})
        e2_n3 = node(3, "", {2: 1}, {4: 1, 7: 1})
        e2_n4 = node(4, "", {3: 1}, {})
        e2_n5 = node(5, "&", {0: 1, 1: 1, 21: 1}, {8: 1})
        e2_n6 = node(7, "^", {3: 1, 14: 1, 15: 1}, {16: 1})
        e2_n7 = node(8, "|", {5: 1}, {12: 1})
        e2_n8 = node(6, "1", {}, {2: 1})
        e2_n9 = node(15, "1", {}, {7: 1})
        e2_n10 = node(16, "~", {7: 1}, {13: 1})
        e2_n11 = node(17, "^", {18: 1, 19: 1}, {2: 1})
        e2_n12 = node(21, "", {20: 1}, {5: 1, 22: 1})
        e2_n13 = node(22, "~", {21: 1}, {23: 1})
        e2_n14 = node(23, "", {22: 1}, {24: 1})
        e2_n15 = node(24, "", {23: 1}, {})
        e2_o0 = node(12, "", {8: 1}, {})
        e2_o1 = node(13, "", {16: 1}, {})

        e2_node = [
            e2_i0, e2_i1, e2_i2, e2_i3, e2_i4, e2_i5, e2_n0, e2_n1, e2_n2,
            e2_n3, e2_n4, e2_n5, e2_n6, e2_n7, e2_n8, e2_n9, e2_n10, e2_n11,
            e2_n12, e2_n13, e2_n14, e2_n15, e2_o0, e2_o1
        ]
        e2_grph = open_digraph([9, 10, 14, 18, 19, 20], [12, 13], e2_node)
        self.e2_grph = bool_circ(e2_grph)

        e2_res_i0 = node(9, "", {}, {0: 1})
        e2_res_i1 = node(10, "", {}, {1: 1})
        e2_res_i2 = node(14, "", {}, {2: 1})
        e2_res_i3 = node(18, "", {}, {2: 1})
        e2_res_i4 = node(19, "", {}, {2: 1})
        e2_res_i5 = node(20, "", {}, {15: 1})

        e2_res_n0 = node(0, "", {9: 1}, {2: 1, 5: 1})
        e2_res_n1 = node(1, "", {10: 1}, {5: 1})
        e2_res_n2 = node(2, "^", {0: 1, 14: 1, 18: 1, 19: 1}, {16: 1})
        e2_res_n3 = node(5, "&", {0: 1, 1: 1, 15: 1}, {8: 1})
        e2_res_n4 = node(8, "|", {5: 1}, {12: 1})
        e2_res_n5 = node(15, "", {20: 1}, {5: 1})
        e2_res_n6 = node(16, "~", {2: 1}, {13: 1})

        e2_res_o0 = node(12, "", {8: 1}, {})
        e2_res_o1 = node(13, "", {16: 1}, {})

        e2_res_node = [
            e2_res_i0, e2_res_i1, e2_res_i2, e2_res_i3, e2_res_i4, e2_res_i5,
            e2_res_n0, e2_res_n1, e2_res_n2, e2_res_n3, e2_res_n4, e2_res_n5,
            e2_res_n6, e2_res_o0, e2_res_o1
        ]
        e2_res_grph = open_digraph([9, 10, 14, 18, 19, 20], [12, 13],
                                   e2_res_node)
        self.e2_res_grph = bool_circ(e2_res_grph)

        # ASSOC_XOR_GATE
        x_n0 = node(0, "", {}, {5: 1})
        x_n1 = node(1, "", {}, {5: 1})
        x_p0 = node(5, "^", {0: 1, 1: 1}, {6: 1})
        x_n2 = node(2, "", {}, {6: 1})
        x_n3 = node(3, "", {}, {6: 1})
        x_p1 = node(6, "^", {5: 1, 2: 1, 3: 1}, {4: 1})
        x_n4 = node(4, "", {6: 1}, {})
        x_list = [x_n0, x_n1, x_n2, x_n3, x_n4, x_p0, x_p1]

        x_g = open_digraph([], [4], x_list)
        self.x_b = bool_circ(x_g)

        x2_n0 = node(0, "", {}, {5: 1})
        x2_n1 = node(1, "", {}, {5: 1})
        x2_n2 = node(2, "", {}, {5: 1})
        x2_n3 = node(3, "", {}, {5: 1})
        x2_p1 = node(5, "^", {0: 1, 1: 1, 2: 1, 3: 1}, {4: 1})
        x2_n4 = node(4, "", {5: 1}, {})
        x2_list = [x2_n0, x2_n1, x2_n2, x2_n3, x2_n4, x2_p1]

        x2_g = open_digraph([], [4], x2_list)
        self.res_x = bool_circ(x2_g)

        #ASSOC_COPY_GATE
        ac_n0 = node(0, "", {}, {1: 1})
        ac_c0 = node(1, "", {0: 1}, {2: 1, 3: 1, 4: 1, 5: 1})
        ac_n1 = node(2, "", {1: 1}, {})
        ac_n2 = node(3, "", {1: 1}, {})
        ac_n3 = node(4, "", {1: 1}, {})
        ac_c1 = node(5, "", {1: 1}, {6: 1, 7: 1, 8: 1})
        ac_n4 = node(6, "", {5: 1}, {})
        ac_n5 = node(7, "", {5: 1}, {})
        ac_n6 = node(8, "", {5: 1}, {})

        ac_list = [
            ac_n0, ac_n1, ac_n2, ac_n3, ac_n4, ac_n5, ac_n6, ac_c0, ac_c1
        ]

        ac_g = open_digraph([], [], ac_list)
        self.ac_b = bool_circ(ac_g)

        ac2_n0 = node(0, "", {}, {5: 1})
        ac2_n1 = node(2, "", {5: 1}, {})
        ac2_n2 = node(3, "", {5: 1}, {})
        ac2_n3 = node(4, "", {5: 1}, {})
        ac2_c1 = node(5, "", {0: 1}, {2: 1, 3: 1, 4: 1, 6: 1, 7: 1, 8: 1})
        ac2_n4 = node(6, "", {5: 1}, {})
        ac2_n5 = node(7, "", {5: 1}, {})
        ac2_n6 = node(8, "", {5: 1}, {})

        ac2_list = [
            ac2_n0, ac2_n1, ac2_n2, ac2_n3, ac2_n4, ac2_n5, ac2_n6, ac2_c1
        ]

        ac2_g = open_digraph([], [], ac2_list)
        self.ac2_b = bool_circ(ac2_g)

        #INVOL_XOR_GATE
        x3_n0 = node(0, "", {}, {3: 1})
        x3_n1 = node(1, "", {}, {3: 1})
        x3_n2 = node(2, "", {}, {3: 1})
        x3_x0 = node(3, "^", {0: 1, 1: 1, 2: 1, 5: 2}, {6: 1})
        x3_c0 = node(5, "", {4: 1}, {3: 2, 7: 1, 8: 1, 9: 1})
        x3_n3 = node(4, "", {}, {5: 1})
        x3_n4 = node(6, "", {3: 1}, {})
        x3_n5 = node(7, "", {5: 1}, {})
        x3_n6 = node(8, "", {5: 1}, {})
        x3_n7 = node(9, "", {5: 1}, {})

        x3_list = [
            x3_n0, x3_n1, x3_n2, x3_n3, x3_n4, x3_n5, x3_n6, x3_n7, x3_x0,
            x3_c0
        ]

        x3_g = open_digraph([], [], x3_list)
        self.x3_b = bool_circ(x3_g)

        res3_x0 = node(3, "^", {0: 1, 1: 1, 2: 1}, {6: 1})
        res3_c0 = node(5, "", {4: 1}, {7: 1, 8: 1, 9: 1})

        res3_list = [
            x3_n0, x3_n1, x3_n2, x3_n3, x3_n4, x3_n5, x3_n6, x3_n7, res3_x0,
            res3_c0
        ]

        res3_g = open_digraph([], [], res3_list)
        self.res3_b = bool_circ(res3_g)

        #ERASURE
        e2_n0 = node(0, "", {}, {3: 1})
        e2_n1 = node(1, "", {}, {3: 1})
        e2_n2 = node(2, "", {}, {3: 1})
        e2_op = node(3, "&", {0: 1, 1: 1, 2: 1}, {4: 1})
        e2_cp = node(4, "", {3: 1}, {})

        e2_list = [e2_n0, e2_n1, e2_n2, e2_op, e2_cp]

        e2_g = open_digraph([], [], e2_list)
        self.e2_b = bool_circ(e2_g)

        e3_n0 = node(0, "", {}, {3: 1})
        e3_n1 = node(1, "", {}, {4: 1})
        e3_n2 = node(2, "", {}, {5: 1})
        e3_c1 = node(3, "", {0: 1}, {})
        e3_c2 = node(4, "", {1: 1}, {})
        e3_c3 = node(5, "", {2: 1}, {})

        e3_list = [e3_n0, e3_n1, e3_n2, e3_c1, e3_c2, e3_c3]

        e3_g = open_digraph([], [], e3_list)
        self.e3_b = bool_circ(e3_g)

        #NOT_XOR
        no_n0 = node(0, "", {}, {3: 1})
        no_n1 = node(1, "", {}, {3: 1})
        no_n2 = node(2, "", {}, {3: 1})
        no_x0 = node(3, "^", {0: 1, 1: 1, 2: 1, 5: 1}, {6: 1})
        no_n3 = node(4, "", {}, {5: 1})
        no_t0 = node(5, "~", {4: 1}, {3: 1})
        no_n4 = node(6, "", {3: 1}, {})

        no_list = [no_n0, no_n1, no_n2, no_n3, no_n4, no_x0, no_t0]

        no_g = open_digraph([], [], no_list)
        self.no_b = bool_circ(no_g)

        no2_n0 = node(0, "", {}, {3: 1})
        no2_n1 = node(1, "", {}, {3: 1})
        no2_n2 = node(2, "", {}, {3: 1})
        no2_n3 = node(4, "", {}, {3: 1})
        no2_x0 = node(3, "^", {0: 1, 1: 1, 2: 1, 4: 1}, {5: 1})
        no2_t0 = node(5, "~", {3: 1}, {6: 1})
        no2_n4 = node(6, "", {5: 1}, {})

        no2_list = [no2_n0, no2_n1, no2_n2, no2_n3, no2_n4, no2_x0, no2_t0]

        no2_g = open_digraph([], [], no2_list)
        self.no2_b = bool_circ(no2_g)

        #NOT_COPY
        nc_n0 = node(0, "", {}, {1: 1})
        nc_t0 = node(1, "~", {0: 1}, {2: 1})
        nc_c0 = node(2, "", {1: 1}, {3: 1, 4: 1, 5: 1})
        nc_n1 = node(3, "", {2: 1}, {})
        nc_n2 = node(4, "", {2: 1}, {})
        nc_n3 = node(5, "", {2: 1}, {})

        nc_list = [nc_n0, nc_n1, nc_n2, nc_n3, nc_t0, nc_c0]

        nc_g = open_digraph([], [], nc_list)
        self.nc_b = bool_circ(nc_g)

        nc2_n0 = node(0, "", {}, {2: 1})
        nc2_c0 = node(2, "", {0: 1}, {1: 1, 6: 1, 7: 1})
        nc2_n1 = node(3, "", {1: 1}, {})
        nc2_n2 = node(4, "", {6: 1}, {})
        nc2_n3 = node(5, "", {7: 1}, {})
        nc2_t0 = node(1, "~", {2: 1}, {3: 1})
        nc2_t1 = node(6, "~", {2: 1}, {4: 1})
        nc2_t2 = node(7, "~", {2: 1}, {5: 1})

        nc2_list = [
            nc2_n0, nc2_n1, nc2_n2, nc2_n3, nc2_t0, nc2_t1, nc2_t2, nc2_c0
        ]

        nc2_g = open_digraph([], [], nc2_list)
        self.nc2_b = bool_circ(nc2_g)

        #INVOL_NOT_GATE
        in_n0 = node(0, "", {}, {1: 1})
        in_t0 = node(1, "~", {0: 1}, {2: 1})
        in_t1 = node(2, "~", {1: 1}, {3: 1})
        in_n1 = node(3, "", {2: 1}, {})

        in_list = [in_n0, in_n1, in_t0, in_t1]

        in_g = open_digraph([], [], in_list)
        self.in_b = bool_circ(in_g)

        in2_n0 = node(0, "", {}, {3: 1})
        in2_n1 = node(3, "", {0: 1}, {})

        in2_list = [in2_n0, in2_n1]

        in2_g = open_digraph([], [], in2_list)
        self.in2_b = bool_circ(in2_g)

    # Methodes

    def test_copy_bool_circ(self):
        graph = self.b_g.copy()
        self.assertEqual(graph, self.b_g)

        graph.set_input_ids({})
        graph.set_output_ids({})
        graph.add_edge(0, 1)
        self.assertIsNot(
            graph, self.b_g
        )  # On test si modifier une copie, modifie aussi l'original

    def test_is_cyclic(self):
        res1 = self.b_g.is_cyclic()
        self.assertEqual(res1, False)

        # On ne peut pas creer un graph cyclique
        try:
            self.b_g.add_edge(4, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_is_well_formed(self):
        self.b_g.is_well_formed()

        # Graph cyclique
        try:
            self.b_g.add_edge(4, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        # Graph avec mauvais label
        try:
            self.b_g[7].set_label('""')
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        # Graph avec mauvaise copie
        try:
            self.tmp_g = self.b_g.copy()
            self.tmp_g.set_output_ids([])
            self.tmp_g.add_edge(4, 7)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        # Graph avec mauvais OU
        try:
            self.g_g.add_edge(5, 4)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        # Graph avec mauvais ET
        try:
            self.tmp_g = self.b_g.copy()
            self.tmp_g.set_output_ids([])
            self.tmp_g[7].set_label("|")
            self.tmp_g.add_edge(4, 7)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        # Graph avec mauvais ~ (trop de in)
        try:
            self.tmp_g = self.b_g.copy()
            self.tmp_g.set_input_ids([])
            self.tmp_g.add_edge(1, 3)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        # Graph avec mauvaise ~ (trop de out)
        try:
            self.b_g.add_edge(3, 4)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_random_bool_circ(self):

        for i in range(1, 11):

            nb_input = np.random.randint(1, 6)
            nb_output = np.random.randint(1, 6)

            g = bool_circ.random_bool_circ(i, nb_input, nb_output)

            nb_node = len(g.get_nodes())
            self.assertEqual(nb_node >= i, True)

            nb_input_ids = len(g.get_input_ids())
            self.assertEqual(nb_input_ids, nb_input)

            nb_output_ids = len(g.get_output_ids())
            self.assertEqual(nb_output_ids, nb_output)

            try:
                g.is_well_formed()
                self.assertEqual(True, True)
            except:
                self.assertEqual(True, False)

        try:
            g = bool_circ.random_bool_circ(5, 0, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g = bool_circ.random_bool_circ(5, 5, 0)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_adder(self):
        b0 = bool_circ.Adder(0)
        self.assertEqual(b0, self.b_a)

        b1 = bool_circ.Adder(0)
        self.assertEqual(b1, self.b_a)

        b3 = bool_circ.Adder(5)
        try:
            b3.is_well_formed()
            self.assertEqual(True, True)
        except:
            self.assertEqual(True, False)

        # D'autres tests visuels dans worksheet_graph pour des Adder plus grands

    def test_half_adder(self):
        b0 = bool_circ.Half_Adder(0)
        self.assertEqual(b0, self.b_ha)

        b1 = bool_circ.Half_Adder(5)
        try:
            b1.is_well_formed()
            self.assertEqual(True, True)
        except:
            self.assertEqual(True, False)

        # D'autres tests visuels dans worksheet_graph pour des Half_Adder plus grands

    def test_register(self):
        r0 = bool_circ.registre(0, 3)
        self.assertEqual(r0, self.r0_g)

        r1 = bool_circ.registre(11, 4)
        self.assertEqual(r1, self.r1_g)

        try:
            r2 = bool_circ.registre(17, 4)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_copy_gate(self):
        t_b_copy = self.t4_b.copy()

        self.t4_b.copy_gate(1, 0)
        self.assertEqual(self.t4_b, self.t4_res)

        self.t4_b2.copy_gate(1, 0)
        self.assertEqual(self.t4_b2, self.t4_res2)

        try:
            t_b_copy.copy_gate(0, 1)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            t_b_copy.copy(1, 2)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_neg_gate(self):
        t_b_copy = self.t2_b.copy()

        self.t2_b.neg_gate(1, 0)
        self.assertEqual(self.t2_b, self.t2_res)

        try:
            t_b_copy.neg_gate(0, 1)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            t_b_copy.neg_gate(1, 2)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_and_gate(self):

        self.t5_b.and_gate(1, 0)
        self.assertEqual(self.t5_b, self.t5_b_res)

        self.t6_b.and_gate(1, 0)
        self.assertEqual(self.t6_b, self.t6_b_res)

    def test_or_gate(self):
        self.t7_b.or_gate(1, 0)
        self.assertEqual(self.t7_b, self.t7_b_res)

        self.t8_b.or_gate(1, 0)
        self.assertEqual(self.t8_b, self.t8_b_res)

    def test_xor_gate(self):
        t_b_copy = self.t_b.copy()

        self.t_b.xor_gate(1, 0)
        self.assertEqual(self.t_b, self.t_res)

        self.t_b2.xor_gate(1, 0)
        self.assertEqual(self.t_b2, self.t_res2)

        try:
            t_b_copy.xor_gate(0, 1)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            t_b_copy.xor_gate(1, 2)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_neutral_gate(self):
        t_b_copy1 = self.t3_b.copy()
        t_b_copy2 = self.t3_b.copy()

        self.t3_b.neutral_gate(0)
        self.assertEqual(self.t3_b, self.t3_res)

        self.t3_b2.neutral_gate(0)
        self.assertEqual(self.t3_b2, self.t3_res)

        self.t3_b3.neutral_gate(0)
        self.assertEqual(self.t3_b3, self.t3_res2)

        try:
            t_b_copy1[0].set_label("~")
            self.t_b_copy1.neutral_gate(0)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            t_b_copy2.add_node("", {}, {0: 1})
            t_b_copy2.neutral_gate(0)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_evaluate(self):
        self.e2_grph.evaluate()
        self.assertEqual(self.e2_grph, self.e2_res_grph)

    def test_assoc_xor_gate(self):
        g_copy = self.x_b.copy()

        self.x_b.assoc_xor_gate(6, 5)
        self.assertEqual(self.x_b, self.res_x)

        try:
            g_copy.assoc_xor_gate(5, 6)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(parents={5: 1})
            g_copy.assoc_xor_gate(6, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.remove_parellel_edges(5, 6)
            g_copy.assoc_xor_gate(6, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_assoc_copy_gate(self):
        g_copy = self.ac_b.copy()

        self.ac_b.assoc_copy_gate(1, 5)
        self.assertEqual(self.ac_b, self.ac2_b)

        try:
            g_copy.assoc_copy_gate(5, 1)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.remove_edge(1, 5)
            g_copy.assoc_copy_gate(1, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(children={1: 1})
            g_copy.assoc_copy_gate(1, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(children={5: 1})
            g_copy.assoc_copy_gate(1, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_invol_xor_gate(self):
        g_copy = self.x3_b.copy()

        g_copy2 = self.x3_b.copy()
        g_copy2.add_edge(5, 3)
        g_copy2.add_edge(5, 3)

        g_copy3 = self.x3_b.copy()
        g_copy3.add_edge(5, 3)

        g_copy4 = self.x3_b.copy()
        g_copy4.remove_edge(5, 3)

        self.x3_b.invol_xor_gate(3, 5)
        self.assertEqual(self.x3_b, self.res3_b)

        g_copy2.invol_xor_gate(3, 5)
        self.assertEqual(g_copy2, self.res3_b)

        g_copy3.invol_xor_gate(3, 5)
        self.assertEqual(g_copy3, g_copy4)

        try:
            g_copy.assoc_xor_gate(5, 3)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.remove_parellel_edges(5, 3)
            g_copy.assoc_xor_gate(3, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.remove_edge(5, 3)
            g_copy.assoc_xor_gate(3, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(parents={3: 1})
            g_copy.assoc_xor_gate(3, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(children={5: 1})
            g_copy.assoc_xor_gate(3, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_erasure(self):
        g_copy = self.e2_b.copy()

        const_graph = self.e2_b.copy()
        const_graph[0].set_label("0")
        const_res = self.e3_b.copy()
        const_res[0].set_label("0")

        self.e2_b.apply_erasure_gate(3, 4)
        self.assertEqual(self.e2_b, self.e3_b)

        const_graph.apply_erasure_gate(3, 4)
        self.assertEqual(const_graph, const_res)

        try:
            g_copy.apply_erasure_gate(4, 3)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.remove_edge(3, 4)
            g_copy.apply_erasure_gate(3, 4)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(parents={3: 1})
            g_copy.apply_erasure_gate(3, 4)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(children={4: 1})
            g_copy.apply_erasure_gate(3, 4)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_not_xor(self):
        g_copy = self.no_b.copy()

        self.no_b.not_through_xor_gate(3, 5)
        self.assertEqual(self.no_b, self.no2_b)

        try:
            g_copy.not_through_xor_gate(5, 3)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.remove_edge(5, 3)
            g_copy.not_through_xor_gate(3, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(children={5: 1})
            g_copy.not_through_xor_gate(3, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(parents={3: 1})
            g_copy.not_through_xor_gate(3, 5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_not_copy(self):
        g_copy = self.nc_b.copy()

        self.nc_b.not_through_copy_gate(1, 2)
        self.assertEqual(self.nc_b, self.nc2_b)

        try:
            g_copy.not_through_copy_gate(2, 1)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.remove_edge(1, 2)
            g_copy.not_through_copy_gate(1, 2)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(children={1: 1})
            g_copy.not_through_copy_gate(1, 2)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(children={2: 1})
            g_copy.not_through_copy_gate(1, 2)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_invol_not_gate(self):
        g_copy = self.in_b.copy()

        self.in_b.invol_not_gate(1, 2)
        self.assertEqual(self.in_b, self.in2_b)

        try:
            g_copy.invol_not_gate(2, 1)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.remove_edge(1, 2)
            g_copy.invol_not_gate(1, 2)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(children={1: 1})
            g_copy.invol_not_gate(1, 2)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            g_copy.add_node(parents={2: 1})
            g_copy.invol_not_gate(1, 2)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_evaluate_half_adder(self):
        ha = bool_circ.Half_Adder(3)

        reg1 = bool_circ.registre(6, size=8)
        reg2 = bool_circ.registre(5, size=8)
        reg = reg1.parallel(reg2)

        comp = ha.compose(reg)
        comp.evaluate()

        comp_nodes = comp.get_nodes()
        comp_outputs = comp.get_output_ids()

        self.assertEqual(len(comp_nodes), 18)
        self.assertEqual(len(comp_outputs), 9)

        s = ""
        for i in comp_outputs:
            output_comp = comp[i]
            s += comp[output_comp.get_parents_ids()[0]].get_label()

        self.assertEqual(s, "000001011")

    def test_dec_enc(self):
        ha = bool_circ.Half_Adder(3)

        for i in range(0, 16):
            for j in range(0, 32):

                reg1 = bool_circ.registre(i * i, size=8)
                reg2 = bool_circ.registre(4 * j + 1, size=8)

                reg = reg1.parallel(reg2)
                comp = ha.compose(reg)

                comp.evaluate()

                # On test si on trouve la bonne reponse

                comp_nodes = comp.get_nodes()
                comp_outputs = comp.get_output_ids()

                self.assertEqual(len(comp_nodes), 18)
                self.assertEqual(len(comp_outputs), 9)

                s = ""

                for k in comp_outputs:
                    s += comp[comp[k].get_parents_ids()[0]].get_label()

                res = i * i + 4 * j + 1
                b = str(bin(res)[2:])

                if len(b) < 9:
                    b = "0" * (8 - len(b)) + b

                    if res >= 2**8:
                        b = "1" + b

                    else:
                        b = "0" + b

                self.assertEqual(s, b)

    def test_dec_enc_1modif(self):
        enc = bool_circ.enc()

        for j in range(7):

            dec = bool_circ.dec()
            add_neg(dec, j)

            for i in range(16):
                reg = bool_circ.registre(i, size=4)

                comp = dec.compose(enc)
                comp.icompose(reg)

                comp.evaluate()

                outputs_comp = comp.get_output_ids()
                outputs_reg = reg.get_output_ids()

                self.assertTrue(len(outputs_comp) == len(outputs_reg) == 4)

                for i in range(4):
                    output_comp = comp[outputs_comp[i]]
                    output_reg = reg[outputs_reg[i]]
                    n_comp = comp[output_comp.get_parents_ids()[0]]
                    n_reg = reg[output_reg.get_parents_ids()[0]]

                    self.assertTrue(n_comp.get_label() == n_reg.get_label())

                    nodes_comp = comp.get_nodes()
                    nodes_reg = reg.get_nodes()

                self.assertTrue(len(nodes_comp) == len(nodes_reg) == 8)

    def test_dec_enc_2modifs(self):
        enc = bool_circ.enc()

        for j in range(6):

            dec = bool_circ.dec()
            add_neg(dec, j)
            add_neg(dec, j + 1)

            for i in range(16):
                reg = bool_circ.registre(i, size=4)

                comp = dec.compose(enc)
                comp.icompose(reg)

                comp.evaluate()

                outputs_comp = comp.get_output_ids()
                outputs_reg = reg.get_output_ids()

                self.assertTrue(len(outputs_comp) == len(outputs_reg) == 4)

                flag = True

                for i in range(4):
                    output_comp = comp[outputs_comp[i]]
                    output_reg = reg[outputs_reg[i]]
                    n_comp = comp[output_comp.get_parents_ids()[0]]
                    n_reg = reg[output_reg.get_parents_ids()[0]]

                    if n_comp.get_label() != n_reg.get_label():
                        flag = False

                    nodes_comp = comp.get_nodes()
                    nodes_reg = reg.get_nodes()

                self.assertTrue(len(nodes_comp) == len(nodes_reg) == 8)

                self.assertFalse(flag)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run"""


# Fonction annexe
def add_neg(dec, no_input):
    """
    Ajoute une porte negative sur un decodeur
    dec : bool_circ -> correspond a un decodeur d'Hamming
    no_input : int -> l'input que l'on souhaite erroner
    """
    dec_input = dec.get_input_ids()

    i_no = dec[no_input]
    fils_id = i_no.get_children_ids()[0]
    dec.remove_edge(no_input, fils_id)

    dec.add_node('~', {no_input: 1}, {fils_id: 1})

    dec.set_input_ids(dec_input)
