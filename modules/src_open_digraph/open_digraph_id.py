class open_digraph_id():

    # Methodes concernant les ids

    def new_id(self):
        """ Renvoie un nouvel id disponible """
        id_list = sorted(self.nodes.keys())

        for i in range(len(id_list)):
            if i != id_list[i]:
                return i

        return len(id_list)

    def graph_to_dict_id(self):
        """ Renvoie un dictionnaire qui associe a chaque id de noeud un unique entier 0 <= i < n """
        dict_res = {}
        node_list = self.get_nodes()

        for i in range(len(node_list)):
            dict_res[i] = node_list[i].copy()

        return dict_res

    def min_id(self):
        """ Renvoie le minimum des id du graph """
        id_list = self.get_nodes_ids()
        return min(id_list)

    def max_id(self):
        """ Renvoie le maximum des id du graph """
        id_list = self.get_nodes_ids()
        return max(id_list)

    def shift_indices(self, n):
        """
        Incremente de n tous ids du graph
        n : int -> positif, nul ou negatif
        """
        inputs = self.get_input_ids()
        outputs = self.get_output_ids()

        new_inputs = []
        new_outputs = []
        new_nodes = []

        for iden, node in self.get_id_node_map().items():
            new_id = iden + n

            node.set_id(new_id)

            children_dict = {}

            for fils_id, arretes in node.children.items():
                children_dict[fils_id + n] = arretes

            node.children = children_dict

            parents_dict = {}

            for pere_id, arretes in node.parents.items():
                parents_dict[pere_id + n] = arretes

            node.parents = parents_dict

            # ???

            new_nodes.append(node)

        # On ne veut pas modifier l'ordre des inputs et des outputs
        for i in range(len(inputs)):
            new_inputs.append(inputs[i] + n)
        for i in range(len(outputs)):
            new_outputs.append(outputs[i] + n)

        self.set_input_ids(new_inputs)
        self.set_output_ids(new_outputs)
        self.nodes = {node.id: node for node in new_nodes}
