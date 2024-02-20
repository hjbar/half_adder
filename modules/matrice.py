import numpy as np


def random_int_list(n, bound):
    """
    Renvoie une matrice de dimension (1, n) dont les valeurs aleatoires sont comprises entre 0 et bound inclus
    n : int -> nombre d'elements de la liste
    bound : int -> la borne superieur des valeurs de la matrice
    """
    return np.random.randint(0, bound + 1, n, dtype="int")


def random_int_matrix(n, bound, null_diag=True):
    """
    Renvoie une matrice de dimension (n, n) dont les valeurs aleatoires sont comprises entre 0 et bound inclus
    n : int -> taille de la matrice avec nb_colonnes = nb_lignes = n
    bound : int -> la borne superieur des valeurs de la matrice
    null_diag : bool option, True par defaut -> les valeurs des diagonales sont nuls si True
    """
    A = np.random.randint(0, bound + 1, (n, n))

    if null_diag:
        ind = np.arange(0, n)
        A[ind, ind] = 0

    return A


def random_symetric_int_matrix(n, bound, null_diag=True):
    """
    Renvoie une matrice symetrique de dimension (n, n) dont les valeurs aleatoires sont comprises entre 0 et bound inclus
    n : int -> taille de la matrice avec nb_colonnes = nb_lignes = n
    bound : int -> la borne superieur des valeurs de la matrice
    null_diag : bool option, True par defaut -> les valeurs des diagonales sont nuls si True
    """
    A = random_int_matrix(n, bound, null_diag=null_diag)
    A = np.tril(A)
    A = A + A.transpose()

    if not null_diag:
        ind = np.arange(0, n)
        A[ind, ind] //= 2

    return A


def random_oriented_int_matrix(n, bound, null_diag=True):
    """
    Renvoie une matrice orientee de dimension (n, n) dont les valeurs aleatoires sont comprises entre 0 et bound inclus
    Matrice orientee i.e. (i, j) != 0 => (j, i) = 0 pour tout i, j appartenant a la matrice orientee
    n : int -> taille de la matrice avec nb_colonnes = nb_lignes = n
    bound : int -> la borne superieur des valeurs de la matrice
    null_diag : bool option, True par defaut -> les valeurs des diagonales sont nuls si True
    """
    A = np.zeros((n, n), dtype="int")

    for i in range(n):
        for j in range(0, i + 1):

            flag = np.random.randint(0, 2)

            if null_diag and i == j:
                A[i, j] = 0
            elif flag == 0:
                A[i, j] = np.random.randint(0, bound + 1)
            else:
                A[j, i] = np.random.randint(0, bound + 1)

    return A


def random_triangular_int_matrix(n, bound, null_diag=True):
    """
    Renvoie une matrice triangulaire superieur de dimension (n, n) dont les valeurs aleatoires sont comprises entre 0 et bound inclus
    n : int -> taille de la matrice avec nb_colonnes = nb_lignes = n
    bound : int -> la borne superieur des valeurs de la matrice
    null_diag : bool option, True par defaut -> les valeurs des diagonales sont nuls si True
    """
    A = random_int_matrix(n, bound, null_diag=null_diag)

    return np.triu(A)


def random_matrix(n,
                  bound,
                  null_diag=True,
                  symetric=False,
                  oriented=False,
                  triangular=False):
    """
    Renvoie une matrice de forme souhaitee de dimension (n, n) dont les valeurs aleatoires sont comprises entre 0 et bound inclus
    n : int -> taille de la matrice avec nb_colonnes = nb_lignes = n
    bound : int -> la borne superieur des valeurs de la matrice
    null_diag : bool option, True par defaut -> les valeurs des diagonales sont nuls si True
    symetric : bool option, False par defaut -> renvoie une matrice symetrique si True
    oriented : bool option, False par defaut -> renvoie une matrice orientee si True
    triangular : bool option, False par defaut -> renvoie une matrice triangular si True
    """
    if symetric:
        return random_symetric_int_matrix(n, bound, null_diag=null_diag)

    elif oriented:
        return random_oriented_int_matrix(n, bound, null_diag=null_diag)

    elif triangular:
        return random_triangular_int_matrix(n, bound, null_diag=null_diag)

    else:
        return random_int_matrix(n, bound, null_diag=null_diag)
