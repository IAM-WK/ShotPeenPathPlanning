#######
# Zur Berechnung der TCP Orientierung in ROLL PITCH YAW WINKELN zu einer gegebenen Richtung als Vektor

# Erklärung:
# Es gilt zu jeder Zelle, die TCP Orientierung in roll-, pitch-, yaw- winkeln zu berechnen.
# gegeben ist hierzu die Normale der jeweiligen Zelle.
# die Richtung der Z-Achse des TCP/Werkzeugs soll senkrecht auf die Oberfläche weisen, d.h. der Vektor entgegen der Normale der Zelle gibt die Ausrichtung des TCP an, bzw dessen z-Achse
#

# 1. Rotmatriz aufstellen um z achse in neue Orienteirung zu übersetzen
# 2. aus Rotationsmatrix die roll- pitch- yaw- winkel exttrahieren

errRundung = 1e-8

import numpy as np
import math
import trimesh
import copy
import sympy
from stl import mesh
import data_structure

from sympy.abc import a, b, c, d, e, f, g, h, i

#neu 

# elementare Rotationsmatrizen um Koordinatenachsen:
def rot_matrix_x(theta):
    
    R_x = np.zeros(shape = (3,3)) 
    R_x[0][0] = 1.0
    R_x[1][1] = R_x[2][2] = np.cos(theta)
    R_x[1][2] = np.sin(theta)*(-1)
    R_x[2][1] = np.sin(theta)

    return R_x

def rot_matrix_y(theta):
    
    R_y = np.zeros(shape = (3,3)) 
    R_y[1][1]  = 1.0
    R_y[0][0] = R_y[2][2] = np.cos(theta)
    R_y[2][0] = np.sin(theta)*(-1)
    R_y[0][2] = np.sin(theta)

    return R_y

def rot_matrix_z(theta):

    R_z = np.zeros(shape = (3,3)) 
    R_z[2][2] = 1.0
    R_z[0][0] = R_z[1][1] = np.cos(theta)
    R_z[0][1] = np.sin(theta)*(-1)
    R_z[1][0] = np.sin(theta)

    return R_z


# 1.: 
# Rotmatrix Aufstellen um z Achse auf -triangle_normal zu drehen
def getRotationmatrix(triangle_normal): # bzgl z achse
    #neu print("\n triangle_normal = ", triangle_normal)
    # Vorgehen: 
    # Allgemeine Rotationsmatrix aufstellen 
    # 1. Normale der Zelle vorher normieren, z Achse per se normiert
    #   Rotationsache berechnen; 
    #       Rot Achse: u = z x -normal_cell, 
    #       so rum, damit Drehrichtung von z zu neuer Orientierung weisend


    # 2. Drehwinkel berechnen: 
    #       Drehwinkel: theta = arccos(scalarprod(z,-normal_cell) / betrag(-normal_cell) / betrag(z) )
    #       (beträge sollten eig eh = 1)
    # 3. Allgemeine Formel für Rot matrix um beliebige Achse u, um Winkel theta:
    #       alpha = u_3/sqrt(u_2^2 + u_3^2)
    #       beta = sqrt(u_2^2 + u_3^2)
    #       R = R_x(-alpha)*R_y(-beta)*R_z(theta)*R_y(beta)*R_x(alpha)
    #           mit R_i Koord Rot Matrizen
    # 
    
    # Bezugsachse ist z-Achse 
    z = [0.0,0.0,1.0]
    # triangle_normal zur Sicherheit normieren, und mal minus 1:
    triangle_normal_norm = np.multiply(triangle_normal, 1/np.linalg.norm(triangle_normal))
    #print("triangle_normal_norm = ", triangle_normal_norm)
    # 1.:
    # Rotationsachse u:
    u = np.cross(z, np.multiply(triangle_normal_norm, -1))
    #print("\n u = ", u)
    if(np.abs(u[0])<= errRundung and np.abs(u[1])<= errRundung and np.abs(u[2])<= errRundung):
        R_matrix = np.zeros(shape = (3,3)) 
        R_matrix[1][1] = R_matrix[0][0] = R_matrix[2][2] = 1.0
        R_matrix[0][1] =  R_matrix[0][2] = R_matrix[1][0] = R_matrix[1][2] = R_matrix[2][0] = R_matrix[2][1] = 0.0 
    else:
        # 2.:
        # Drehwinkel theta: 
        #print("np.dot(z, triangle_normal_norm) = ", np.dot(z, triangle_normal_norm))
        theta = np.arccos(np.dot(z, triangle_normal_norm)) # in bogenmaß
        #print(" theta = ", theta)
        # 3.:

        ####### berechnung nach uni dings trafo dokument START
        if(u[2] == 0):
            arg_alpha = 0.0
        else:
            arg_alpha = u[2]/np.sqrt(np.power(u[1], 2) + np.power(u[2], 2))
            
        alpha = np.arccos(arg_alpha)
        #print("alpha = ", alpha)
        beta = np.arcsin(-1*u[0])
        
        # Rotmatrix R: 

        R_matrix = rot_matrix_x(alpha*(-1)) @ rot_matrix_y(beta*(-1)) @ rot_matrix_z(theta) @ rot_matrix_y(beta) @ rot_matrix_x(alpha)
    
    return R_matrix

# 2.: 
# Roll-, Pitch-, Yaw-Winkel aus Rotmatrix extrahieren/berechnen
def getRollPitchYaw(R):
    # R = Rotationmatrix
    
    #print("R = ", R)
    
    pitch = np.arctan2(-1*R[2][0],  np.sqrt(np.power(R[0][0], 2) + np.power(R[1][0], 2)))
    
    if(np.absolute(pitch - np.pi/2) <= errRundung): # wenn nicht singulär
        yaw = 0.0
        roll = np.arctan2(R[0][1], R[1][1])
    elif(np.absolute(pitch + np.pi/2) <= errRundung):
        yaw = 0.0
        roll = -1* np.arctan2(R[0][1], R[1][1])
        
    else:
        yaw = np.arctan2(R[1][0]/np.cos(pitch), R[0][0]/np.cos(pitch))
        roll = np.arctan2(R[2][1]/np.cos(pitch), R[2][2]/np.cos(pitch))

    # Anm.: Quelle, Buch: roll = gamma, pitch = beta, yaw = alpha
    rollPitchYaw = [roll, pitch, yaw]
    return rollPitchYaw # in bogenmaß

def radToDeg(angleRad):
    erg = angleRad*180/np.pi
    return erg

def radToDeg_list(angleRad_list):
    angleDeg_list = []
    for i in range(len(angleRad_list)):
        angleDeg_list.append(radToDeg(angleRad_list[i]))
    return angleDeg_list





# 1.: 
# Rotmatrix Aufstellen um richtungsvektor um drehachse um winkel zu drehen
def getRotationmatrix_drehachseWinkel(drehachse, winkel): # bzgl z achse

    # Vorgehen: 
    # Allgemeine Rotationsmatrix aufstellen 
    # 1. Normale der Zelle vorher normieren, z Achse per se normiert
    #   Rotationsache berechnen; 
    #       Rot Achse: u = z x -normal_cell, 
    #       so rum, damit Drehrichtung von z zu neuer Orientierung weisend


    # 2. Drehwinkel berechnen: 
    #       Drehwinkel: theta = arccos(scalarprod(z,-normal_cell) / betrag(-normal_cell) / betrag(z) )
    #       (beträge sollten eig eh = 1)
    # 3. Allgemeine Formel für Rot matrix um beliebige Achse u, um Winkel theta:
    #       alpha = u_3/sqrt(u_2^2 + u_3^2)
    #       beta = sqrt(u_2^2 + u_3^2)
    #       R = R_x(-alpha)*R_y(-beta)*R_z(theta)*R_y(beta)*R_x(alpha)
    #           mit R_i Koord Rot Matrizen
    # 
    
   
    # 1.:
    # Rotationsachse u:
    u = drehachse
    #neu print("\n R: drehachse: u = ", u)
    # 2.:
    # Drehwinkel theta: 
    theta = winkel # in bogenmaß
    #neu print("\n R: drehachse: theta = ", theta)
    # 3.:

    ####### berechnung nach uni dings trafo dokument START
    #"""
    if(u[2] == 0):
        arg_alpha = 0.0
    else:
        arg_alpha = u[2]/np.sqrt(np.power(u[1], 2) + np.power(u[2], 2))
        
    alpha = np.arccos(arg_alpha)
    beta = np.arcsin(-1*u[0])
    
    # Rotmatrix R: 

    R = rot_matrix_x(alpha*(-1)) @ rot_matrix_y(beta*(-1)) @ rot_matrix_z(theta) @ rot_matrix_y(beta) @ rot_matrix_x(alpha)
    
    
    return R

def setzeMatrixWertekleinerErrorzuNull(R):
    # R: 3x3 Matrix, bzw quadratisch
    R_new = np.zeros(shape = (3,3)) 
    for i in range(len(R)):
        for j in range(len(R)):
            if(R[i][j] <= errRundung):
                R_new[i][j] = 0.0
            else: 
                R_new[i][j] = R[i][j]
    return R_new

"""
def setzeWinkelWertekleinerErrorzuNullDeg(winkel_liste):

    winkel_new = np.zeros(shape=(len(winkel_liste)))
    for i in range(len(winkel_liste)):
        if(np.abs(winkel_liste[i]-errRundung) <= errRundung):
            winkel_new[i] = 0.0
        else:
            winkel_new[i] = winkel_liste[i]
    return winkel_new
"""



############################

# patch wise die orientierungen berechnen
def getListe_achsenKOSB(listIntersection_PatchSchar_sorted_i, listIntersection_PatchSchar_sorted_iplus1, list_normals_sorted_i):
    # listIntersection_PatchSchar_sorted = listIntersection_PatchSchar_sorted[i], aktueller punkt der punkte des pfades eines patches
    #list_normals_sorted[i] = aktuelle (i te) normale

    # z achse ist negativer normalenvektor
    temp_zB = np.multiply(list_normals_sorted_i, -1.0)
    achse_zB = np.multiply(temp_zB, 1/np.linalg.norm(temp_zB))
    # y achse ist verbindung des aktuellen punktes zum nächsten
    temp_yB = np.subtract(listIntersection_PatchSchar_sorted_iplus1, listIntersection_PatchSchar_sorted_i)
    achse_yB = np.multiply(temp_yB, 1/np.linalg.norm(temp_yB))
    # x achse ergibt sich entsprechend den y, z, achsen, so dass RHS 
    temp_xB = np.cross(achse_yB, achse_zB)
    achse_xB = np.multiply(temp_xB, 1/np.linalg.norm(temp_xB))

    liste_achsenKOSB = [achse_xB, achse_yB, achse_zB] # normierte KOS achsen

    return liste_achsenKOSB


def getRotationmatrixBasiswechsel(liste_achsenKOSB):
    # liste_achsenKOSB = [[vektor_achse0],[vektor_achse1],[vektor_achse2]]

    liste_achsenKOSA = [[1,0,0],[0,1,0],[0,0,1]] # Basis KOS
    
    # abc
    equations1 = [liste_achsenKOSB[0][0]-liste_achsenKOSA[0][0]*a-liste_achsenKOSA[1][0]*b-liste_achsenKOSA[2][0]*c, liste_achsenKOSB[0][1]-liste_achsenKOSA[0][1]*a-liste_achsenKOSA[1][1]*b-liste_achsenKOSA[2][1]*c, liste_achsenKOSB[0][2]-liste_achsenKOSA[0][2]*a-liste_achsenKOSA[1][2]*b-liste_achsenKOSA[2][2]*c]
    # def
    equations2 = [liste_achsenKOSB[1][0]-liste_achsenKOSA[0][0]*d-liste_achsenKOSA[1][0]*e-liste_achsenKOSA[2][0]*f, liste_achsenKOSB[1][1]-liste_achsenKOSA[0][1]*d-liste_achsenKOSA[1][1]*e-liste_achsenKOSA[2][1]*f, liste_achsenKOSB[1][2]-liste_achsenKOSA[0][2]*d-liste_achsenKOSA[1][2]*e-liste_achsenKOSA[2][2]*f]
    # ghi
    equations3 = [liste_achsenKOSB[2][0]-liste_achsenKOSA[0][0]*g-liste_achsenKOSA[1][0]*h-liste_achsenKOSA[2][0]*i, liste_achsenKOSB[2][1]-liste_achsenKOSA[0][1]*g-liste_achsenKOSA[1][1]*h-liste_achsenKOSA[2][1]*i, liste_achsenKOSB[2][2]-liste_achsenKOSA[0][2]*g-liste_achsenKOSA[1][2]*h-liste_achsenKOSA[2][2]*i]
    # lösen mit sympy der LGSe
    solution_abc = sympy.solve(equations1, a,b,c, dict = True)
    solution_def = sympy.solve(equations2, d,e,f, dict = True)
    solution_ghi = sympy.solve(equations3, g,h,i, dict = True)

    # ergebnisse in matrix eintragen
    R_matrix = np.zeros(shape = (3,3))
    # 1. zeile
    R_matrix[0][0] = solution_abc[0][a] 
    R_matrix[0][1] = solution_abc[0][b] 
    R_matrix[0][2] = solution_abc[0][c] 
    # 2. zeile
    R_matrix[1][0] = solution_def[0][d] 
    R_matrix[1][1] = solution_def[0][e] 
    R_matrix[1][2] = solution_def[0][f] 
    # 3. zeile
    R_matrix[2][0] = solution_ghi[0][g] 
    R_matrix[2][1] = solution_ghi[0][h] 
    R_matrix[2][2] = solution_ghi[0][i] 

    return R_matrix

def getRollPitchYaw_pathPoint(listIntersection_PatchSchar_sorted_i, listIntersection_PatchSchar_sorted_iplus1, list_normals_sorted_i):
    achsen = getListe_achsenKOSB(listIntersection_PatchSchar_sorted_i, listIntersection_PatchSchar_sorted_iplus1, list_normals_sorted_i)
    print()
    R_basisToB = getRotationmatrixBasiswechsel(achsen)
    
    rollPitchYawB = getRollPitchYaw(R_basisToB)
    print("achsen = ", achsen, "R_basisToB = ", R_basisToB, "rollPitchYawB = ", rollPitchYawB)
    return rollPitchYawB

"""
# test 
achsen = getListe_achsenKOSB([1,1,0],[2,2,0],[0,0,-1])
print("achsen = ", achsen)
R_basisToB = getRotationmatrixBasiswechsel(achsen)
print("R_basisToB = ", R_basisToB)
rollPitchYawB = radToDeg_list(getRollPitchYaw(R_basisToB))
print("rollPitchYawB = ", rollPitchYawB)
"""