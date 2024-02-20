from modules.bool_circ import *

# On verifie qu'on obtient bien les memes bits au depart et apres l'evaluation
# On test cela pour tous les entiers allant de 0 a 15 (inclus)

print()
print("Verif 1: on obtient bien les bits de depart a la fin")
print()

enc = bool_circ.enc()
dec = bool_circ.dec()

for i in range(16):
    reg = bool_circ.registre(i, size=4)

    comp = dec.compose(enc)
    comp.icompose(reg)

    comp.evaluate()

    outputs_comp = comp.get_output_ids()
    outputs_reg = reg.get_output_ids()

    assert len(outputs_comp) == len(outputs_reg) == 4

    for i in range(4):
        output_comp = comp[outputs_comp[i]]
        output_reg = reg[outputs_reg[i]]
        n_comp = comp[output_comp.get_parents_ids()[0]]
        n_reg = reg[output_reg.get_parents_ids()[0]]

        assert n_comp.get_label() == n_reg.get_label()

        nodes_comp = comp.get_nodes()
        nodes_reg = reg.get_nodes()

    assert len(nodes_comp) == len(nodes_reg) == 8

print()
print("OK")
print()


def add_neg(dec, no_input):
    """
    Ajoute une porte negative sur un decodeur
    dec : bool_circ -> correspond a un decodeur d'Hamming
    no_input : int -> l'input que l'on souhaite erroner
    """
    dec_input = dec.get_input_ids()

    i_no = dec[no_input]
    fils_id = i_no.get_children_ids()[0]
    dec.remove_edge(no_input, fils_id)

    dec.add_node('~', {no_input: 1}, {fils_id: 1})

    dec.set_input_ids(dec_input)


# On verifie qu'avoir une erreur dans le decodeur ne change pas le resultat
# On va tester cela sur chaque input, pour chaque nombre allant de 0 a 15 (inclus)

print()
print("Verif 2: avoir une erreur dans le decodeur ne change pas le resultat")
print()

enc = bool_circ.enc()

for j in range(7):

    dec = bool_circ.dec()
    add_neg(dec, j)

    for i in range(16):
        reg = bool_circ.registre(i, size=4)

        comp = dec.compose(enc)
        comp.icompose(reg)

        comp.evaluate()

        outputs_comp = comp.get_output_ids()
        outputs_reg = reg.get_output_ids()

        assert len(outputs_comp) == len(outputs_reg) == 4

        for i in range(4):
            output_comp = comp[outputs_comp[i]]
            output_reg = reg[outputs_reg[i]]
            n_comp = comp[output_comp.get_parents_ids()[0]]
            n_reg = reg[output_reg.get_parents_ids()[0]]

            assert n_comp.get_label() == n_reg.get_label()

            nodes_comp = comp.get_nodes()
            nodes_reg = reg.get_nodes()

        assert len(nodes_comp) == len(nodes_reg) == 8

print()
print("OK")
print()

# On verifie qu'avoir 2 erreurs dans le decodeur ne permet pas de retrouver le resultat
# On va tester cela sur chaque input (2 par 2), pour chaque nombre allant de 0 a 15 (inclus)

print()
print("Verif 3: avoir 2 erreurs dans le decodeur change le resultat")
print()

enc = bool_circ.enc()

for j in range(6):

    dec = bool_circ.dec()
    add_neg(dec, j)
    add_neg(dec, j + 1)

    for i in range(16):
        reg = bool_circ.registre(i, size=4)

        comp = dec.compose(enc)
        comp.icompose(reg)

        comp.evaluate()

        outputs_comp = comp.get_output_ids()
        outputs_reg = reg.get_output_ids()

        assert len(outputs_comp) == len(outputs_reg) == 4

        flag = True

        for i in range(4):
            output_comp = comp[outputs_comp[i]]
            output_reg = reg[outputs_reg[i]]
            n_comp = comp[output_comp.get_parents_ids()[0]]
            n_reg = reg[output_reg.get_parents_ids()[0]]

            if n_comp.get_label() != n_reg.get_label():
                flag = False

            nodes_comp = comp.get_nodes()
            nodes_reg = reg.get_nodes()

        assert len(nodes_comp) == len(nodes_reg) == 8

        assert flag == False

print()
print("OK")
print()
