from modules.bool_circ import *

# On verifie qu'une addition fonctionne bien grace au half-adder

print()
print(
    "On verifie qu'on obtient le bon resultat de l'addition avec un half-adder"
)
print()

ha = bool_circ.Half_Adder(3)

for i in range(0, 16):
    for j in range(0, 32):

        reg1 = bool_circ.registre(i * i, size=8)
        reg2 = bool_circ.registre(4 * j + 1, size=8)

        reg = reg1.parallel(reg2)
        comp = ha.compose(reg)

        comp.evaluate()

        # On test si on trouve la bonne reponse

        comp_nodes = comp.get_nodes()
        comp_outputs = comp.get_output_ids()

        assert len(comp_nodes) == 18
        assert len(comp_outputs) == 9

        s = ""

        for k in comp_outputs:
            s += comp[comp[k].get_parents_ids()[0]].get_label()

        res = i * i + 4 * j + 1
        b = str(bin(res)[2:])

        if len(b) < 9:
            b = "0" * (8 - len(b)) + b

            if res >= 2**8:
                b = "1" + b

            else:
                b = "0" + b

        assert s == b

print()
print("OK")
print()
