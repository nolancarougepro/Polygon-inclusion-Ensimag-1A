#!/usr/bin/env python3

def are_aligned(p1, p2, p3):
    """Teste si les points sont alignés"""
    return (p1[0] == p2[0] == p3[0]) and ((p1[1] == p2[1] == p3[1]) or (p1[2] == p2[2] == p3[2]))

def remove_intermediate_points(file_read, file_write):
    """Ecrit dans un fichier les points extremes."""
    prev_point = None
    prev_prev_point = None
    compteur = 0
    for line in file_read:
        parts = line.split()
        if len(parts) >= 3:
            x = parts[0]
            y = float(parts[1])
            z = float(parts[2])
            current_point = (x, y, z)
            if compteur == 0:
                print(*current_point, file=file_write)
                compteur = compteur + 1
            if prev_point is not None and prev_prev_point is not None:
                if are_aligned(prev_prev_point, prev_point, current_point):
                    # Le point actuel est aligné, donc nous ne l'écrivons pas
                    continue
                else:
                    # Le point actuel n'est pas aligné, nous écrivons le précédent
                    print(*prev_point, file=file_write)
            prev_prev_point = prev_point
            prev_point = current_point
    print(*current_point, file=file_write)

def traite_fichier(file):
    """Traite le fichier"""
    with open(file, 'r') as file_read, open('_tmp', 'w') as file_write:
        remove_intermediate_points(file_read, file_write)
