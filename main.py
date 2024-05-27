#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
import sys
import random
import traite_fichier
import os
from tycat import read_instance

def droite_croise(point_incl, point_1, point_2):
    #Fonction qui determine si la drotie formé par les deux points est au dessus
    #du points de référence. Retourne 1 si c'est le cas 0 sinon.

    res = 0
    x_a,y_a = point_1
    x_b,y_b = point_2
    x_ref,y_ref = point_incl

    coeff_dir = (y_b - y_a)/(x_b - x_a)
    calcule_y_droite = coeff_dir * x_ref + y_a - x_a * coeff_dir

    if y_ref > calcule_y_droite:
        res = 1 

    return res

def liste_abs_max(polygones):
    #Fonction qui ordonne les polygones selon la valeur de l'abscisse maximale de chaque polygone
    abs_max=[]
    num_poly = 0
    for poly in polygones:
        liste_abs = [(poly.points[k].coordinates)[0] for k in range (len(poly.points))]
        liste_ord = [(poly.points[k].coordinates)[1] for k in range (len(poly.points))]
        abs_max.append((max(liste_abs), min(liste_abs), max(liste_ord), min(liste_ord), poly, num_poly))
        num_poly += 1
    abs_max.sort()
    return abs_max

def determine_croise(point_incl, point_1, point_2):
    #Fonction qui détermine si un point de référence est en dessous de la droite formée
    #par deux points. Retourne 1 si c'est le cas 0 sinon.

    compteur = 0
    point_incl_x = point_incl[0]
    point_1_x = point_1[0]
    point_2_x = point_2[0]

    if (point_1_x <= point_incl_x <= point_2_x) or (point_1_x >= point_incl_x >= point_2_x):
        compteur = droite_croise(point_incl, point_1, point_2)
    
    return compteur

def trouve_plus_petit(tab):
    #Entrée : un tableau de tableau de polygone. Et retourne 
    #le tableau avec les plus petits polygones inclus.
    tab_ret = [None] * len(tab)
    for i in range(len(tab)):
        if len(tab[i]) == 1:
            tab_ret[i] = tab[i][0]
        elif tab[i] == []:
            tab_ret[i] = -1
        else:
            max_taille = -1
            indice = None
            for j in range(len(tab[i])):
                if max_taille < len(tab[tab[i][j]]):
                    max_taille = len(tab[tab[i][j]])
                    indice = tab[i][j]
                    tab_ret[i] = indice
    return tab_ret

def prends_points_suivants(polygones, x_ref):
    #Trouve les points avec une abscisse différente
    #Permettant de gérer les cas des points alignés

    i = 1
    while polygones.points[i].coordinates[0] == x_ref:
        i += 1

    x, y = polygones.points[i].coordinates
    x_prec, y_prec = polygones.points[i-1].coordinates
    return (x, y), (x_prec, y_prec)

def trouve_inclusions_v1(polygones):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    tab = [0] * len(polygones)  # Initialisation du vecteur d'inclusions avec des -1
    for i, poly_ref in enumerate(polygones):

        x_dep, _ = poly_ref.points[0].coordinates #Point de reférence
        (x_2, y_2), (x_1, y_1) = prends_points_suivants(poly_ref, x_dep)
        x_ref = random.uniform(x_1,x_2)
        coeff_dir = (y_2 - y_1)/(x_2 - x_1)
        y_ref = coeff_dir * x_ref + y_1 - x_1 * coeff_dir

        liste_poly_incl = []

        for j, poly_a_test in enumerate(polygones):
            if i != j:  # Ne pas comparer un polygone avec lui-même
                compteur = 0
                for k in range(len(poly_a_test.points)):        
                    valeur_croise = determine_croise([x_ref, y_ref], poly_a_test.points[k].coordinates,poly_a_test.points[(k + 1)%len(poly_a_test.points)].coordinates)
                    compteur += valeur_croise
                if compteur % 2 != 0:
                    liste_poly_incl.append(j)  # Le polygone i est inclus dans le polygone j
        tab[i] = liste_poly_incl

    tab = trouve_plus_petit(tab)

    return tab

def trouve_inclusions_v2(polygones):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    tab = [-1] * len(polygones)  # Initialisation du vecteur d'inclusions avec des -1
    abs_max = liste_abs_max(polygones)
    for i in range(0, len(abs_max)-1, 1):
        (_, abmin_ref, ordmax_ref, ordmin_ref, poly_ref, num_poly_ref) = abs_max[i]
        x_dep, _ = poly_ref.points[0].coordinates #Point de reférence
        (x_2, y_2), (x_1, y_1) = prends_points_suivants(poly_ref, x_dep)
        x_ref = random.uniform(x_1,x_2)
        coeff_dir = (y_2 - y_1)/(x_2 - x_1)
        y_ref = coeff_dir * x_ref + y_1 - x_1 * coeff_dir

        poly_incl = -1

        for j in range(i+1, len(abs_max), 1):
            (_, abmin_test, ordmax_test, ordmin_test, poly_a_test, num_poly_a_test) = abs_max[j]
            if abmin_test < abmin_ref and ordmax_test > ordmax_ref and ordmin_test < ordmin_ref:
                compteur = 0
                for k in range(0,len(poly_a_test.points),1):
                    valeur_croise = determine_croise([x_ref, y_ref], poly_a_test.points[k].coordinates,poly_a_test.points[(k + 1)%len(poly_a_test.points)].coordinates)
                    compteur += valeur_croise
                if compteur % 2 != 0:
                    poly_incl = num_poly_a_test  # Le polygone ref est inclus dans le polygone test
                    break
        tab[num_poly_ref] = poly_incl

    return tab

def trouve_inclusions_v3(file):
    """Traite le fichier puis execute v2"""
    traite_fichier.traite_fichier(file)
    polygones = read_instance("_tmp")
    tab = trouve_inclusions_v2(polygones)
    os.remove("_tmp")
    return tab

def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """

    if(sys.argv[1]) == "v1":
        for fichier in sys.argv[2:]:
            polygones = read_instance(fichier)
            inclusions = trouve_inclusions_v1(polygones)
            print(inclusions)
    elif(sys.argv[1]) == "v2":
        for fichier in sys.argv[2:]:
            polygones = read_instance(fichier)
            inclusions = trouve_inclusions_v2(polygones)
            print(inclusions)
    elif(sys.argv[1]) == "v3":
        for fichier in sys.argv[2:]:
            inclusions = trouve_inclusions_v3(fichier)
            print(inclusions)
    else:
        print("Utilisation : ./main.py v1/v2/v3 fichiers")




if __name__ == "__main__":
    if(len(sys.argv) >= 2):
        main()
    else:
        print("Utilisation : v1/v2/v3 fichiers")
