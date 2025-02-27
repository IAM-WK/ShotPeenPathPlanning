# planes.py

import numpy as np
import math
import trimesh
import copy
import sympy
from sympy import Symbol
from stl import mesh
import data_structure

# eingabeparameter
from eingabeparameter import ebenenabstand
d_ebenenschar = ebenenabstand # abstand der ebenen einer schar, d.h. des pfades später
err = 1e-6

# FUNKTION: calcNormalAvg:
# Berechnung der durschnittlichen normalen eines patches
def calcNormalAvg(list_normals):
    # list_normals = liste der normalen zu denen average berechnet werden soll, je als 3d vektor
    normal_sum = [0,0,0]
    for normal in list_normals: # alle normalen aufsummieren
        normal_sum = np.add(normal_sum, normal)
    # summe aller normalen durch anzahl der normalen in list_normals teilen
    normal_avg = np.multiply(normal_sum, 1/len(list_normals))
    # normal_avg normieren
    normal_avg0 = np.multiply(normal_avg, math.sqrt(np.dot(normal_avg, normal_avg)))
    return normal_avg0

def getAllVerticesOfPatch(patch, list_triangles_verticesIndex, list_vertices_coordinates):
    # FUNKTION: get liste aller vertices eines patches, MIT dopplungen (ohen### rasu)
    # patch = liste der triangles index, welche in patch liegen
    verticesOfPatch = [] # liste anlegen für die vertices 
    # erste vertex anhängen
    verticesOfPatch.append(list_vertices_coordinates[list_triangles_verticesIndex[0][0]])
    
    for i in range(len(patch)): # jedes triangle des patches durchgehen
            for j in range(3): # alle vertices des triangles durchgehen
                vertex_cur = list_vertices_coordinates[list_triangles_verticesIndex[patch[i]][j]]
                ###if(not(data_structure.checkIfVectorIsInList(verticesOfPatch, vertex_cur))):
                verticesOfPatch.append(vertex_cur)
    return verticesOfPatch

### TEST
#print(getAllVerticesOfPatch([0, 1, 2], [[0, 1], [1,3], [3,1]], [[1, 1, 1], [0, 1, 2], [1, 2, 3], [0, 0, 3], [0, 0, 1]]))

def getMinMax_inRichtung(patch, richtung, list_triangles_verticesIndex, list_vertices_coordinates):
    # Berechnung der min und max Ausdehnung (skalar) des Patches in Richtung richtung 
    # für initialen aufpunkt der ebenenschar, sowie maß für ende

    # patch = liste der triangles index, welche in patch liegen
    # KOSrichtung = vektor als liste, welche richtung drstellt in welche die ausdehnung des patches bestimmt werdne soll
    # [1,0,0], [0,1,0], [0,0,1]

    # retrun: vmin max ausdehnung in die richtung, je als scalar
    # prüfen, welche KOSrichtung
    scalar_richtung_coord = []
    verticesOfPatch = getAllVerticesOfPatch(patch, list_triangles_verticesIndex, list_vertices_coordinates)
    
    

    for i in range(len(verticesOfPatch)): # ausdehungen in richtung
        scalar_richtung_coord.append(np.dot(verticesOfPatch[i], richtung))
    #max und min wert aus der liste auslesen
    maxWert = np.max(scalar_richtung_coord)
    minWert = np.min(scalar_richtung_coord)
    # index des ersten elements in liste, für welches ausdehnung maximal bzw minimal ist
    maxIndex_verticesOfPatch = data_structure.getIndexOf0DElementInList(scalar_richtung_coord, maxWert)
    minIndex_verticesOfPatch = data_structure.getIndexOf0DElementInList(scalar_richtung_coord, minWert)
    # da sortierung gleich ist,  mit gefundenem Index, entsprechenden Punkt aus dem patch zu min bzw max Ausdehnung auslesen
    point_minAusdehnungInRichtung = verticesOfPatch[minIndex_verticesOfPatch]
    point_maxAusdehnungInRichtung = verticesOfPatch[maxIndex_verticesOfPatch]

    """
    if(KOSrichtung == [1, 0, 0]): # x

    elif(KOSrichtung == [0, 1, 0]): # y

    elif(KOSrichtung == [0, 0, 1]): # z
    """
    # punkte mit min bzw max ausdehnung in richtung returnen
    return point_minAusdehnungInRichtung, point_maxAusdehnungInRichtung 
    

def checkIfpatchEben(list_normals_patchCur):
    # prüfen, ob alle normalen vektoren der dreiecke des patches gleich sind
    # list_normals_patch = liste der lnormalen in patch
    check = False
    a = 0 # zähler
    for i in range(len(list_normals_patchCur)): # jedes dreieck durchgehen
        if(data_structure.checkVectorEqual(list_normals_patchCur[0], list_normals_patchCur[i])):
            a = a + 1

    if(a == len(list_normals_patchCur)):
        check = True
    return check


def getEbenenSchar_patch(patch, list_normals_patch, list_triangles_verticesIndex, list_vertices_coordinates):
    # FUNKTION: Erstellen der ebenenschar zu einem patch, 
    # return: ebenenSchar = [[liste  aller aufpunkte, die  jeweils eine ebenen bilden], [vektor der normale der schar]]
    # patch = liste der triangles index, welche in patch liegen
    # list_normals_patch = liste aller normalen je triangle, welches in patch liegt
    # 
    #   
    # Fall: patch ist eben
    if(checkIfpatchEben(list_normals_patch)):
        normalAvg = list_normals_patch[0] # ohnehin alle nomrlaenvektoren gleich in diesem Fall

        # Normale für ebenenSchar bestimmen
        #normalAvg = calcNormalAvg(list_normals_patch)
        # für cubboid Außenflächen: prüfen, ob normalAvg einer KOS achse entspricht
        if(np.linalg.norm(np.subtract(normalAvg, [1,0,0]))<= err or np.linalg.norm(np.subtract(normalAvg, [-1,0,0]))<= err):
            # wenn normalAvg = x Achse
            ### normalSchar = [0,0,1] # z-Achse als normale wählen
            normalSchar = [0,1,0] # y-Achse als normale wählen
        elif(np.linalg.norm(np.subtract(normalAvg, [0,1,0]))<= err or np.linalg.norm(np.subtract(normalAvg, [0,-1,0]))<= err):
            # wenn normalAvg = y Achse
            ### normalSchar = [0,0,1] # z-Achse als normale wählen
            normalSchar = [1,0,0] # x-Achse als normale wähl
        elif(np.linalg.norm(np.subtract(normalAvg, [0,0,1]))<= err or np.linalg.norm(np.subtract(normalAvg, [0,0,-1]))<= err):
            # wenn normalAvg = z Achse
            normalSchar = [1,0,0] # x-Achse als normale wählen
        else: # ansonsten y-Achse als Schnittgerade wählen 
            normalSchar = [0,1,0]


    # Fall: patch ist nicht eben
    else:
        # zwei normalenvektoren des patches, die unterschiedlich
        for i in range(len(list_normals_patch)):
            if(not data_structure.checkVectorEqual(list_normals_patch[0], list_normals_patch[i])):
                index = i
                break
                
        normalSchar = np.cross(list_normals_patch[0], list_normals_patch[index])/np.linalg.norm(np.cross(list_normals_patch[0], list_normals_patch[index]))
    """
        if(data_structure.checkVectorEqual(normalSchar, [-1.0,0.0,0.0])):
            normalSchar = [1.0,0.0,0.0]
        elif(data_structure.checkVectorEqual(normalSchar, [0.0,-1.0,0.0])):
            normalSchar = [0.0,1.0,0.0]
        elif(data_structure.checkVectorEqual(normalSchar, [0.0,0.0,-1.0])):
            normalSchar = [0.0,0.0,1.0]
    """ 

    aufpunkte = [] # liste aller aufpunkte erstellen, die schar bilden
    #ausdehung in normalSchar berechnen: 
    min_normalDir, max_normalDir = getMinMax_inRichtung(patch, normalSchar, list_triangles_verticesIndex, list_vertices_coordinates)
    #print("min_normalDir, max_normalDir = ", min_normalDir, max_normalDir)
    ausdehung_normalDir = np.linalg.norm(np.subtract(np.multiply(normalSchar,max_normalDir), np.multiply(normalSchar,min_normalDir)))
    #print("ausdehung_normalDir = ", ausdehung_normalDir)
    anzahl_ebenen = int(ausdehung_normalDir/d_ebenenschar)
    #print("anzahl_ebenen = ", anzahl_ebenen)

    # ersten Aufpunkt für ebenenSchar bestimmen
    #aufpunkt0 = np.multiply(normalSchar, min_normalDir)

    for i in range(anzahl_ebenen):
        aufpunkte.append(np.add(np.add(min_normalDir, np.multiply(normalSchar, d_ebenenschar/2)), np.multiply(normalSchar, d_ebenenschar*i))) # geändert
    
    ebenenSchar = []
    ebenenSchar.append(aufpunkte)
    ebenenSchar.append(normalSchar)
    #print(" ebenenSchar = ", ebenenSchar)
    return ebenenSchar 


