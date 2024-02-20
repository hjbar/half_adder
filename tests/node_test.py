import sys
import os

root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)
import unittest
from modules.node import *


class InitTest(unittest.TestCase):

    # Node

    def test_init_node(self):
        n0 = node(0, 'i', {}, {1: 1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1: 1})
        self.assertIsInstance(n0, node)
        self.assertIsNot(n0.copy(), n0)


class NodeTest(unittest.TestCase):

    # Setup

    def setUp(self):
        self.n0 = node(0, 'a', {}, {1: 1})
        self.n1 = node(1, 'b', {1: 1, 2: 2}, {3: 1, 4: 2})

    # Getters

    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)

    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')

    def test_get_parent(self):
        self.assertEqual(self.n0.get_parents_ids(), list({}.keys()))

    def test_get_children(self):
        self.assertEqual(self.n0.get_children_ids(), list({1: 1}.keys()))

    # Setters

    def test_set_id(self):
        self.n0.set_id(10)
        self.assertEqual(self.n0.get_id(), 10)

    def test_set_label(self):
        self.n0.set_label("test")
        self.assertEqual(self.n0.get_label(), "test")

    def test_set_parent(self):
        d = {2: 6, 7: 4}
        self.n0.set_parents_ids(d)
        self.assertEqual(self.n0.get_parents_ids(), list(d.keys()))
        self.assertEqual(list(self.n0.parents.values()), list(d.values()))

    def test_set_children(self):
        d = {6: 2, 4: 7}
        self.n0.set_children_ids(d)
        self.assertEqual(self.n0.get_children_ids(), list(d.keys()))
        self.assertEqual(list(self.n0.children.values()), list(d.values()))

    def test_add_parent(self):
        d = {5: 1}
        self.n0.add_parent_id(5)
        self.assertEqual(self.n0.get_parents_ids(), list(d.keys()))
        self.assertEqual(list(self.n0.parents.values()), list(d.values()))

        d2 = {5: 2}
        self.n0.add_parent_id(5)
        self.assertEqual(self.n0.get_parents_ids(), list(d2.keys()))
        self.assertEqual(list(self.n0.parents.values()), list(d2.values()))

    def test_add_child(self):
        d = {1: 1, 6: 1}
        self.n0.add_child_id(6)
        self.assertEqual(self.n0.get_children_ids(), list(d.keys()))
        self.assertEqual(list(self.n0.children.values()), list(d.values()))

        d2 = {1: 2, 6: 1}
        self.n0.add_child_id(1)
        self.assertEqual(self.n0.get_children_ids(), list(d2.keys()))
        self.assertEqual(list(self.n0.children.values()), list(d2.values()))

    # Removers

    def test_remove_parent_once(self):
        self.n1.remove_parent_once(1)
        self.assertEqual(self.n1, node(1, 'b', {2: 2}, {3: 1, 4: 2}))
        self.n1.remove_parent_once(2)
        self.assertEqual(self.n1, node(1, 'b', {2: 1}, {3: 1, 4: 2}))
        self.n1.remove_parent_once(2)
        self.assertEqual(self.n1, node(1, 'b', {}, {3: 1, 4: 2}))

    def test_remove_parent_id(self):
        self.n1.remove_parent_id(1)
        self.assertEqual(self.n1, node(1, 'b', {2: 2}, {3: 1, 4: 2}))
        self.n1.remove_parent_id(2)
        self.assertEqual(self.n1, node(1, 'b', {}, {3: 1, 4: 2}))

    def test_remove_child_once(self):
        self.n1.remove_child_once(3)
        self.assertEqual(self.n1, node(1, 'b', {1: 1, 2: 2}, {4: 2}))
        self.n1.remove_child_once(4)
        self.assertEqual(self.n1, node(1, 'b', {1: 1, 2: 2}, {4: 1}))
        self.n1.remove_child_once(4)
        self.assertEqual(self.n1, node(1, 'b', {1: 1, 2: 2}, {}))

    def test_remove_child_id(self):
        self.n1.remove_child_id(3)
        self.assertEqual(self.n1, node(1, 'b', {1: 1, 2: 2}, {4: 2}))
        self.n1.remove_child_id(4)
        self.assertEqual(self.n1, node(1, 'b', {1: 1, 2: 2}, {}))

    # Methodes

    def test_node_copy(self):
        n1_copy = self.n1.copy()
        self.assertEqual((n1_copy), (self.n1))

        # On va tester que modifier une copie, ne modifie pas aussi l'original :

        n1_copy.add_parent_id(3)
        self.assertIsNot((n1_copy), (self.n1))

        n1_copy = self.n1.copy()
        n1_copy.add_child_id(3)
        self.assertIsNot((n1_copy), (self.n1))

        n1_copy = self.n1.copy()
        n1_copy.label += " "
        self.assertIsNot((n1_copy), (self.n1))

    def test_indegree(self):
        res1 = self.n0.indegree()
        res2 = self.n1.indegree()

        self.assertEqual(res1, 0)
        self.assertEqual(res2, 3)

    def test_outdegree(self):
        res1 = self.n0.outdegree()
        res2 = self.n1.outdegree()

        self.assertEqual(res1, 1)
        self.assertEqual(res2, 3)

    def test_degree(self):
        res1 = self.n0.degree()
        res2 = self.n1.degree()

        self.assertEqual(res1, 1)
        self.assertEqual(res2, 6)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
