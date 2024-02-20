from modules.node import *


class open_digraph_compositions():

    # Methodes concernant la/les composition(s)

    @classmethod
    def identity(cls, n):
        """
        Creer un open_digraph qui represente l'identite sur n fils
        n: int
        """
        inputs = list(range(0, 2 * n, 2))
        outputs = list(range(1, 2 * n, 2))
        dic = []

        for i in range(0, 2 * n, 2):
            dic.append(node(i, "", {}, {i + 1: 1}))
            dic.append(node(i + 1, "", {i: 1}, {}))

        return cls(inputs, outputs, dic)

    def iparallel(self, g):
        """
        Compose parallelement self par g sans modifier g
        g: open_digraph
        """
        if len(g.get_nodes_ids()) == 0:
            return

        if len(self.get_nodes_ids()) != 0:
            minInd = self.min_id()
            maxInd = g.max_id()
            self.shift_indices(maxInd - minInd + 1)

        for iden, node in g.get_id_node_map().items():
            self.nodes[iden] = node.copy()

        self.inputs += g.get_input_ids()
        self.outputs += g.get_output_ids()

    def parallel(self, g):
        """
        Renvoie la composition parallele de self par g sans modifier ni self, ni g
        g: open_digraph
        """
        f = self.copy()
        f.iparallel(g)
        return f

    def icompose(self, f):
        """
        Compose sequentiellement self par f sans modifier f
        Renvoie une erreur si nombre d'entree de self != nombre de sortie de f
        f: open_digraph
        """
        len_input_ids_list = len(self.get_input_ids())

        if len_input_ids_list != len(f.get_output_ids()):
            raise ValueError(
                "le nombre d'entre de self ne coincide pas avec le nombre de sortie de f"
            )

        f_copy = f.copy()

        if len(f.get_nodes_ids()) == 0:
            return

        if len(self.get_nodes_ids()) != 0:
            maxInd = self.max_id()
            minInd = f_copy.min_id()
            f_copy.shift_indices(maxInd - minInd + 1)

        for i in range(len_input_ids_list):
            # indice des noeuds d'entré de f et de sortie de self
            f_out = f_copy.get_output_ids()[0]
            self_in = self.get_input_ids()[0]
            # indice du père du noeud d'id f_out et indice du fils du noeud d'id self_in
            parent = f_copy[f_out].get_parents_ids()[0]
            child = self[self_in].get_children_ids()[0]
            # On ajoute 'parent' au parents de 'child'
            self[child].add_parent_id(parent)
            # On ajoute 'child'  au children de 'parent'
            f_copy[parent].add_child_id(child)
            # On retire les entrees de self et les sorties de f
            del self[self_in]
            del f_copy[f_out]

        for iden, node in f_copy.get_id_node_map().items():
            self.nodes[iden] = node

        self.set_input_ids(f_copy.get_input_ids())

    def compose(self, f):
        """
        Renvoie la composition sequentielle de self par f sans modifier ni self, ni f
        Renvoie une erreur si nombre d'entree de self != nombre de sortie de f
        f: open_digraph
        """
        g = self.copy()
        g.icompose(f)
        return g

    def connected_components(self):
        """ Renvoie le nombre de composantes connexes, et un dictionnaire qui associe chaque id de noeuds du graphe a un int qui correspond a une composante connexe """

        def add_group(node, dic, stack, cpt):
            """ Sous-fonction de connected_components """
            iden = node.get_id()
            dic[iden] = cpt

            for id_parent in node.get_parents_ids():
                if id_parent not in dic:
                    stack.append(id_parent)

            for id_children in node.get_children_ids():
                if id_children not in dic:
                    stack.append(id_children)

            return

        cpt = 0  # nombre de composant connexe du graphe
        dic = {}  # node.id : id du composant connexe
        node_dic = self.get_id_node_map()

        for iden in node_dic:
            if iden not in dic:
                stack = [iden]

                while (len(stack) > 0):
                    cur = stack.pop()  #???
                    if cur not in dic:
                        add_group(self[cur], dic, stack, cpt)
                cpt += 1

        return cpt, dic

    def connected_components_list(self):
        """ Renvoie une liste d’open_digraphs, chacun correspondant a une composante connexe du graphe de depart """
        #Est-ce que l'on conserve les informations sur les noeuds???

        length, nodes = self.connected_components()
        t = [([], [], []) for i in range(length)]

        input_ids = self.get_input_ids()
        output_ids = self.get_output_ids()

        for iden in nodes:
            # On ajoute le noeud dans le tableau contenant tous les noeuds
            t[nodes[iden]][2].append(self[iden])

            if iden in input_ids:
                # On ajoute l'identifiant du noeud dans le tableau des entrées
                t[nodes[iden]][0].append(iden)

            elif iden in output_ids:
                # On ajoute l'identifiant du noeud dans le tableau des sorties
                t[nodes[iden]][1].append(iden)

        for i in range(length):
            t[i] = self.__class__(t[i][0], t[i][1], t[i][2])

        return t
