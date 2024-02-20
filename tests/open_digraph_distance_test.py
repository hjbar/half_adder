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

        # Pour les tests de l'algo de Dijkstra

        # Dist et Prev de self.g_g pour src = a (id : 0) avec direction = None
        self.dict_dist1 = {0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2}
        self.dict_prev1 = {1: 0, 2: 0, 5: 1, 6: 2, 3: 0, 4: 0}

        # Dist et Prev de self.g_g pour src = a (id : 0) avec direction = -1
        self.dict_dist2 = {0: 0, 3: 1, 4: 1}
        self.dict_prev2 = {3: 0, 4: 0}

        # Dist et Prev de self.g_g pour src = a (id : 0) avec direction = 1
        self.dict_dist3 = {0: 0, 1: 1, 2: 1, 5: 2, 6: 2}
        self.dict_prev3 = {1: 0, 2: 0, 5: 1, 6: 2}

        # Pour les tests de shortest_path

        # Chemin de i0 vers i0 pour self.g_g
        self.dist_list1 = []

        # Chemin de o0 vers o1 pour self.g_g
        self.dist_list2 = [5, 1, 2, 6]

        # Chemin de o0 vers i1 pour self.g_g
        self.dist_list3 = [5, 1, 0, 4]

        # Pour les tests de dist_common_parents

        # n1=b et n2=o1 pour self.g_g
        self.dist_cp1 = {0: (1, 2), 1: (0, 2), 3: (2, 3), 4: (2, 3)}

        # n1=a et n2=o0 pour self.g_g
        self.dist_cp2 = {0: (0, 2), 3: (1, 3), 4: (1, 3)}

        # n1=i0 et n2=i1 pour self.g_g
        self.dist_cp3 = {}

        # Declaration du graph du TP 8

        t_i10 = node(10, 'i10', {}, {0: 1})
        t_i11 = node(11, 'i11', {}, {2: 1})

        t_n0 = node(0, '0', {10: 1}, {3: 1})
        t_n1 = node(1, '1', {}, {4: 1, 5: 1, 8: 1})
        t_n2 = node(2, '2', {11: 1}, {4: 1})
        t_n3 = node(3, '3', {0: 1}, {5: 1, 6: 1, 7: 1})
        t_n4 = node(4, '4', {1: 1, 2: 1}, {6: 1})
        t_n5 = node(5, '5', {1: 1, 3: 1}, {7: 1})
        t_n6 = node(6, '6', {3: 1, 4: 1}, {8: 1, 9: 1})
        t_n7 = node(7, '7', {3: 1, 5: 1}, {12: 1})
        t_n8 = node(8, '8', {1: 1, 6: 1}, {})
        t_n9 = node(9, '9', {6: 1}, {})

        t_o12 = node(12, '12', {7: 1}, {})

        t_node_list = [
            t_n0, t_n1, t_n2, t_n3, t_n4, t_n5, t_n6, t_n7, t_n8, t_n9, t_i10,
            t_i11, t_o12
        ]

        self.g_topo = open_digraph([10, 11], [12], t_node_list)

        # Declaration d'un 2eme graph pour les tests du TP8

        self.g_topo2 = self.g_g.copy()
        self.g_topo2.remove_parallel_edges(1, 2)

        # Pour les tests du tri topologique

        self.topo_list1 = [[0, 1, 2], [3, 4], [5, 6], [7, 8, 9]]

        self.topo_list2 = [[0], [1, 2]]

        self.topo_list3 = [[0], [1], [2]]

        # Pour les tests de longest path

        # self.g_topo 0 -> 3
        self.long_path1 = (1, [0, 3])

        # self_g_topo 0 -> 5
        self.long_path2 = (2, [0, 3, 5])

        # self.g_topo 0 -> 7
        self.long_path3 = (3, [0, 3, 5, 7])

        # self.g_topo 1 -> 8
        self.long_path4 = (3, [1, 4, 6, 8])

        # self.g_g avec a -> a
        self.long_path5 = (0, [])

        # self.g_g avec a -> b
        self.long_path6 = (1, [0, 1])

        # self.g_g avec a -> c
        self.long_path7 = (2, [0, 1, 2])

    # Test des methodes

    def test_algo_dijkstra(self):
        dist1, prev1 = self.g_g.Dijkstra(0)

        self.assertEqual(self.dict_dist1, dist1)
        self.assertEqual(self.dict_prev1, prev1)

        dist2, prev2 = self.g_g.Dijkstra(0, direction=-1)

        self.assertEqual(self.dict_dist2, dist2)
        self.assertEqual(self.dict_prev2, prev2)

        dist3, prev3 = self.g_g.Dijkstra(0, direction=1)

        self.assertEqual(self.dict_dist3, dist3)
        self.assertEqual(self.dict_prev3, prev3)

    def test_shortest_path(self):
        path1 = self.g_g.shortest_path(3, 3)
        self.assertEqual(path1, self.dist_list1)

        path2 = self.g_g.shortest_path(5, 6)
        self.assertEqual(path2, self.dist_list2)

        path3 = self.g_g.shortest_path(5, 4)
        self.assertEqual(path3, self.dist_list3)

    def test_dist_common_parents(self):
        dico1 = self.g_g.dist_common_parents(1, 6)
        self.assertEqual(dico1, self.dist_cp1)

        dico2 = self.g_g.dist_common_parents(0, 5)
        self.assertEqual(dico2, self.dist_cp2)

        dico3 = self.g_g.dist_common_parents(3, 4)
        self.assertEqual(dico3, self.dist_cp3)

    def test_topological_sort(self):
        res = open_digraph.empty().topological_sort()
        self.assertEqual(res, [])

        res1 = self.g_topo.topological_sort()
        self.assertEqual(res1, self.topo_list1)

        res2 = self.g_topo2.topological_sort()
        self.assertEqual(res2, self.topo_list2)

        res3 = self.g_g.topological_sort()
        self.assertEqual(res3, self.topo_list3)

        # Le graph est cyclique, topological_sort doit soulever une erreur
        g_oriented = open_digraph.random(12,
                                         15,
                                         1,
                                         2,
                                         form="loop-free-undirected")
        try:
            g_oriented.topological_sort()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_graph_depth(self):
        g_vide = open_digraph.empty()
        self.assertEqual(g_vide.graph_depth(), -1)

        self.assertEqual(self.g_topo.graph_depth(), 3)

        self.assertEqual(self.g_topo2.graph_depth(), 1)

        self.assertEqual(self.g_g.graph_depth(), 2)

    def test_node_depth(self):
        # On ne peut pas trouver la profondeur d'un noeud qui n'existe pas
        g_vide = open_digraph.empty()
        try:
            g_vide.node_depth(0)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

        self.assertEqual(self.g_topo.node_depth(0), 0)

        self.assertEqual(self.g_topo.node_depth(3), 1)

        self.assertEqual(self.g_topo.node_depth(5), 2)

        self.assertEqual(self.g_topo.node_depth(8), 3)

        self.assertEqual(self.g_topo.node_depth(7), 3)

        self.assertEqual(self.g_topo2.node_depth(2), 1)

        self.assertEqual(self.g_g.node_depth(2), 2)

        self.assertEqual(self.g_g.node_depth(0), 0)

        # Le noeud d'id 5 est output, il n'est donc pas pris en compte
        try:
            self.g_g.node_depth(5)
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

    def test_longest_path(self):
        res1 = self.g_topo.longest_path(0, 3)
        self.assertEqual(res1, self.long_path1)

        res2 = self.g_topo.longest_path(0, 5)
        self.assertEqual(res2, self.long_path2)

        res3 = self.g_topo.longest_path(0, 7)
        self.assertEqual(res3, self.long_path3)

        res4 = self.g_topo.longest_path(1, 8)
        self.assertEqual(res4, self.long_path4)

        res5 = self.g_g.longest_path(0, 0)
        self.assertEqual(res5, self.long_path5)

        res6 = self.g_g.longest_path(0, 1)
        self.assertEqual(res6, self.long_path6)

        res7 = self.g_g.longest_path(0, 2)
        self.assertEqual(res7, self.long_path7)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
