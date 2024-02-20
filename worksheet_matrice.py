from modules.matrice import *

print()

print("Test de random_int_list :\n")
print(random_int_list(5, 15))

print("\n")

print("Test de random_int_matrix, null_diag = True :\n")
print(random_matrix(5, 15))

print("\n")

print("Test de random_int_matrix, null_diag = False :\n")
print(random_matrix(5, 15, null_diag=False))

print("\n")

print("Test de random_symetric_int_matrix, null_diag = True :\n")
print(random_matrix(5, 15, symetric=True))

print("\n")

print("Test de random_symetric_int_matrix, null_diag = False :\n")
print(random_matrix(5, 15, null_diag=False, symetric=True))

print("\n")

print("Test de random_oriented_int_matrix, null_diag = True :\n")
print(random_matrix(5, 15, oriented=True))

print("\n")

print("Test de random_oriented_int_matrix, null_diag = False :\n")
print(random_matrix(5, 15, null_diag=False, oriented=True))

print("\n")

print("Test de random_triangular_int_matrix, null_diag = True :\n")
print(random_matrix(5, 15, triangular=True))

print("\n")

print("Test de random_triangular_int_matrix, null_diag = False :\n")
print(random_matrix(5, 15, null_diag=False, triangular=True))
