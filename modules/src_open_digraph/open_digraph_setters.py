from modules.node import *
import numpy as np


class open_digraph_setters():

    # Setters

    def set_input_ids(self, inputs):
        """
        Met a jour la valeur de inputs
        inputs: int list
        """
        self.inputs = inputs

    def set_output_ids(self, outputs):
        """
        Met a jour la valeur de outputs
        outputs: int list
        """
        self.outputs = outputs

    def add_input_id(self, n):
        """
        Ajoute une valeur a inputs
        n: int
        """
        self.inputs.append(n)

    def add_output_id(self, n):
        """
        Ajoute une valeur a outputs
        n: int
        """
        self.outputs.append(n)

    def add_edge(self, src, tgt):
        """
        Rajoute une arete du noeud d’id tgt au noeud d’id src
        src: int -> identifiant du noeud dont l'arête est sortante
        tgt: int -> identifiant du noeud dont l'arête est entrante
        """
        if tgt in self.get_output_ids():
            raise ValueError(
                "Le noeud target passé en argument est un noeud Sortant")

        elif tgt in self.get_input_ids():
            raise ValueError(
                "Le noeud target passé en argument est un noeud Entrant")

        elif src in self.get_output_ids():
            raise ValueError(
                "Le noeud Source passé en argument est un noeud Sortant")
        elif src in self.get_input_ids():
            raise ValueError(
                "Le noeud Source passé en argument est un noeud Entrant")

        else:
            self[tgt].add_parent_id(src)
            self[src].add_child_id(tgt)

    def add_edges(self, edges):
        """
        Rajoute des aretes entre les noeuds des paires de la liste passee en argument
        edges: (int, int) list avec (int, int) tuples tel que (src node, tgt node)
        """
        for tgt, src in edges:
            self.add_edge(tgt, src)

    def add_node(self, label='', parents=None, children=None):
        """
        Rajoute un noeud au graphe
        label: string
        parents: int->int dict les noeuds parents du noeud
        children: int->int dict les noeuds fils du noeud
        """
        if parents == None:
            parents = {}

        if children == None:
            children = {}

        id_node = self.new_id()
        new_node = node(id_node, label, parents, children)

        self.nodes[id_node] = new_node

        # On vérifie que le graph soit bien valide, on souleve une erreur sinon
        for parent_id in parents:
            if parent_id in self.get_output_ids():
                raise ValueError(
                    f"L'un des parents d'indentifiant {parent_id} est un noeud sortant"
                )

            elif parent_id in self.get_input_ids():
                raise ValueError(
                    f"L'un des parents d'indentifiant {parent_id} est un noeud entrant"
                )

            else:
                children_node = self[parent_id].children
                children_node[id_node] = parents[parent_id]

        for child_id in children:
            if child_id in self.get_output_ids():
                raise ValueError(
                    f"L'un des enfants d'indentifiant {child_id} est un noeud sortant"
                )

            elif child_id in self.get_input_ids():
                raise ValueError(
                    f"L'un des enfants d'indentifiant {child_id} est un noeud entrant"
                )

            else:
                parents_node = self[child_id].parents
                parents_node[id_node] = children[child_id]

        return id_node

    def add_input_node(self, iden):
        """
        Ajoute un noeud en input qui pointe vers le noeud d'id iden
        iden : int
        """
        if iden in self.get_output_ids():
            raise ValueError("le noeud passé en argument est un noeud Sortant")

        elif iden in self.get_input_ids():
            raise ValueError("le noeud passé en argument est un noeud Entrant")

        else:
            id_node = self.add_node(parents={}, children={iden: 1})
            self.add_input_id(id_node)

    def add_output_node(self, iden):
        """
        Ajoute un noeud en output qui est pointe par le noeud d'id iden
        iden : int
        """
        if iden in self.get_output_ids():
            raise ValueError("le noeud passé en argument est un noeud Sortant")

        elif iden in self.get_input_ids():
            raise ValueError("le noeud passé en argument est un noeud Entrant")

        else:
            id_node = self.add_node(parents={iden: 1}, children={})
            self.add_output_id(id_node)

    def add_random_input(self):
        """
        Ajoute une entrée qui pointe sur un noeud aléatoire qui n'est ni une entree ni une sortie
        """
        list_input = self.get_input_ids()
        list_output = self.get_output_ids()

        nodes = self.get_nodes()
        iden = nodes[np.random.randint(0, len(nodes))].get_id()
        if iden not in list_input and iden not in list_output:
            self.add_input_node(iden)

    def add_random_output(self):
        """
        Ajoute une sortie qui est pointé par un noeud aléatoire qui n'est ni une entree ni une sortie
        """
        list_input = self.get_input_ids()
        list_output = self.get_output_ids()

        nodes = self.get_nodes()
        iden = nodes[np.random.randint(0, len(nodes))].get_id()
        if iden not in list_input and iden not in list_output:
            self.add_output_node(iden)
