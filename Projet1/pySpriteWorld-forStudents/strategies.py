# -*- coding: utf-8 -*-

from Astar import *
import random


# -----------------------------------------------------------------------------------

def choisit_couleur_pref(fioles):
    """ Prend un dictionnaire de fiole en entrée et retourne un tuple avec les couleurs par ordre de préférance et 
    un dictionnaire avec la récompense associé à chaque fioles """
    color = ["r","j","b"]
    random.shuffle(color)
    return color

def FioleValue(color,fioles):
    dico = {}
    for f in fioles:
        if fioles[f] == color[0]:            
            dico[f] = 10
        elif fioles[f] == color[1]:
            dico[f] = 7
        else:
            dico[f] = 2
    return  dico

def Clustering(fioles,wallStates):
    """Prend une liste de fioles et retourne une liste des clusters"""
    LCluster = fioles[::]
    for f1 in LFioles:
        for f2 in LFioles:
            if f1 != f2:
                distance = len(Astar(f1,f2,wallStates, distance_Manhattan))
                if distance < 3:
                    LCluster[f1].append(f2)
                    LCluster[f2] = None;
    return LCluster

def evalue_fiole(color,fiole):
    if fiole == color[0]:            
        return 10
    elif fiole == color[1]:
        return 7
    else:
        return 2

def ClusterValue(color, fioles, Lcluster):
    "Ne marche pas car un dictionnaire ne peux contenir d'objet mutable"""
    dico = {}
    for cluster in Lcluster:
        #si c'est une fioles
        if len(cluster) == 1:
            dico[cluster] = "toto"
        
def construit_dico_proximite(fioles,wallStates):
    dico = dict()
    for f1 in fioles:
        distance = 0
        for f2 in fioles:
            if f1 != f2:
                distance += len(Astar(f1,f2,wallStates, distance_Manhattan))
        dico[f1] = distance
    return dico
# -------------------------------------------------------------------------------------
#                        ESPACE DEDIE AU STRATEGIE
#-------------------------------------------------------------------------------------

#remarque : les strategies retournes un tuple (row, col) correspondant au prochain coup a jouer

def strategie_bestValeurProche(color,fioles, positionJoueurs,numJoueur, wallStates):
    """ Chaque fiole a une valeur : valFiole - distFiole et on prend la fiole avec la plus grande valeur. Ainsi notre algo va prendre les fioles a poximité avant d'aller vers celle loin
-> DicoValFioles a comme clef les fioles et comme valeur la récompense associé a la fiole"""
    if fioles == {}:
        return positionJoueurs[numJoueur]
    dicoValFioles = FioleValue(color, fioles)
    dicoFiole = dict()
    maxVal = -1000000
    maxf = None
    for f in dicoValFioles:
        distance = len(Astar(positionJoueurs[numJoueur],f,wallStates,distance_Manhattan))
        dicoFiole[f] = dicoValFioles[f] - distance
        if dicoFiole[f] > maxVal and distance != 0:
            maxVal = dicoFiole[f]
            maxf = f
    chemin = Astar(positionJoueurs[numJoueur], maxf, wallStates, distance_Manhattan)
    if chemin == []:
        return positionJoueurs[numJoueur]
    return chemin[0]

def strategie_naive(color,fioles, positionJoueurs,numJoueur, wallStates):
    """ Strategie naive qui consiste a maximiser le nombre de fioles ramassés en allant chercher la fiole la plus proche de sa position"""
    maxd = 10000000
    maxf = None
    for f in fioles:
        distance = len(Astar(positionJoueurs[numJoueur], f, wallStates, distance_Manhattan))
        if distance < maxd:
            maxd = distance
            maxf = f
    chemin = Astar(positionJoueurs[numJoueur], maxf, wallStates, distance_Manhattan)
    #si le joueur est sur la fiole a ramasser
    if chemin == []:
        return positionJoueurs[numJoueur]
    return chemin[0]

def strategie_bestVal_proximite(color, fioles, positionJoueurs, numJoueur, wallStates,alpha=0.5,betta=1.5):
    """ Favorise les fioles proches et qui sont en groupes,
alpha est un parametre d'exploration compris entre 0 et 1"""
    dico_proximite = construit_dico_proximite(fioles,wallStates)
    dico_valeur_fiole = FioleValue(color, fioles)
    dicoFiole = dict()
    maxVal = -1000000
    maxf = None
    for f in dico_valeur_fiole:
        distance = len(Astar(positionJoueurs[numJoueur], f, wallStates, distance_Manhattan))
        dicoFiole[f] = betta*dico_valeur_fiole[f] - distance - alpha*dico_proximite[f]
        if dicoFiole[f] > maxVal and distance != 0:
            maxVal = dicoFiole[f]
            maxf = f
    chemin = Astar(positionJoueurs[numJoueur], maxf, wallStates, distance_Manhattan)
    if chemin == []:
        return positionJoueurs[numJoueur]
    return chemin[0]

def strategie_Cluser(color, fioles,positionJoueurs, numJoueur, wallStates):
    """ Prend en compte les cluster de taille 3 """
    dico_valeur_fiole = FioleValue(color, fioles)
    dicoFiole = dict()
    LCluster = Clustering(fioles, wallStates)
    maxVal = -1000000
    maxf = None

    

def strategie_bestValeurProche_possible(color,fioles, positionJoueurs, numJoueur, wallStates):
    """Variante de la strategie bestValeurProche qui tient compte de l'adversaire et ne vas pas chercher une
    fiole si l'adversaire est plus proche de cette fiole que lui
    rq : marche mal"""
    positionAdv = abs(1 - numJoueur)
    if fioles == {}:
        return positionJoueurs[numJoueur]
    dicoValFioles = FioleValue(color, fioles)
    dicoFiole = dict()
    maxVal_possible = -1000000
    maxf_possible = None
    maxVal_imp = -10000000
    maxf_imp = None
    for f in dicoValFioles:
        distance = len(Astar(positionJoueurs[numJoueur], f, wallStates, distance_Manhattan))
        distance_adv = len(Astar(positionAdv, f, wallStates, distance_Manhattan))
        dicoFiole[f] = dicoValFioles[f] - distance
        #si je suis plus proche de la fiole que mon adversaire
        if dicoFiole[f] > maxVal_possible and distance != 0 and (distance - distance_adv >= 0):
            maxVal_possible = dicoFiole[f]
            maxf_possible = f
        if dicoFiole[f] > maxVal_imp and distance != 0 and (distance- distance_adv < 0) and distance_adv <= 5:
            maxVal_imp = dicoFiole[f]
            maxf_imp = f
    if maxf_possible is not None:
        chemin = Astar(positionJoueurs[numJoueur], maxf_possible, wallStates, distance_Manhattan)
    else:
        chemin = Astar(positionJoueurs[numJoueur], maxf_imp, wallStates, distance_Manhattan)
    if chemin == []:
        return positionJoueurs[numJoueur]
    return chemin[0]

#------------------------------------------------------------------------------------
#                     STRATEGIE CONTRE
#------------------------------------------------------------------------------------

def chemin_bestValeur_Proche(color,fioles,joueur, wallStates):
    """ retourne le tuple avec la meilleur fiole et le chemin pour y aller"""
    if fioles == {}:
        return joueur
    dicoValFioles = FioleValue(color, fioles)
    dicoFiole = dict()
    maxVal = -1000000
    maxf = None
    for f in dicoValFioles:
        distance = len(Astar(joueur,f,wallStates,distance_Manhattan))
        dicoFiole[f] = dicoValFioles[f] - distance
        if dicoFiole[f] > maxVal and distance != 0:
            maxVal = dicoFiole[f]
            maxf = f
    chemin = Astar(joueur, maxf, wallStates, distance_Manhattan)
    if chemin == []:
        return joueur
    return (maxf,chemin)

def calcule_chemin(color, fioles, posJoueur, wallStates):
    """ retourne un chemin qui est [(fiole, distance)] avec la distance pour aller a la fiole depuis la derniere position"""
    s = []
    LFioles = fioles[::]
    while LFioles != {}:
        #Tant qu'il y a des fioles on prend la meilleur fiole possible
        f,c = chemin_bestValeur_Proche(color, LFioles, posJoueur,wallStates)
        posJoueur = f
        del LFioles[f]
        #si on a deja parcours une case
        distance_precedant = 0
        if s != []:
            precedant = s[-1]
            distance_precedant = precedant[1]
        s.append(f, len(c) + distance_precedant)
    return s

def dist_fiole(chemin, fiole):
    for etat in chemin:
        if etat[0] == fiole:
            return etat[1]
    print("erreur fiole non présente")


def construit_dico_gain(color,cheminJoueur,cheminAdv,fioles, dicoValFiole):
    """ Prend 2 chemin et retourne le dictionnaire de gain de mon joueur"""
    dico_gain = dict()
    for f in fioles:
        ma_dist = dist_fiole(cheminJoueur, f)
        adv_dist = dist_fiole(cheminAdv, f)
        if ma_dist - adv_dist >= 0:
            dico_gain[f] = dicoValFiole[f]
        else:
            dico_gain[f] = -1*dicoValFiole[f]
    return dico_gain

def somme_gain(dico_gain):
    somme = 0
    for f in dico_gain:
        somme += dico_gain[f]
    return somme

def permutation(fiole,positionChemin, cheminJoueur,wallStates):
    LFioles = []
    NouveauChemin = cheminJoueur[0:positionChemin]
    changementChemin = cheminJoueur[positionChemin:]
    for etat in changementChemin:
            LFioles.append(etat[0])
    derniere_case = NouveauChemin[-1]
    #on ajoute la case a permuté dans notre chemin
    NouveauChemin.append((fiole, len(Astar(derniere_case[0],fiole, wallStates, Distance_Manhattan))))
    Suite = calcule_chemin(color,LFioles, fiole, wallStates)
    #on concatene les chemins
    chemin = NouveauChemin + Suite
    return chemin

#changement etat ?
def strategie_Contre(color,fioles,positionJoueurs,numJoueur,wallStates):
    #initialisation de l'algorithme
    dico_valeur_fiole = FioleValue(color, fioles)
    supposition_color_adv = color[::]
    Jchemin = calcule_chemin(color, fioles,positionJoueurs[numJoueur],wallStates)
    ADVchemin = calcule_chemin(supposition_color_adv, fioles,positionJoueurs[abs(1 - numJoueur)], wallStates)
    dico_gain = construit_dico_gain(color,Jchemin, ADVchemin,fioles,dico_valeur_fiole)
    gain = somme_gain(dico_gain)
    curseur = None
    #pour les permutations utiles:
    for f in fioles:
        for positionChemin in range(len(Jchemin)):
            #distance de la position initial à  la fiole en passant par les positionChemin precedantes
            distance = (Jchemin[0:positionChemin])[1] + len(Astar(Jchemin[0],f,wallStates,Distance_Manhattan))
            #si on peux récupérer la fiole
            if distance < dist_fiole(ADVchemin,f):
                new = permutation(f,positionChemin,Jchemin,wallStates)
                new_dico_g = construit_dico_gain(color, Jchemin, ADVcheminn,fioles, dico_valeur_fiole)
                new_gain = somme_gain(new_dico_g)
                new_curseur = (f,positionChemin)

                #on verifie si cela améliore la recherche
                if new_gain > gain:
                    gain = new_gain
                    curseur = new_curseur

    #si il n'y a aucune amélioration
    if curseur == None:
        return Jchemin
    else:
        f,pos = curseur
        new_chemin = permutation(f,pos,Jchemin,wallStates)
        return new_chemin
