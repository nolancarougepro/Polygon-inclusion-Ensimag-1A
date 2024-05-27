#!/usr/bin/env python3

import random
from time import time
from sys import argv
import os

if(len(argv) == 3):
    nbr_polygones = int(argv[2])

def croise_segment(pt1_1, pt1_2, pt2_1, pt2_2):
    """détermine si les segments formés par les points se croisent"""
    x_a, y_a = pt1_1
    x_b, y_b = pt1_2
    x_c, y_c = pt2_1
    x_d, y_d = pt2_2
    coeff_dir1 = (y_b - y_a)/(x_b - x_a)
    coeff_dir2 = (y_d - y_c)/(x_d - x_c)
    ord_ori1 = y_a-x_a*coeff_dir1
    ord_ori2 = y_c-x_c*coeff_dir2
    x_inter = (ord_ori1-ord_ori2)/(coeff_dir2-coeff_dir1) #abscisse de l'intersection des droites
    if not(x_a<= x_inter<= x_b or x_b<= x_inter<= x_a):
        return False
    return (x_c<= x_inter<= x_d or x_d<= x_inter<= x_c)


def croise(pt1, pt2, liste):
    """détermine si le fait de générer le segment
    entre pt1 et pt2 va entraîner un croisement
    avec les points déjà existant"""
    for poly in liste:
        for i in range(0, len(poly), 1):
            pt_ref1 = poly[i]
            pt_ref2 = poly[(i+1)%len(poly)]
            if croise_segment(pt1, pt2, pt_ref1, pt_ref2):
                return True
    return False

def genere_poly_alea(nbr_point, liste_points_existant, abs_g_image, largeur_image, ord_b_image, hauteur_image):
    """génère un nouveau polygone de nbr_point points
    à partir de len(liste_extrem) polygones existant.
    liste_extrem contient les listes de coordonnées de chaque point de chaque polygone"""
    liste_points_existant.append([])
    pt = (abs_g_image + largeur_image*random.random(), ord_b_image + hauteur_image*random.random())
    liste_points_existant[-1].append(pt)
    nbr_pt_places = 1
    deb = time()
    res = True
    while nbr_pt_places < nbr_point:
        if time() - deb > 1:
            res = False
            break
        pt_nouv = (abs_g_image + largeur_image*random.random(), ord_b_image + hauteur_image*random.random())
        if len(liste_points_existant[-1]) == 1:#le deuxième point du polygone peut être placé sans faire attention à lui-même
            if not croise(pt, pt_nouv, liste_points_existant[:-1]):
                pt = pt_nouv
                nbr_pt_places +=1
                liste_points_existant[-1].append(pt)
        elif len(liste_points_existant[-1]) == nbr_point-1:#pour le dernier point, il faut aussi regarder le segment avec le premier point
            if not croise(pt, pt_nouv, liste_points_existant) and not croise(liste_points_existant[-1][0], pt_nouv, liste_points_existant):
                pt = pt_nouv
                nbr_pt_places +=1
                liste_points_existant[-1].append(pt)
        else:
            if not croise(pt, pt_nouv, liste_points_existant):
                pt = pt_nouv
                nbr_pt_places +=1
                liste_points_existant[-1].append(pt)
    if not res:
        liste_points_existant.pop()
    return None


def main():
    fichier = open(f"test/{argv[1]}/{nbr_polygones}_fichier_test.poly", 'w')
    liste_points = []
    while len(liste_points) < nbr_polygones:
        genere_poly_alea(random.randint(3, 8), liste_points, 0, 10, 0, 10)
    for i, poly in enumerate(liste_points):
        for j in range(0, len(poly), 1):
            fichier.write(f"{i} {poly[j][0]} {poly[j][1]}\n")
    fichier.close()


if __name__ == "__main__":
    if(len(argv) == 3):
        doss = "test/" + argv[1] + "/"
        if os.path.isdir(doss):
            debut = time()
            main()
            fin = time()
            print(fin-debut)
        else:
            print(f"Le dossier {argv[1]} n'existe pas dans le dossier test")
    else:
        print("Utilisation : ./generateur_poly.py nom_dossier_dans_/test nbr_poly")
