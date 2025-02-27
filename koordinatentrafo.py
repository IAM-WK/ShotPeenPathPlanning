import numpy as np
import trimesh
import copy
#import func # war nur zum testen, ob trajectory
import csv 
from stl import mesh
import pymeshlab


tol = 10e-06
d = 5.0 #
d_edge = d/2

angle_rot_x = np.pi # um 180 deg bzw pi rad drehung um y achse, um KOS zu überführen


def trafo_new_KOS_axis(point, new_KOS_axis_list):
    #### Funktion: Punkt aus Standard KOS in neues KOS, 
    ####           bechrieben durch new_KOS_axis_list (= [[x_achse_x, x_achse_y, x_achse_z],  [], []]),
    ####           umrechnen

    #neue Liste anlegen für den transformierten punkt 
    point_transformed = [None]* len(point)
    # Umrechnen des punktes in neus KOS
    for i in range(len(new_KOS_axis_list)):  # 3, da 3D
        point_transformed[i] = np.dot(point, new_KOS_axis_list[i])
        
    return point_transformed

def rot_matrix_x(theta):
    
    R_x = np.zeros(shape = (4,4)) 
    R_x[0][0] = R_x[3][3] = 1.0
    R_x[1][1] = R_x[2][2] = np.cos(theta)
    R_x[1][2] = np.sin(theta)*(-1)
    R_x[2][1] = np.sin(theta)

    return R_x

def rot_matrix_y(theta):
    
    R_y = np.zeros(shape = (4,4)) 
    R_y[1][1] = R_y[3][3] = 1.0
    R_y[0][0] = R_y[2][2] = np.cos(theta)
    R_y[2][0] = np.sin(theta)*(-1)
    R_y[0][2] = np.sin(theta)

    return R_y

def rot_matrix_z(theta):

    R_z = np.zeros(shape = (4,4)) 
    R_z[2][2] = R_z[3][3] = 1.0
    R_z[0][0] = R_z[1][1] = np.cos(theta)
    R_z[0][1] = np.sin(theta)*(-1)
    R_z[1][0] = np.sin(theta)

    return R_z


def translation_matrix(vector_translation):
    #Matrix T, für Translation als np.array, um +point
    T = np.zeros(shape = (4,4)) 
    for i in range(len(T)): #Diagonaleinträge T
        T[i][i] = 1.0 
    
    for i in range(len(T)-1): #letzte Spalte Matrix: Translation
        T[i][3] = vector_translation[i] 
    return T

def rot_matrix(point, axis_vec, theta):

    # !!! Beachten: axis_vec, Orientierung!, sonst Drehung falschrum 

    #### Funktion: rotiert einen Punkt point um beliebige Achse axis_vec um den Winkel theta, 
    #
    # Parameter:   point: Punkt, der rotiert werden soll
    #              axis_vec: Rotationsachse
    #              theta: Rotationswinkel
    # return:      point_rot: rotierter Punkt

    #Berechnung s. TU WIEN tablet

    #Matrix T, für Translation als np.array, um +point
    T = np.zeros(shape = (4,4)) 
    for i in range(len(T)): #Diagonaleinträge T
        T[i][i] = 1.0 
    
    for i in range(len(T)-1): #letzte Spalte Matrix: Translation
        T[i][3] = point[i] 

    #Berechnung der Hilfswinkel:
    alpha = np.arccos(axis_vec[2]/(np.sqrt(pow(axis_vec[1],2)+pow(axis_vec[2],2))))
    beta = np.arccos((np.sqrt(pow(axis_vec[1],2)+pow(axis_vec[2],2))))

    #Rotationsmatrizen R um Koordinatenachsen i: R_i
    # !!! sin, cos numpy, deg oder rad ??? !!!

    #R_x
    R_x = rot_matrix_x(alpha)
    #R_y
    R_y = rot_matrix_y(beta)
    #R_z
    R_z = rot_matrix_z(theta)

    #gesamt Matrix R berechnen:
    R = T @ np.linalg.inv(R_x) @ np.linalg.inv(R_y) @ R_z @ R_y @ R_x @ np.linalg.inv(T)

    point_rot = R @ point #Trafo anwenden
    return point_rot

def koordinatentrafo_rotation_coordAxis_point(point, theta, coordAxis):
    ####
    #  0.0 an point anhängen 
    # valide Werte für coordAxis: "x", "y", "z"
    point_appended = []
    for i in range(len(point)):
        point_appended.append(point[i])
    point_appended.append(0.0)

    #trafo
    if(coordAxis == "x"):
        R_coordAxis = rot_matrix_x(theta)
    elif(coordAxis == "y"):
        R_coordAxis = rot_matrix_y(theta)
    elif(coordAxis == "z"):
        R_coordAxis = rot_matrix_z(theta)
    else:
        print("Invalid argument coordAxis. Please enter: 'x', 'y' or 'z'.")

    point_new_appended = R_coordAxis @ point_appended

    # 4. eintrag wieder löschen
    point_new = []
    for i in range(len(point_new_appended)-1):
        point_new.append(point_new_appended[i])
    #print("\n point_new:  ",  point_new) #### TEST
    return point_new

def koordinatentrafo_rotation_coordAxis_points(point_list, theta, coordAxis):
    #### Funktion:
    
    point_new_list = [None] * len(point_list)
    for i in range(len(point_list)):
        point_new_list[i] = koordinatentrafo_rotation_coordAxis_point(point_list[i], theta, coordAxis)
    
    return point_new_list

def koordinatentrafo_translation_point(point, coord_0):
    #### Funktion:
    #
    #
    #print("\n koordinatentrafo_translation_point(point, coord_0): ", point, ", ", coord_0)
    point_new = np.subtract(point, coord_0)
    #print("\n point_new: ", point_new) #### TEST 
    return point_new

def koordinatentrafo_translation_points(point_list, coord_0):
    #### Funktion:
    #
    #
    point_new_list = [None] * len(point_list)
    for i in range(len(point_list)):
        point_new_list[i] = np.subtract(point_list[i], coord_0)
    
    return point_new_list

