from modules.open_digraph import *
from modules.bool_circ import *
from modules.matrice import *
import inspect

# Création d'un graph

n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})

i0 = node(3, 'i0', {}, {0: 1})
i1 = node(4, 'i1', {}, {0: 1})

o0 = node(5, 'o0', {1: 1}, {})
o1 = node(6, 'o1', {2: 1}, {})

node_list = [n0, n1, n2, i0, i1, o0, o1]

G = open_digraph([3, 4], [5, 6], node_list)

# Création d'une liste de graph

G_list = [G, G, G]

# Test d'affichage d'un noeud

print()
print("Le noeud n0 :")
print(n0)
print()

# Test d'affichage d'une liste de noeud

print("La liste des noeuds :")
print(node_list)
print()

# Test d'un graph

print("Le graph G :")
print(G)
print()

# Test d'une liste de graph

print("La liste des graphs :")
print(G_list)
print()

# Affichage de la liste des methodes de Node & Open_diagraph

print("La liste des methodes de la classe Node :")
print(dir(node))
print()

print("La liste des methodes de la classe Open_diagraph :")
print(dir(open_digraph))
print()

# Affichage du code source de la methode set_input_ids de la classe Open_diagraph

print("Code source de set_input_ids :")
print(inspect.getsource(open_digraph.set_input_ids))
print()

# Affichage de la doc de la methode set_input_ids de la classe Open_diagraph

print("Doc de set_input_ids :")
print(inspect.getdoc(open_digraph.set_input_ids))
print()

# Affichage du fichier dans lequel se trouve la methode set_input_ids de la classe Open_diagraph

print("Fichier de set_input_ids :")
print(inspect.getfile(open_digraph.set_input_ids))
print()

# Afficher un graph a partir d'une matrice d'adjacence

mat = random_matrix(5, 3, symetric=True)
g = open_digraph.graph_from_adjacency_matrix(mat)
g.is_well_formed()

print(
    "Graph cree a partir d'une matrice d'adjacence (matrice aleatoire symetrique) :"
)
print(g)
print()

mat = random_matrix(5, 3, oriented=True)
g = open_digraph.graph_from_adjacency_matrix(mat)
g.is_well_formed()

print(
    "Graph cree a partir d'une matrice d'adjacence (matrice aleatoire orientee) :"
)
print(g)
print()

mat = random_matrix(5, 3, triangular=True)
g = open_digraph.graph_from_adjacency_matrix(mat)
g.is_well_formed()

print(
    "Graph cree a partir d'une matrice d'adjacence (matrice aleatoire triangulaire) :"
)
print(g)
print()

# Creation de fichiers .dot tests pour afficher les graphs

print("Creation d'un fichier .dot avec verbose=False et fichier local")
G.save_as_dot_file("tmp_test_verbose_false.dot")
print("Fichier cree")
print()

print("Creation d'un fichier .dot avec verbose=True et fichier local")
G.save_as_dot_file("tmp_test_verbose_true.dot", verbose=True)
print("Fichier cree")
print()

print(
    "Creation d'un fichier .dot avec verbose=False et fichier dans d'autres repertoires"
)
G.save_as_dot_file("tmp_test/tmpdetmp/test_verbose_false.dot")
print("Fichier cree")
print()

print(
    "Creation d'un fichier .dot avec verbose=True et fichier dans d'autres repertoires"
)
G.save_as_dot_file("tmp_test/tmpdetmp/test_verbose_true.dot", verbose=True)
print("Fichier cree")
print()

print("Affiche la visualisation du graph avec verbose=False")
G.display()
print()

print("Affiche la visualisation du graph avec verbose=True")
G.display(verbose=True)
print()

print("Adder de 2")
A0 = bool_circ.Adder(2)
A0.display()
print()

print("Adder de 5")
A0 = bool_circ.Adder(5)
A0.display()
print(A0)

print("Half_Adder de 2")
A0 = bool_circ.Half_Adder(2)
A0.display()
print()

print("Half_Adder de 5")
A0 = bool_circ.Adder(5)
A0.display()
print(A0)

print("evaluate sur Half_Adder de 5")
A0 = bool_circ.Half_Adder(1)
print(A0)
A0.evaluate()
# A0.display()
print(A0)

G = bool_circ.random_bool_circ(50, 5, 5)
reg = bool_circ.registre(20, size=5)
comp = G.compose(reg)
comp.evaluate()
print(comp)
G.evaluate()
print(G)
