__author__ = "reza0310"
import os
import time
import pygame
import sys
from math import sqrt
import threading

def aff_total(*args):
    global blanc, map, mode, zoom, zioum
    effacer_texte()
    blanc = pygame.transform.scale(blanc, (1400, 1100))
    fenetre.blit(blanc, (0, 0))
    if args[0] == "menu":
        texte = "MODE JEU"
        text = font.render(texte, True, (0, 0, 0))
        fenetre.blit(text, (700, 275))
        texte = "MODE HISTOIRE"
        text = font.render(texte, True, (0, 0, 0))
        fenetre.blit(text, (700, 825))
        clique = False
        pygame.display.update()
        while not clique:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[1] < 550:
                        mode = "JEU"
                        map = "jeu"
                    else:
                        mode = "HISTOIRE"
                        map = "histoire (1)"
                    zoom = "petit"
                    zioum = False
                    return
                elif event.type == pygame.QUIT:
                    sys.exit()
    elif args[0] == "victoire":
        texte = "Le joueur {} a gagné!".format(args[1])
        text = font.render(texte, True, (0, 0, 0))
        fenetre.blit(text, (700, 275))

class entite():
    contenus = []

    def __init__(self, infos, extract_x, extract_y):
        x = extract_x.index(infos[0] + ", " + infos[1])
        y = extract_y - 1
        contenu = infos[1].split(".")
        if contenu[3] == "p":
            possi = True
        else:
            possi = False
        self.type = contenu[0][8:]
        self.x = int(x) + 1
        self.y = int(y) + 1
        self.num = contenu[1]
        self.proprio = contenu[2]
        self.est_possede = possi
        self.contenu = str(infos[1][8:])
        self.sol = chercher(int(x) + 1, int(y) + 1)["sol"]
        entite.contenus.append(self.contenu)
        fichier = open("textes{}soldats{}{}.txt".format(os.sep, os.sep, self.type), "r")
        ligne = fichier.readlines()
        fichier.close()
        ligne = ligne[1][4:]
        if ligne[-1] == "\n":
            ligne.replace("\n", "")
        self.pvs = int(ligne)
        self.image = images["joueur"]
        self.activer()
        return

    def bouger(self, **kwargs):
        texte = "Au tour du joueur " + possede.proprio
        aff(texte, 20, True)
        texte = "Nombre d'actions restantes: " + str(possede.actions - 1)
        aff(texte, 40, False)
        texte = "Nombre de pvs restants: " + str(possede.pvs)
        aff(texte, 60, False)
        texte = "Carte: " + map
        aff(texte, 1000, False)

        x = self.x
        y = self.y
        if kwargs['direction'] == "droite":
            x += 1
        elif kwargs['direction'] == "gauche":
            x -= 1
        if kwargs['direction'] == "bas":
            y += 1
        elif kwargs['direction'] == "haut":
            y -= 1
        cible = chercher(x, y)
        if cible["contenu"] == "rien":
            modif(x, y, cible["sol"], possede.contenu)
            modif(possede.x, possede.y, possede.sol, "rien")
            possede.sol = cible["sol"]
            possede.x = x
            possede.y = y
            enregistrer()
            file = open("textes{}sols{}{}.txt".format(os.sep, os.sep, possede.sol))
            file = file.readlines()
            ok = int(file[0].split(" ")[1])
            self.actionner(ok+1)

    def activer(self):
        file = open("textes{}soldats{}{}.txt".format(os.sep, os.sep, self.type), "r")
        stats = file.readlines()
        file.close()
        self.actions = int(stats[0][9:])

    def actionner(self, nombre):
        self.actions -= nombre
        if self.actions <= 0:
            entite.passation()

    def blesser(self, nombre):
        self.pvs -= nombre

    def animation(self, *args):
        print("lané")

        def animer(*args):
            arg = 0
            print(len(args))
            while arg <= len(args)-1:
                self.image = args[arg]
                arg += 1
                print("image changée")
                pygame.display.update()
                time.sleep(args[arg])
                arg += 1

        animation = threading.Thread(target=animer, args=args)
        animation.start()
        return

    @staticmethod
    def passation():
        global entites, possede
        for entitee in entites:
            if entitee.est_possede:
                index = entites.index(entitee)
                entitee.est_possede = False
                if index == len(entites)-1:
                    index = 0
                else:
                    index += 1
                print(index)
                entites[index].est_possede = True
                print(entites, possede)
                entites[index].activer()
                possede = entite.qui_est_possede(entites)
                return

    @staticmethod
    def qui_est_possede(entites):
        for entitee in entites:
            if entitee.est_possede:
                return entitee

    @staticmethod
    def qui_est_la(entites, x, y):
        for entitee in entites:
            if entitee.x == x and entitee.y == y:
                return entitee

def afficher():
    if zoom == "grand":
        affichage_grand()
    else:
        affichage_petit()

def effacer_texte():
    fenetre.blit(blanc, (1100, 0))
    return

def aff(texte, y, effacer):
    global font
    if effacer:
        effacer_texte()
    x = 1120
    text = font.render(texte, True, (0, 0, 0))
    fenetre.blit(text, (x, y))

def click(pos):
    if pos[0] <= 1100:
        if zoom == "petit":
            case_x = int(pos[0] / 100)
            case_y = int(pos[1] / 100)
            case = chercher(possede.x+(case_x-4), possede.y+(case_y-4))
        else:
            case_x = int(pos[0] / 11)+1
            case_y = int(pos[1] / 11)+1
            case = chercher(case_x, case_y)

        with open("textes{}sols{}{}.txt".format(os.sep, os.sep, case['sol']), encoding="utf-8") as fichier_sol:
            texte = fichier_sol.readlines()
        aff("SOL:", 10, True)
        aff("Nom: {}".format(case['sol']), 40, False)
        aff("Apparence:", 60, False)
        aff("Modifications:", 80, False)
        l = 110
        for ligne in texte:
            if ligne[-1] == "\n":
                ligne = ligne[:-1]
            ligne = "|     -" + ligne
            aff(ligne, l, False)
            l += 20
        if case["sol"] != "evenement":
            if not case['contenu'] in entite.contenus:
                with open("textes{}contenus{}{}.txt".format(os.sep, os.sep, case['contenu']), encoding="utf-8") as fichier_sol:
                    texte = fichier_sol.readlines()
                aff("Contenu:", 560, False)
                aff("Nom: {}".format(case['contenu']), 590, False)
                aff("Apparence:", 610, False)
                aff("Modifications:", 630, False)
                l = 650
                for ligne in texte:
                    if ligne[-1] == "\n":
                        ligne = ligne[:-1]
                    ligne = "|     -" + ligne
                    aff(ligne, l, False)
                    l += 20
            else:
                print(case_x, case_y, possede.x, possede.y)
                mob = entite.qui_est_la(entites, case_x-4+possede.x, case_y-4+possede.y)
                texte = "Appartient à " + mob.proprio
                aff(texte, 650, False)
                texte = "A encore " + str(mob.actions - 1) + " actions."
                aff(texte, 670, False)
                texte = "A encore " + str(mob.pvs) + " pvs."
                aff(texte, 690, False)

        else:
            texte = case["contenu"]
            texte = texte.split("/")
            effacer_texte()
            l = 20
            for ligne in texte:
                if ligne[-1] == "\n":
                    ligne = ligne[:-1]
                aff(ligne, l, False)
                l += 20
        return

def affichage_petit():
    numlig = possede.y - 4
    numcas_min = possede.x - 4
    numlig_max = possede.y + 7
    numcas_max = possede.x + 7
    while numlig < numlig_max:
        for numcas in range(numcas_min, numcas_max):
            dicocase = chercher(numcas, numlig)
            sol = images[dicocase["sol"]]
            debut_y = (numlig - (possede.y - 5)) * 100 - 100
            debut_x = (numcas - (possede.x - 5)) * 100 - 100
            fenetre.blit(sol, (debut_x, debut_y))
            if dicocase["contenu"] in entite.contenus:
                image = entite.qui_est_la(entites, numcas, numlig).image
                fenetre.blit(image, (debut_x, debut_y))
        numlig += 1

def affichage_grand():
    global zoom, zioum
    if not zioum:
        debut = time.time()
        numlig = 1
        numcas_min = 1
        numcas_max = 101
        while numlig != 101:
            for numcas in range(numcas_min, numcas_max):
                dicocase = chercher(numcas, numlig)
                sol = images[dicocase["sol"]]
                sol = pygame.transform.scale(sol, (11, 11))
                debut_y = (numlig * 11)-11
                debut_x = (numcas * 11)-11
                fenetre.blit(sol, (debut_x, debut_y))
            numlig += 1
        #Chercher perso contrôlé
        vous = images["vous"]
        fenetre.blit(vous, (possede.x*11-11, possede.y*11-11))
        fin = time.time()
        aff("Dezoomé en environ {} secondes.".format(int(fin-debut)), 10, True)
        zioum = True
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            zioum = False
            zoom = "petit"
            return
    else:
        vous = images["vous"]
        fenetre.blit(vous, (possede.x * 11 - 11, possede.y * 11 - 11))

def chercher(case, ligne):
    try:
        if ligne >= 1 and case >= 1:
            ligne = fichier[ligne - 1]
            ligne = ligne.split(";")
            case = ligne[case - 1]
            case = case.split(", ")
            sol = case[0].split(":")
            sol = sol[1]
            contenu = case[1].split(":")
            contenu = contenu[1]
            try:
                contenu = contenu.replace("\n", "")
            except:
                print("bien")
            return {"sol": sol, "contenu": contenu}
        else:
            return {"sol":"noir","contenu":"noir"}
    except:
        return {"sol": "noir", "contenu": "noir"}

def modif(case, ligne, sol, contenu):
    num = ligne
    ligne = fichier[ligne - 1]
    ligne = ligne.replace("\n", "")
    ligne = ligne.split(";")
    ligne[case - 1] = "sol:"+sol+", contenu:"+contenu
    l = ""
    for element in ligne:
        l += element + ";"
    l = l[:len(l)-1]
    l += "\n"
    fichier[num-1] = l

def init_anomalies(arg):
    global fichier, pvs
    try:
        fichier = open("textes{}maps{}{}.csv".format(os.sep, os.sep, map), "r", encoding="UTF-8")
        fichier = fichier.readlines()
    except:
        fichier = open("textes{}maps{}{}.csv".format(os.sep, os.sep, map), "r")
        fichier = fichier.readlines()
    n = 0
    with open("textes{}elements.txt".format(os.sep), "r") as f:
        contenus = []
        choses = f.readlines()
        for chose in choses:
            if chose[-1] == "\n":
                chose = chose[:-1]
            contenus.append("contenu:{}".format(chose))
            contenus.append("contenu:{}\n".format(chose))
    for ligne in fichier:
        n += 1
        ligne = ligne.split(";")
        for case in ligne:
            case = case.split(", ")
            if case[1] not in contenus:
                if len(case[1].split(".")) == 4:
                    entites.append(entite(case, ligne, n))
    if arg == "mort":
        for pv in pvs:
            if int(pv) <= 0:
                num = pvs.index(pv)+1
                for perso in entites:
                    if perso["num_soldat"] == num:
                        modif(perso["x"], perso["y"], perso["sol"], "rien")
                        entites.pop(perso)
                        enregistrer()
    elif str(type(arg)) == "<class 'int'>":
        player = int(possede.proprio)
        print("check", arg, player)
        if player == arg:
            texte = "Le joueur " + str(player) + " a gagné!!!"
            aff(texte, 50, True)

def enregistrer():
    with open("textes{}maps{}{}.csv".format(os.sep, os.sep, map), "w") as modification:
        f = ""
        for element in fichier:
            f += element
        modification.write(f)
    return

def attaquer(possede, x, y):
    xd = possede.x
    yd = possede.y
    if xd >= x:
        terme1 = xd-x
    else:
        terme1 = x-xd
    if yd >= y:
        terme2 = yd-y
    else:
        terme2 = y-yd
    somme = (terme1**2) + (terme2**2)
    distance = int(sqrt(somme))
    print("Attaque a",distance,"cases")
    fichier = open("textes{}soldats{}{}.txt".format(os.sep, os.sep, possede.type), "r")
    ligne = fichier.readlines()
    fichier.close()
    ligne = ligne[2]
    portee = int(ligne[8:])
    if distance <= portee: #Si à portée
        case = chercher(x, y)
        case = case["contenu"]
        case = case.split(".")
        if len(case) == 4: #Si c'est un joueur
            entite.qui_est_la(entites, x, y).blesser(1)
            print("Touché")
            possede.actionner(3)
    else:
        print("Cible trop éloignée")
    return

pygame.init() # Initialisation de pygame
fenetre = pygame.display.set_mode((1400, 1100)) #Création de la fenêtre
pygame.display.set_caption("Afficheur") #Renommage de la fenêtre

crashed = False #Mise en place de quelque booléennes
fin = False

images = {} #Préchargement des images
dossier_images = os.listdir("images")
print("Images:",dossier_images)
for image in dossier_images:
    img = pygame.image.load('images{}{}'.format(os.sep, image))
    images[image[:-4]] = img

blanc = images["blanc"] #Définition des bases de l'affichage (fond et police)
font = pygame.font.SysFont("arial", 20)

aff_total("menu") #Menu de mode

entites = []
joueurs = ["joueur 1", "joueur 2"]

init_anomalies("rien")
possede = entite.qui_est_possede(entites)
possede.activer()

blanc = pygame.transform.scale(blanc, (300, 1100))
print("possede:", possede)
texte = "Au tour du joueur " + possede.proprio
aff(texte, 20, True)
texte = "Nombre d'actions restantes: " + str(possede.actions - 1)
aff(texte, 40, False)
texte = "Nombre de pvs restants: " + str(possede.pvs)
aff(texte, 60, False)
texte = "Carte: " + map
aff(texte, 1000, False)

clock = pygame.time.Clock()
fenetre.blit(blanc, (1100, 0))

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            enregistrer()
            crashed = True
            fin = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                possede.bouger(direction="gauche")
            elif event.key == pygame.K_RIGHT:
                possede.bouger(direction="droite")
            elif event.key == pygame.K_UP:
                possede.bouger(direction="haut")
            elif event.key == pygame.K_DOWN:
                possede.bouger(direction="bas")
            elif event.key == 119: #touche z pour zoomer
                zioum = False
                if zoom == "petit":
                    zoom = "grand"
                else:
                    zoom = "petit"
            elif event.key == 113: #touche a pour attaquer
                pos = pygame.mouse.get_pos()
                if pos[0] <= 1100:
                    if zoom == "petit":
                        case_x = int(pos[0] / 100) + (possede.x-4)
                        case_y = int(pos[1] / 100) + (possede.y-4)
                    else:
                        case_x = int(pos[0] / 11) + 1
                        case_y = int(pos[1] / 11) + 1
                attaquer(possede, case_x, case_y)
            elif event.key == 116: #touche t pour terminer son tour / passer à la map suivante
                if mode == "JEU":
                    possede.actionner(100000)
                else:
                    anci_map = map
                    anci_map = anci_map.split(" ")
                    numero = int(anci_map[1].replace("(", "").replace(")", ""))+1
                    map = "histoire ({})".format(numero)
                    print(map)
                    init_anomalies(False)
                    enregistrer()
            elif event.key == 114: #touche r pour retourner à la map précédente
                if mode == "HISTOIRE":
                    anci_map = map
                    anci_map = anci_map.split(" ")
                    numero = int(anci_map[1].replace("(", "").replace(")", ""))-1
                    if numero > 0:
                        map = "histoire ({})".format(numero)
                    else:
                        map = "histoire (1)"
                    print(map)
                    init_anomalies(False)
                    enregistrer()
            elif event.key == 101: #touche e
                possede.animation(images["joueur"], 1, images["editeur"], 1, images["joueur"], 1)
            else:
                print(event.key)

        elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                click(pos)

    if mode == "JEU":
        for joueur in joueurs:
            vie = 0
            num = 0
            for entitee in entites:
                if entitee.proprio == joueur[7:] and entitee.pvs > 0:
                    vie += 1
                num += 1
            if vie == 0 and num == len(entites):
                joueurs.remove(joueur)
                crashed = True
                joueure = joueurs[0]
    else:
        fin = True

    afficher()
    pygame.display.update()
    clock.tick(60)

if not fin:
    aff_total("victoire", joueure)
    pygame.display.update()
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True

pygame.quit()
quit()