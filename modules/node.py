class node:

    def __init__(self, identity, label, parents, children):
        """
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        """
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

    def __str__(self):
        """ Renvoie une chaine de caracteres utilisable par print """
        string = "|"
        string += "Id = " + str(self.id) + ", "
        string += "Label = " + str(self.label) + ", "
        string += "Parents = " + str(self.parents) + ", "
        string += "Children = " + str(self.children)
        string += "|"
        return string

    def __repr__(self):
        """ Permet de print un iterateur contenant des nodes """
        return self.__str__()

    def __eq__(self, node):
        """ Surcharge de l'egalite """
        return self.get_id() == node.get_id() and self.get_label(
        ) == node.get_label(
        ) and self.parents == node.parents and self.children == node.children

    # Methodes

    def copy(self):
        """ Renovie une copie d'une node """
        return self.__class__(self.get_id(), self.get_label(),
                              self.parents.copy(), self.children.copy())

    # Getters

    def get_id(self):
        """ Renvoie l'identifiant du noeud """
        return self.id

    def get_label(self):
        """ Renvoie la chaîne de caractere label du noeud """
        return self.label

    def get_parents_ids(self):
        """ Renvoie les ids des parents du noeud """
        return list(self.parents.keys())

    def get_children_ids(self):
        """ Renvoie les ids des fils du noeud """
        return list(self.children.keys())

    def child_mul(self, iden):
        """
        Renvoie la multiplicite entre le noeud et le fils d'id iden
        iden : int -> id du fils
        """
        return self.children[iden]

    def parent_mul(self, iden):
        """
        Renvoie la multiplicite entre le noeud et le parent d'id iden
        iden : int -> id du parent
        """
        return self.parents[iden]

    # Setters

    def set_id(self, n):
        """
        Met a jour la valeur de l'id du noeud
        n: entier
        """
        self.id = n

    def set_label(self, s):
        """
        Met a jour la valeur du label du noeud
        s: string
        """
        self.label = s

    def set_parents_ids(self, parents_ids):
        """
        Met a jour la valeur de parents
        parents_ids: int->int dict
        """
        self.parents = parents_ids

    def set_children_ids(self, children_ids):
        """
        Met a jour la valeur de children
        children_ids: int->int dict
        """
        self.children = children_ids

    def add_parent_id(self, iden):
        """
        Ajoute un parent d'id iden pour ce noeud sinon l'incremente de 1 le nombre d'arrete
        iden: int
        """
        if iden not in self.get_parents_ids():
            self.parents[iden] = 1
        else:
            self.parents[iden] += 1

    def add_child_id(self, iden):
        """
        Ajoute un fils d'id iden pour ce noeud sinon l'incremente de 1 le nombre d'arrete
        iden: int
        """
        if iden not in self.get_children_ids():
            self.children[iden] = 1
        else:
            self.children[iden] += 1

    # Removers

    def remove_parent_once(self, parent_id):
        """
        Retire une multiplicité de l'id du parent dans le dictionnaire du champ parents
        parent_id : int
        """
        self.parents[parent_id] = self.parents[parent_id] - 1
        if self.parents[parent_id] == 0:
            del self.parents[parent_id]

    def remove_child_once(self, child_id):
        """
        Retire une multiplicité de l'id du fils dans le dictionnaire du champ children
        child_id : int
        """
        self.children[child_id] = self.children[child_id] - 1
        if self.children[child_id] == 0:
            del self.children[child_id]

    def remove_parent_id(self, parent_id):
        """
        Retire du dictionnaire du champ parent l'élement de clé parent_id
        parent_id : int
        """
        del self.parents[parent_id]

    def remove_child_id(self, child_id):
        """
        Retire du dictionnaire du champ fils l'élement de clé child_id
        child_id : int
        """
        del self.children[child_id]

    # Methodes

    def indegree(self):
        """ Renvoie le degre entrant d'un noeud """
        res = 0

        for degree in self.parents.values():
            res += degree

        return res

    def outdegree(self):
        """ Renvoie le degre sortant d'un noeud """
        res = 0

        for degree in self.children.values():
            res += degree

        return res

    def degree(self):
        """ Renvoie le degre total d'un noeud """
        return self.indegree() + self.outdegree()
