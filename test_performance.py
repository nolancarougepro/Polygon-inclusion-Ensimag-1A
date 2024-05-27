#!/usr/bin/env python3

from time import time
from tycat import read_instance
from main import trouve_inclusions_v1, trouve_inclusions_v2, trouve_inclusions_v3
import sys

def test_all_file():
    """Test tous les fichiers avec les trois versions"""
    for j in range(1,11,1):
        print("Dossier : ", j, "-------------------------------------------")
        for i in range(25,501,25):
            print("Nombre de polygones : ", i)
            fichier_a_test = f"test/{j}/{i}_fichier_test.poly"

            polygones = read_instance(fichier_a_test)

            deb = time()
            inclusions_v1 = trouve_inclusions_v1(polygones)
            fin = time()
            print("Version 1 : ", fin-deb)

            
            deb = time()
            inclusions_v2 = trouve_inclusions_v2(polygones)
            fin = time()
            print("Version 2 : ", fin-deb)

            deb = time()
            inclusions_v3 = trouve_inclusions_v3(fichier_a_test)
            fin = time()
            print("Version 3 : ", fin-deb)

            if(inclusions_v1 == inclusions_v2 == inclusions_v3):
                pass
            else:
                print("Erreur pour le test all")

def test_file(version):
    """Test tous les fichiers avec une version"""
    for j in range(1,11,1):
        print(j, "-------------------------------------------")
        for i in range(25,501,25):
            fichier_a_test = f"test/{j}/{i}_fichier_test.poly"

            polygones = read_instance(fichier_a_test)

            deb = time()
            if(version == "v1"):
                inclusions_v1 = trouve_inclusions_v1(polygones)
            elif(version == "v2"):
                inclusions_v2 = trouve_inclusions_v2(polygones)
            elif(version == "v3"):
                inclusions_v3 = trouve_inclusions_v3(fichier_a_test)
            fin = time()

            print(fin-deb)


def test_special():
    """Test le fichier special"""
    fichier_a_test = "test/special.poly"
    polygones = read_instance(fichier_a_test)

    deb = time()
    inclusions_v1 = trouve_inclusions_v1(polygones)
    fin = time()
    print(f"Temps pour special polygones avec la version 1: {fin-deb}")

    deb = time()
    inclusions_v2 = trouve_inclusions_v2(polygones)
    fin = time()
    print(f"Temps pour special polygones avec la version 2: {fin-deb}")

    deb = time()
    inclusions_v3 = trouve_inclusions_v3(fichier_a_test)
    fin = time()
    print(f"Temps pour special polygones avec la version 3: {fin-deb}")

    if(inclusions_v1 == inclusions_v2 == inclusions_v3):
        pass
    else:
        print("Erreur pour le test special")

def main():
    if(len(sys.argv) != 2):
        print("Utilisation : ./test_bis.py v1/v2/v3/special/all")
    else:
        if(sys.argv[1] == "v1" or sys.argv[1] == "v2" or sys.argv[1] == "v3"):
            test_file(sys.argv[1])

        elif(sys.argv[1] == "special"):
            test_special()

        elif(sys.argv[1] == "all"):
            test_all_file()
            test_special()

        else:
            print("Utilisation : ./test_bis.py v1/v2/v3")

if __name__ == "__main__":
    main()