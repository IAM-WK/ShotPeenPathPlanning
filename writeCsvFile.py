import csv

def write_list_to_csv_dat(filename, list_points):
    with open( filename, 'w', newline='') as csv_file:
        csv_file.write("x, y, z \r\n")
        mywriter = csv.writer(csv_file, delimiter=',')
        mywriter.writerows(list_points)
    print("\r\n list_points written to file ", filename) 
    return None

def patchToVerticesList(patch, list_triangle_verticesIndex, list_vertices_coordinates, filename):

    liste_vertices = []
    
    for triIndex in patch:
        for verticesIndex in range(3):
            liste_vertices.append(list_vertices_coordinates[list_triangle_verticesIndex[triIndex][verticesIndex]])
    print("W: liste_vertices = ", liste_vertices)
    write_list_to_csv_dat(filename, liste_vertices)

def writeTriangle(triangle_index, list_triangle_verticesIndex, list_vertices_coordinates, filename):
    triangle_verticesCoordinates = []
    for i in range(3): # TRIangle
        triangle_verticesCoordinates.append(list_vertices_coordinates[list_triangle_verticesIndex[triangle_index][i]])

    
    triangle_verticesCoordinates.append(list_vertices_coordinates[list_triangle_verticesIndex[triangle_index][0]])
    print("triangle_verticesCoordinates = ", triangle_verticesCoordinates)
    write_list_to_csv_dat(filename, triangle_verticesCoordinates)