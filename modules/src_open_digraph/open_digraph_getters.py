class open_digraph_getters():

    # Getters

    def get_input_ids(self):
        """ Renvoie les identifiants des nodes d'entrée du graphe """
        return self.inputs

    def get_output_ids(self):
        """ Renvoie les identifiants des nodes de sortie du graphe """
        return self.outputs

    def get_id_node_map(self):
        """ Renvoie un dictionnaire id:node """
        return self.nodes

    def get_nodes(self):
        """ Renvoie une liste de tous les noeuds """
        return list(self.nodes.values())

    def get_nodes_ids(self):
        """ Renvoie une liste de tous les identifiants des noeuds """
        return list(self.nodes.keys())

    def get_node_by_ids(self, ids):
        """
        Renvoie une liste des nodes à partir d'une liste d'indentifiant
        ids : int list
        """
        return [self.__getitem__(i) for i in ids]
