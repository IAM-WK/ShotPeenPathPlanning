# linearAlg.py

import numpy as np
import sympy

#from sympy.abc import t, u # für intersectionLineLine_parameter
from sympy import Symbol # für intersectionLineLine_parameter

from obstacle_class import *

# funktion
def getGerade_twoPoints(point1, point2):
    # return gerade = [[coord_aufpunkt],[richtungsvektor]]
    gerade = []
    gerade.append(point1)
    gerade.append(np.subtract(point2, point1))
    #print("erstellte gerade aus zwei punkten: ", gerade)
    return gerade


def intersectionLineLine_parameter(line1, line2):
    # return geradedn parameeter
    # line_i = [[aufpunkt],[richtungsvektor]]
    #print("\n line1 = ", line1)
    #print(" line2", line2)
    # komponenten einzeln extrahieren in gleichungen 
    eqSys = []
    # ergebnisse liste
    #parameter = []
    t = Symbol('t')
    u = Symbol('u')
    
    #sol = sympy.solve(np.subtract(eq_list[0], np.multiply(eq_list[1], t)), t, dict = True) # sub or ad


    #if(len(sol) == 1): # wenn eine lösung
    #    sol_t = sol[0][t]
    #    obstacle_info = Obstacle_Info(False, sol_t)

    for i in range(3): # 3, da 3D
        eqSys.append(line1[0][i] + t*line1[1][i] - line2[0][i] - u*line2[1][i])
    #print(eqSys)
    t1_t2 = sympy.solve(eqSys, t, u, dict = True)
    list_t1_t2 = []
    
    #print("A: t1_t2 = ", t1_t2)
    if(len(t1_t2) != 0):
        #t1_t2_list = 
        #if(len(t1_t2[0]) == 1): # geraden identisch, unendlich viele SP
        if(len(t1_t2) == 1): # geraden identisch, unendlich viele SP
            lineIntersection_Info = LineIntersection_Info(True, None)
            #parameter.append()
        #elif(len(t1_t2[0] == 2)): # ein SP
        elif(len(t1_t2 == 2)): # ein SP
            lineIntersection_Info = LineIntersection_Info(False, t1_t2[0][t])
            #parameter.append(t1_t2[0][t])
            #parameter.append(t1_t2[0][u])

    else: # kein ergebnis / schnitt, kein SP
        lineIntersection_Info = LineIntersection_Info(False, None)
    #print(parameter)

    return lineIntersection_Info

def calcVerbindungNorm(point1, point2):
    # point i vektor
    erg = np.subtract(point2, point1)/np.linalg.norm(np.subtract(point2, point1))
    return erg

# Werte die fast null (entsprechend zulaessigem error, gleich null setzen)
def nullRundungsfehlerAufnull_vektor(vektor, errZulaessig):
    vektorNew = []
    for i in range(len(vektor)):
        if(np.abs(vektor[i]) <= errZulaessig):
            vektorNew.append(0.0)
        else:
            vektorNew.append(vektor[i])
    return vektorNew

def nullRundungsfehlerAufnull_ListVektoren(List_vektoren, errZulaessig):
    List_vektorNew = []
    for j in range(len(List_vektoren)):    
        List_vektorNew.append([])
        List_vektorNew[j].append(nullRundungsfehlerAufnull_vektor(List_vektoren[j], errZulaessig))
    return List_vektorNew
    
#winkel zwischen zwei vektoren berechnen
def calcAngleVectors(vec1, vec2):
    dotProd = np.dot(vec1, vec2)
    angle = np.arccos(dotProd/np.sqrt(np.dot(vec1, vec1))*np.sqrt(np.dot(vec2, vec2)))
    
    return angle




