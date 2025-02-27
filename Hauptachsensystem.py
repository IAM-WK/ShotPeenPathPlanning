# Hauptachsensystem.py
# Berechnung des HAS aus der STL Geometrie

import numpy as np
import trimesh
import copy
import sympy
from stl import mesh

"""
import func_einspannung_new

"""
import koordinatentrafo
import data_structure
import linearAlg


from sympy import Symbol # fuer alNormalShar


    
def get_index_list_element(x, liste):
    #### Funktion: index des elements x aus liste liste finden
    #### 
    index_liste = None

    for i in range(len(liste)):
        if(liste[i] == x):
            index_liste = i
            break
    return index_liste
        

# global var
theta_mainAxis_krit = np.pi/4 # kritischer winkel um später facets zusammenzufassen in mainAxis richtung

theta_n_krit = np.pi/60 #np.pi/4 # 45 deg, winkelabweichung bis zu dem facets noch alsa ein patch 
# tehta_n_krit kritscher wert der winkelabweichung zweier normalenvektoren zweier facets, 
# zum initialen zusammenfassen mehrerer benachbarter facets zu einem patch/surface

tol = 1e-06 # toleranz

def norm_vec(vec): 
    #Funktion:  Vektor vec, der dim n, normieren
    #Parameter: Vektor vec, der zu normieren
    #return:    normierter Vektor, als np.array
    for i in range(len(vec)-1):
        if(vec[i] != vec[i+1]):
            betrag_vec = np.sqrt(np.dot(vec, vec))
            norm_vec = np.multiply(vec, (1/betrag_vec))
            return norm_vec
    if(vec[0] == 0): #wenn vec = Nullvektor, dim n
        vec = np.array(vec)
        return vec  


def eq_linabh(lh_0, lh_1, rh_0, rh_1):
    #### Funktion: prüfen, ob zwei Glgen linear abh.
    # Parameter: lh_i: linke seite der eq, in Form, z.B. lh_0 = [1, 2] == 1*x_1+ 2*x_2, 2d liste
    #            rh_i: rechte seite der eq, in Form , z.B. rh_0 = 3, skalar
    #return:     True (sind lin. abh.), bzw. False (sind nicht lin. abh.)
    if (norm_vec(lh_0)[0] == norm_vec(lh_1)[0] and norm_vec(lh_0)[1] == norm_vec(lh_1)[1] and rh_0/np.linalg.norm(lh_0) == rh_1/np.linalg.norm(lh_1) ):
        #dann lh[0] = rh[0] und lh[1] = rh[1] linear abh.e glg.en
        return True
    else:
        return False


# Funktion: main achsen finden, 2D, nur ein freiheitsgrad bei suche ;/
# 
def mainAxis2D(alpha, trimesh_geometry): 
    #### !!! !!!! theoretish müsste ich noch 2. schleife einfügen für eine rotation um eine 2. koord achse, damit in 3d bestmögl gefunden werden kann!
    # --> neue funktion mainAxis3D 
    # alpha: inkrementeller winkel in rad , um den ahsen gedreht werden um bestmöglihe ausrihtung zu finden
    
    # Liste M erstellen: 
    # M: Maß, um zu ermittteln, welhe Ahsen ausrihtung am besten zu geometrie passt
    M = []
    # Liste Axis erstellen:
    Axis = []
    # Ahsen festlegen, zunähst als default ahsen
    Axis.append([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    
    j = 0 # Zähler while shleife
    alpha_sum = 0
    while (alpha_sum < np.pi): 
        M.append(0.0) # neuen j.ten Wert in M shreiben, 
        if(j != 0): # Ahsen umrehnen, d.h. um alpha drehen
            # rotated Axis berehnen
            # rotation der ahsen um z achse (bleibt konstant, um alpha)
            Axis.append(koordinatentrafo.koordinatentrafo_rotation_coordAxis_points(Axis[j-1], alpha, "y"))
            
            for i in range(len(trimesh_geometry.facets)): # für alle faets des trimeshs
                # A: betrag der projektionen des normalen vektors des i ten faets auf die Koordinatenahse
                A = [np.absolute(np.dot(trimesh_geometry.facets_normal[i], Axis[j][0])), np.absolute(np.dot(trimesh_geometry.facets_normal[i], Axis[j][1])), np.absolute(np.dot(trimesh_geometry.facets_normal[i], Axis[j][2]))]
                # ermitteln, auf welhe ahse projektion am größten
                a = np.max(A)
                # gefundenes max (gewihtet) mit flähe des faets multiplizieren, zu M hinzuaddieren
                M[j] = M[j] + a*trimesh_geometry.facets_area[i]
        j = j+1
        alpha_sum = alpha_sum + alpha

    # index des elements aus M auslesen, welches maximalen wert aufweist
    max_M = np.max(M)
    index_max_M = get_index_list_element(max_M, M)
    # entsprechende achsen auslesen

    main_axis = Axis[index_max_M]

    return main_axis


# Funktion: berechnet alle achsen bei rotation von kos um z achse, retrunt alle möglichen achsen als liste
# 
def listAxis2D(alpha): 
    #### !!! !!!! theoretish müsste ich noch 2. schleife einfügen für eine rotation um eine 2. koord achse, damit in 3d bestmögl gefunden werden kann!
    # --> neue funktion mainAxis3D 
    # alpha: inkrementeller winkel in rad , um den ahsen gedreht werden um bestmöglihe ausrihtung zu finden
    
    # Liste M erstellen: 
    # M: Maß, um zu ermittteln, welhe Ahsen ausrihtung am besten zu geometrie passt
    #M = []
    # Liste Axis erstellen:
    Axis = []
    # Ahsen festlegen, zunähst als default ahsen
    Axis.append([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    
    j = 0 # Zähler while shleife
    alpha_sum = 0
    while (alpha_sum < np.pi): 
        #M.append(0.0) # neuen j.ten Wert in M shreiben, 
        if(j != 0): # Ahsen umrehnen, d.h. um alpha drehen
            # rotated Axis berehnen
            # rotation der ahsen um z achse (bleibt konstant, um alpha)
            Axis.append(koordinatentrafo.koordinatentrafo_rotation_coordAxis_points(Axis[j-1], alpha, "z"))
            
        j = j+1
        alpha_sum = alpha_sum + alpha

    return Axis


# Funktion: ausgehend von funktion listaxis2d
# 
def mainAxis3D(alpha, trimesh_geometry): # trimesh_geometry als arg hinzugefügt, evtl hier nicht mehr passende aufrufe in datei

    #### bisschen ineffizient 

    # --> neue funktion mainAxis3D 
    # alpha: inkrementeller winkel in rad , um den ahsen gedreht werden um bestmöglihe ausrihtung zu finden
    
    # Liste Axis erstellen:
    Axis2D = listAxis2D(alpha) # Axis2D enthält alle möglichkeiten an rotierter Achsen um z Achse

    # liste anlegen für alle möglichen KOS/achsen, durch zusätzliche rot um y achse
    Axis = []
    alpha_sum_y = 0.0
    j = 0
    for i in range(len(Axis2D)): 
        Axis.append(Axis2D[i]) # axis 2d um null rotiert um y appenden
        
        while(alpha_sum_y < np.pi):
            j = j+1
            # rotated Axis berehnen
            # rotation der ahsen um z achse (bleibt konstant, um alpha)
            Axis.append(koordinatentrafo.koordinatentrafo_rotation_coordAxis_points(Axis[j-1], alpha, "y"))
            #print("\n j = ", j)
            alpha_sum_y = alpha_sum_y + alpha # gesamtwinkel um den bereits gedreht berechnen
            
    #print("\n Axis: ", Axis)
    
    # Liste M erstellen: 
    # M: Maß, um zu ermittteln, welhe Ahsen ausrihtung am besten zu geometrie passt
    M = []

    for k in range(len(Axis)):
        M.append(0.0) # k ten eintrag von M anlegen
        for i in range(len(trimesh_geometry.facets)): # für alle faets des trimeshs
                # A: betrag der projektionen des normalen vektors des i ten faets auf die Koordinatenahse
                A = [np.absolute(np.dot(trimesh_geometry.facets_normal[i], Axis[k][0])), np.absolute(np.dot(trimesh_geometry.facets_normal[i], Axis[k][1])), np.absolute(np.dot(trimesh_geometry.facets_normal[i], Axis[k][2]))]
                # ermitteln, auf welhe ahse projektion am größten
                a = np.max(A)
                # gefundenes max (gewihtet) mit flähe des faets multiplizieren, zu M hinzuaddieren
                M[k] = M[k] + a*trimesh_geometry.facets_area[i]

    # index des elements aus M auslesen, welches maximalen wert aufweist
    max_M = np.max(M)
    index_max_M = get_index_list_element(max_M, M)
    # entsprechende achsen auslesen

    main_axis = Axis[index_max_M]

    return main_axis


# Funktion: die aus 3 Achsen, welche ein RHS bilden, 
#           die entspprechenden neg achsen berechenn und somit liste von 6 achsen ausgibt, 
#           und alle Achsen vektoren normiert
def getMainAxis6(mainAxis3):
    # mainAxes3 = liste der 3 main achsen

    # liste für 6 achsen
    Axis = []

    for i in range(len(mainAxis3)):
        Axis.append(mainAxis3[i])
        neg_axis_temp = np.multiply(mainAxis3[i], -1)
        Axis.append(neg_axis_temp)
    
    return Axis



# Funktion:
# Eingabe: sortiert nach triangle_index liste aller normalanvektoren zu den triangles
# Ausgabe: index der...
#           case 1: erst besten Zelle, welche, in eine HAS weist
#           case 2: erst beste Zelle, dessen normale/Ausrichtung am nähchsten an einer HAS richtung liegt
# für wahl des ersten triangles zur patchbildung
def getIndexTriangleMainAxis(mainAxis6, list_triangles_normals):
    #
    for i in range(len(mainAxis6)): # len = 6 
        # prüfen ob gleich mit zulaessigem error 
        for j in range(len(list_triangles_normals)):
            if(data_structure.checkVectorEqual(mainAxis6[i], list_triangles_normals[j])): # wenn gleich
                return j # index des triangles, welches in eine HAS richtung liegt
    
    # falls keine Zelle genau in HAS richtung ausgerichtet sein sollte 
    # zweite schleife 

    angle_list = [] # liste aller winkel angeben
    minAngle_list = []
    minAngle_triangleIndex_list = [] # drei einträge, je achse dier minimale winkel
    for i in range(len(mainAxis6)): # len = 6
        # prüfen ob gleich mit zulaessigem error 
        angle_list.append([])
        for j in range(len(list_triangles_normals)):
            # winkel berechnen der zellen zu HAS Richtung, und in liste speichern
            angle_list[i].append(linearAlg.calcAngleVectors(mainAxis6[i],list_triangles_normals[j]))

        minAngle_triangleIndex_list.append(angle_list.index(min(angle_list[i]))) # index des winkels ist index des normalen vektors in der liste, und damit index des triangles
        minAngle_list.append(min(angle_list[i]))

    # aus den min listen das min raussuchen 
    index_triangle = minAngle_triangleIndex_list[minAngle_list.index(min(minAngle_list))]

    return index_triangle








