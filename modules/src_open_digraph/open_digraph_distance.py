class open_digraph_distance():

    # Methodes concernant les distances

    def Dijkstra(self, src, direction=None, tgt=None):
        """
        Renvoie le dictionnaire des distances du graph et la liste des precedents en partant d'un noeud source grace l'algorithme de Dijkstra
        src: int -> id node
        direction: -1, 1 ou None -> -1 traite seulement les parents, 1 seulement les enfants, None tout
        tgt: int -> id node ou None -> si défini s'arrete des qu'on a la distance minimal entre la source et la target
        """

        f = lambda elem: dist[elem]

        Q = [src]
        dist = {src: 0}
        prev = {}

        while (len(Q) > 0):

            u = min(Q, key=f)
            Q.remove(u)

            if (direction == 1):
                neighbours = self[u].get_children_ids()
            elif (direction == -1):
                neighbours = self[u].get_parents_ids()
            else:
                neighbours = self[u].get_parents_ids(
                ) + self[u].get_children_ids()

            for v in neighbours:
                n_in_dist = v not in dist

                if n_in_dist:
                    Q.append(v)
                if n_in_dist or dist[v] > dist[u] + 1:
                    dist[v] = dist[u] + 1
                    prev[v] = u

            if tgt is not None and u == tgt:
                return dist, prev

        return dist, prev

    def shortest_path(self, src, tgt):
        """
        Renvoie la liste du plus court chemin entre un noeud source et un noeud cible
        src: int -> id node
        tgt: int -> id node
        """
        if (src == tgt):
            return []

        dist, prev = self.Dijkstra(src, direction=None, tgt=tgt)

        path = [None for i in range(dist[tgt] + 1)]
        path[len(path) - 1] = tgt
        cur = tgt

        i = len(path) - 2
        while i >= 0:
            cur = prev[cur]
            path[i] = cur
            i -= 1

        return path

    def dist_common_parents(self, id1, id2):
        """
        Renvoie un dict id: tuple des distances des parents communs au noeud n1 et au noeud n2
        id1: int -> id node
        id2: int -> id node
        """
        dist_n1 = self.Dijkstra(id1, direction=-1)[0]
        dist_n2 = self.Dijkstra(id2, direction=-1)[0]

        dict_res = {}

        for iden, val in dist_n1.items():
            if iden in dist_n2:
                dict_res[iden] = (val, dist_n2[iden])

        return dict_res

    def topological_sort(self):
        """ Renvoie le resultat du tri topologique sous forme d'une liste de liste d'id """
        g = self.copy()

        del g[g.get_input_ids()]
        del g[g.get_output_ids()]

        node_list = g.get_nodes()
        res = []

        while len(node_list) != 0:
            parents_list = []

            for node in node_list:
                if node.get_parents_ids() == []:
                    parents_list.append(node.get_id())

            if parents_list == []:
                raise ValueError("Le graph est cyclique!")

            res.append(parents_list)

            del g[parents_list]
            node_list = g.get_nodes()

        return res

    def graph_depth(self):
        """ Renvoie la profondeur du graph """
        return len(self.topological_sort()) - 1

    def node_depth(self, iden):
        """
        Renvoie la profondeur du noeud dont l'identifiant est passe en argument
        iden: int
        """
        topo_sort_list = self.topological_sort()

        for prof, id_list in enumerate(topo_sort_list):
            if iden in id_list:
                return prof

        raise ValueError(
            "L'id donne est argument n'est pas associe a un noeud du graph")

    def longest_path(self, src, tgt):
        """
        Renvoie un tuple contenant la longeur du plus long chemin entre la source et la cible avec le chemin sous forme de list d'id
        src: int -> id node
        tgt: int -> id node
        """

        def path():
            """
            Sous-fonction de longest_path
            Renvoie le chemin le plus long entre la source et la cible sous forme de list d'id
            """
            if src == tgt:
                return []

            path = [None for i in range(dist[tgt] + 1)]
            path[len(path) - 1] = tgt
            cur = tgt

            i = len(path) - 2
            while i >= 0:
                cur = prev[cur]
                path[i] = cur
                i -= 1

            return path

        topo_sort_list = self.topological_sort()

        dist = {src: 0}
        prev = {}

        prof_src = self.node_depth(src)
        prof_max_search = len(topo_sort_list)

        for i in range(prof_src, prof_max_search):
            for iden in topo_sort_list[i]:
                for parent_id in self[iden].get_parents_ids():

                    if parent_id in dist:
                        if (iden not in dist) or (dist[parent_id] + 1 >
                                                  dist[iden]):
                            dist[iden] = dist[parent_id] + 1
                            prev[iden] = parent_id

                if iden == tgt:
                    return dist[tgt], path()

        raise ValueError(
            f"Distance impossible a evaluer entre le noeud d'id:{src} et noeud d'id:{tgt}"
        )
