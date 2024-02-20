from modules.src_open_digraph.open_digraph_compositions import *
from modules.src_open_digraph.open_digraph_distance import *
from modules.src_open_digraph.open_digraph_removers import *
from modules.src_open_digraph.open_digraph_getters import *
from modules.src_open_digraph.open_digraph_setters import *
from modules.src_open_digraph.open_digraph_display import *
from modules.src_open_digraph.open_digraph_matrice import *
from modules.src_open_digraph.open_digraph_fusion import *
from modules.src_open_digraph.open_digraph_base import *
from modules.src_open_digraph.open_digraph_id import *

from modules.matrice import *
from modules.node import *


class open_digraph(open_digraph_compositions, open_digraph_distance,
                   open_digraph_removers, open_digraph_getters,
                   open_digraph_setters, open_digraph_display,
                   open_digraph_matrice, open_digraph_fusion,
                   open_digraph_base, open_digraph_id):

    def __init__(self, inputs, outputs, nodes):
        """
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        """
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id: node
                      for node in nodes}  # self.nodes: <int,node> dict

    def __str__(self):
        """ Renvoie une chaine de caracteres utilisable par print """
        string = "Inputs : " + str(self.inputs) + "\n"
        string += "Outputs : " + str(self.outputs) + "\n"
        string += "Nodes : " + str(self.nodes) + "\n"
        return string

    def __repr__(self):
        """ Permet de print un iterateur contenant des open_digraph  """
        return self.__str__()

    def __eq__(self, graph):
        """ Surchage de l'egalite """
        return self.get_input_ids() == graph.get_input_ids(
        ) and self.get_output_ids() == graph.get_output_ids(
        ) and self.get_id_node_map() == graph.get_id_node_map()

    def __getitem__(self, iden):
        """
        Renvoie une node à partir de son identifiant
        identity : int
        """
        return self.nodes[iden]

    def __delitem__(self, *args):
        """
        Retire du graph les noeuds dont les identifiants ont ete passes en argument
        *args : La fonction prend en argument un ou plusieurs entiers ou une liste d'entiers
        """
        # Pour une certaine raison, lorsque l'on passe plusieurs entiers à la fois ou une liste on obtient un tuple de tuple
        if isinstance(args[0], tuple) or isinstance(args[0], list):
            args = args[0]

        for id_node in args:
            node = self[id_node]

            children_ids = node.get_children_ids()
            for child_key in children_ids:
                self.remove_parallel_edges(id_node, child_key)

            parents_ids = node.get_parents_ids()
            for parent_key in parents_ids:
                self.remove_parallel_edges(parent_key, id_node)

            input_ids = self.get_input_ids()
            new_inputs = [
                input_id for input_id in input_ids if input_id != id_node
            ]
            self.set_input_ids(new_inputs)

            output_ids = self.get_output_ids()
            new_outputs = [
                output_id for output_id in output_ids if output_id != id_node
            ]
            self.set_output_ids(new_outputs)

            del self.get_id_node_map()[id_node]
