class open_digraph_fusion:

    # Methode concernant la fusion

    def node_fusion(self, id_n1, id_n2, new_label=""):
        """
        Methode qui fusionne les deux noeuds dans le graphe dont l'on a donne les identifiant les noeuds ne sont pas directement lie.
        id_n1 : int -> identifiant du premier noeud
        id_n2 : int -> identifiant du second noeud
        new_label : string -> label du nouveau noeud cree par la fusion, par defaut ""
        Pas de valeur de retour
        """
        n1 = self[id_n1]
        n2 = self[id_n2]

        n1_parents = n1.parents.copy()
        n2_parents = n2.parents.copy()

        n1_children = n1.children.copy()
        n2_children = n2.children.copy()

        if id_n1 in n2_parents or id_n1 in n2_children:
            raise ValueError(f"Les noeuds d'id {id_n1} et {id_n2} sont liés")

        n1_parents.update(n2_parents)
        n1_children.update(n2_children)

        del self[id_n1]
        del self[id_n2]

        return self.add_node(new_label, n1_parents, n1_children)
