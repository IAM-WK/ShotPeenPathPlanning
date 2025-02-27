# intersection_patches.py

import numpy as np
import math
import trimesh
import copy
import sympy
from sympy import Symbol
from stl import mesh
import data_structure
import planes

#####
from obstacle_class import *
#####
#neu 

# FUNKTION: reihenfolge der eingabeliste umkehren
def revOrderList(liste):
    listeRev = [] # neue liste anlegen
    for i in range(len(liste)):
        listeRev.append(liste[len(liste)-1-i]) # elemente aus "liste" umgekehrt in neue liste "listeRev" einsortieren
    return listeRev


# FUNKTION: euklid. abstand zweier vektoren berechnen
def calcEuclidianDist(point1, point2):
    vectorDist = np.subtract(point2, point1) # verbindungs/abstandsvektor
    dist = math.sqrt(np.dot(vectorDist, vectorDist)) # norm des abstandsvektors
    return dist


# FUNKTION: gleichung aufstellen zu schnitt gerade ebene
def IntersectionPlaneGerade_getEqList(plane, gerade): 
    # plane in form [aufpunkt, normale] 
    # geradde in form [aufpunkt, richtungsvektor]
    # plane und geraden verrechnen und aufteilen in Summe aus part ohne *x und mit *x
    d = np.subtract(np.dot(plane[0], plane[1]), np.dot(plane[1], gerade[0])) # seite ohne parameter
    # gerade = [aufpunkt, richtungsvektor]
    normaleX = np.dot(plane[1], gerade[1]) # seite mit parameter

    return [d, normaleX] # linke seite, rechte seite

# parameter zu schnitt aus plane und gerade berechnen
def IntersectionPlaneGerade_solveParameter(plane, gerade):
    # eq lösen
    eq = IntersectionPlaneGerade_getEqList(plane, gerade)
    parameter = eq[0]/eq[1]
    return parameter

# schnittpunkt zu plane und gerade berechnen
def IntersectionPlaneGerade_solvePoint(plane, gerade):
    # eq lösen und punkt berechnen
    parameter = IntersectionPlaneGerade_solveParameter(plane, gerade)
    intersectionPoint = np.add(np.multiply(gerade[1], parameter), gerade[0])
    return intersectionPoint


"""
def geradeEq(gerade_vector, parameter):
    # gerade_vector = [aufpunkt, richtungsvektor]
    return_vector = np.add(gerade_vector[0], np.multiply(gerade_vector[1], parameter))
    return return_vector
"""

# FUNKTION: getNormalsOfTriangles()
# liest normale der triangles aus welche  in list_triangleIndex, anhand triangleIndex 
# in RF der list_triangleIndex
# listTriangles_normal = triangles_normals, direkt m.h. trimesh auslesbar, sortiert nach triangles
def getNormalsOfTriangles(listTriangles_normal, list_triangleIndex):
    normals = [] # liste anlegen, welche die normalen, in RF, je als 3d vektor beinhaltet
    for i in range(len(list_triangleIndex)):
        normals.append(listTriangles_normal[list_triangleIndex[i]])
    return normals

def solveEqList(eq_list):
    # Eq_list in Form: [vektor1ohnex, vektor2mitx]
    # vektor1: zahlenwerte
    # vektor2: multipliziert mit parameter

    #print("\n eq_list[0] = ", eq_list[0], "\n eq_list[1] = ", eq_list[1]) #TEST
    t = Symbol('t')
    sol = sympy.solve(np.subtract(eq_list[0], np.multiply(eq_list[1], t)), t, dict = True) # sub or ad


    if(len(sol) == 1): # wenn eine lösung
        sol_t = sol[0][t]
        obstacle_info = Obstacle_Info(False, sol_t)

    elif(len(sol) > 1): # fall gerade liegt in ebene 
        sol_t = None
        obstacle_info = Obstacle_Info(True, sol_t)

    elif(len(sol) == 0): # wenn keine lösung
        #neu print("Gerade schneidet Ebene nicht oder Gerade liegt in Ebene.")
        sol_t = None
        obstacle_info = Obstacle_Info(False, sol_t)

    return obstacle_info

def solveParameter_intersectionPlaneGerade(plane, gerade):
    # get Eq 
    
    eq_list = IntersectionPlaneGerade_getEqList(plane, gerade)
    obstacle_info = solveEqList(eq_list)
    #sol_parameter = obstacle_info.parameter
    return obstacle_info



# FUNKTION: Berechnen des Ounktes auf einer gerade, anhand der geradengleichung sowei der angabe des parameters
def calcPointGerade(gerade, parameter):
    # gerade in Fomr : [aufpunkt, richtungsvektor]
    point = np.add(gerade[0], np.multiply(gerade[1], parameter))
    return point

#FUNKTION: Berechnen der Schnittpunkte der Triangle Berandungen mit einer Ebene, falls vorhanden
def intersectionPoints_trianglePlane(list_triangle_verticesIndex,  list_vertices_coordinates, triangle_index, plane):
    # je triangle plane intersection 
    # 0 SPe: kein Schnitt
    # 1 SPe: plane geht durch eine vertex des triangles
    # 2 SPe: plane durchschneidet triangle
    # unendlich viele SPe: falls eine triangle edge genau innerhalb der plane lieg

    # drei geraden, je edge des triangles, erstellen:
    # gerade je als [aufpunkt, richtungsvektor]
    geraden = []
    geraden.append([list_vertices_coordinates[list_triangle_verticesIndex[triangle_index][0]], np.subtract(list_vertices_coordinates[list_triangle_verticesIndex[triangle_index][1]], list_vertices_coordinates[list_triangle_verticesIndex[triangle_index][0]])])
    geraden.append([list_vertices_coordinates[list_triangle_verticesIndex[triangle_index][1]], np.subtract(list_vertices_coordinates[list_triangle_verticesIndex[triangle_index][2]], list_vertices_coordinates[list_triangle_verticesIndex[triangle_index][1]])])
    geraden.append([list_vertices_coordinates[list_triangle_verticesIndex[triangle_index][2]], np.subtract(list_vertices_coordinates[list_triangle_verticesIndex[triangle_index][0]], list_vertices_coordinates[list_triangle_verticesIndex[triangle_index][2]])])
    
  
    listIntersectionParam = [] # liste für parameter aus schnitten
    listIntersectionPoints = [] # liste für intersection points

    for i in range(3): # je edge
        # Schnitt berechnen
        ####print("aktuelle gerade ", i, " : ", geraden[i]) # test
        intersectionParam = IntersectionPlaneGerade_solveParameter(plane, geraden[i]) # schnitt mit edge/ gerade i berechnen
        ####print("\n intersectionParam = ", intersectionParam) # TEST
        if((intersectionParam != None) and (intersectionParam >= 0 and intersectionParam <= 1)): # wenn schnittpunkt ex., d.h. t != None ist, und schnittpunkt innerhalb der edge liegt, d.h. (t>=0 , t>=1)
            listIntersectionParam.append(intersectionParam) # parameter in liste schreiben
            # punkt zugehrig zu intersectionParam m.h. geradengleichung ausrechnen
            
            ####print("     calcPointGerade(geraden[i], intersectionParam) = ", IntersectionPlaneGerade_solvePoint(plane, geraden[i]))
            listIntersectionPoints.append(IntersectionPlaneGerade_solvePoint(plane, geraden[i]))

    # SOFA: plane lliegt genau auf einer edge des triangles, dann erhält man zwei mal den eckpunkt als intersection point, mächte diesen aber nur einmal
    # daher in diesem Fall, ein element löschen
    # ggf doppelte punkte löschen
    if(len(listIntersectionPoints) == 2):
        if(data_structure.checkVectorEqual(listIntersectionPoints[0],listIntersectionPoints[1])):
            del listIntersectionPoints[1]
    if(len(listIntersectionPoints) == 3):
        #print("listIntersectionPoints", listIntersectionPoints)
        if(data_structure.checkVectorEqual(listIntersectionPoints[0],listIntersectionPoints[2])):
            del listIntersectionPoints[2]
            #print("listIntersectionPoints", listIntersectionPoints)
        elif(data_structure.checkVectorEqual(listIntersectionPoints[1],listIntersectionPoints[2])):
            del listIntersectionPoints[1]
            #print("listIntersectionPoints", listIntersectionPoints)

    #print("zu triangle ", triangle_index, ", listIntersectionPoints = ", listIntersectionPoints)
    return listIntersectionPoints



def sortIntersectionPoints(points_list, triangleIndex_list, list_triangles_normal, plane_normal): 
    # points_list als ergebnis aus inntersectoinPoints_trianglesPatchPlane
    # in Form: [[p1, p3], [p4, p2], [p1, p4], ...]
    
    #neu print("\n points_list = ", points_list, " \n")
    
    # triangleIndex_list wird ebenfalls sortieren
    list_triangleIndex_sorted = []
    # liste um rand list indizes zu merken
    list_listIndex_einmalig = []

    list_points_einmalig = []
    # ersten eintrag in liste eintragen 
    list_points_sorted = [] 

    #################################################   
    for i in range(len(points_list)): # je punktepaar
        #print("\n i = ", i) # TEST
        for j in range(len(points_list[i])): # je punkt in i tem punktepaar
            #print("     j = ", j, "\n       points_list[i][j] = ", points_list[i][j]) # TEST
            a = 0 # zähler
            for k in range(len(points_list)): # k ist index des punktepaars 
                for l in range(len(points_list[k])): # je punkt in k tem punktepaar
                    #print("\n           points_list[k][l] = ", points_list[k][l]) # TEST
                    if(data_structure.checkVectorEqual(points_list[i][j], points_list[k][l])):
                        ##if(k != i and j != l): # nur für print test
                        ##    print("equal = ", points_list[i][j], points_list[k][l])
                        a = a +1 # zähler + 1
                        #print("         a = ", a)
            #print("a = ", a)
            if(a == 1): # point point_list[i][j] nur einmal in liste point_list
                list_points_einmalig.append(points_list[i][j])

                # die i s sind ränder, (für triIndex sortierung merken)
                list_listIndex_einmalig.append(i) # hier: i = index der triangles, welches ränder der schnittgeraden beinhaltet
        
    list_points_alrSorted_index = []
    #if(len(list_points_einmalig) == 2): # Fall: geschlossene oberfläche
    if(planes.checkIfpatchEben(getNormalsOfTriangles(list_triangles_normal, triangleIndex_list))): # fall einer ebenen OF
        # punkte mit min max Audehnungen in n richtung als Anfangs Endpunkt wählen

        if(len(list_points_einmalig) == 2): # Fall: geschlossene oberfläche):
            
            list_points_sorted.append(list_points_einmalig[0])
            list_points_sorted.append(list_points_einmalig[1])
            #print("\n list_points_sorted = ", list_points_sorted)
            list_triangleIndex_sorted.append(triangleIndex_list[list_listIndex_einmalig[0]])
            list_triangleIndex_sorted.append(triangleIndex_list[list_listIndex_einmalig[1]])

        else: # alle punkte nacheinander anhan des abstandes aneinander hängen
            richtung = np.subtract(list_points_einmalig[0], list_points_einmalig[1])


            scalar_richtung_coord = []
            for i in range(len(list_points_einmalig)): # ausdehungen in richtung
                scalar_richtung_coord.append(np.dot(list_points_einmalig[i], richtung))
                #neu print("list_points_einmalig[i] = ", list_points_einmalig[i])
            #max und min wert aus der liste auslesen
            maxWert = np.max(scalar_richtung_coord)
            minWert = np.min(scalar_richtung_coord)
            #print("minWert, maxWert = ", minWert, maxWert)
            # index des ersten elements in liste, für welches ausdehnung maximal bzw minimal ist
            maxIndex = data_structure.getIndexOf0DElementInList(scalar_richtung_coord, maxWert)
            minIndex = data_structure.getIndexOf0DElementInList(scalar_richtung_coord, minWert)
            
            # da sortierung gleich ist,  mit gefundenem Index, entsprechenden Punkt aus dem patch zu min bzw max Ausdehnung auslesen

            list_points_sorted.append(list_points_einmalig[minIndex])
            list_points_sorted.append(list_points_einmalig[maxIndex])

            list_triangleIndex_sorted.append(triangleIndex_list[list_listIndex_einmalig[minIndex]])
            list_triangleIndex_sorted.append(triangleIndex_list[list_listIndex_einmalig[maxIndex]])
            
        
    else: # nicht ebenes patch
        # 0. elemente in list_points_sorted, points,  sowie list_triangleIndex_sorted, triindex, schrieben
        list_points_sorted.append(list_points_einmalig[0])
        list_triangleIndex_sorted.append(triangleIndex_list[list_listIndex_einmalig[0]])

        for k in range(len(points_list)*2-1): # k ist overall anzahl an punkten -1
            #print("\n k = ", k) 
            for i in range(len(points_list)): # für jedes punkte paar
                if(not(data_structure.checkIfScalarIsInList(list_points_alrSorted_index, i))): # wenn punkteppar noch nihct einsortiert wurde, dann...
                    
                    for j in range(len(points_list[i])): # ... für die beiden punkte aus diesem paar... 
                        #print("         points_list[", i, "][", j, "] = ", points_list[i][j])
                        if(data_structure.checkVectorEqual(points_list[i][j], list_points_sorted[k])): # prüfen, ob der punkt aus punkte paar gleich ist, wie aktueller (k ter) punkt aus sorted list
                            #print("         points_list[", i, "] = ", points_list[i])
                            if(len(points_list[i])==2): # wenn es ein punkte paar ist, 
                                ##### doppelt eintragen, da je punkt aus punktepaar, mit len ==2 
                                list_triangleIndex_sorted.append(triangleIndex_list[i]) # i.tes triangle eintragen
                                list_triangleIndex_sorted.append(triangleIndex_list[i]) # i.tes triangle eintragen
                                if(j == 0):
                                    #print(" j = 0")
                                    list_points_sorted.append(points_list[i][j]) #  dann innere punkte doppelt
                                    list_points_sorted.append(points_list[i][j+1])
                                    list_points_alrSorted_index.append(i)
                                elif(j == 1):
                                    #print(" j = 1")
                                    list_points_sorted.append(points_list[i][j]) #  dann innere punkte doppelt
                                    list_points_sorted.append(points_list[i][j-1])
                                    list_points_alrSorted_index.append(i)
                            #print(" list_points_sorted = ", list_points_sorted)
        list_points_sorted.remove(list_points_einmalig[0])
        list_triangleIndex_sorted.remove(list_triangleIndex_sorted[0])
        

    return list_points_sorted, list_triangleIndex_sorted



def intersectionPoints_trianglesPatchPlane(list_triangle_verticesIndex,  list_vertices_coordinates, patch, plane, list_triangles_normal):
    # patch: liste der trianglesIndex, die in patch enthalten
    # plane: [aufpunkt, normale]
    # SPe berechnen der triangles in patch mit der ebene plane

    list_intersectionPoints_patchPlane = [] # liste anlegen für Schittpunkte
    list_triIndex = [] # liste anlegen für triangles, die geschnitten werden
    
    for triIndex in patch: # für alle triangles (geg durch triangleIndex) innerhallb des patch
        # temporär points anlegen, welche die schnittpunkte des aktuellen triangles triIndedx mit der plane beinhaltet
        points =  intersectionPoints_trianglePlane(list_triangle_verticesIndex,  list_vertices_coordinates, triIndex, plane)
        if(len(points) != 0): # falls schnittpunkt(e) ex. 
            # points = liste Spe eines triangle mit plane
            # diese als  liste in list_intersectionPoints_patchPlane liste schreiben
            list_intersectionPoints_patchPlane.append(points)
            # sowie zugehörigen triIndex in list_triIndex schreiben
            # d.h. soertierung list_intersectionPoints_patchPlane und list_triIndex gleich 
            list_triIndex.append(triIndex)
    # punktepaare in sich sortieren, 
    # d.h. wenn zwei punkte aus schnitt mit einem triangle, dann richtung vorgeben, sodass alle punktepaare in gleicher richtung orientiert sind
    # liste list_intersectionPoints_patchPlane sortieren, so dass, punkte  mit gleichen einträgen nebeneinander
    list_intersectionPoints_patchPlane_sorted, list_triIndex_sorted = sortIntersectionPoints(list_intersectionPoints_patchPlane, list_triIndex, list_triangles_normal, plane[1])

    return list_intersectionPoints_patchPlane_sorted, list_triIndex_sorted
    #return list_intersectionPoints_patchPlane, list_triIndex

# FUNKTION: 
def intersectionPoints_trianglesPatchPlaneSchar(list_triangle_verticesIndex,  list_vertices_coordinates, patch, planeSchar, list_triangles_normal):
    # Berechnung der Schnittpunkte eines patches mit einer Ebenenschar, 
    # Ablauf: 
    # berechnung der schnitte ebene mit patch, in RF der schar, 
    # schar geg als: [[aufpunkt0, aufpunkt1, aufpunkt2, ...], [normale]] (ebenen einer schar liegen parallel mit äquidistantem abstand, normale also konst über schar)
    # berechnung der schnittpunkte einer ebene mit dem patch, gem. intersectionPoints_trianglesPatchPlane(...)
    # aneinanderhängen der einzelnen listen aus jedme schnitt patch x Ebene_i

    # liste anlegen für schnitte der einzelnen ebenen mit patch, jeder i-te listeneintrag entspricht SPen aus i-ter ebene aus schar mit dem patch
    listIntersection_PatchSchar = [] 
    # liste für sortierte punkte 
    listIntersection_PatchSchar_sorted = [] 
    # liste um tri indizes zu sortieren entsprechend der punktepaar sortierung
    listTriIndex_PatchSchar = []
    listTriIndex_PatchSchar_sorted = []


    #neu print("intersectionPoints_trianglesPatchPlaneSchar START: ")
    # 0. eintrag in listen schreiben
    listIntersection_PatchSchar.append(intersectionPoints_trianglesPatchPlane(list_triangle_verticesIndex,  list_vertices_coordinates, patch, [planeSchar[0][0], planeSchar[1]], list_triangles_normal)[0])
    listIntersection_PatchSchar_sorted.append(intersectionPoints_trianglesPatchPlane(list_triangle_verticesIndex,  list_vertices_coordinates, patch, [planeSchar[0][0], planeSchar[1]], list_triangles_normal)[0])
    
    listTriIndex_PatchSchar.append(intersectionPoints_trianglesPatchPlane(list_triangle_verticesIndex,  list_vertices_coordinates, patch, [planeSchar[0][0], planeSchar[1]], list_triangles_normal)[1])
    listTriIndex_PatchSchar_sorted.append(intersectionPoints_trianglesPatchPlane(list_triangle_verticesIndex,  list_vertices_coordinates, patch, [planeSchar[0][0], planeSchar[1]], list_triangles_normal)[1])
    
    # reihenfolge der jeweiligen schnitte mit i.ter ebene ermitteln
    # dazu: 0. schnittgerade RF belassen,
    #       1. schnittgerade RF so rum drehen, dass 0. eintrag näher am letzten eintrag der 0. schnittgerade liegt als 
    #          i+1. sortierreihenfolge so wählen, dass abstand des ersten punktes der i+1. zu letztem eintrag der i. gerade kleiner ist als abstand des letzen punktes der i+1. zu letztem eintrag der i. gerade
    
    for i in range(1, len(planeSchar[0])): # für jede plane in planeSchar sortierte schnittpunkte mit patch berechnen
        # je mit neuer ebene als funktionsparameter plane
        listIntersection_PatchSchar.append(intersectionPoints_trianglesPatchPlane(list_triangle_verticesIndex,  list_vertices_coordinates, patch, [planeSchar[0][i], planeSchar[1]], list_triangles_normal)[0])
        listTriIndex_PatchSchar.append(intersectionPoints_trianglesPatchPlane(list_triangle_verticesIndex,  list_vertices_coordinates, patch, [planeSchar[0][i], planeSchar[1]], list_triangles_normal)[1])
        
        if(len(listIntersection_PatchSchar[0]) != 0):
            ########
            distA = calcEuclidianDist(listIntersection_PatchSchar_sorted[i-1][len(listIntersection_PatchSchar_sorted[i-1])-1], listIntersection_PatchSchar[i][0]) # abstand zu erstem eintrag der neuen geraden
            distB = calcEuclidianDist(listIntersection_PatchSchar_sorted[i-1][len(listIntersection_PatchSchar_sorted[i-1])-1], listIntersection_PatchSchar[i][len(listIntersection_PatchSchar[i])-1]) # abstand zu letztem eintrag der neuen geraden
            
            if(distA > distB): # prüfen, zu welchem punkt (0. oder letzter) abstand kleiner ist
                # falls abstand von 0. punkt in iter liste zu hinterstem punkt in i-1ter liste größer ist, als von hinterstem punkt in iter liste zu hinterstem punkt in i-1ter liste 
                # dann RF der i. liste umkehren
                listIntersection_PatchSchar_sorted.append(revOrderList(listIntersection_PatchSchar[i]))
                listTriIndex_PatchSchar_sorted.append(revOrderList(listTriIndex_PatchSchar[i]))
                
            else:
                # sonst RF belassen
                listIntersection_PatchSchar_sorted.append(listIntersection_PatchSchar[i])
                listTriIndex_PatchSchar_sorted.append(listTriIndex_PatchSchar[i])
                ##############
                # listTriIndex_PatchSchar_sorted bidher noch in listen je gerade unterteilt, zusammenführen, in eine liste nur mit indizes der triangles
    listTriIndex_sorted = []
    for i in range(len(listTriIndex_PatchSchar_sorted)):
        for j in range(len(listTriIndex_PatchSchar_sorted[i])):
            listTriIndex_sorted.append(listTriIndex_PatchSchar_sorted[i][j])

    return listIntersection_PatchSchar_sorted, listTriIndex_sorted

# FUNKTION:
def getPathOfPatch_points_normals(list_triangles_normals, list_triangle_verticesIndex,  list_vertices_coordinates, patch, planeSchar, list_triangles_normal):
    
    listIntersection_PatchSchar_sorted, listTriIndex_PatchSchar_sorted = intersectionPoints_trianglesPatchPlaneSchar(list_triangle_verticesIndex,  list_vertices_coordinates, patch, planeSchar, list_triangles_normal)
    list_normals_sorted = getNormalsOfTriangles(list_triangles_normals, listTriIndex_PatchSchar_sorted)

    return listIntersection_PatchSchar_sorted, list_normals_sorted
