class open_digraph_base():

    # Methodes de base

    @classmethod
    def empty(cls):
        """ Defini un graphe vide """
        return cls([], [], [])

    def copy(self):
        """ Renvoie une copie d'un graph """
        nodes = []
        for node in self.get_nodes():
            nodes.append(node.copy())

        input_ids = self.get_input_ids()
        output_ids = self.get_output_ids()
        return self.__class__(input_ids.copy(), output_ids.copy(), nodes)

    def is_well_formed(self):
        """
        Souleve une erreur si le graph n'est pas correct
        Le assert est effectue dans cette fonction afin d'avoir une erreur plus precise
        """
        input_list = self.get_input_ids()

        for iden in input_list:
            node = self[iden]
            if len(node.get_parents_ids()) != 0:
                raise ValueError("Un input possede un pere.")
            if len(node.get_children_ids()) != 1:
                return ValueError("Un input ne possede pas qu'un fils.")

        output_list = self.get_output_ids()

        for iden in output_list:
            node = self[iden]
            if len(node.get_parents_ids()) != 1:
                raise ValueError("Un output possede pas qu'un pere.")
            if len(node.get_children_ids()) != 0:
                raise ValueError("Un output possde un fils.")

        input_output_list = input_list + output_list
        node_id_list = self.get_nodes_ids()

        for iden in input_output_list:
            if iden not in node_id_list:
                raise ValueError(
                    "Un output ou un input du graph n'est pas dans la liste de noeuds."
                )

        node_val_list = self.get_nodes()

        for i in range(len(node_id_list)):
            if node_id_list[i] != node_val_list[i].get_id():
                raise ValueError(
                    "Un id ne pointe pas sur le bon noeud dans nodes")

        for iden in node_id_list:
            node = self[iden]

            for next_id_node in node.get_children_ids():
                next_node = self[next_id_node]
                if next_id_node not in node.children or iden not in next_node.parents or node.children[
                        next_id_node] != next_node.parents[iden]:
                    raise ValueError(
                        "La multicite entre 2 noeuds n'est pas bonne.")

            for prev_id_node in node.get_parents_ids():
                prev_node = self[prev_id_node]
                if prev_id_node not in node.parents or iden not in prev_node.children or node.parents[
                        prev_id_node] != prev_node.children[iden]:
                    raise ValueError(
                        "La multicite entre 2 noeuds n'est pas bonne.")
