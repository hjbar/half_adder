from modules.open_digraph import *
from modules.matrice import *
from modules.node import *

import numpy as np


class bool_circ(open_digraph):

    def __init__(self, g):
        """
        Constructeur de la Sous-classe d'open_digraph representant un circuit booleen
        g : une instance d'open_digraph
        """
        bool_g = g.copy()

        super().__init__(bool_g.get_input_ids(), bool_g.get_output_ids(),
                         bool_g.get_nodes())

        self.is_well_formed()

    # Methodes de classe

    @classmethod
    def parse_parentheses(cls, *args):
        """
        Renvoie un circuit booleen cree a partir d'une chaine de caractere
        s: str -> decrit un circuit booleen
        """
        g = open_digraph.empty()
        var_dic = {}

        for s in args:

            current_node = g.add_node()
            g.add_output_node(current_node)

            s2 = ''

            for char in s:

                if char == '(':

                    noeud = g[current_node]
                    noeud.set_label(s2)
                    current_node = g.add_node(children={current_node: 1})
                    s2 = ''

                elif char == ')':

                    noeud = g[current_node]
                    iden = noeud.get_id()

                    if s2 != '':
                        if s2 not in var_dic:
                            var_dic[s2] = [iden]
                        else:
                            var_dic[s2].append(iden)

                    current_node = noeud.get_children_ids()[0]
                    s2 = ''

                else:

                    s2 += char

        var_list = []

        for name, id_list in var_dic.items():

            var_list.append(name)
            length = len(id_list)

            if length > 1:
                for i in range(1, length):
                    new_id = g.node_fusion(id_list[0], id_list[i])
                    id_list[0] = new_id

        return cls(g), var_list

    @classmethod
    def random_bool_circ(cls, n, inputs, outputs):
        """
        Genere un circuit boolean aleatoire correcte
        n : int -> nombre de noeud minimal
        inputs : int -> nombre d'inputs > 1
        outputs : int -> nombre d'outputs > 1
        """

        # Etape 0

        if inputs < 1 or outputs < 1:
            raise ValueError("Il y a au moins un input et un output")

        # Etape 1

        g = open_digraph.random(n, 1, form="DAG")

        node_list = g.get_nodes()

        # Etape 2

        for node in node_list:
            iden = node.get_id()

            if node.indegree() == 0:
                g.add_input_node(iden)

            if node.outdegree() == 0:
                g.add_output_node(iden)

        # Etape 2bis

        list_input = g.get_input_ids()
        nb_input = len(list_input)
        # s'il y a trop d'inputs on fusionne les inputs
        while nb_input > inputs:

            g.fuse_random_inputs()
            nb_input = len(list_input)

        list_output = g.get_output_ids()
        nb_output = len(list_output)
        # s'il y a trop d'outputs on fusionne les outputs
        while nb_output > outputs:
            g.fuse_random_outputs()
            nb_output = len(list_output)

        list_input = g.get_input_ids()
        list_output = g.get_output_ids()
        nb_input = len(list_input)
        # s'il n'y a pas assez d'input, on en ajoute de maniere aleatoire
        while nb_input < inputs:
            g.add_random_input()
            nb_input = len(list_input)

        list_output = g.get_output_ids()
        nb_output = len(list_output)
        # s'il n'y a pas assez d'output, on en ajoute de maniere aleatoire
        while nb_output < outputs:
            g.add_random_output()
            nb_output = len(list_output)

        # On memorise les outputs pour ne pas modifier la liste des outputs avec la methode remove_parallel_edges
        list_output = g.get_output_ids()

        # Etape 3

        new_node_list = g.get_nodes()

        for node in new_node_list:
            # noeud de degree entrant 1 et de degree sortant 1 alors c'est une porte logique 'neg'
            if node.indegree() == node.outdegree() == 1:
                symbol = "~"
                node.set_label(symbol)
            # noeud de degree entrant superieur a 1 alors c'est une porte logique 'and' ou 'or' ou 'xor'
            elif node.indegree() > 1 and node.outdegree() == 1:
                symbol = ["&", "|", "^"][np.random.randint(0, 3)]
                node.set_label(symbol)
            # noeud de degree entrant superieur a 1, degree superieur a 1, alors on transforme le noeud en une porte logique binaire dont le fils represente une copie
            elif node.indegree() > 1 and node.outdegree() > 1:
                old_iden = node.get_id()
                tmp_children = node.children.copy()

                # On retire les aretes entre le noeud courant et ses fils
                for iden in tmp_children.keys():
                    g.remove_parallel_edges(old_iden, iden)

                # On cree un noeud copie qui pointe vers les anciens fils du noeud courant et qui est pointee par le noeud courant
                new_iden = g.add_node(label="",
                                      parents={old_iden: 1},
                                      children=tmp_children)

                symbol = ["&", "|", "^"][np.random.randint(0, 2)]

                node.set_children_ids({new_iden: 1})
                node.set_label(symbol)
            # sinon ( un noeud entrant, plus d'un noeud sortant ) alors c'est un noeud representant une copie
            else:
                node.set_label("")

        # On affecte la liste des outputs avant l'etape 3 a la liste des outputs du graphe
        g.set_output_ids(list_output)

        # Return

        return cls(g)

    @classmethod
    def Adder(cls, n):
        """
        Creer le graph correspond a l'addition de taille n
        n : int
        """

        # Creation de Adder0
        if n == 0:
            # Inputs
            i0 = node(9, "", {}, {0: 1})
            i1 = node(10, "", {}, {1: 1})
            i2 = node(11, "", {}, {4: 1})
            # Noeud copie
            c0 = node(0, "", {9: 1}, {2: 1, 5: 1})
            c1 = node(1, "", {10: 1}, {2: 1, 5: 1})
            c3 = node(3, "", {2: 1}, {6: 1, 7: 1})
            c4 = node(4, "", {11: 1}, {6: 1, 7: 1})
            # porte logique binaire
            n2 = node(2, "^", {0: 1, 1: 1}, {3: 1})
            n5 = node(5, "&", {0: 1, 1: 1}, {8: 1})
            n6 = node(6, "&", {3: 1, 4: 1}, {8: 1})
            n7 = node(7, "^", {3: 1, 4: 1}, {13: 1})
            n8 = node(8, "|", {5: 1, 6: 1}, {12: 1})
            # Outputs
            o0 = node(12, "", {8: 1}, {})
            o1 = node(13, "", {7: 1}, {})

            node_list = [
                c0, c1, n2, c3, c4, n5, n6, n7, n8, i0, i1, i2, o0, o1
            ]

            g = open_digraph([9, 10, 11], [12, 13], node_list)
            return cls(g)

        else:
            # On cree les deux Adder de rang (n-1)
            g0 = cls.Adder(n - 1)
            # Le second est une copie du premier ( ainsi on appel n fois Adder )
            g1 = g0.copy()
            # le nombre d'input et d'output des Adder de rang(n-1)
            nb_input = len(g0.get_input_ids())  # 2 ** n
            nb_output = len(g0.get_output_ids())  # 2 ** (n-1)
            # On fait la composition parallele des Adder
            g0.iparallel(g1)
            # On obtient l' id de la sortie de l'adder (n-1) qui donne la carry
            carry_output = g0.get_output_ids()[nb_output]
            # On obtient l'id de l'input qui prend en entree la carry
            carry_input = g0.get_input_ids()[nb_input - 1]
            # On ajoute une arete entre le parent de la sortie et le fils de l'input
            g0.add_edge(g0[carry_output].get_parents_ids()[0],
                        g0[carry_input].get_children_ids()[0])
            # puis on supprime la sortie
            del g0[carry_output]
            # on supprimer l'entree
            del g0[carry_input]
            # On rearrange les inputs dans le tableau des inputs de telle sorte que les bits de meme rang soit en entree du meme additionneur
            g_inputs = g0.get_input_ids()

            sep = 2**(n - 1)
            k = sep
            limit = 2 * sep
            while k < limit:

                tmp = g_inputs[k]
                g_inputs[k] = g_inputs[sep + k]
                g_inputs[sep + k] = tmp
                k += 1

            return g0

    @classmethod
    def Half_Adder(cls, n):
        """
        Creer le graph correspond a la demi-addition de taille n
        n : int
        """
        g = cls.Adder(n)
        # On modifie simplement le label du derniere input et on le supprime de la liste des inputs
        inputs = g.get_input_ids()
        g[inputs.pop()].set_label("0")
        return g

    @classmethod
    def registre(cls, n, size=8):
        """
        Construit un circuit booleen representant le registre instancie en l'entier n
        n : int -> L'entier instancie
        size : int -> Le nombre de bit que l'on utilise pour ecrire l'entier. Valeur par defaut 8
        """

        if 2**size <= n:
            raise ValueError(
                f"Le registre n'est pas assez grand pour stocker l'entier {n}")

        reg = open_digraph.empty()
        code = bin(n)[2:]
        len_code = len(code)
        i = size - 1

        while i >= 0:
            lbl = '0' if i >= len_code else code[len_code - i - 1]

            id_node = reg.add_node(label=lbl, parents={}, children={})
            reg.add_output_node(id_node)

            i -= 1

        return cls(reg)

    @classmethod
    def enc(cls):
        """ Construit le circuit boolean de l'encodeur du code de Hamming avec 7 bits """

        comp0 = "(x0)^(x1)^(x3)"
        comp1 = "(x0)^(x2)^(x3)"
        comp2 = "(x1)^(x2)^(x3)"

        g = cls.parse_parentheses(comp0, comp1, comp2)[0]

        del g[g.get_output_ids()]

        g.add_input_node(3)
        g.add_input_node(2)
        g.add_input_node(7)
        g.add_input_node(4)

        g.add_output_node(0)
        g.add_output_node(10)
        g.add_output_node(3)
        g.add_output_node(5)
        g.add_output_node(2)
        g.add_output_node(7)
        g.add_output_node(4)

        return g

    @classmethod
    def dec(cls):
        """ Construit le circuit boolean du decodeur de code de Hamming avec 7 bits """

        # inputs
        i0 = node(0, '', {}, {7: 1})
        i1 = node(1, '', {}, {8: 1})
        i2 = node(2, '', {}, {9: 1})
        i3 = node(3, '', {}, {10: 1})
        i4 = node(4, '', {}, {11: 1})
        i5 = node(5, '', {}, {12: 1})
        i6 = node(6, '', {}, {13: 1})
        g_inputs = [0, 1, 2, 3, 4, 5, 6]

        # fils non connectes a des outputs des inputs
        n0 = node(7, '^', {0: 1, 9: 1, 11: 1, 13: 1}, {14: 1})
        n1 = node(8, '^', {1: 1, 9: 1, 12: 1, 13: 1}, {15: 1})
        n2 = node(9, '', {2: 1}, {7: 1, 8: 1, 24: 1})
        n3 = node(10, '^', {3: 1, 11: 1, 12: 1, 13: 1}, {16: 1})
        n4 = node(11, '', {4: 1}, {7: 1, 10: 1, 25: 1})
        n5 = node(12, '', {5: 1}, {8: 1, 10: 1, 26: 1})
        n6 = node(13, '', {6: 1}, {7: 1, 8: 1, 10: 1, 27: 1})

        # fils des trois premiers xor
        n7 = node(14, '', {7: 1}, {19: 1, 20: 1, 21: 1, 23: 1})
        n8 = node(15, '', {8: 1}, {18: 1, 20: 1, 22: 1, 23: 1})
        n9 = node(16, '', {10: 1}, {17: 1, 21: 1, 22: 1, 23: 1})

        # premiere porte neg
        n10 = node(17, '~', {16: 1}, {20: 1})
        n11 = node(18, '~', {15: 1}, {21: 1})
        n12 = node(19, '~', {14: 1}, {22: 1})

        # porte &
        n13 = node(20, '&', {14: 1, 15: 1, 17: 1}, {24: 1})
        n14 = node(21, '&', {14: 1, 16: 1, 18: 1}, {25: 1})
        n15 = node(22, '&', {15: 1, 16: 1, 19: 1}, {26: 1})
        n16 = node(23, '&', {14: 1, 15: 1, 16: 1}, {27: 1})

        # derniere porte xor
        n17 = node(24, '^', {9: 1, 20: 1}, {28: 1})
        n18 = node(25, '^', {11: 1, 21: 1}, {29: 1})
        n19 = node(26, '^', {12: 1, 22: 1}, {30: 1})
        n20 = node(27, '^', {13: 1, 23: 1}, {31: 1})

        # outputs
        o0 = node(28, '', {24: 1}, {})
        o1 = node(29, '', {25: 1}, {})
        o2 = node(30, '', {26: 1}, {})
        o3 = node(31, '', {27: 1}, {})
        g_outputs = [28, 29, 30, 31]

        node_list = [
            i0, i1, i2, i3, i4, i5, i6, n0, n1, n2, n3, n4, n5, n6, n7, n8, n9,
            n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, o0, o1, o2,
            o3
        ]
        g = open_digraph(g_inputs, g_outputs, node_list)

        return cls(g)

    def copy_gate(self, id1, id2):
        """
        Applique la transformation de la porte 'copie'
        id1 : int -> id d'une porte ""
        id2 : int -> id d'une constante 0 ou 1
        """

        n1 = self[id1]
        n2 = self[id2]

        if n1.get_label() != "":
            raise ValueError("Le noeud d'id1 n'est pas une copie ("
                             ")")

        n2_label = n2.get_label()

        if n2_label != "0" and n2_label != "1":
            raise ValueError("Le noeud d'id2 n'est pas une constante (0 ou 1)")

        g_input = self.get_input_ids()
        g_output = self.get_output_ids()

        for iden in n2.get_parents_ids():
            del self[iden]

        n1_children = n1.children.copy()
        del self[id1]
        del self[id2]

        for iden in n1_children:

            self.add_node(label=n2_label,
                          parents={},
                          children={iden: n1_children[iden]})

        self.set_input_ids(g_input)
        self.set_output_ids(g_output)

    def neg_gate(self, id1, id2):
        """
        Applique la transformation de la porte 'non'
        id1 : int -> id d'une porte ~
        id2 : int -> id d'une constante 0 ou 1
        """
        n1 = self[id1]
        n2 = self[id2]

        if n1.get_label() != "~":
            raise ValueError("Le noeud d'id1 n'est pas un non (~)")

        n2_label = n2.get_label()

        if n2_label != "0" and n2_label != "1":
            raise ValueError("Le noeud d'id2 n'est pas une constante (0 ou 1)")

        g_output = self.get_output_ids()

        for iden in n2.get_parents_ids():
            del self[iden]

        new_label = "1" if n2_label == "0" else "0"

        self[id1].set_label(new_label)

        del self[id2]
        self.set_output_ids(g_output)

    def and_gate(self, id1, id2):
        """
        Applique la transformation de la porte &
        id1 : int -> id d'une porte &
        id2 : int -> id d'une constante 0 ou 1
        """
        n1 = self[id1]
        n2 = self[id2]

        if n1.get_label() != '&':
            raise ValueError("Le noeud d'id1 n'est pas un 'et'")

        n2_label = n2.get_label()

        if n2_label != '1' and n2_label != '0':
            raise ValueError("Le noeud d'id2 n'est pas 0 ou 1")

        g_input = self.get_input_ids()
        g_output = self.get_output_ids()

        for iden in n2.get_parents_ids():
            del self[iden]

        del self[id2]
        if n2_label == '0':
            n1.set_label('0')
            for iden in n1.get_parents_ids():
                self.add_node(parents={iden: n1.parents[iden]})
                self.remove_parallel_edges(iden, id1)

        self.set_input_ids(g_input)
        self.set_output_ids(g_output)

    def or_gate(self, id1, id2):
        """
        Applique la transformation de la porte |
        id1 : int -> id d'une porte |
        id2 : int -> id d'une constante 0 ou 1
        """
        n1 = self[id1]
        n2 = self[id2]

        if n1.get_label() != '|':
            raise ValueError("Le noeud d'id1 n'est pas un 'ou'")

        if n2.get_label() != '0' and n2.get_label() != '1':
            raise ValueError("Le noeud d'id2 n'est pas 0 ou 1")

        g_output = self.get_output_ids()

        for iden in n2.get_parents_ids():
            del self[iden]

        del self[id2]
        if n2.get_label() == '1':
            n1.set_label('1')
            for iden in n1.get_parents_ids():
                if iden in self.get_input_ids():
                    new_id = self.add_node()
                    self[iden].set_children_ids({new_id: 1})
                    self[new_id].set_parents_ids({iden: 1})
                    n1.set_parents_ids({})
                else:
                    self.add_node(parents={iden: n1.parents[iden]})
                    self.remove_parallel_edges(iden, id1)

        self.set_output_ids(g_output)

    def xor_gate(self, id1, id2):
        """
        Applique la transformation de la porte 'ou exclusif'
        id1 : int -> id d'une porte ^
        id2 : int -> id d'une constante 0 ou 1
        """
        n1 = self[id1]
        n2 = self[id2]

        if n1.get_label() != "^":
            raise ValueError("Le noeud d'id1 n'est pas un ou exclusif (^)")

        n2_label = n2.get_label()

        if n2_label != "0" and n2_label != "1":
            raise ValueError("Le noeud d'id2 n'est pas une constante (0 ou 1)")

        outputs = self.get_output_ids()

        for iden in n2.get_parents_ids():
            del self[iden]

        del self[id2]

        if n2_label == "1":

            children_copy = n1.children.copy()

            for iden in children_copy.keys():
                self.remove_parallel_edges(id1, iden)

            new_id = self.add_node("~", {id1: 1}, children_copy)

            n1.set_children_ids({new_id: 1})
            self.set_output_ids(outputs)

    def apply_bin_gate(self, id1, id2):
        """
        Applique la transformation adapté au noeud d'id2
        id1 : int -> id d'une porte &, |, ^ ou ~
        id2 : int -> id d'une constante 0 ou 1
        """
        label = self[id1].get_label()
        if label == '':
            self.copy_gate(id1, id2)
        elif label == '&':
            self.and_gate(id1, id2)
        elif label == '|':
            self.or_gate(id1, id2)
        elif label == '^':
            self.xor_gate(id1, id2)
        elif label == '~':
            self.neg_gate(id1, id2)

    def neutral_gate(self, id1):
        """
        Applique la transformation de la porte neutre
        id1 : int -> id d'une porte |, ^ ou &
        """
        n1 = self[id1]
        label = n1.get_label()
        parents_id = n1.get_parents_ids()

        if parents_id == []:

            if label == "|" or label == "^":
                n1.set_label("0")

            elif label == "&":
                n1.set_label("1")

            else:
                raise ValueError(
                    "Le noeud d'id1 n'est pas une porte |, ^ ou &")

        else:
            raise ValueError("Le noeud d'id1 possede des parents")

    def _estCoLeaf_(self, iden):
        """ Sous-fonction de evaluate qui permet de verifier si le noeud d'id iden est une co-feuille
            iden: int -> id du noeud qu'on test pour savoir si c'est une co-feuille
            renvoie True si le noeud est une co-feuille, False sinon
        """
        inputs = self.get_input_ids()
        # Les outputs ne comptent pas comme des co-feuilles dans evaluate
        if iden in self.get_output_ids():
            return False
        # Un noeud est une co-feuille si tous ces parents sont des inputs
        # ( si un noeud n'a pas de parent alors tous ces parents sont des inputs ^^)
        if len(self[iden].get_parents_ids()) != 0:
            return False
        else:
            return True

    def _eraseBranch_(self, id1, id2):
        """methode utilise dans evaluate qui retire le noeud id1 et tous ses parents qui sont effacables
           id1: int -> id du noeud contenant une operation binaire ( noeud qui pointe)
           id2: int -> id d'un noeud copie ( noeud qui est pointee )
        """
        parents = self[id1].get_parents_ids()
        # On efface le noeud qui pointe et le noeud pointee
        self.apply_erasure_gate(id1, id2)

        # les parents d'id1 peuvent devenir effacables suite a sa suppression
        for iden in parents:
            node_children = self[iden].get_children_ids()
            # Si un parent est effacable alors on l'efface
            if len(node_children) == 1 and iden not in self.get_input_ids():
                fils_id = node_children[0]
                # En reappelant la fonction on s'assure de retirer tous ces parents effacables
                self._eraseBranch_(iden, fils_id)

    def _evaluate_co_leaves_(self):
        """ Sous-Fonction de evaluate qui evalue tous les noeuds constants"""
        # tableau dans lequel on ajoute tous les noeuds sans parents
        co_leaves = [
            iden for iden in self.get_id_node_map() if self._estCoLeaf_(iden)
        ]
        i = 0
        cpt = 0
        # Tant que l'on a pas traite tous les noeuds sans parents
        while i < len(co_leaves):
            node_id = co_leaves[i]
            node_label = self[node_id].get_label()

            # si le noeud est une constante, on regarde quel transformation on peut appliquer
            if node_label == '0' or node_label == '1':
                child_id = self[node_id].get_children_ids()[0]
                child_label = self[child_id].get_label()
                i += 1
                # Si le fils du noeud est une sortie, on ne fait rien
                if child_id not in self.get_output_ids():
                    self.apply_bin_gate(child_id, node_id)
                    # si le fils est une copie, on recalcule co_leaves car il est possible que l'on ait ajouté plusieurs noeuds sans parents.
                    if child_label == '':
                        co_leaves = [
                            iden for iden in self.get_id_node_map()
                            if self._estCoLeaf_(iden)
                        ]
                        i = 0
                    # Si le fils n'a plus de parent on l'ajoute a l'ensemble
                    # On applique pas directement
                    elif len(self[child_id].get_parents_ids()) == 0:
                        co_leaves.append(child_id)
            # si le noeud n'est pas une constante ou une copie et qu'il n'a pas de parent alors on simplifie le noeud
            elif len(
                    self[node_id].get_parents_ids()) == 0 and node_label != '':
                self.neutral_gate(node_id)
            # sinon on ignore le noeud
            else:
                i += 1

    def evaluate(self):
        """
        Applique des transformations sur le graphe jusqu'à ce qu'il n'y en ait plus
        """
        # On evalue les noeuds n'ayant pas de parent, tant qu'il existe des noeuds sans parents
        self._evaluate_co_leaves_()

        # On parcours les noeuds par profondeur des moins profond au plus profond
        top_sort = self.topological_sort()

        k = 0
        while k < len(top_sort):

            i = 0
            # On increment k ici car plus tard on utilise des break
            k += 1
            ens = top_sort[k - 1]
            while i < len(ens):

                node_id = ens[i]
                node = self[node_id]
                node_label = node.get_label()
                reset_loop = True  # flag indiquant si on reprend de 0
                recal_sort = True  # flag indiquant si on recalcule le tri topologique

                if node.outdegree() >= 1 and node.indegree() >= 1:

                    fils_id = node.get_children_ids()[0]
                    fils = self[fils_id]
                    fils_label = fils.get_label()
                    # Si le fils n'est pas un output et est un noeud copie sans fils alors on efface le noeud courant
                    # et tous ces parents qui deviennent effacable
                    if fils_label == '' and fils.outdegree(
                    ) == 0 and node.outdegree(
                    ) == 1 and fils_id not in self.get_output_ids():
                        self._eraseBranch_(node_id, fils_id)
                    # On traite le cas ou le noeud courant est une porte neg
                    elif node_label == '~':

                        if fils_label == '^':
                            self.not_through_xor_gate(fils_id, node_id)
                        elif fils_label == '' and fils.outdegree() > 0:
                            self.not_through_copy_gate(node_id, fils_id)
                        elif fils_label == '~':
                            self.invol_not_gate(node_id, fils_id)
                        else:
                            # Si on ne fait pas de transformation on a pas besoin de recalculer le tri topologique
                            recal_sort = False
                            # On a pas besoin non plus de faire de reparcourir tout le tri topologique en entier
                            reset_loop = False
                            i += 1
                    # On traite le cas ou le noeud courant est une porte xor et le fils est une porte xor
                    elif node_label == '^' and fils_label == '^':
                        # On a pas besoin de reparcourir le tri topologique en entier
                        reset_loop = False
                        self.assoc_xor_gate(fils_id, node_id)
                    # On traite le cas ou le noeud courant est une copie
                    elif node_label == '':

                        node_children = node.get_children_ids()
                        j = 0
                        reset_loop = False
                        recal_sort = False

                        while j < len(node_children):

                            fils_id = node_children[j]
                            fils = self[fils_id]
                            fils_label = self[fils_id].get_label()

                            parent_id = node.get_parents_ids()[0]
                            # Si le noeud copie n'a qu'un pere qui n'est pas un input et qu'un fils qui n'est pas un output alors on peut retirer le noeud copie et relier son pere et son fils par une arte
                            if node.outdegree(
                            ) == 1 and fils_id not in self.get_output_ids(
                            ) and parent_id not in self.get_input_ids():
                                self.add_edge(parent_id, fils_id)
                                del self[node_id]
                                j += 1
                            # Si le fils n'est pas un output et que c'est une copie alors on fait l'associativite
                            elif fils_label == '' and fils_id not in self.get_output_ids(
                            ):

                                self.assoc_copy_gate(node_id, fils_id)
                                # Dans assoc copy gate on retire le noeud d'id node_id du graphe
                                node_id = fils_id
                                node = fils
                                node_label = fils_label
                                node_children = fils.get_children_ids()
                                j = 0
                                # On a besoin de recalculer le tri topologique car on modifie la profondeur d'en dessous
                                recal_sort = True

                            else:
                                if fils_label == '^' and node.child_mul(
                                        fils_id) % 2 == 0:

                                    self.invol_xor_gate(fils_id, node_id)
                                    # Parce que le noeud xor n'a pas ete traité, sa profondeur peut etre diminuer de 2 a la suite de l'involution
                                    reset_loop = True
                                    recal_sort = True
                                    if self[fils_id].indegree() == 0:
                                        # Si le noeud n'a plus de parent suite a l'involution on transforme le noeud en 0 et on l'evalue
                                        # tous les noeuds constants
                                        self.neutral_gate(fils_id)
                                        self._evaluate_co_leaves_()

                                j += 1
                    else:
                        # si on ne fait pas de transformation on a pas besoin de recalculer le tri
                        reset_loop = False
                        recal_sort = False
                    # Si recal_sort est True on recalcule le tri sinon on regarde le prochain noeud dans la profondeur k actuelle
                    # En pratique, on recalcule le tri lorsque des transformation ont ete realisee
                    if recal_sort:
                        top_sort = self.topological_sort()
                        # On reparcours l'ensemble des noeuds de profondeur k
                        i = 0
                        # Si reset_loop est True, on sort de la boucle while et on reexplore le tri de 0
                        # on reparcourt le tri lorsque la transformation peut creer une arete entre un noeud de profondeur k-1 avant la
                        # transformation et un noeud de profondeur k+1 apres la transformation
                        # On reparcours le tri apres not_through_xor, not_through_copy, invol_not, invol_xor, erase
                        if reset_loop:
                            k = 0
                            break
                    else:
                        i += 1

                    if len(top_sort) > k - 1:
                        # On s'assure que l'ensemble de noeud explore soient à jour
                        ens = top_sort[k - 1]
                    else:
                        break

                else:
                    reset_loop = False
                    recal_sort = False
                    i += 1

    def assoc_xor_gate(self, id1, id2):
        """
        Applique la transformation de l'associativite de la porte xor
        id1: int -> id d'une porte xor (celle qui est pointee)
        id2: int -> id d'une porte xor (celle qui pointe)
        """
        n1 = self[id1]
        n2 = self[id2]

        n1_label = n1.get_label()
        n2_label = n2.get_label()

        n1_parents = n1.get_parents_ids()
        n2_children = n2.get_children_ids()

        if n1_label != "^" or n2_label != "^":
            raise ValueError(
                "L'un des deux ids ne correspond a une porte xor (^) !")

        if n2.outdegree() != 1:
            raise ValueError(
                "Le noeud d'id2 ne possede pas qu'un lien enfant !")

        if id1 not in n2_children or id2 not in n1_parents:
            raise ValueError(
                "Les noeuds d'id1 et d'id2 ne sont pas connectes !")

        n1_children = n1.get_children_ids()
        g_outputs = self.get_output_ids()

        n2_parents = n2.get_parents_ids()
        g_inputs = self.get_input_ids()

        self.remove_parallel_edges(id2, id1)
        new_id = self.node_fusion(id2, id1)

        self[new_id].set_label("^")

        self.set_input_ids(g_inputs)
        self.set_output_ids(g_outputs)

    def assoc_copy_gate(self, id1, id2):
        """
        Applique la transformation de l'associativite de la porte copy
        id1: int -> id d'une porte copy (celle qui pointe)
        id2: int -> id d'une porte copy (celle qui est pointee)
        """
        n1 = self[id1]
        n2 = self[id2]

        n1_label = n1.get_label()
        n2_label = n2.get_label()

        n1_children = n1.get_children_ids()
        n2_parents = n2.get_parents_ids()

        if n1_label != "" or n2_label != "":
            raise ValueError(
                "L'un des deux ids ne correspond a une porte copy () !")

        if id1 not in n2_parents or id2 not in n1_children:
            raise ValueError(
                "Les noeuds d'id1 et d'id2 ne sont pas connectes !")

        if n1.indegree() != 1:
            raise ValueError("Le noeud d'id1 possede trop de parents !")

        if n2.indegree() != 1:
            raise ValueError("Le noeud d'id2 possed trop de parents !")

        pere = n1.get_parents_ids()[0]

        n1_real_children = n1.children.copy()
        if id2 in n1_real_children:
            del n1_real_children[id2]

        g_input = self.get_input_ids()
        g_output = self.get_output_ids()
        del self[id1]

        self.add_edge(pere, id2)

        for iden, arretes in n1_real_children.items():
            for _ in range(arretes):
                self.add_edge(id2, iden)

        self.set_input_ids(g_input)
        self.set_output_ids(g_output)

    def invol_xor_gate(self, id1, id2):
        """
        Applique la transformation de l'involution de la porte xor
        id1: int -> id d'une porte xor (celle qui est pointee)
        id2: int -> id d'une porte copie (celle qui pointe)
        """
        n1 = self[id1]
        n2 = self[id2]

        n1_label = n1.get_label()
        n2_label = n2.get_label()

        n1_parents = n1.get_parents_ids()
        n2_children = n2.get_children_ids()

        if n1_label != "^" or n2_label != "":
            raise ValueError(
                "L'un des deux ids ne correspond pas a la bonne porte")

        if id1 not in n2_children or id2 not in n1_parents:
            raise ValueError(
                "Les noeuds d'id1 et d'id2 ne sont pas connectes !")

        if n1.parents[id2] != n2.children[id1]:
            raise ValueError(
                "Les arretes entre noeuds d'id1 et d'id2 n'est pas valide !")

        if n1.outdegree() != 1:
            raise ValueError("La porte xor possede trop de fils !")

        if n2.indegree() != 1:
            raise ValueError("La porte copie possede trop de parents !")

        g_input = self.get_input_ids()
        g_output = self.get_output_ids()
        if n1.parents[id2] % 2 == 0:
            self.remove_parallel_edges(id2, id1)

        else:
            while (n1.parents[id2] > 1):
                self.remove_edge(id2, id1)
                self.remove_edge(id2, id1)
        self.set_input_ids(g_input)
        self.set_output_ids(g_output)

    def apply_erasure_gate(self, id1, id2):
        """
        Applique l'effacement sur une porte operateur quelconque
        id1: int -> id d'une porte operateur (celle qui pointe)
        id2: int -> id d'une porte copie (celle qui est pointee)
        """
        n1 = self[id1]
        n2 = self[id2]

        n1_label = n1.get_label()
        n2_label = n2.get_label()

        n1_children = n1.get_children_ids()
        n2_parents = n2.get_parents_ids()

        if n2_label != "":
            raise ValueError(
                "L'un des deux ids ne correspond pas a la bonne porte")

        if id1 not in n2_parents or id2 not in n1_children:
            raise ValueError(
                "Les noeuds d'id1 et d'id2 ne sont pas connectes !")

        if n1.outdegree() != 1:
            raise ValueError("La porte xor possede trop de fils !")

        if n2.indegree() != 1:
            raise ValueError("La porte copie possede trop de parents !")

        if n2.outdegree() > 0:
            raise ValueError("La porte copie possede trop de fils !")

        n1_parents = n1.get_parents_ids()
        del self[id1]
        del self[id2]

        for iden in n1_parents:
            self.add_node(label="", parents={iden: 1}, children={})

    def not_through_xor_gate(self, id1, id2):
        """
        Applique le NON a travers le XOR
        id1: int -> id d'une porte XOR (celle qui est pointee)
        id2: int -> id d'une porte NON (celle qui pointe)
        """
        n1 = self[id1]
        n2 = self[id2]

        n1_label = n1.get_label()
        n2_label = n2.get_label()

        n1_parents = n1.get_parents_ids()
        n2_children = n2.get_children_ids()

        if n1_label != "^" or n2_label != "~":
            raise ValueError(
                "L'un des deux ids ne correspond pas a la bonne porte")

        if id1 not in n2_children or id2 not in n1_parents:
            raise ValueError(
                "Les noeuds d'id1 et d'id2 ne sont pas connectes !")

        if n2.indegree() != 1 or n2.outdegree() != 1:
            raise ValueError(
                "La porte NON possede trop de fils ou trop de parents !")

        if n1.outdegree() != 1:
            raise ValueError("La porte XOR possede trop de fils !")

        n1_real_parents = n1.parents.copy()
        n1_real_children = n1.children.copy()
        n2_real_parents = n2.parents.copy()

        if id2 in n1_real_parents.keys():
            del n1_real_parents[id2]

        if id2 in n1_real_children.keys():
            del n1_real_children[id2]

        if id1 in n2_real_parents.keys():
            del n2_real_parents[id1]

        inputs = self.get_input_ids()
        outputs = self.get_output_ids()

        del self[id1]
        del self[id2]

        new_xor = self.add_node(label="^")

        for iden, arretes in n1_real_parents.items():
            for _ in range(arretes):
                self.add_edge(iden, new_xor)

        for iden, arretes in n2_real_parents.items():
            for _ in range(arretes):
                self.add_edge(iden, new_xor)

        new_not = self.add_node(label="~", parents={new_xor: 1})

        for iden, arretes in n1_real_children.items():
            for _ in range(arretes):
                self.add_edge(new_not, iden)
        self.set_input_ids(inputs)
        self.set_output_ids(outputs)

    def not_through_copy_gate(self, id1, id2):
        """
        Applique le NON a travers la porte COPIE
        id1: int -> id d'une porte NON (celle qui pointe)
        id2: int -> id d'une porte COPIE (celle qui est pointee)
        """
        n1 = self[id1]
        n2 = self[id2]

        n1_label = n1.get_label()
        n2_label = n2.get_label()

        n1_children = n1.get_children_ids()
        n2_parents = n2.get_parents_ids()

        if n1_label != "~" or n2_label != "":
            raise ValueError(
                "L'un des deux ids ne correspond pas a la bonne porte")

        if id1 not in n2_parents or id2 not in n1_children:
            raise ValueError(
                "Les noeuds d'id1 et d'id2 ne sont pas connectes !")

        if n1.indegree() != 1 or n1.outdegree() != 1:
            raise ValueError(
                "La porte NON possede trop de fils ou trop de parents !")

        if n2.indegree() != 1:
            raise ValueError("La porte COPIE possede trop de parents !")

        n1_real_parents = n1.parents.copy()

        if id2 in n1_real_parents.keys():
            del n1_real_parents[id2]

        inputs = self.get_input_ids()
        outputs = self.get_output_ids()
        del self[id1]

        for iden, arretes in n1_real_parents.items():
            for _ in range(arretes):
                self.add_edge(iden, id2)

        n2_children = n2.get_children_ids()
        n2_real_children = n2.children.copy()

        for iden, arretes in n2_real_children.items():
            for _ in range(arretes):
                self.remove_edge(id2, iden)

        for iden in n2_children:
            self.add_node(label="~", parents={id2: 1}, children={iden: 1})

        self.set_input_ids(inputs)
        self.set_output_ids(outputs)

    def invol_not_gate(self, id1, id2):
        """
        Applique la transformation de l'involution de la porte NOT
        id1: int -> id d'une porte NOT (celle qui pointe)
        id2: int -> id d'une porte NOT (celle qui est pointee)
        """
        n1 = self[id1]
        n2 = self[id2]

        n1_label = n1.get_label()
        n2_label = n2.get_label()

        n1_children = n1.get_children_ids()
        n2_parents = n2.get_parents_ids()

        if n1_label != "~" or n2_label != "~":
            raise ValueError(
                "L'un des deux ids ne correspond pas a la bonne porte")

        if id1 not in n2_parents or id2 not in n1_children:
            raise ValueError(
                "Les noeuds d'id1 et d'id2 ne sont pas connectes !")

        if n1.indegree() != 1 or n1.outdegree() != 1:
            raise ValueError(
                "La porte not (qui pointe) possede trop de fils ou de parents !"
            )

        if n2.indegree() != 1 or n2.outdegree() != 1:
            raise ValueError(
                "La porte not (qui est pointee) possede trop de fils ou de parents !"
            )

        pere = n1.get_parents_ids()[0]
        fils = n2.get_children_ids()[0]

        inputs = self.get_input_ids()
        outputs = self.get_output_ids()
        del self[id1]
        del self[id2]

        self.add_edge(pere, fils)
        self.set_input_ids(inputs)
        self.set_output_ids(outputs)

    # Methodes de base

    def copy(self):
        """ Renvoie une copie d'un bool_circ """
        input_ids = self.get_input_ids()
        output_ids = self.get_output_ids()
        nodes = self.get_nodes()

        g = open_digraph(input_ids, output_ids, nodes)

        return self.__class__(g.copy())

    def is_cyclic(self):
        """ Renvoie True si le graph est cyclique, False sinon """
        input_ids = self.get_input_ids()
        output_ids = self.get_output_ids()
        nodes = self.get_nodes()

        g = open_digraph(input_ids, output_ids, nodes)

        return self.is_cyclic_bis(g.copy(), [])

    def is_cyclic_bis(self, g, feuille_list):
        """
        Fonction bis qui gere la recurcivite
        g : open_digraph -> Contient les noeuds visibles par la fonction
        feuille_list : node list -> Contient les noeuds feuilles du graph
        """
        nodes = g.get_nodes()

        if len(nodes) == 0:
            return False

        else:

            for node in nodes:
                if node.outdegree() == 0:
                    feuille_list.append(node.get_id())

            if len(feuille_list) == 0:
                return True

        del g[feuille_list]
        return self.is_cyclic_bis(g, [])

    def is_well_formed(self):
        """
        Souleve une erreur si le graph n'est pas correct
        Le assert est effectue dans cette fonction afin d'avoir une erreur plus precise
        """
        if self.is_cyclic():
            raise ValueError("Le bool_circ est cyclique.")

        node_list = self.get_nodes()
        symbol = ["&", "|", "~", "", "0", "1", "^"]

        for node in node_list:
            label = node.get_label()

            if label not in symbol:
                raise ValueError(
                    "Un label ne correspond aux labels autorises pour un bool_circ"
                )

            if label == "" and node.indegree() > 1:
                raise ValueError("Un noeud 'copie' possede plus qu'une entree")

            if (label == "&" or label == "|"
                    or label == '^') and node.outdegree() > 1:
                raise ValueError(
                    "Un noeud '&' ou '|' ou '^' possede plus qu'une sortie")

            if label == "~" and (node.indegree() > 1 or node.outdegree() > 1):
                raise ValueError(
                    "Un noeud '~' possede plus qu'une sortie et/ou plus qu'une entree"
                )
