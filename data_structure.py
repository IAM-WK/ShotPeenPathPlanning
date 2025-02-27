
import numpy as np
import trimesh
import copy
import sympy
from stl import mesh

err = 1e-6 


# Funktion: vergleicht zwei vektoren, gleicher dim
def checkVectorEqual(vector1, vector2):
    check = False
    eq = 0 #zähler
    #print("\n")
    #print("\n len(vector1), len(vector2) = ", len(vector1), ", ", len(vector2)) # TEST
    for i in range(len(vector1)): # jede coord der vektoren vergleichen
        #print(" i = ", i) # TEST
        #print(" vector1[", i, "] = ", vector2[i], ", vector2[", i, "]",  vector2[i]) # TEST
        #if(vector1[i] == vector2[i]): 
        #print(" v1[i] - v2[i] = ", np.subtract(vector1[i],vector2[i]) ) # TEST
        if(np.absolute(vector1[i]-vector2[i]) <= err):
            
            #print("vector1[i], vector2[i] = ", vector1[i], vector2[i]) # TEST
            eq = eq+1 # zähler
            #print("eq = ", eq)
    if (eq == len(vector1)): # 3 d
        check = True
    #print(check) # TEST
    
    #print(" vector1, vector2 = ", vector1, vector2, " , equal = ", check)
    return  check


# Funktion: vergleicht zwei edges miteinandenr, true = gleich, false = unterschiedlich
def checkEdgeEqual(edge1, edge2):
    # edge1 und edge2 je als = [[vertice1], [vertice2]]
    check = False 
    # wenn edge gleich, d.h. wenn die beiden vertices, die edge bilden gleich sind, dann ...
    if((checkVectorEqual(edge1[0], edge2[0]) and checkVectorEqual(edge1[1], edge2[1])) or (checkVectorEqual(edge1[1], edge2[0]) and checkVectorEqual(edge1[0], edge2[1]))):
        check = True
    return check


# Funktion: prüfen, ob ein vektor bereits in liste: 
# Anm.: Dimensionen der listenvektoren und des vergleichsvektors müssen natürlich übereinstimmen 
def checkIfVectorIsInList(list_vectors, vector):
    # False = noch nicht in liste
    # True = bereits in liste
    check = False
    a = 0

    for i in range(len(list_vectors)):
        a = 0 # a resetten
        for j in range(len(vector)):
            if ((list_vectors[i][j]) == vector[j]): 
                a = a+1
        if (a == len(vector)): # wenn alle drei einträge des vektors gleich, dann vektor bereits in liste --> True
            check = True
            return check
    return check

def checkIfScalarIsInList(list_scalars, scalar):
    # False = noch nicht in liste
    # True = bereits in liste
    check = False
    a = 0
    for i in range(len(list_scalars)):
        a = 0 # a resetten
        if ((list_scalars[i]) == scalar): 
            check = True
            return check
    return check

def checkIfEdgeIsInList(listEdges_coordinates, edge_coordinates):
    #
    # listEdges_coordinates = je edge eintrag aus je liste aus zwei vertices als vektoren/coordinates
    check = False # return wert, 
    # false, wen  nicht in liste, 
    # true, wenn in liste
    for i in range(len(listEdges_coordinates)):
        # jede edge in liste durchgehen und prüfen, ob
        # beide vertices, die edge bilden in liste iter edge sind, d.h. ob edge gleich ist
        if(checkIfVectorIsInList(listEdges_coordinates[i], edge_coordinates[0]) and checkIfVectorIsInList(listEdges_coordinates[i], edge_coordinates[1])):
            # wenn edge gleich ist
            check = True
            break # wenn gleiche edge gefunden, break

    return check
            
def getIndexOf0DElementInList(liste, element):
    # element ist vektor
    a = 0 # zähler 
    for i in range(len(liste)):
        #print("\n element = ", element)
        if(liste[i] == element):
            
            #print("      liste[", i, "] = ", liste[i])
            index = i
            #print("      index = ", index)
            return index
    # falls element nicht in liste gefunden wird: 
    if(a == len(liste)):
        print("\n Element ", element, "is not in list ", liste, ". Nothing returned. \n (Funktion: getIndexOfElementInList(...)) \n")



def getIndexOfElementInList(liste, element):
    # element ist vektor
    a = 0 # zähler 
    for i in range(len(liste)):
        #print("\n element = ", element)
        if(checkVectorEqual((liste[i]), element)):
            
            #print("      liste[", i, "] = ", liste[i])
            index = i
            #print("      index = ", index)
            return index
    # falls element nicht in liste gefunden wird: 
    if(a == len(liste)):
        print("\n Element ", element, "is not in list ", liste, ". Nothing returned. \n (Funktion: getIndexOfElementInList(...)) \n")

        

# Funktion: alle Vertices des meshs (hier nur Koordinaten dieser) auslesen und in liste schreiben
def readTrimesh_listVertices_coordinates(list_trimesh_mesh_triangles):
    list_vertices_coordinates = []
    for i in range(len(list_trimesh_mesh_triangles)):
        for j in range(3):
            # prüfen, ob aktuelle vertex bereits in liste, wenn nicht, dann einfügen
            if(checkIfVectorIsInList(list_vertices_coordinates, list_trimesh_mesh_triangles[i][j]) == False): 
                list_vertices_coordinates.append(list_trimesh_mesh_triangles[i][j])
    #list_vertices_coordinates = np.array(list_vertices_coordinates)
    return list_vertices_coordinates

def getTriangleIndex_Vertices(list_trimesh_mesh_triangles, list_vertices):
    # prüfen, zu welchen triangles vertex aus list_vertices je gehört, index des triangles (bzw der #n triangles) speichern in liste 
    # list_triangleIndex enthält je vertex(gleich sortiert wie eingabe liste list_vertices) eine liste, welche die indizes der triangles beinhaltet, welche zu dem entsprechenden vertex gehören
    list_triangleIndex = []
    for i in range(len(list_vertices)):
        list_triangleIndex.append([])
        for j in range(len(list_trimesh_mesh_triangles)): 
            
    # für jedes vertex vergleich mit allen vertices eines jeden triangle, und merken, welche triangle gleiche vertex aufweisen
            if(checkIfVectorIsInList(list_trimesh_mesh_triangles[j], list_vertices[i]) == True):
                list_triangleIndex[i].append(j) # i ist index des aktuellen vertex, j ist index des aktuellen triangles
    
    #list_triangleIndex = np.array(list_triangleIndex) # np array
    return list_triangleIndex
            

def getListVertices(trimesh_mesh):
    listVertices = [] # liste aller vertices, jeweils als liste der coordinaten, triangleIndex
    # list_vertices_coordinates liste erstellen
    list_vertices_coordinates = readTrimesh_listVertices_coordinates(trimesh_mesh)
    list_vertices_triangleIndex = getTriangleIndex_Vertices(trimesh_mesh, list_vertices_coordinates)

    # in eine liste schreiben
    for i in range(len(list_vertices_coordinates)):
        listVertices.append([[list_vertices_coordinates[i]], [list_vertices_triangleIndex[i]]])
    
    return listVertices

# Funktion: edges auslesen
def getListEdges_coordinate(trimesh_mesh, list_trimesh_mesh_triangles, list_vertices_coordinate):

    #for i in range(len(list_trimesh_mesh_triangles)): # je triangle
    #    for j in range(3): #je trainngle drei vertices, und drei edges
    #        if(checkIfVectorIsInList(list_edges) == False and checkIfVectorIsInList() == False): # wenn noch nicht in liste, dann...

    # list_triangles_edge zunächst erstellen: 
    list_triangles_edges = []
    for i in range(len(list_trimesh_mesh_triangles)): # je triangle
        list_triangles_edges.append([]) # für jedes triangle eine liste anlegen 
    
        list_triangles_edges[i].append([trimesh_mesh.triangles[i][0], trimesh_mesh.triangles[i][1]])
        list_triangles_edges[i].append([trimesh_mesh.triangles[i][1], trimesh_mesh.triangles[i][2]])
        list_triangles_edges[i].append([trimesh_mesh.triangles[i][2], trimesh_mesh.triangles[i][0]])

    list_triangles_allEdges = []
    for i in range(len(list_triangles_edges)):
        for j in range(len(list_triangles_edges[i])):
            list_triangles_allEdges.append(list_triangles_edges[i][j])


    list_edges = [] # später return wert
    # liste list_triangles_allEdges noch redundant --> nur noch jede edge eindeutig in lieste list_edges schreiben
    
    list_edges.append(list_triangles_allEdges[0]) # erstes element hinzufügen


    for i in range(1, len(list_triangles_allEdges)): # ausgangs liste durchgehen
        a = 0 # zähler reset
        #print("\n i = ", i) # TEST

        for j in range(len(list_edges)): # ziel liste durchgehen
            
            #print("list_triangles_allEdges[", i, "], list_edges[", j, "] = ", list_triangles_allEdges[i], list_edges[j]) # TEST
            if(checkEdgeEqual(list_triangles_allEdges[i], list_edges[j]) == False): # je elemente vergleichen
                # wenn nicht gleich, zähler +1
                print() # TEST
                a = a+1
                #print("list_triangles_allEdges[i], list_edges[j] = ", list_triangles_allEdges[i], list_edges[j])
            else:
                break
            #print("\n           len(list_edges) = ", len(list_edges))
            #print("             a = ", a)
        #print("len(list_edges) = ", len(list_edges))
        if(a == len(list_edges)): # wenn ALLE elemente NICHT übereinstimmen, dann ...
            list_edges.append(list_triangles_allEdges[i])


            
    return list_edges

# FUNKTION: gleiche Fkt. wie getListEdges_coordinate aber mit ausgabe der vertices indizes statt der vertices koordinaten
# return = liste der edges, je in form einer liste, welche die indizes der vertices enthält, welche die edge bilden
def getListEdges0(trimesh_mesh, list_trimesh_mesh_triangles, list_vertices_coordinate):

   
    # list_triangles_edge zunächst erstellen: 
    list_triangles_edges = []
    for i in range(len(list_trimesh_mesh_triangles)): # je triangle
        list_triangles_edges.append([]) # für jedes triangle eine liste anlegen 
    
        list_triangles_edges[i].append([trimesh_mesh.triangles[i][0], trimesh_mesh.triangles[i][1]])
        list_triangles_edges[i].append([trimesh_mesh.triangles[i][1], trimesh_mesh.triangles[i][2]])
        list_triangles_edges[i].append([trimesh_mesh.triangles[i][2], trimesh_mesh.triangles[i][0]])

    list_triangles_allEdges = []
    for i in range(len(list_triangles_edges)):
        for j in range(len(list_triangles_edges[i])):
            list_triangles_allEdges.append(list_triangles_edges[i][j])


    list_edges = [] # 
    # liste list_triangles_allEdges noch redundant --> nur noch jede edge eindeutig in lieste list_edges schreiben
    
    list_edges.append(list_triangles_allEdges[0]) # erstes element hinzufügen
    # TEST:

    for i in range(1, len(list_triangles_allEdges)): # ausgangs liste durchgehen
        a = 0 # zähler reset
        #print("\n i = ", i) # TEST

        for j in range(len(list_edges)): # ziel liste durchgehen
            
            #print("list_triangles_allEdges[", i, "], list_edges[", j, "] = ", list_triangles_allEdges[i], list_edges[j]) # TEST
            if(checkEdgeEqual(list_triangles_allEdges[i], list_edges[j]) == False): # je elemente vergleichen
                # wenn nicht gleich, zähler +1
                # TEST
                a = a+1
            else:
                break
        if(a == len(list_edges)): # wenn ALLE elemente NICHT übereinstimmen, dann ...
            list_edges.append(list_triangles_allEdges[i])

    # indizes der vertices angeben statt coord der vertices
    list_edges_2 =[]
    for i in range(len(list_edges)):# neuen eintrag je edge
        list_edges_2.append([getIndexOfElementInList(list_vertices_coordinate, list_edges[i][0]), getIndexOfElementInList(list_vertices_coordinate, list_edges[i][1])]) # indizes der zwei vertices der i. edge 
            
    return list_edges_2


# FUNKTION: gleiche Fkt. wie getListEdges_coordinate aber mit ausgabe der vertices indizes statt der vertices koordinaten
# return = liste der edges, je in form einer liste, welche die indizes der vertices enthält, welche die edge bilden
def getListEdges(trimesh_mesh, list_trimesh_mesh_triangles, list_vertices_coordinate):

    # list_triangles_edge zunächst erstellen: 
    list_triangles_edges = []
    for i in range(len(list_trimesh_mesh_triangles)): # je triangle
        list_triangles_edges.append([]) # für jedes triangle eine liste anlegen 
    
        list_triangles_edges[i].append([list_trimesh_mesh_triangles[i][0], list_trimesh_mesh_triangles[i][1]])
        list_triangles_edges[i].append([list_trimesh_mesh_triangles[i][1], list_trimesh_mesh_triangles[i][2]])
        list_triangles_edges[i].append([list_trimesh_mesh_triangles[i][2], list_trimesh_mesh_triangles[i][0]])

    list_triangles_allEdges = []
    for i in range(len(list_triangles_edges)):
        for j in range(len(list_triangles_edges[i])):
            
            list_triangles_allEdges.append(list_triangles_edges[i][j])

    

    list_edges = [] # 
    # liste list_triangles_allEdges noch redundant --> nur noch jede edge eindeutig in lieste list_edges schreiben
    
    list_edges.append(list_triangles_allEdges[0]) # erstes element hinzufügen
    

    for i in range(1, len(list_triangles_allEdges)): # ausgangs liste durchgehen
        if(not(checkIfEdgeIsInList(list_edges, list_triangles_allEdges[i]))): # wenn edge i noch nicht in list_edge
            # ... edge in liste_edge schreiben
            list_edges.append(list_triangles_allEdges[i])


    # indizes der vertices angeben statt coord der vertices
    list_edges_2 =[]
    for i in range(len(list_edges)):# neuen eintrag je edge
        
        
        list_edges_2.append([getIndexOfElementInList(list_vertices_coordinate, list_edges[i][0]), getIndexOfElementInList(list_vertices_coordinate, list_edges[i][1])]) # indizes der zwei vertices der i. edge 
            
    return list_edges_2

# FUNKTION: erstellt, return:
#           1. liste, zu triangles, je triangle ein eintrag = liste mit indizes der vertices, die traingle bilden,  
#           2. liste, zu triangles, je trianlge ein eintrag = liste mit indizes der edges, die triangle bilden
#           
#           eingabe: 
#           liste der triangles, je als liste der vertices_coord
#           liste der edges, als vertices_index
#           liste der vertices,  als koordinaten
def getListTriangles_VerticesIndex_EdgeIndex(list_trimesh_mesh_triangles, listEdges_verticesIndex, listVertices_coordinate):
    # 1. liste, zu triangles, je triangle ein eintrag = liste mit indizes der vertices, die traingle bilden erstellen: 
    # 
    list_triangles_verticesIndex = []
    for i in range(len(list_trimesh_mesh_triangles)):   
        list_triangles_verticesIndex.append([])
        for j in range(3): # 3 vertices je triangle
            list_triangles_verticesIndex[i].append(getIndexOfElementInList(listVertices_coordinate, list_trimesh_mesh_triangles[i][j]))

    # 2. liste, zu triangles, je trianlge ein eintrag = liste mit indizes der edges, die triangle bilden
    #   
    list_triangles_edgesIndex = []       
    for i in range(len(list_triangles_verticesIndex)): # je triangle i
        list_triangles_edgesIndex.append([]) # je traingle i eine liste als eintrag anlegen
        
        for k in range(len(listEdges_verticesIndex)): #  je edges durchgehen und passende raussuchen
            # k ist index der edge
            # wenn beide vertices (index) in triangle vorkommen, dann diese edge hinzufügen
            a = 0 # zähler
            if(checkIfScalarIsInList(list_triangles_verticesIndex[i], listEdges_verticesIndex[k][0]) and checkIfScalarIsInList(list_triangles_verticesIndex[i], listEdges_verticesIndex[k][1])): # wenn 2 einträge (= vertices indizes) gleich sind, dann ist edge vorhanden, in triangle i
                list_triangles_edgesIndex[i].append(k)
                a = a+1 # zähler 
                if(a == 3): # abbruch, wenn alle drei edges des triangles i gefunden wurden 
                    break

    return list_triangles_verticesIndex, list_triangles_edgesIndex



# FUNKTION: 
#           erstellt/return: 
#           liste, je edge ein eintrag, welcher die indizes der beiden triangles enthält, welche die edge enthalten
#           eingabe: 
#           list_edges: liste der edges, edge je als [verticeIndex1, verticeIndex2]
#           liste der edges, edge je als liste der indizes der vertices, die edge bilden
def getListEdges_IndexOfTriangles(listTriangles_edgesIndex, list_edges):

    listEdges_TrianglesIndex = [] # return liste anlegen 
    for i in range(len(list_edges)): # edges durchgehen, d.h. i entspricht allgemienem indize der edge (edge indize = nummerierung der edge)
        a = 0
        listEdges_TrianglesIndex.append([]) # listen eintrag für i. edge erstellen
        for j in range(len(listTriangles_edgesIndex)): # j entspricht index/nummer des triangles
            if(checkIfScalarIsInList(listTriangles_edgesIndex[j], i)):
                a = a+1
                listEdges_TrianglesIndex[i].append(j) # num des triangles, welche edge enthält einfügen
                if(a == 2): 
                    break # bei 2 gefundnene edges kann abgebrochen werden, da dies das max

    return listEdges_TrianglesIndex

# FUNKTION: getTriangles_normals 
def getTriangles_normals(list_trimesh_mesh_triangles):
    
    listTriangles_normals = trimesh.triangles.normals(list_trimesh_mesh_triangles)[0]
    return listTriangles_normals

# Funktion: getLists_VerticesEdgesTriangles(trimesh_mesh):
#           return: 7 Listen, in RF: 
#               Listen: vertices_coordinates
#                       vertices_trianglesIndex
#                       edges_verticesIndex
#                       edges_trianglesIndex
#                       triangles_edgesIndex
#                       triangles_verticesIndex
#                       triangles_normals
#           eingabe: trimesh_mesh
def getLists_VerticesEdgesTriangles(trimesh_mesh):
        # liste trimesh.triangles in array casten
    list_trimesh_mesh_triangles_0 = trimesh_mesh.triangles # !!! ???
    list_trimesh_mesh_triangles = []
    for i in range(len(list_trimesh_mesh_triangles_0)): # je triangle in list
        list_trimesh_mesh_triangles.append([])
        for j in range(len(list_trimesh_mesh_triangles_0[i])): # je vertices in triangle
            list_trimesh_mesh_triangles[i].append(np.array(list_trimesh_mesh_triangles_0[i][j]))
    # Listen vertices:
    vertices_coordinates = readTrimesh_listVertices_coordinates(list_trimesh_mesh_triangles)
    vertices_triangleIndex = getTriangleIndex_Vertices(list_trimesh_mesh_triangles, vertices_coordinates)
    # Listen edges_verticesIndex:
    
    edges_verticesIndex = getListEdges(trimesh_mesh, list_trimesh_mesh_triangles, vertices_coordinates)
    # Listen triangles: 
    # triangles_verticesIndex, triangles_edgesIndex: 
    triangles_verticesIndex, triangles_edgesIndex = getListTriangles_VerticesIndex_EdgeIndex(list_trimesh_mesh_triangles, edges_verticesIndex, vertices_coordinates)
    # triangles_normals:
    triangles_normals = getTriangles_normals(list_trimesh_mesh_triangles)
    # Listen edges_trianglesIndex:
    edges_trianglesIndex = getListEdges_IndexOfTriangles(triangles_edgesIndex, edges_verticesIndex)




    return vertices_coordinates, vertices_triangleIndex, edges_verticesIndex, edges_trianglesIndex, triangles_edgesIndex, triangles_verticesIndex, triangles_normals


    


##################################################################


