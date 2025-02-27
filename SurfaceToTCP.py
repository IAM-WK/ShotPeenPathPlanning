################
# Koordinaten des Punktes auf Oberfläche in Koordinaten für TCP umrechnen
# Koordinaten des TCP Punktes auf STL KOS In Roboter KOS umrechnen
# 
# 

import numpy as np
import math
import trimesh
import copy
import sympy
from stl import mesh
import data_structure

# eingabeparameter
from eingabeparameter import d_offset, pos_probe
# offset = abstand des TCP zur Oberfläche, in mm
offset = d_offset # EINGABEPARAMETER
# NullPos Roboter = [560, 0, 485, 180, -90, 0]
t_KosTrafo = pos_probe # zum beispiel entsprechend einzugeben, in Rob KOS

# 
# Koordinaten Trafo
def PositionSurfaceToTCP(coordinatesSurface, normal):
    # Übergabe je Position: Koordinaten x,y,z sowie nomalenvektor

    # coordinates = [x, y, z]
    # normal = normalen Vektor der OF an Punkt coordinates
    #vBerechnung der TCP Position
    # Fall: keine Hinterschneidung

    coordinatesTCP = np.add(coordinatesSurface, np.multiply(normal,offset))
    ####return coordinatesTCP, normal
    return coordinatesTCP

def KOSTrafo_StlToRob(coordinatesTCP_stl): # EINGABEPARAMETER
    # Umrechnung der koordinaten, coordinates = [x, y, z]
    # von Stl Kos in Roboter Kos
    # mit Hilfe translatorischhem Verschiebungsketor t_KosTrafo von Roboter origin zu Stl origin
    coordinatesTCP_rob = np.add(t_KosTrafo, coordinatesTCP_stl)
    return coordinatesTCP_rob
