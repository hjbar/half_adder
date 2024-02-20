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

        # Pour les tests de iparellel & parallel

        self.p_g = self.g_g.copy()

        g_n0 = node(7, 'a', {10: 1, 11: 1}, {8: 1, 9: 1})
        g_n1 = node(8, 'b', {7: 1}, {9: 2, 12: 1})
        g_n2 = node(9, 'c', {7: 1, 8: 2}, {13: 1})
        g_i0 = node(10, 'i0', {}, {7: 1})
        g_i1 = node(11, 'i1', {}, {7: 1})
        g_o0 = node(12, 'o0', {8: 1}, {})
        g_o1 = node(13, 'o1', {9: 1}, {})

        g2_n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        g2_n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        g2_n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        g2_i0 = node(3, 'i0', {}, {0: 1})
        g2_i1 = node(4, 'i1', {}, {0: 1})
        g2_o0 = node(5, 'o0', {1: 1}, {})
        g2_o1 = node(6, 'o1', {2: 1}, {})

        good_g_node_list = [
            g_n0, g_n1, g_n2, g_i0, g_i1, g_o0, g_o1, g2_n0, g2_n1, g2_n2,
            g2_i0, g2_i1, g2_o0, g2_o1
        ]

        self.good_g = open_digraph([10, 11, 3, 4], [12, 13, 5, 6],
                                   good_g_node_list)

        # Pour les tests de icompose & compose

        self.c_g = self.g_g.copy()

        g2_n0 = node(7, 'a', {10: 1, 11: 1}, {8: 1, 9: 1})
        g2_n1 = node(8, 'b', {7: 1}, {9: 2, 0: 1})
        g2_n2 = node(9, 'c', {7: 1, 8: 2}, {0: 1})
        g2_o0 = node(10, 'i0', {}, {7: 1})
        g2_o1 = node(11, 'i1', {}, {7: 1})

        g_n0 = node(0, 'a', {8: 1, 9: 1}, {1: 1, 2: 1})
        g_n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        g_n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        g_i0 = node(5, 'o0', {1: 1}, {})
        g_i1 = node(6, 'o1', {2: 1}, {})

        good_c_g_node_list = [
            g_n0, g_n1, g_n2, g_i0, g_i1, g2_n0, g2_n1, g2_n2, g2_o0, g2_o1
        ]

        self.good_c_g = open_digraph([10, 11], [5, 6], good_c_g_node_list)

        # Pour les tests de identity

        i_n0 = node(0, '', {}, {1: 1})
        i_n1 = node(1, '', {0: 1}, {})

        i_node_list = [i_n0, i_n1]

        self.i_g = open_digraph([0], [1], i_node_list)

        i3_n0 = node(0, '', {}, {1: 1})
        i3_n1 = node(1, '', {0: 1}, {})

        i3_n2 = node(2, '', {}, {3: 1})
        i3_n3 = node(3, '', {2: 1}, {})

        i3_n4 = node(4, '', {}, {5: 1})
        i3_n5 = node(5, '', {4: 1}, {})

        i3_node_list = [i3_n0, i3_n1, i3_n2, i3_n3, i3_n4, i3_n5]

        self.i3_g = open_digraph([0, 2, 4], [1, 3, 5], i3_node_list)

        # Pour les tests de connected_components et connected_components_list

        self.dic1 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.list1 = [open_digraph([4, 3], [6, 5], g_node_list)]

        g_n0 = node(7, 'a', {10: 1, 11: 1}, {8: 1, 9: 1})
        g_n1 = node(8, 'b', {7: 1}, {9: 2, 12: 1})
        g_n2 = node(9, 'c', {7: 1, 8: 2}, {13: 1})
        g_i0 = node(10, 'i0', {}, {7: 1})
        g_i1 = node(11, 'i1', {}, {7: 1})
        g_o0 = node(12, 'o0', {8: 1}, {})
        g_o1 = node(13, 'o1', {9: 1}, {})

        g2_n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        g2_n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        g2_n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})
        g2_i0 = node(3, 'i0', {}, {0: 1})
        g2_i1 = node(4, 'i1', {}, {0: 1})
        g2_o0 = node(5, 'o0', {1: 1}, {})
        g2_o1 = node(6, 'o1', {2: 1}, {})

        self.dic2 = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            6: 1,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0
        }
        node_list21 = [g_n0, g_n1, g_n2, g_i0, g_i1, g_o0, g_o1]
        node_list22 = [g2_n0, g2_n1, g2_n2, g2_i0, g2_i1, g2_o0, g2_o1]
        self.list2 = [
            open_digraph([11, 10], [13, 12], node_list21),
            open_digraph([4, 3], [6, 5], node_list22)
        ]

        self.graph3 = self.g_g.copy()
        self.graph3.add_node()
        self.dic3 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 1}
        self.list3 = [
            open_digraph([4, 3], [6, 5], g_node_list),
            open_digraph([], [], [node(7, "", {}, {})])
        ]

    # Test des methodes

    def test_iparallel(self):
        test_g_g = self.g_g.copy()
        self.p_g.iparallel(self.g_g)
        self.assertEqual((self.p_g), (self.good_g))
        self.assertEqual((test_g_g), (self.g_g))

        test_p_g = self.p_g.copy()

        self.p_g.iparallel(open_digraph.empty())
        self.assertEqual((test_p_g), (self.p_g))

        p2_g = open_digraph.empty()
        p2_g.iparallel(self.p_g)
        self.assertEqual((p2_g), (self.p_g))
        self.assertEqual((test_p_g), (self.p_g))

        del p2_g[0]
        self.assertEqual((test_p_g), (self.p_g))

    def test_parallel(self):
        test_g_g = self.g_g.copy()
        test_p_g = self.p_g.copy()

        res0 = self.p_g.parallel(self.g_g)

        self.assertEqual((res0), (self.good_g))
        self.assertEqual((test_g_g), (self.g_g))
        self.assertEqual((test_p_g), (self.p_g))

        p2_g = self.p_g.copy()
        test_p2_g = p2_g.copy()

        res1 = p2_g.parallel(open_digraph.empty())

        self.assertEqual((res1), (p2_g))
        self.assertEqual((test_p2_g), (p2_g))

        p3_g = open_digraph.empty()
        test_p3_g = p3_g.copy()

        res2 = p3_g.parallel(self.p_g)

        self.assertEqual((res2), (self.p_g))
        self.assertEqual((test_p_g), (self.p_g))
        self.assertEqual((test_p3_g), (p3_g))

        del res2[0]
        self.assertEqual((test_p_g), (self.p_g))

    def test_icompose(self):
        test_g_g = self.g_g.copy()
        self.c_g.icompose(self.g_g)

        self.c_g.is_well_formed()

        self.assertEqual(self.c_g, self.good_c_g)
        self.assertEqual((test_g_g), (self.g_g))

        try:
            self.c_g.icompose(open_digraph.empty())
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            vide = open_digraph.empty()
            vide.icompose(self.c_g)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        test_c_g = self.c_g.copy()
        del self.c_g[0]
        self.assertEqual((test_c_g), (self.good_c_g))

        vide_base = open_digraph.empty()
        vide1 = open_digraph.empty()
        vide2 = open_digraph.empty()

        vide1.icompose(vide2)

        vide1.is_well_formed()

        self.assertEqual((vide1), (vide_base))
        self.assertEqual((vide2), (vide_base))

    def test_compose(self):
        test_g_g = self.g_g.copy()
        test_c_g = self.c_g.copy()
        res1 = self.c_g.compose(self.g_g)

        res1.is_well_formed()

        self.assertEqual((res1), (self.good_c_g))
        self.assertEqual((test_g_g), (self.g_g))
        self.assertEqual((test_c_g), (self.c_g))

        try:
            res = self.c_g.compose(open_digraph.empty())
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        try:
            vide = open_digraph.empty()
            vide.compose(self.c_g)
            res = self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        test = res1.copy()
        del res1[0]
        self.assertEqual((test), (self.good_c_g))

        vide_base = open_digraph.empty()
        vide1 = open_digraph.empty()
        vide2 = open_digraph.empty()

        res2 = vide1.compose(vide2)

        res2.is_well_formed()

        self.assertEqual((res2), (vide_base))
        self.assertEqual((vide1), (vide_base))
        self.assertEqual((vide2), (vide_base))

    def test_identity(self):
        iden0 = open_digraph.identity(0)
        self.assertEqual((iden0), (open_digraph.empty()))

        iden1 = open_digraph.identity(1)
        self.assertEqual((iden1), (self.i_g))

        iden3 = open_digraph.identity(3)
        self.assertEqual((iden3), (self.i3_g))

    def test_connected_components(self):
        cpt1, dic1 = self.g_g.connected_components()
        self.assertEqual(cpt1, 1)
        self.assertEqual(dic1, self.dic1)

        cpt2, dic2 = self.good_g.connected_components()
        self.assertEqual(cpt2, 2)
        self.assertEqual(dic2, self.dic2)

        cpt3, dic3 = self.graph3.connected_components()
        self.assertEqual(cpt3, 2)
        self.assertEqual(dic3, self.dic3)

    def test_connected_components_list(self):
        list1 = self.g_g.connected_components_list()
        self.assertEqual(list1, self.list1)

        list2 = self.good_g.connected_components_list()
        self.assertEqual(list2, self.list2)

        list3 = self.graph3.connected_components_list()
        self.assertEqual(list3, self.list3)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
