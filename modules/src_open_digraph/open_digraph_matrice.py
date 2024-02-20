from modules.matrice import *
import random


class open_digraph_matrice():

    @classmethod
    def graph_from_adjacency_matrix(cls, mat):
        """
        Renvoie un open_digraph cree a partir d'une matrice d'adjacence
        mat : int list->list -> une matrice d'adjacence
        """
        cls = cls.empty()
        n = len(mat)

        for i in range(n):
            cls.add_node(label=chr(i + 97))

        for i in range(n):
            for j in range(n):

                nb_arrete = mat[i][j]

                if nb_arrete > 0:
                    cls.add_edges([(i, j) for _ in range(nb_arrete)])

        return cls

    @classmethod
    def random(cls, n, bound, inputs=0, outputs=0, form="free"):
        """
        Creer un graph aleatoire soumit un differentes options :
            - free : graph cree a partir d'une matrice aleatoire quelconque
            - DAG : graph cree a partir d'une matrice aleatoire triangulaire
            - oriented : graph cree a partir d'une matrice aleaoire orientee
            - loop-free : graph cree a partir d'une matrice aleatoire quelconque avec des diagonales non-nuls
            - undirected : graph cree a partir d'une matrice aleatoire symetrique
            - loop-free undirected : graph cree a partir d'une matrice aleatoire symetrique avec des diagonales non-nuls
        n : int -> nombre de noeuds du graph (sans compter les inputs/outputs)
        bound : int -> nombre d'arretes maximales entre 2 noeuds
        inputs : int -> nombre d'inputs dans le graph
        outputs : int -> nombre d'outputs dans le graph
        form : string -> options du type de graph cree
        """
        if n < max(inputs, outputs):
            raise ValueError(
                "Le nombre de noeuds est trop faible pour avoir le nombre d'inputs et d'outputs choisit."
            )

        elif n == 0:
            return cls.empty()

        if form == "free":
            mat = random_matrix(n, bound)

        elif form == "DAG":
            mat = random_matrix(n, bound, triangular=True)

        elif form == "oriented":
            mat = random_matrix(n, bound, oriented=True)

        elif form == "loop-free":
            mat = random_matrix(n, bound, null_diag=False)

        elif form == "undirected":
            mat = random_matrix(n, bound, symetric=True)

        elif form == "loop-free-undirected":
            mat = random_matrix(n, bound, null_diag=False, symetric=True)

        else:
            raise ValueError("La forme du graph choisie n'est pas valide.")

        cls = cls.graph_from_adjacency_matrix(mat)
        id_list = cls.get_nodes_ids()
        n = len(id_list) - 1

        for _ in range(inputs):
            iden = id_list.pop(random.randint(0, n))
            n -= 1
            cls.add_input_node(iden)

        for _ in range(outputs):
            iden = id_list.pop(random.randint(0, n))
            n -= 1
            cls.add_output_node(iden)

        return cls

    def adjacency_matrix(self):
        """ Renvoie la matrice d'adjacence d'un graph """
        g_copy = self.copy()

        input_ids = g_copy.get_input_ids()
        del g_copy[input_ids]

        output_ids = g_copy.get_output_ids()
        del g_copy[output_ids]

        dict_nodes = g_copy.graph_to_dict_id()
        n = len(dict_nodes)
        A = np.zeros((n, n), dtype="int")

        for i in range(n):

            node = dict_nodes[i]
            children_list = node.get_children_ids()

            for j in children_list:

                A[i, j] = node.children[j]

        return A
