# sort patches.py

import numpy as np

import planes
import linearAlg
import data_structure

normal_patchesMitNormalAvgRaus = [0.0,0.0,-1.0] # normale die nicht in Pfad einsortiert wird, da sie die Einspannung / AuflageFläche darstellt. 
winkel_krit = np.pi/4

def sortPatches(list_patches_triangleIndex, list_triangles_normals, normal_patchesMitNormalRaus):
    #
    #
    # ausgabe der sortierten pacth indizes
    list_patchIndex_sorted = []

    # liste der übrigen patchesIndizes, die noch nicht sortiert 
    list_patchIndex_übrig = []
    for i in range(len(list_patches_triangleIndex)): # für jede patch index merken
        list_patchIndex_übrig.append(i)
    
    # mittlere normalen vektroen je patch bestimmen: 
    list_patches_normals = [] # liste, je patch liste mit allen normalenvektoren des patches
    list_patches_normalAvg = [] # liste, je patch der mittlere Normalenvektro als eintrag
    # beide sortiert nach patch index
    for i in range(len(list_patches_triangleIndex)): # für jedes patch
        list_patches_normals.append([])
        # mittleren Normalen vektor bestimmen:
        # je patch liste in der list_patches_normals speichern, in der je alle normals enthalten
        for triangleIndex in list_patches_triangleIndex[i]:
            list_patches_normals[i].append(list_triangles_normals[triangleIndex])

        # normal avg des aktuellen (i ten) patch bestimmen und in liste list_patches_normalAvg speichern
        list_patches_normalAvg.append(planes.calcNormalAvg(list_patches_normals[i]))

    # 1. patch so wählen, dass ausrichtung möglichst nahe an -x
    achse = [-1, 0, 0]
    list_angleNormalAvgX = []
    for i in range(len(list_patches_normalAvg)): # je patch
        list_angleNormalAvgX.append(linearAlg.calcAngleVectors(list_patches_normalAvg[i], achse))
    
    index0 = list_angleNormalAvgX.index(min(list_angleNormalAvgX))
    list_patchIndex_sorted.append(index0) # index des patches mit minimaler abweichung zu achse
    list_patchIndex_übrig.remove(index0)
    

    #list_angleBetweenPatches_temp = []
    a = len(list_patchIndex_übrig) # zähler
    while(a >= 0): # solange noch patches übrig sind
        #patchIndex_minAngle, list_patchIndex_übrig = sortNextPatch_normal(list_patchIndex_übrig, list_patchIndex_übrig[i], list_patches_normalAvg)
        list_angleBetweenPatches_temp = []
        for patchIndex_übrig_curr in list_patchIndex_übrig: #### -1 ???
            # patchIndex_curr ist index des neusten/ hintereten patch in liste der sortierten patches  
            #print("len(list_patchIndex_sorted) = ", len(list_patchIndex_sorted))
            list_angleBetweenPatches_temp.append(linearAlg.calcAngleVectors(list_patches_normalAvg[list_patchIndex_sorted[len(list_patchIndex_sorted)-1]], list_patches_normalAvg[patchIndex_übrig_curr]))
            # index des minimalen aus derwinkel liste, ist index, welches angabe wo in liste list_patchIndex_übrig_func, index des entsprechenden patches steht, 
        if(len(list_patchIndex_übrig) != 0):    
            patchIndex_minAngle = list_patchIndex_übrig[list_angleBetweenPatches_temp.index(min(list_angleBetweenPatches_temp))]

            list_patchIndex_sorted.append(patchIndex_minAngle)
            list_patchIndex_übrig.remove(patchIndex_minAngle)
        a = a - 1

    ####
    # patch entfernen, fall eines normal_Avg = normal_patchesMitNormalRaus
    for i in range(len(list_patches_normalAvg)): # alle patches durchgehe
        if(data_structure.checkVectorEqual(list_patches_normalAvg[i], normal_patchesMitNormalRaus)):
            # i ist patch index
            list_patchIndex_sorted.remove(i)
    
    return list_patchIndex_sorted



