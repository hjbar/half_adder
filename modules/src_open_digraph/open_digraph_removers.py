import numpy as np


class open_digraph_removers():

    # Removers

    def remove_edge(self, src, tgt):
        """
        Retire une arête entre le noeud src et tgt
        src : int
        tgt : int
        """
        self[src].remove_child_once(tgt)
        self[tgt].remove_parent_once(src)

        new_inputs = [
            input_id for input_id in self.get_input_ids()
            if input_id != src or self[src].children != {}
        ]
        self.set_input_ids(new_inputs)

        new_outputs = [
            output_id for output_id in self.get_output_ids()
            if output_id != tgt or self[tgt].parents != {}
        ]
        self.set_output_ids(new_outputs)

    def remove_edges(self, l):
        """
        Retire une arrete entre les noeuds et les tgt donnés par une liste
        l : (int, int) list
        """
        for src, tgt in l:
            self.remove_edge(src, tgt)

    def remove_parallel_edges(self, src, tgt):
        """
        Retire toutes les arêtes entre le noeud src et tgt
        src : int
        tgt : int
        """
        self[src].remove_child_id(tgt)
        self[tgt].remove_parent_id(src)

        new_inputs = [
            input_id for input_id in self.get_input_ids() if input_id != src
        ]
        self.set_input_ids(new_inputs)

        new_outputs = [
            output_id for output_id in self.get_output_ids()
            if output_id != tgt
        ]
        self.set_output_ids(new_outputs)

    def remove_several_parallel_edges(self, l):
        """
        Retire toutes les arrêtes entre les noeuds et les tgt donnés par une liste
        l : (int, int) list
        """
        for src, tgt in l:
            self.remove_parallel_edges(src, tgt)

    # A discuter
    def fuse_random_inputs(self):
        """
        Fusionne deux entrés aléatoires. Il doit y avoir au moins deux entrés.
        """
        list_input = self.get_input_ids()
        nb_input = len(list_input)

        ni_1 = list_input[np.random.randint(0, nb_input)]
        self.get_input_ids().remove(ni_1)

        nb_input = len(list_input)

        ni_2 = list_input[np.random.randint(0, nb_input)]
        self.get_input_ids().remove(ni_2)

        children_input = {ni_1: 1, ni_2: 1}
        new_node = self.add_node(children=children_input)
        self.add_input_node(new_node)

    def fuse_random_outputs(self):
        """
        Fusionne deux sorties aléatoires. Il doit y a voir au moins deux sorties pour l'executer
        """
        list_output = self.get_output_ids()
        nb_output = len(list_output)

        no_1 = list_output[np.random.randint(0, nb_output)]
        self.get_output_ids().remove(no_1)

        nb_output = len(list_output)

        no_2 = list_output[np.random.randint(0, nb_output)]
        self.get_output_ids().remove(no_2)

        parent_output = {no_1: 1, no_2: 1}
        new_node = self.add_node(parents=parent_output)
        self.add_output_node(new_node)
