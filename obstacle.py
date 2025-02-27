# obstacle.py


import numpy as np
import math
import trimesh
import copy
import sympy
from sympy import Symbol
from stl import mesh
import data_structure
import planes
import intersection_patches
import linearAlg

import patches # ? braucht man das hier überhaupr?
import SurfaceToTCP
import orientation



######
#import obstacle_class
######

err_obst = 0.01

def checkIntersecctionLineTriangleEdges(SP_parameter, gerade, triangle_index, list_triangles_verticesIndex, list_vertices_coordinates, list_triangles_normals):
    
    sp = intersection_patches.calcPointGerade(gerade, SP_parameter)
    
    #print("         SP = ", sp)
    
    
    # vertices des triangles auslesen, in liste vertices speichern
    vertices = []
    for i in range(len(list_triangles_verticesIndex[triangle_index])): # 3, da triangle
        vertices.append(list_vertices_coordinates[list_triangles_verticesIndex[triangle_index][i]])
    #print("\n vertices = ", vertices)
    
    #for currVerticesIndex in list_triangles_verticesIndex[triangle_index]: # 3, da triangle
    #    vertices.append(list_vertices_coordinates[currVerticesIndex])

    # geraden auftellen je von vertex ausgehend zu pointSP hin !
    geraden_verticesToPointSP = []
    for i in range(len(list_triangles_verticesIndex[triangle_index])): # 3, da triangle
        geraden_verticesToPointSP.append(linearAlg.getGerade_twoPoints(vertices[i], sp))
        #print("\n geraden_verticesToPointSP = ", geraden_verticesToPointSP)
    # edges zu geraden umwandeln
    geraden_edges = []
    # sortiert nach reihenfolge der veertices zu sp geraden, zu denen schnitte berechnet werden sollen 
    geraden_edges.append(linearAlg.getGerade_twoPoints(vertices[1], vertices[2]))
    geraden_edges.append(linearAlg.getGerade_twoPoints(vertices[2], vertices[0]))
    geraden_edges.append(linearAlg.getGerade_twoPoints(vertices[0], vertices[1]))
    
    # schnitte berechnen
    a = 0 # zähler 
    for i in range(len(geraden_edges)): 
        #print("i = ", i)
        lineIntersection_Info_temp = linearAlg.intersectionLineLine_parameter(geraden_verticesToPointSP[i], geraden_edges[i])
        
        #if(not param_temp.b_linesIdentisch): # wenn nicht identisch 
        # prüfen, ob liste eintrag, bzw ob geraden windschief, parallel, keinen schnitt auf weisen.#
        if(not lineIntersection_Info_temp.b_linesIdentisch):
            if(lineIntersection_Info_temp.parameter is not None):
                if(len(lineIntersection_Info_temp.parameter) == 2):
                    if(lineIntersection_Info_temp.parameter >= 1.0-err_obst): # prüfen, ob dazwischen
                        a = a + 1
        #else:
            #raise Exception('checkIntersecctionLineTriangleEdges: SP_Gerade und Kante identisch')
            #print("throw error, in checkIntersecctionLineTriangleEdges")
    if(a == 3): # alle Bed.en erfüllt
        # point innerhalb triangle
        #return [True, SP]
        return True
    else: # schnitt nicht mit dem triangle
        #return [False, None]
        return False


def checkIntersecctionLineInPlane_TriangleEdges(gerade, triangle_index, list_triangles_verticesIndex, list_vertices_coordinates, list_triangles_normals):
    #fall dass strahlgerade innerhalb der ebene des triagnles liegt, dann keinen eindeutigen chnittpunkt mit der ebene
    # dehalb hier berechnung, ob ein schnittpunkt mit einer edge des triangles vorliegt. 

    #SP = intersection_patches.calcPointGerade(gerade, SP_parameter)
    #print("         SP = ", SP)
    
    # vertices des triangles auslesen, in liste vertices speichern
    vertices = []
    for i in range(len(list_triangles_verticesIndex[triangle_index])): # 3, da triangle
        vertices.append(list_vertices_coordinates[list_triangles_verticesIndex[triangle_index][i]])

    # geraden auftellen je von vertex ausgehend zu pointSP hin !
    
    ## edges zu geraden umwandeln
    geraden_edges = []
    # sortiert nach reihenfolge der veertices zu sp geraden, zu denen schnitte berechnet werden sollen 
    geraden_edges.append(linearAlg.getGerade_twoPoints(vertices[1], vertices[2]))
    geraden_edges.append(linearAlg.getGerade_twoPoints(vertices[2], vertices[0]))
    geraden_edges.append(linearAlg.getGerade_twoPoints(vertices[0], vertices[1]))
    
    # schnitte berechnen
    #a = 0 # zähler 
    for i in range(len(geraden_edges)):
        lineIntersection_Info = linearAlg.intersectionLineLine_parameter(gerade, geraden_edges[i])
        
        # prüfen, ob liste eintrag, bzw ob geraden windschief, parallel, keinen schnitt auf weisen.#
        if(lineIntersection_Info.isObstacle_inPlane()):
            if(lineIntersection_Info.parameter >= 0 and lineIntersection_Info.parameter <= 1): # wenn zwischen tcp un surface punkt liegt
                return True
    return False

def checkIntersectionLineTriangle(gerade, triangle_index, list_triangles_verticesIndex, list_vertices_coordinates, list_triangles_normals):
    # gerade = [[aufpunkt],[richtungsvektor]], 
    # gerade, enthält informationen über oberflächen sowie tcp punkt, = verbindung
    # wobei aufpunkt hier pointSF, zu tcp punkt 
    # und richtungsvektor nicht normiert, verbindung zwischen SFpunkt und tcp punkt
    #     
    # SP = Schnittpunkt gerade mit triagnle_unendliche_ebene, berechnen
    triangle_normal = list_triangles_normals[triangle_index] # normale auslesen
    triangle_normal_norm = np.multiply(triangle_normal, 1/np.linalg.norm(triangle_normal)) # normale normieren
    plane = [list_vertices_coordinates[list_triangles_verticesIndex[triangle_index][0]], triangle_normal_norm] # ebene zu triangle aufstellen
    

    obstacle_info = intersection_patches.solveParameter_intersectionPlaneGerade(plane, gerade) # sp ebene gerade berechnen
    SP_parameter = obstacle_info.parameter

    if(not obstacle_info.b_liegtInEbeneTriangle):
        if SP_parameter is not None: # wenn es einen schnitt gibt
            # es gibt genau eine lösung
            if(SP_parameter > 0 and SP_parameter <= 1): # wenn zwischen tcp un surface punkt liegt
                res_check = checkIntersecctionLineTriangleEdges(SP_parameter, gerade, triangle_index, list_triangles_verticesIndex, list_vertices_coordinates, list_triangles_normals)
                obstacle_info.setObstacle(res_check)
            else: # schnitt nicht zwischenOF punkt und tcp punkt
                #return [False, None]
                obstacle_info.setObstacle(False)
        else: # kein schnitt mit triangle ebene
            #return [False, None]
            obstacle_info.setObstacle(False)

    else: # strahl liegt in ebene

        print("fall: strahlgerade liegt in ebene")
        #SP = None
        #return [True, SP]
        res_check = checkIntersecctionLineInPlane_TriangleEdges(SP_parameter, gerade, triangle_index, list_triangles_verticesIndex, list_vertices_coordinates, list_triangles_normals)
        obstacle_info.setObstacle(res_check)

    return obstacle_info.b_isObstacle

######


# obstacle detection

# ??? ? parameter raus weil unnötig oder ? , triangleIndex_pointSF
def obstacleDetected_point_lineTwoPoints(coordinates_pointSF, coordinates_pointTCP, list_triangles_normals, list_triangle_index, list_triangles_verticesIndex, list_vertices_coordinates):
    # Prüfen, ob ein Hindernis in eigentlcher Strahlrichtung von TCP zur Oberfläche des aktuellen, zu bearbeitenden Punktes liegt.
    # 
    # coordinates_pointSF, triangleIndex_pointSF = angaben zu current pointSF, point on SurFace
    # list_triangles_normals = liste der normalen aller triangles
    # coordinates_pointTCP = coordinates zu pointTCP, punkt des TCP
    # list_triangle_index = liste der inndizes ALLER triangles der geometrie

    check = False # erstmal kein hindernis erkannt

    # gerade aufstellen von pointSF zu pointTCP
    # aufpunkt der geraden ist pointSF
    gerade_pointSFToTCP = linearAlg.getGerade_twoPoints(coordinates_pointSF, coordinates_pointTCP)
    

    # prüfen ob die gerade mit dreieck schneidet
    # funktion checkIntersectionLineTriangle()
    for triangle_index in range(len(list_triangle_index)):
        # sobald ein dreieck ein hindernis darstellt, true returnrn, für "es ist ein hindernis vorhanden." "
        check = checkIntersectionLineTriangle(gerade_pointSFToTCP, triangle_index, list_triangles_verticesIndex, list_vertices_coordinates, list_triangles_normals)
        #print("Hindernis vorliegend/ obstacle found: ", check)
        if(check): # wenn ein triangle gescchnitten wird, dann 
            # wenn triangle triangle_index geschnitten wird von strahlgeraden, dann prüfen, ob schnitt zwischen Strahl als zwischen pointSF und pointTCP liegt, >1 Hindernis , da bei gleich ja das zu treffende surface wäre
            # wenn ja, dann hinderniss, wenn nein kein hindernis
            #check = True # True für hindernis vorhanden
            print("OBSTACLE DETECTED")
            break
    
    return check

"""
def obstacleDetected_point_linePointDirection(gerade, list_triangles_normals, list_triangle_index, list_triangles_verticesIndex, list_vertices_coordinates):
    # Prüfen, ob ein Hindernis in eigentlcher Strahlrichtung von TCP zur Oberfläche des aktuellen, zu bearbeitenden Punktes liegt.
    # 
    # coordinates_pointSF, triangleIndex_pointSF = angaben zu current pointSF, point on SurFace
    # list_triangles_normals = liste der normalen aller triangles
    # coordinates_pointTCP = coordinates zu pointTCP, punkt des TCP
    # list_triangle_index = liste der inndizes ALLER triangles der geometrie

    check = False # erstmal kein hindernis erkannt

    # gerade aufstellen von pointSF zu pointTCP
    # aufpunkt der geraden ist pointSF
    gerade_pointSFToTCP = gerade

    # prüfen ob die gerade mit dreieck schneidet
    # funktion checkIntersectionLineTriangle()
    for triangle_index in range(len(list_triangle_index)):
        # sobald ein dreieck ein hindernis darstellt, true returnrn, für "es ist ein hindernis vorhanden." "
        if(checkIntersectionLineTriangle(gerade_pointSFToTCP, list_triangle_index[triangle_index], list_triangles_verticesIndex, list_vertices_coordinates, list_triangles_normals)): # wenn ein triangle gescchnitten wird, dann 
            # wenn triangle triangle_index geschnitten wird von strahlgeraden, dann prüfen, ob schnitt zwischen Strahl als zwischen pointSF und pointTCP liegt, >1 Hindernis , da bei gleich ja das zu treffende surface wäre
            # wenn ja, dann hinderniss, wenn nein kein hindernis
            check = True # True für hindernis vorhanden
            break
    
    return check
"""


##########
# Funktion to avoid obstacle 

# 
# wenn ein hindernis initial bei einem punkt erkannt wurde, dann diese Funktion verwenden, zur Berechnung einer hindernisfreien Position.
def calcNewTCPPosition_woObstacle(angle_inc, point_coord, index_triangleOfPoint, list_triangles_verticesIndex, list_vertices_coordinates, list_triangles_normals, list_triangle_index):
    # returnt TCP neue coordinates sowie orientierung des TCPS, so dass keein hinterschnitt mehr vorliegt/ im weg liegt. 

    # angle_innc = angle um den position bewegt wird um neue  position zu finden, die kein hindernis mehr aufweist zwischen pointTCP und pointSFNew
    # hierzu verwendung der funktion calcNewPosition_angle() aus  linearAlg


    
    # initiale drehachse wird zu einer beliebigen edge_ofTriangle gesetzt, was einer Kante des triangles entpricht, berechnen:
    # da diese in ebene senkrecht zu n des triangles liegt #########
    edge_ofTriangle = np.subtract(list_vertices_coordinates[list_triangles_verticesIndex[index_triangleOfPoint][0]], list_vertices_coordinates[list_triangles_verticesIndex[index_triangleOfPoint][1]])
    # 1. berechnung der drehachsen, die zur neuen positions bestimmung dienen
    list_drehachsen = []
    # die 0. drehachse ist die 0. edge des triangles, normiert
    drehachse_init = linearAlg.calcVerbindungNorm(list_vertices_coordinates[list_triangles_verticesIndex[index_triangleOfPoint][0]], list_vertices_coordinates[list_triangles_verticesIndex[index_triangleOfPoint][1]])
    list_drehachsen.append(drehachse_init)

    
    Winkel_drehachse_ges = 0.0
    rotmatrix_calcDrehachsen = orientation.getRotationmatrix_drehachseWinkel(list_triangles_normals[index_triangleOfPoint], Winkel_drehachse_ges)
    
    normal = list_triangles_normals[index_triangleOfPoint]
    while(Winkel_drehachse_ges <= 2*np.pi):
        #rotmatrix zu neuem winkel berechnen

        # initiale drehachse wird zu edge_ofTriangle gesetzt, was einer Kante des triangles entpricht
        rotmatrix_calcDrehachsen = orientation.getRotationmatrix_drehachseWinkel(normal, Winkel_drehachse_ges)@edge_ofTriangle
        list_drehachsen.append(rotmatrix_calcDrehachsen*normal)

        # winkel für neuen durchlauf erhöhen
        Winkel_drehachse_ges = Winkel_drehachse_ges + angle_inc


    # neue positionen in schleifen prüfen
    # in äußerer schleife für fixn winkel
    # in zweiter insatnz für    
    # eine fixe drehachse
    winkel_ges_winkel = angle_inc
    
    while(winkel_ges_winkel <= np.pi*2): # bis ein kreisumlauf vollbracht ist, 
        # schleife je winkel
        for i in range(len(list_drehachsen)):
            # drehen mit drehmatrix um list_drehachse[i] um winkel_ges_winkel
            # mithilfe rot matrix, diese aufstellen
            # mittels aktueller list_drehachse[i] sowie dem winkel winkel_ges_winkel
            # und damit den ursprünlichen normalenvekor abbilden
            newOrientation = orientation.getRotationmatrix_drehachseWinkel(list_drehachsen[i], winkel_ges_winkel).dot(normal)
            
            # neuen tcp punkt zu neuer orientierung bestimmen
            newTCP = SurfaceToTCP.PositionSurfaceToTCP(point_coord, newOrientation)
            
            # prüfen, ob für neuen TCP Punkt mit neuer Ausrichtung zu gleichem Punkt auf OF, ein Hindernis vorliegt
            #gibt true aus, wenn hindernis vorliegt.
            if(not obstacleDetected_point_lineTwoPoints(point_coord, newTCP, list_triangles_normals, list_triangle_index, list_triangles_verticesIndex, list_vertices_coordinates)):
                # also fall: kein hindernis: 
                newPoint_TCP = newTCP
                newOrientation_normal = newOrientation
                #print("\n R: newOrientation_normal = ", newOrientation_normal)
                #print("newPoint_TCP = ", newPoint_TCP)
                return [True, [newPoint_TCP, newOrientation_normal]] # True = neue Position ohne Hindernis gefunden
                # rückgabe der neuen Position
                break
        
        winkel_ges_winkel = winkel_ges_winkel + angle_inc
    #print("\n R: point_coord = ", point_coord)
    return [False, [point_coord]] # False = keine passende Poition gefunden, 
    # rückgabe des alten punktes der Of, damit später in pfad prüfen, ob false oder ttrue, wenn false, dann den wert in 1 aus der liste der punkte removen. 