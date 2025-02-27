# mainFunction.py

#beinhaltet main Funktion, welche den Pfad zu einer geometrie berechnet. 

#import 
import numpy as np
import trimesh

import data_structure
import patches
import planes
import intersection_patches
import SurfaceToTCP
import orientation
import obstacle
import Hauptachsensystem
import sortPatches

import writeCsvFile
import write_file_job
import csv

# zur Messung der Laufzeiten
import time
# time variablen, welche zusammmenaddiert werden müsen global definieren, damit nicht aus funktion übergeben werden muss
# time var zu 0.0 setzen, damit dann je funktion für alle patches innerhalb schleife aufaddiert werden kann

# time_einlesen
time_einlesen = 0.0
# time_has
time_has = 0.0
# time_patch
time_patch = 0.0
# time_intersection 
time_intersection = 0.0
# time_TCPKoord 
time_TCPKoord = 0.0
# time_hindernis
time_hindernis = 0.0
# time_KOSTrafo
time_KOSTrafo = 0.0
# time_patchSort
time_patchSort = 0.0

anzahl_triangles = 0
anzahl_knoten = 0



#####
# eingabeparameter
from eingabeparameter import path_stl, hinterschnitt, anlge_patches, angle_hindernisAusweichen


# eingabeparameter zum Schreiben der Job-Datei
from eingabeparameter import name_jobDatei, werkzeugnummer, geschwindigkeit_movl, geschwindigkeit_movj, timer
#####




def getTCPPoseData(path_stl): 

    # gloable var übergeben
    # time_einlesen
    global time_einlesen
    # time_has
    global time_has
    # time_patch
    global time_patch
    # time_patchSort
    global time_patchSort

    # anzahl
    global anzahl_triangles 
    global anzahl_knoten


    time_before_temp = time.time()

    # 1. 
    # data_structure.py
    # Daten einlesen aus stl datei 

    # einlesen der geometrie m.H. trimesh lib 
    trimesh_geometry = trimesh.load_mesh(path_stl, "stl")
    #vertices_coordinates, vertices_triangleIndex, edges_verticesIndex, edges_trianglesIndex, triangles_edgesIndex, triangles_verticesIndex, triangles_normals = data_structure.getLists_VerticesEdgesTriangles(trimesh_geometry)
    list_vertices_coordinates, list_vertices_triangleIndex, list_edges_verticesIndex, list_edges_trianglesIndex, list_triangles_edgesIndex, list_triangles_verticesIndex, list_triangles_normals = data_structure.getLists_VerticesEdgesTriangles(trimesh_geometry)

    anzahl_triangles = len(list_triangles_verticesIndex)
    anzahl_knoten = len(list_vertices_triangleIndex)
    # time einlesen 
    time_temp = time.time() 
    time_einlesen = time_temp - time_before_temp
    time_before_temp = time_temp

    # return list_vertices_coordinates, list_vertices_triangleIndex, list_edges_verticesIndex, list_edges_trianglesIndex, list_triangles_edgesIndex, list_triangles_verticesIndex, list_triangles_normals

    # 2. 
    # patches.py
    # patches bilden mit Funktion getPatches()

    # !!! !
    # index_triangleInit !!! ! Noch funktion mit HAS EINFÜGEN ! SCHREIBEN

    # list_triangles_trianglesIndex anlegen
    # durchnummeriern der triangels
    list_triangles_trianglesIndex = []
    for i in range(len(list_triangles_edgesIndex)):
        list_triangles_trianglesIndex.append(i)

    # zu bestimmung des initialen trianngles, HAS ermitteln
    mainAxis = Hauptachsensystem.mainAxis3D(np.pi/100, trimesh_geometry)
    mainAxis6 = Hauptachsensystem.getMainAxis6(mainAxis)
    # initiales dreieck bestimmen: 
    index_triangleInit = Hauptachsensystem.getIndexTriangleMainAxis(mainAxis6, list_triangles_normals)
    
    # time HAS
    time_temp = time.time()
    time_has = time_temp - time_before_temp
    time_before_temp = time_temp

    # patches erstllen 
    list_patches_trianglesIndex = patches.getPatches(index_triangleInit, list_triangles_trianglesIndex, list_triangles_edgesIndex, list_triangles_normals, anlge_patches)
    
    # time patch
    time_temp = time.time()
    time_patch = time_temp - time_before_temp
    time_before_temp = time_temp
    
    #print("list_patches_trianglesIndex = ", list_patches_trianglesIndex)



    # return patches_list,
    # liste mit listen aller patches, wobei diese wiederum je aus den indizes der triangles besteht, welche das patch bilden 

    # liste der sortierten normalen vektoren zu jeddempatch erstellen
    list_normals_patch = []
    for i in range(len(list_patches_trianglesIndex)): # je patch
        list_normals_patch.append([])
        for j in range(len(list_patches_trianglesIndex[i])):
            list_normals_patch[i].append(list_triangles_normals[list_patches_trianglesIndex[i][j]])

                # PATCHWISE START
                # 3.
                # intersection_patches.py
                # Bilden eines Zickzack Pfades für die Patches

                # je Patch ergibt sich Pfad mmit Hilfe der Funktion intersectionPoints_trianglesPatchPlaneSchar(list_triangle_verticesIndex,  list_vertices_coordinates, patch, planeSchar, list_triangles_normal)
                # je Patch return liste der points on surface und liste der triangleIndizes je point, gleich sortiert

                # d.h. Schleife für alle Patches schreiben, welche die oben genannte funktion für alle Patches durchführt. 
                # und ergebnis in eine Liste schreibt, mit Liste je Patch von [ergebnis aus je Patch]


                # return list_patches_pointsOnSF_and_triangleIndizes

                # 4.
                # SurfaceToTCP.py
                # je Patch: je point: Bestimmung der TCP Position anhand der SurfacePoints, je point püfen, ob hindernis, 
                #                                                                                           wenn ja:   dann neue, alternative TCPPos, und newOrientierungOF berechnen, 
                #                                                                                           wenn nein: standardmäßige TCPPos berechnung, und OrientierungOF

                # 5. 
                # je Patch: je [Point, Orientation] 

                # 5 a. 
                # SurfaceToTCP.py
                # point transformieren, mit Hilfe der Funktion KOSTrafo_StlToRob, Eingabe ist der point in STL KOS

                # return sortierte Liste aller [pointTCP] je ppoint des pfades je patch

                # 5 b. 
                # orientation.py
                # orientierung des Manipulators bestimmen, anhand der OrientierungOF, mit Funktion 
                #                                                                     1. getRotationmatrix()
                #                                                                     2. getRollNickYaw()
                #                                                                     3. radToDeg()

                # return sortierte Liste aller [Roll Nick Yaw Winkel in Grad] je point des pfades je patch

                # 5 c. 
                # daten sortiert aneinander hängen sodass sich je patch, eine liste ergibt mit je [[point],[TCPOrientation]]

                # PATCHWISE END

    """
    nrPatch = 5
    print("patch 0 = ", list_patches_trianglesIndex[nrPatch])
    print("list_normals_patch[0] = ", list_normals_patch[nrPatch])
    
    patchData_0 = getTCPPoseData_patch(list_triangles_verticesIndex,  list_vertices_coordinates, list_normals_patch[nrPatch], list_patches_trianglesIndex[nrPatch], list_triangles_normals, list_triangles_trianglesIndex)
    #getTCPPoseData_patchTEST(list_triangles_verticesIndex,  list_vertices_coordinates, list_normals_patch[nrPatch], list_patches_trianglesIndex[nrPatch], list_triangles_normals, list_triangles_trianglesIndex)
    
    fileName_verticesOfPatch = "allVertices_ofPatch_" + str(nrPatch) + ".csv"
    writeCsvFile.patchToVerticesList(list_patches_trianglesIndex[nrPatch], list_triangles_verticesIndex, list_vertices_coordinates, fileName_verticesOfPatch)       
    

    print("\n \n ")
    for i in range(len(list_normals_patch)):
        print("Patch nr. :", i, "     :  ", list_normals_patch[i])
    print("\n \n ")
    """




    patchData = []
    if(hinterschnitt): # falls hinterschnitt, dann mit getTCPPoseData_patch_withObstacle berechnen
        for i in range(len(list_patches_trianglesIndex)):
            #print("patch i : ", i)
            # list_normals patch raus, da ich das in funktion selbst auslese
            patchData.append(getTCPPoseData_patch_withObstacle(list_triangles_verticesIndex,  list_vertices_coordinates, list_patches_trianglesIndex[i], list_triangles_normals, list_triangles_trianglesIndex, i))
    else: # falls kein hinterschnitt, dann mit getTCPPoseData_patch_woObstacle berechnen
        for i in range(len(list_patches_trianglesIndex)):
            #print("patch i : ", i)
            patchData.append(getTCPPoseData_patch_woObstacle(list_triangles_verticesIndex,  list_vertices_coordinates, list_patches_trianglesIndex[i], list_triangles_normals, list_triangles_trianglesIndex, i))
            
    #print("\n \n \n patchData[0] = ", patchData[0])
    #print("\n \n \n ")
    
    # patchData ergebnisse runden, damit Roboter annimmt, auf 2 nachkommastellen
    # und entsprechend wieder in gleichem Format zurückgeben 
    patchData_gerundet = []
    for i in range(len(patchData)): # je patch
        patchData_gerundet.append([])
        for j in range(len(patchData[i])): #immer länge = 2: 0 ist koord, 1 sind winkel
            patchData_gerundet[i].append([]) # zwei listen anlegen je patch i
            for k in range(len(patchData[i][j])): # anzahl der anzufahrenden posen des patches 
                #patchData_gerundet[i][j].append([]) # je koord, bzw winkel (k) liste anlegen
                #for l in range(len(patchData[i][j][k])): # l konstant 3, entweder bei j = 0 3 koord, oder bei j = 1, 3 winkel
                    # einzelwerte runden
                    
                    # sehr kleine Werte zu null setzen
                    #if(patchData[i][j][k] < 0.01): # nur zwei nachkommastellen
                    #    patchData_gerundet[i][j][k].append(0.00) # k. koord bzw winkel gerundeten wert anhängen
                    #else:

                # listen runden
                patchData_gerundet[i][j].append(np.round_(patchData[i][j][k], decimals = 2))


    # Fall, basierend auf Joint Limits:
    # Winkelangaben: [0.0,90.0,0.0], [180,-90,0] geben gleiche z düsen ausrichtung, aber letzteres ist jointlimit freundlich
    for i in range(len(patchData_gerundet)):
        for j in range(len(patchData_gerundet[i][1])): # 1 da winkel betrachtet werden, also für alle winkelsätze j...#
            if(data_structure.checkVectorEqual(patchData_gerundet[i][1][j], [0.0,90.0,0.0])): # wenn SOFA
                # wert auf joint limit freundlichen wert setzen
                patchData_gerundet[i][1][j][0] = 180.0
                patchData_gerundet[i][1][j][1] = -90.0
                patchData_gerundet[i][1][j][2] = 0.0







    # patchData nach patches sortieren
    # patches aneinander sortieren


    # 6.
    # 
    # sortieren der patches
    # durch bestimmung des normal avg je patch, 
    # systematisch über winkeldifferenz als maß, die patchesPfade sortieren
    time_before_temp = time.time()
    #print("patchsort time_before_temp = ", time_before_temp)
    list_patches_patchIndex_sorted = sortPatches.sortPatches(list_patches_trianglesIndex, list_triangles_normals, [0,0,-1])    


    #list_patches_patchIndex_sorted enthält indizes der patches, in richtiger sortierung
    
    
    patchData_sorted = []
    for patchIndex_sorted in list_patches_patchIndex_sorted:
        patchData_sorted.append(patchData_gerundet[patchIndex_sorted])
    
    
    # time patchSort
    time_temp = time.time()
    time_patchSort = time_temp - time_before_temp
    time_before_temp = time_temp
    
    #print("patchsort time_temp = ", time_temp)
    # 7. Job Datei erstellen
    # writeJobDat.py
    # einlesen der einen liste, die aus 6. kommt und überführen

    # overall return ist dann die Job Datei :)

    # times printen 
    #print("\n \n \n TIME: time_einlesen = ", time_einlesen, "\n time_has = ", time_has,  "\n time_patch = ", time_patch,  "\n time_intersection = ", time_intersection,  "\n time_TCPKoord = ", time_TCPKoord,  "\n time_hindernis = ", time_hindernis, "\n time_KOSTrafo = ", time_KOSTrafo, "\n time_patchSort = ", time_patchSort)


    return patchData_sorted # TEST !!! !
    

    
    #test_5_coord, test_5_orientierung = getTCPPoseData_patch_woObstacle(list_triangles_verticesIndex,  list_vertices_coordinates, list_normals_patch[5], list_patches_trianglesIndex[5], list_triangles_normals, list_triangles_trianglesIndex, 5)
    #print("\n \n test_5_coord = ", test_5_coord)
    #print("\n \n test_5_orientierung = ", test_5_orientierung)
    #return patchData_sorted

###############################

#   getTCPPoseData_patch(list_triangles_verticesIndex,  list_vertices_coordinates, list_normals_patch[nrPatch], list_patches_trianglesIndex[nrPatch], list_triangles_normals, list_triangles_trianglesIndex)
def getTCPPoseData_patch_woObstacle(list_triangles_verticesIndex,  list_vertices_coordinates, patch, list_triangles_normal, list_triangles_trianglesIndex, nrPatch): 
    # d.h. später Schleife für alle Patches schreiben, welche die definierete funktion für alle Patches durchführt. 
    # und ergebnis in eine Liste schreibt, mit Liste je Patch von [ergebnis aus je Patch]

    # globale var für die zeit übergeben
    # time_intersection 
    global time_intersection 
    # time_TCPKoord 
    global time_TCPKoord
    # time_hindernis
    global time_hindernis
    # time_KOSTrafo
    global time_KOSTrafo


    time_before_temp = time.time()# aktuelle laufzeit auslesen

    # patch = list_patches_trianglesIndex[i] 

    # PATCHWISE START, i-tes Patch
    # 3.
    # intersection_patches.py
    # Bilden eines Zickzack Pfades für die Patches

    # je patch sortierte liste der normalenvektoren des patches
    list_normals_patch = []
    for triangleIndex in patch: # für jedes triangle des patches 
        list_normals_patch.append(list_triangles_normal[triangleIndex])
        # sortiert nach sotierung der triangles in patch 
    

    # je Patch ergibt sich Pfad mmit Hilfe der Funktion intersectionPoints_trianglesPatchPlaneSchar(list_triangle_verticesIndex,  list_vertices_coordinates, patch, planeSchar, list_triangles_normal)
    # je Patch return liste der points on surface und liste der triangleIndizes je point, gleich sortiert
    planeSchar = planes.getEbenenSchar_patch(patch, list_normals_patch, list_triangles_verticesIndex, list_vertices_coordinates) 
    listIntersection_PatchSchar_sorted_pointsInPlaneGroup, listTriIndex_sorted = intersection_patches.intersectionPoints_trianglesPatchPlaneSchar(list_triangles_verticesIndex,  list_vertices_coordinates, patch, planeSchar, list_triangles_normal)
    
    # listIntersection_PatchSchar_sorted_pointsInPairs in gelihcer reihenfolge von paaren lösen
    listIntersection_PatchSchar_sorted = []
    for i in range(len(listIntersection_PatchSchar_sorted_pointsInPlaneGroup)):
        
        for j in range(len(listIntersection_PatchSchar_sorted_pointsInPlaneGroup[i])):
            listIntersection_PatchSchar_sorted.append(listIntersection_PatchSchar_sorted_pointsInPlaneGroup[i][j])
            #listIntersection_PatchSchar_sorted.append(listIntersection_PatchSchar_sorted_pointsInPlaneGroup[i][j])
    # return list_patches_pointsOnSF_and_triangleIndizes
    # !!! ! ??? ? PRÜFEN, OB PUNKTE AUSGABE IN PUNKTEPAAREN IST ODER IN EINZELNEN PUNKTEN? , glaub einzeln 

    # list_normals_sorted erstellen 
    # sortiert nach sortierung der intersectionPoints
    list_normals_sorted = []
    for triangleIndex in listTriIndex_sorted:
        #print(triangleIndex)
        list_normals_sorted.append(list_triangles_normal[triangleIndex])
    
    # hier return list_normals_sorted ()zu den intersection points)

   
    # time_intersectoin
    time_temp = time.time()
    time_intersection = time_intersection + time_temp - time_before_temp
    time_before_temp = time_temp

    # 4.
    # SurfaceToTCP.py
    # je Patch: je point: Bestimmung der TCP Position anhand der SurfacePoints, je point püfen, ob hindernis, 
    #                                                                                           wenn ja:   dann neue, alternative TCPPos, und newOrientierungOF berechnen, 
    #                                                                                           wenn nein: standardmäßige TCPPos berechnung, und OrientierungOF

    TCP_coordinates_0 = [] # liste ohne hindernis erkennung
    TCP_orientation_0 = [] # in rad
    

    
    #filename = "pointsSF_koord_patch" + str(nrPatch) + "_woObstacle.csv"
    #writeCsvFile.write_list_to_csv_dat(filename, listIntersection_PatchSchar_sorted)

    #print("\n list_normals_sorted = ", list_normals_sorted)
    
    for i in range(len(listIntersection_PatchSchar_sorted)):
        # Berechnung der TCP_coordinatesnewOrientation_normal
        TCP_coordinates_0.append(SurfaceToTCP.PositionSurfaceToTCP(listIntersection_PatchSchar_sorted[i], list_normals_sorted[i]))
        # Berechnung der Orientation
        #print("i = ", i)
        # Umstellung für Winkelberechnung
        
        rotmatrix_temp = orientation.getRotationmatrix(list_normals_sorted[i])
        rollPitchYaw_temp = orientation.getRollPitchYaw(rotmatrix_temp)
        """
        if(i != len(listIntersection_PatchSchar_sorted)-1):
            rollPitchYaw_temp = orientation.getRollPitchYaw_pathPoint(listIntersection_PatchSchar_sorted[i], listIntersection_PatchSchar_sorted[i+1], list_normals_sorted[i])
        else: # für letzte Orientierung 
            rollPitchYaw_temp = orientation.getRollPitchYaw_pathPoint(listIntersection_PatchSchar_sorted[i-1], listIntersection_PatchSchar_sorted[i], list_normals_sorted[i])
        """
        #HIER
        #print("rotmatrix_temp = ", rotmatrix_temp)
        #print("     list_normals_sorted[i] = ", list_normals_sorted[i])
        #print("     rollPitchYaw_temp = ", rollPitchYaw_temp, "\n ")
        TCP_orientation_0.append(rollPitchYaw_temp)
        #TCP_orientation_0.append(orientation.getRollPitchYaw(orientation.getRotationmatrix(list_normals_sorted[i])))
        
    
    #filename = "pointsTCP_koord_patch" + str(nrPatch) + "_woObstacle.csv"
    #writeCsvFile.write_list_to_csv_dat(filename, TCP_coordinates_0)

    # time_TCPKoord
    time_temp = time.time()
    time_TCPKoord = time_TCPKoord + time_temp - time_before_temp
    time_before_temp = time_temp


    # KOS TRAFO FÜR coordinates durchführen
    
    TCP_coordinates = [] # liste mit hinderniserkennung und ausweicchen
    TCP_orientation = [] # in rad


    for i in range(len(TCP_coordinates_0)):
        TCP_coordinates.append(SurfaceToTCP.KOSTrafo_StlToRob(TCP_coordinates_0[i]))

    #filename = "ROBKOS_pointsTCP_koord_patch" + str(nrPatch) + "_woObstacle.csv"
    #writeCsvFile.write_list_to_csv_dat(filename, TCP_coordinates)

    TCP_orientation_deg = []
    for i in range(len(TCP_orientation_0)):
        #TCP_orientation_deg.append(orientation.setzeWinkelWertekleinerErrorzuNullDeg(orientation.radToDeg_list(TCP_orientation_0[i])))        
        TCP_orientation_deg.append(orientation.radToDeg_list(TCP_orientation_0[i]))

    #print("Patch:", nrPatch, ", \\ TCP_orientation_0 = ", TCP_orientation_0, ", \\ TCP_orientation_deg = ", TCP_orientation_deg)

    
    # return sortierte Liste aller [Roll Nick Yaw Winkel in Grad] je point des pfades je patch

    # 5 c. 
    # daten sortiert aneinander hängen sodass sich je patch, eine liste ergibt mit je [[point],[TCPOrientation]]
    list_patch_pointTCP_orientationTCP = []
    list_patch_pointTCP_orientationTCP.append(TCP_coordinates)
    list_patch_pointTCP_orientationTCP.append(TCP_orientation_deg)

    
    # time_KOSTrafo
    time_temp = time.time()
    time_KOSTrafo = time_KOSTrafo + time_temp - time_before_temp
    time_before_temp = time_temp


    return list_patch_pointTCP_orientationTCP

###############################


def getTCPPoseData_patch_withObstacle(list_triangles_verticesIndex,  list_vertices_coordinates, patch, list_triangles_normal, list_triangles_trianglesIndex, nrPatch): 
    # d.h. später Schleife für alle Patches schreiben, welche die definierete funktion für alle Patches durchführt. 
    # und ergebnis in eine Liste schreibt, mit Liste je Patch von [ergebnis aus je Patch]

    
    # globale var für die zeit übergeben
    # time_intersection 
    global time_intersection 
    # time_TCPKoord 
    global time_TCPKoord
    # time_hindernis
    global time_hindernis
    # time_KOSTrafo
    global time_KOSTrafo


    time_before_temp = time.time() # aktuelle laufzeit auslesen

    # patch = list_patches_trianglesIndex[i] 

    # PATCHWISE START, i-tes Patch
    # 3.
    # intersection_patches.py
    # Bilden eines Zickzack Pfades für die Patches

    # je patch sortierte liste der normalenvektoren des patches
    list_normals_patch = []
    for triangleIndex in patch: # für jedes triangle des patches 
        list_normals_patch.append(list_triangles_normal[triangleIndex])
        # sortiert nach sotierung der triangles in patch 
    

    # je Patch ergibt sich Pfad mmit Hilfe der Funktion intersectionPoints_trianglesPatchPlaneSchar(list_triangle_verticesIndex,  list_vertices_coordinates, patch, planeSchar, list_triangles_normal)
    # je Patch return liste der points on surface und liste der triangleIndizes je point, gleich sortiert
    planeSchar = planes.getEbenenSchar_patch(patch, list_normals_patch, list_triangles_verticesIndex, list_vertices_coordinates) 
    listIntersection_PatchSchar_sorted_pointsInPlaneGroup, listTriIndex_sorted = intersection_patches.intersectionPoints_trianglesPatchPlaneSchar(list_triangles_verticesIndex,  list_vertices_coordinates, patch, planeSchar, list_triangles_normal)
    
    # listIntersection_PatchSchar_sorted_pointsInPairs in gelihcer reihenfolge von paaren lösen
    listIntersection_PatchSchar_sorted = []
    for i in range(len(listIntersection_PatchSchar_sorted_pointsInPlaneGroup)):
        
        for j in range(len(listIntersection_PatchSchar_sorted_pointsInPlaneGroup[i])):
            listIntersection_PatchSchar_sorted.append(listIntersection_PatchSchar_sorted_pointsInPlaneGroup[i][j])
            #listIntersection_PatchSchar_sorted.append(listIntersection_PatchSchar_sorted_pointsInPlaneGroup[i][j])
    # return list_patches_pointsOnSF_and_triangleIndizes
  
    # list_normals_sorted erstellen 
    # sortiert nach sortierung der intersectionPoints
    list_normals_sorted = []
    for triangleIndex in listTriIndex_sorted:
        list_normals_sorted.append(list_triangles_normal[triangleIndex])
    

    # 4.
    # SurfaceToTCP.py
    # je Patch: je point: Bestimmung der TCP Position anhand der SurfacePoints, je point püfen, ob hindernis, 
    #                                                                                           wenn ja:   dann neue, alternative TCPPos, und newOrientierungOF berechnen, 
    #                                                                                           wenn nein: standardmäßige TCPPos berechnung, und OrientierungOF

    TCP_coordinates_0 = [] # liste ohne hindernis erkennung
    TCP_orientation_0 = [] # in rad
    
    #filename = "SF_koord_patch" + str(nrPatch) + "_withObstacle.csv"
    #writeCsvFile.write_list_to_csv_dat(filename, listIntersection_PatchSchar_sorted)
    
    # time_intersection
    time_temp = time.time()
    time_intersection = time_intersection + time_temp - time_before_temp
    time_before_temp = time_temp

    
    for i in range(len(listIntersection_PatchSchar_sorted)):
        # Berechnung der TCP_coordinatesnewOrientation_normal
        TCP_coordinates_0.append(SurfaceToTCP.PositionSurfaceToTCP(listIntersection_PatchSchar_sorted[i], list_normals_sorted[i]))
        # Berechnung der Orientation
        rotmatrix_temp = orientation.getRotationmatrix(list_normals_sorted[i])
        rollPitchYaw_temp = orientation.getRollPitchYaw(rotmatrix_temp)
        #print("rotmatrix_temp = ", rotmatrix_temp)
        #print("     list_normals_sorted[i] = ", list_normals_sorted[i])
        #print("     rollPitchYaw_temp = ", rollPitchYaw_temp, "\n ")
        TCP_orientation_0.append(rollPitchYaw_temp)
        #TCP_orientation_0.append(orientation.getRollPitchYaw(orientation.getRotationmatrix(list_normals_sorted[i])))
        
    
    # time_TCPKoord
    time_temp = time.time()
    time_TCPKoord = time_TCPKoord + time_temp - time_before_temp
    time_before_temp = time_temp

    # KOS TRAFO FÜR coordinates durchführen
    
    TCP_coordinates = [] # liste mit hinderniserkennung und ausweicchen
    TCP_orientation = [] # in rad

    #hiervor csv datei schreiben

    ##for i in range(len(TCP_coordinates_0)):
    ##    TCP_coordinates.append(SurfaceToTCP.KOSTrafo_StlToRob(TCP_coordinates_0[i]))

    #print("\n TCP_coordinates = ", TCP_coordinates)
    
    # Hindernis detection
    # für jeden punkt durchführen aus listIntersection_PatchSchar_sortedTCP_coordinates_0[i]
    # für den erdsten punkt durchführen:
    for i in range(len(TCP_coordinates_0)):
        # obstacle.obstacleDetected_point_lineTwoPoints() returnt True bei einem "Hindernis", und False bei "kein Hindernis"
        # prüfen, ob HIndernis auftritt für den aktuellen punkt i
        #print("\n i = ", i)
        #print("\n listIntersection_PatchSchar_sorted[i] = ", listIntersection_PatchSchar_sorted[i])
        #print("\n TCP_coordinates_0[i] = ", TCP_coordinates_0[i], "\n ")
        #print("\n list_triangles_trianglesIndex = ", list_triangles_trianglesIndex, "\n ")
        if(obstacle.obstacleDetected_point_lineTwoPoints(listIntersection_PatchSchar_sorted[i], TCP_coordinates_0[i], list_triangles_normal, list_triangles_trianglesIndex, list_triangles_verticesIndex, list_vertices_coordinates)):
            print("\n i = ", i, ":       HINDERNIS an: ", listIntersection_PatchSchar_sorted[i] )

            # true, wenn hindernis vorliegend
            # berechnung einer neuen TCP Position, mittels calcNewTCPPosition_woObstacle()
            temp_boo_pos = obstacle.calcNewTCPPosition_woObstacle(angle_hindernisAusweichen, listIntersection_PatchSchar_sorted[i], listTriIndex_sorted[i], list_triangles_verticesIndex, list_vertices_coordinates, list_triangles_normal, list_triangles_trianglesIndex)
            if(temp_boo_pos[0]): # wenn anfahren möglich, d.h. eine neie position gefuden wurde
                # dann die neue gefundene tcp position speichern
                # und die neue orientierung entsprechend berechnen und speichern
                temp_TCP_coordinates = temp_boo_pos[1][0]
                TCP_coordinates.append(temp_TCP_coordinates) 

                #print("\n R: TCP_coordinates[i] = ", TCP_coordinates[i])
                #print("\n R: listIntersection_PatchSchar_sorted[i] = ", listIntersection_PatchSchar_sorted[i])
                TCP_orientation.append(orientation.getRollPitchYaw(orientation.getRotationmatrix(np.subtract(temp_TCP_coordinates, listIntersection_PatchSchar_sorted[i]))))
            # 
            #else: # anfahren nicht möglich,
                # Anm.: lösung könnten sein angle_hindernisAusweichen zu verfeinern, falls dies nichts nützt, punkt nicht erreichbar

                # alte tcp_position nicht in neue liste schreiben, d.h. einfach rausnehmen. 
        else: # falls kein hindernis vorliegt
            # ursrprüngliche coord und winkel in liste speichern 
            TCP_coordinates.append(TCP_coordinates_0[i]) # neu raus
            TCP_orientation.append(TCP_orientation_0[i]) # neu raus

            ###
    

    TCP_orientation_deg = []
    for i in range(len(TCP_orientation_0)):
        #TCP_orientation_deg.append(orientation.setzeWinkelWertekleinerErrorzuNullDeg(orientation.radToDeg_list(TCP_orientation_0[i])))        
        TCP_orientation_deg.append(orientation.radToDeg_list(TCP_orientation_0[i]))        

    
    # time_hindernis
    time_temp = time.time()
    time_hindernis = time_hindernis + time_temp - time_before_temp
    time_before_temp = time_temp

    # KOS TRAFO FÜR coordinates durchführen
    
    TCP_coordinates_trafo = [] # liste mit hinderniserkennung und ausweicchen
    #TCP_orientation = [] # in rad


    for i in range(len(TCP_coordinates)):
        TCP_coordinates_trafo.append(SurfaceToTCP.KOSTrafo_StlToRob(TCP_coordinates[i]))

    
    #filenametcp = "TCP_koord_patch" + str(nrPatch) + "_withObstacle.csv"
    #writeCsvFile.write_list_to_csv_dat(filenametcp, TCP_coordinates_0)
    
    #filenametcp = "TCP_rollPitchYaw_patch" + str(nrPatch) + "_withObstacle.csv"
    #writeCsvFile.write_list_to_csv_dat(filenametcp, TCP_orientation_deg)
    # return TCP_coordinates, TCP_orientation_deg

                # 5. 
                # je Patch: je [Point, Orientation] 

                # 5 a. 
                # SurfaceToTCP.py
                # point transformieren, mit Hilfe der Funktion KOSTrafo_StlToRob, Eingabe ist der point in STL KOS

                # return sortierte Liste aller [pointTCP] je ppoint des pfades je patch

                # 5 b. 
                # orientation.py
                # orientierung des Manipulators bestimmen, anhand der OrientierungOF, mit Funktion 
                #                                                                     1. getRotationmatrix()
                #                                                                     2. getRollNickYaw()
                #                                                                     3. radToDeg()

    # return sortierte Liste aller [Roll Nick Yaw Winkel in Grad] je point des pfades je patch

    # 5 c. 
    # daten sortiert aneinander hängen sodass sich je patch, eine liste ergibt mit je [[point],[TCPOrientation]]
    list_patch_pointTCP_orientationTCP = []
    list_patch_pointTCP_orientationTCP.append(TCP_coordinates_trafo)
    list_patch_pointTCP_orientationTCP.append(TCP_orientation_deg)

    
    # time_KOSTrafo
    time_temp = time.time()
    time_KOSTrafo = time_KOSTrafo + time_temp - time_before_temp
    time_before_temp = time_temp
    
    
    return list_patch_pointTCP_orientationTCP

###############################




 
# Eingabe der Eingabeparameter:
# zum Erstellen der Job-Datei
from eingabeparameter import name_jobDatei, werkzeugnummer, geschwindigkeit_movl, geschwindigkeit_movj, timer

def main():
    time_before_temp = time.time()

    
    time_0 = time_before_temp

    pathData = getTCPPoseData(path_stl)

    # time pathData
    time_temp = time.time()
    time_pathData = time_temp - time_before_temp
    time_before_temp = time_temp

    RCONF_list_24int = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    write_file_job.JBI_file(name_jobDatei, werkzeugnummer, timer, "ROBOT", RCONF_list_24int, "2023/06/15 08:00", "ROBOT", geschwindigkeit_movl, geschwindigkeit_movj, pathData)
    
    # time writeJobFile
    time_temp = time.time()
    time_writeJobFile = time_temp - time_before_temp
    time_before_temp = time_temp

    time_ges = time.time()-time_0
    
    
    # times printen 
    #print("\n \n \n TIME: time_pathData = ", time_pathData, "\n time_writeJobFile = ", time_writeJobFile,  "\n time_ges =", time_ges)

    
    # globale var für die zeit übergeben
    # time_einlesen
    global time_einlesen
    # time_has
    global time_has
    # time_patch
    global time_patch
    # time_intersection 
    global time_intersection 
    # time_TCPKoord 
    global time_TCPKoord
    # time_hindernis
    global time_hindernis
    # time_KOSTrafo
    global time_KOSTrafo
    # time_time_patchSort
    global time_patchSort

    #print("\n \n \n TIME: time_einlesen = ", time_einlesen, "\n time_has = ", time_has,  "\n time_patch = ", time_patch,  "\n time_intersection = ", time_intersection,  "\n time_TCPKoord = ", time_TCPKoord,  "\n time_hindernis = ", time_hindernis, "\n time_KOSTrafo = ", time_KOSTrafo, "\n time_patchSort = ", time_patchSort)

    # anzahl
    global anzahl_triangles 
    global anzahl_knoten

    #print("\n anzahl_triangles = ", anzahl_triangles, "\n anzahl_knoten = ", anzahl_knoten)
    

    # Ergebnisse in Datei speichern

    #geometry = "Quader"
    #bahnabstand = 5.0

    #filename = "Laufzeit_" + str(geometry) + "_" + str(bahnabstand)
    #with open(filename, 'w', newline='') as txtfile:
    #    txtfile.write("\n anzahl_triangles = "+ str(anzahl_triangles) + "\n anzahl_knoten = "+ str(anzahl_knoten))
    #    txtfile.write("\n \n \n TIME: time_pathData = "+ str(time_pathData)+ ", "+ str(time_pathData/time_ges*100)+ "\n time_writeJobFile = "+ str(time_writeJobFile)+ ", "+ str(time_writeJobFile/time_ges*100)+  "\n time_ges ="+ str(time_ges) +", "+ str(time_ges/time_ges*100))
    #    txtfile.write("\n \n \n TIME: time_einlesen = "+ str(time_einlesen)+", "+ str(time_einlesen/time_ges*100)+ "\n time_has = "+ str(time_has)+", "+ str(time_has/time_ges*100)+  "\n time_patch = "+ str(time_patch)+", "+ str(time_patch/time_ges*100)+  "\n time_intersection = "+ str(time_intersection)+", "+ str(time_intersection/time_ges*100)+  "\n time_TCPKoord = "+ str(time_TCPKoord)+", "+ str(time_TCPKoord/time_ges*100)+  "\n time_hindernis = "+ str(time_hindernis)+", "+ str(time_hindernis/time_ges*100)+ "\n time_KOSTrafo = "+ str(time_KOSTrafo)+", "+ str(time_KOSTrafo/time_ges*100)+ "\n time_patchSort = "+ str(time_patchSort)+", "+ str(time_patchSort/time_ges*100))

    #print("\r\n", str(geometry) + ", ", str(bahnabstand) + " written to file ", filename) 
    
###############################

