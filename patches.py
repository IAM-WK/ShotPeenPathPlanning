
import numpy as np
import math
import trimesh
import copy
import sympy
from stl import mesh
import data_structure

def checkIfneighbour(list_triangle_edgesIndex, triangleIndex1, triangleIndex2):
    check = False
    for i in range(len(list_triangle_edgesIndex)):
        # wenn eine edge des 2. triangles auch eine edge des 1. ist, dann nachbarn 
        if((data_structure.checkIfScalarIsInList(list_triangle_edgesIndex[triangleIndex1], list_triangle_edgesIndex[triangleIndex2][0])) or (data_structure.checkIfScalarIsInList(list_triangle_edgesIndex[triangleIndex1], list_triangle_edgesIndex[triangleIndex2][1])) or (data_structure.checkIfScalarIsInList(list_triangle_edgesIndex[triangleIndex1], list_triangle_edgesIndex[triangleIndex2][2]))):
            check = True
    # !!!
    # wenn nachbarn , dann chack = True
    return check

def getNeighbours_0(list_triangle_edgesIndex, list_trianglesIndex_toBeSearched, triangleIndex1):
    list_neighbours_triangleIndex = [] # liste der nachbarn zu triangleIndex1, in form der traingle indizes
    for i in list_trianglesIndex_toBeSearched:
        if(checkIfneighbour(list_triangle_edgesIndex, triangleIndex1, i)):
            list_neighbours_triangleIndex.append(i)

    if(len(list_neighbours_triangleIndex) == 0):
        return 0

    return list_neighbours_triangleIndex

def getNeighbours(list_triangle_edgesIndex, list_trianglesIndex_toBeSearched, triangleIndex1):
    list_neighbours_triangleIndex = [] # liste der nachbarn zu triangleIndex1, in form der traingle indizes
    
    for i in list_trianglesIndex_toBeSearched:
        if(checkIfneighbour(list_triangle_edgesIndex, triangleIndex1, i)):
            list_neighbours_triangleIndex.append(i)

    return list_neighbours_triangleIndex

def calcAngle(vector1, vector2):
    angleArg = np.dot(vector1, vector2)/(math.sqrt(np.dot(vector1, vector1)))/(math.sqrt(np.dot(vector2, vector2)))

    # Rundungsfehler asugleichen, sonst error in cos
    if (angleArg > 1.0):
        angleArg = 1.0
    elif(angleArg < -1.0):
        angleArg = -1.0
    angle = np.arccos(angleArg)
    # ausgabe in rad
    return angle


def checkAngle(normal1, normal2, alpha):
    # alpha in rad
    check = False
    angle = calcAngle(normal1, normal2)
    
    if(angle <= alpha):
        check = True 
    return check 

# triangle als indizes liste: [0, 1, 2, 3, 4, 5,] len = liste aller triangle
def buildPatch(index_triangleInit, list_triangles_trianglesIndex, list_triangles_edgesIndex, list_triangles_normals, alpha):
    #[[1, 4, 500], [500, 7, 8]]
    # eine zelle nehmen, in liste schreiben
    # suche ihre nachbarzellen aus liste aller zellen
    # prüfe für alle nachbarzellen, ob winkel zw normalen < alpha    
    #                               wenn ja, dann hinzufügen von neuer zelle zu liste
    list_triangles_trianglesIndex_NotSearched = copy.deepcopy(list_triangles_trianglesIndex)
    liste_triangles_patch = [] # 
    liste_triangles_patch.append(index_triangleInit) # init element eintragen
    list_triangles_trianglesIndex_NotSearched.remove(index_triangleInit) # init element removen, da bereits verwendet

    liste_triangles_patch, list_triangles_trianglesIndex_NotSearched = buildNextPatch(index_triangleInit, index_triangleInit, list_triangles_edgesIndex, list_triangles_normals, alpha, liste_triangles_patch, list_triangles_trianglesIndex_NotSearched)
    #list_triangles_trianglesIndex_NotSearched = buildNextPatch(index_triangleInit, index_triangleInit, list_triangles_edgesIndex, list_triangles_normals, alpha, liste_triangles_patch, list_triangles_trianglesIndex_NotSearched)
    
    return liste_triangles_patch

def buildNextPatch(index_triangleInit, cur_index_triangle, list_triangles_edgesIndex, list_triangles_normals, alpha, list_patch, list_triangles_trianglesIndex_NotSearched):
    # index_triangleInit: intialer triangle index, zum vergleichen des winkels
    # cur_index_triangle: bei erstem aufruf in buildPatch = index_triangleInit, wird jedes mal varriert
    # list_triangles_edgesIndex: liste der triangles (sortiert), je als lists der edge inidzes
    # list_triangles_normals: liste der triangles (sortiert), je als normal des triangles
    # alpha: winkel für winkelbedingung
    # list_patch: Zielliste, die triangles enthalten soll, welche zu patch zugehörig
    # list_triangles_trianglesIndex_NotSearched: enthält indizes der triangles, welche noch nicht zu zielliste liste_triangles_patch hizugefüft wurden
    #                                            d.h. wird jede rekursion geupdated, wenn ein neues patch element gefunden wrude

    # abbruch der rekursion: wenn kein nachbar gefunden wird --> abbruch ? 
    # abbruch der rekursion: wennn zwar mind ein nachbar gefunden, aber keiner der nachbarn winkelbed erfüllt
    # d.h. insgesamt, wenn kein neues triangle zu list_patch hinzugefügt wird.
    

    # wenn nachbarn zu cur_index_triangle innerhalb der list_triangles_trianglesIndex_NotSearched
    cur_neighbours_indexTriangle = getNeighbours(list_triangles_edgesIndex,  list_triangles_trianglesIndex_NotSearched, cur_index_triangle)
    
    if(len(cur_neighbours_indexTriangle) != 0): # wenn nachbarn zu cur_index_tirangle ex., ...
        for i in range(len(cur_neighbours_indexTriangle)): # alle ex.en nachbarn durchlaufen
            
            # prüfen, ob winklebed. zwischen initTriangle normale und aktuellem nachbarn erfüllt ist
            if(checkAngle(list_triangles_normals[cur_neighbours_indexTriangle[i]], list_triangles_normals[index_triangleInit], alpha)): # je überprüfen, ob winkelbed erfüllt ist
                # wenn winkelbed erfüllt ist,
                if(not(data_structure.checkIfScalarIsInList(list_patch, cur_neighbours_indexTriangle[i]))): 
                    list_patch.append(cur_neighbours_indexTriangle[i]) # in patch liste einfügen
                if(data_structure.checkIfScalarIsInList(list_triangles_trianglesIndex_NotSearched, cur_neighbours_indexTriangle[i])):
                    list_triangles_trianglesIndex_NotSearched.remove(cur_neighbours_indexTriangle[i]) # aus liste notSearched removen
                # Rekursion
                list_patch, list_triangles_trianglesIndex_NotSearched = buildNextPatch(index_triangleInit, cur_neighbours_indexTriangle[i], list_triangles_edgesIndex, list_triangles_normals, alpha, list_patch, list_triangles_trianglesIndex_NotSearched)
    return list_patch, list_triangles_trianglesIndex_NotSearched

    # 
    # eine zelle nehmen, in liste schreiben
    # suche ihre nachbarzellen aus liste aller zellen
    # prüfe für alle nachbarzellen, ob winkel zw normalen < alpha 
    #                               wenn ja, dann hinzufügen von neuer zelle zu liste

def buildNextPatch_0(index_triangleInit, cur_index_triangle, list_triangles_edgesIndex, list_triangles_normals, alpha, liste_triangles_patch, list_triangles_trianglesIndex_NotSearched):
    #[[1, 4, 500], [500, 7, 8]]
    # eine zelle nehmen, in liste schreiben
    # suche ihre nachbarzellen aus liste aller zellen
    # prüfe für alle nachbarzellen, ob winkel zw normalen < alpha    
    #                               wenn ja, dann hinzufügen von neuer zelle zu liste

    
    # nachbarn von liste_triangles_patch finden
    #abbruch, wenn es keine nachbarn mehr findet, oder keine nachbarn die angle bed erfüllen
    cur_neighbours = getNeighbours(list_triangles_edgesIndex, list_triangles_trianglesIndex_NotSearched, cur_index_triangle)
    

    #if(len(cur_neighbours) != 0): # wenn es nachbarn gibt
    if(cur_neighbours != 0): # wenn es nachbarn gibt    
        #print("\n       len(cur_neighbours) = ", len(cur_neighbours))
        print("\n 0")
        for j in range(len(cur_neighbours)):
            if(cur_neighbours != 0 and checkAngle(list_triangles_normals[index_triangleInit], list_triangles_normals[cur_neighbours[j]], alpha)): # wenn die nachbarn, die winkelbed erfüllen
                
                liste_triangles_patch.append(cur_neighbours[j])
                list_triangles_trianglesIndex_NotSearched.remove(cur_neighbours[j])

                liste_triangles_patch, list_triangles_trianglesIndex_NotSearched = buildNextPatch(index_triangleInit, cur_neighbours[j], list_triangles_edgesIndex, list_triangles_normals, alpha, liste_triangles_patch, list_triangles_trianglesIndex_NotSearched)
                
    else:
        print("else")
    return liste_triangles_patch, list_triangles_trianglesIndex_NotSearched
                
        
        
# funktion, die alle cells in patches sortiert
def getPatches(index_triangleInit, list_triangles_trianglesIndex, list_triangles_edgesIndex, list_triangles_normals, alpha):
    # return patches_list


    # list_triangles_trianglesIndex kopieren
    list_triangles_trianglesIndex_copy = []
    for i in range(len(list_triangles_trianglesIndex)):
        list_triangles_trianglesIndex_copy.append(list_triangles_trianglesIndex[i])

    # liste für patches anlegen
    patches_list = []
    patches_list.append(buildPatch(index_triangleInit, list_triangles_trianglesIndex, list_triangles_edgesIndex, list_triangles_normals, alpha))
    for i in range(len(patches_list[0])):
        list_triangles_trianglesIndex_copy.remove(patches_list[0][i])
        # hinzugefügte/ einsortierte triangles aus allgmeienr rest liste löschen

    j = 1
    while (len(list_triangles_trianglesIndex_copy) > 0): 
        patches_list.append(buildPatch(list_triangles_trianglesIndex_copy[0], list_triangles_trianglesIndex_copy, list_triangles_edgesIndex, list_triangles_normals, alpha))
        
        for i in range(len(patches_list[j])):
            list_triangles_trianglesIndex_copy.remove(patches_list[j][i])
            # hinzugefügte/ einsortierte triangles aus allgmeienr rest liste löschen
        j = j + 1

    return patches_list
