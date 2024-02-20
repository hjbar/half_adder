from modules.node import *
import os


class open_digraph_display():

    # Methodes concernant le display d'un graph

    @classmethod
    def from_dot_file(cls, filename):
        """ Renvoie un open_digraph cree depuis un fichier .dot """

        if (filename.split('.')[1] != "dot"):
            raise ValueError("Le fichier n'est pas un fichier dot")

        parser = open(filename, 'r')

        if (parser.read(7) != 'digraph'):
            raise ValueError("Le fichier dot ne represente pas un digraph")

        parser.readline()
        data = parser.readlines()

        nodes = {}
        inputs = []
        outputs = []

        for line in data[0:-1]:

            if (line[-3] == ']'):
                t = line.split('=')
                label = None
                iden = None
                i = 0

                if "label" in t[i]:
                    i += 1
                    label = t[i].split('"')[1]

                if "id" in t[i]:
                    i += 1
                    iden = int(t[i].split('"')[1])

                else:
                    iden = int(t[0].split(' ')[0][2:])

                if "input" in t[i]:
                    i += 1
                    inputs.append(iden)

                elif "output" in t[i]:
                    i += 1
                    outputs.append(iden)
                nodes[iden] = node(iden, label, {}, {})

            else:
                t = line.split(" -> ")
                id1 = int(t[0][2:])
                id2 = int(t[1][1:-2])
                nodes[id1].add_child_id(id2)
                nodes[id2].add_parent_id(id1)

        parser.close()
        return cls(inputs, outputs, nodes.values())

    def save_as_dot_file(self, path, verbose=False):
        """
        Creer un fichier .dot pour visualiser le graph
        path : string -> url du fichier
        verbose : bool options -> affiche l'id ou non
        """
        dir_name = os.path.dirname(path)

        if dir_name != "" and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        f = open(path, "w")
        f.write("digraph G {\n")

        copy_g = self.copy()
        input_ids = copy_g.get_input_ids()
        output_ids = copy_g.get_output_ids()
        node_list = copy_g.get_nodes()

        for node in node_list:
            iden = node.get_id()
            f.write(f"\tv{iden} [label=")

            label = node.get_label()
            f.write(f'"{label}"')

            if verbose == True:
                f.write(f',id="{iden}"')

            if iden in input_ids:
                index = input_ids.index(iden)
                f.write(f',input="{index}"]')

            elif iden in output_ids:
                index = output_ids.index(iden)
                f.write(f',output="{index}"]')

            else:
                f.write("]")

            f.write(";\n")

        for node in node_list:
            iden_base = node.get_id()

            for iden, nb in node.children.items():
                for _ in range(nb):
                    f.write(f"\tv{iden_base} -> v{iden};\n")

        f.write("}")

        f.close()

    def display(self, verbose=False):
        """
        Creer un fichier pdf pour visualiser le graph, puis l'ouvre, puis le supprime
        verbose : bool options -> affiche l'id ou non
        """
        self.save_as_dot_file("tmp/graph.dot", verbose)

        os.system("dot -Tpdf tmp/graph.dot -o tmp/graph.pdf")
        os.system("evince tmp/graph.pdf")
        os.system("rm -rf tmp")
