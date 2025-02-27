import numpy as np
import trimesh
import copy
import sympy
from stl import mesh
import csv

#import koordinatentrafo # ??? nos

# eingabeparameter
# from eingabeparameter import name_jobDatei, werkzeugnummer, geschwindigkeit_movl, geschwindigkeit_movj, timer
# 


# # Anm.: Zeilenumbrüche in Text dat m.H. "\r\n" realisieren, sonst Datei nicht für Roboter lesbar


def write_list_to_csv_dat(filename, list_points):
    with open( filename, 'w', newline='') as csv_file:
        csv_file.write("x, y, z \r\n")
        mywriter = csv.writer(csv_file, delimiter=',')
        mywriter.writerows(list_points)
    print("\r\n list_points written to file ", filename) # testen 
    return None

#### Funktionen zum erstellen der JOB.JBI Datei

def JBI_file(name_jobDatei, werkzeugnummer, timer, POSTYPE_string, RCONF_list_24int, DATE_str, FRAME_string, geschwindigkeit_movl, geschwindigkeit_movj, pathData): # vorher war letzter parameter = trajectories_woEinspannung_list
    ####
    # geschwindigkeit_movl : velocity (z.B. 50.0) in mm/s
    # geschwindigkeit_movj : in prozent (z.B. 20.0)
    # DATE_str = "2023/02/16 17:21", z.B.
    #frame_str = BASE zb
    # s. NEWJOB3.JBI, was ist RCONF ????
    # s. NEWJOB3.JBI, was ist NPOS ?
    
    # anzahl_pos insgesamt berechnen 
    anzahl_pos = 1 # für null pos
    for i in range(len(pathData)): # je patch
        for j in range(len(pathData[i][0])):  # je koord in patch i
            anzahl_pos = anzahl_pos + 1 # zähler erhöhen


    #### ändern, sodass endung niht mehr in text name steht
    name_jobDatei_endung = name_jobDatei + ".JBI"
    with open( name_jobDatei_endung, 'w', newline='') as JBI_file:
        JBI_file.write("/JOB\r\n")
        JBI_file.write("//NAME " + name_jobDatei + "\r\n")
        JBI_file.write("//POS\r\n")
        JBI_file.write("///NPOS " + str(anzahl_pos)+"," + str(0)+"," + str(0)+"," + str(0)+"," + str(0)+"," + str(0) + "\r\n")
        JBI_file.write("///TOOL " + str(werkzeugnummer) + "\r\n")
        JBI_file.write("///POSTYPE " +str(POSTYPE_string)+"\r\n")
        JBI_file.write("///RECTAN\r\n")
        
        
        #Winkel = [[180.0, 0.0, 0.0], [180.0, -90.0, -90.0], [180.0, -90.0, -90.0], [180.0, -90.0, -90.0], [180.0, -90.0, -90.0]] # facets, erste seitliche dann oberes
        # Punkte auslesen aus trajectories_woEinspannung_list
        #zähler für alle punkte/ variablen:
        count_var = 0

        # RCONF
        JBI_file.write("///RCONF ") #### ??? ??? 
        for l in range(len(RCONF_list_24int)):
            if(l != len(RCONF_list_24int)-1):
                JBI_file.write(str(RCONF_list_24int[l]) + ",")
            else: # ende
                JBI_file.write(str(RCONF_list_24int[l]) + "\r\n")

        ##JBI_file.write("\r\n")
        #JBI_file.write("///RCONF 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\r\n") 


        # Nullpos eingeben
        JBI_file.write("C0000" + str(count_var) + "=")
        # in pathData[i][0]: punkt koordinaten, 
        JBI_file.write(str(560.00) + "," + str(0.00) + "," + str(485.00))
        # in pathData[i][1]: winkel,
        #JBI_file.write("," + str(pathData[i][1][j][0])  + "," + str(pathData[i][1][j][1])  + "," + str(pathData[i][1][j][2])  + "\r\n")
        JBI_file.write("," + str(180)  + "," + str(-90.00)  + "," + str(0.00)  + "\r\n")
        
        count_var = 1

        for i in range(len(pathData)): # je patch
            
            for j in range(len(pathData[i][0])): # je punkt in patch
                """
                if(i != 0 and j == 0):
                    JBI_file.write("///RCONF 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\r\n") #### ??? TEST ??? 
                elif(i != 0 and j == 1):
                    JBI_file.write("///RCONF 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\r\n") 
                """
                print("j : ", j)
                if(count_var < 10):
                    JBI_file.write("C0000" + str(count_var) + "=")
                elif(count_var< 100):
                    JBI_file.write("C000" + str(count_var) + "=")
                elif(count_var< 1000):
                    JBI_file.write("C00" + str(count_var) + "=")
                elif(count_var< 10000):
                    JBI_file.write("C0" + str(count_var) + "=")
                elif(count_var< 100000):
                    JBI_file.write("C" + str(count_var) + "=")
                # Erinnerung: Eingabe der Daten ist liste
                # jeder eintrag ein Patch: 
                # je Patch: zwei listen
                # 1. schleife: patchNummer durchlaufen
                # 2. Schleife: Punktnummer durchlaufen
                # erste ist liste der coordinaten also: eingabe[patchNummer][0][Punktnummer]
                # zweie ist liste der winkel also: eingabe[patchNummer][1][Punktnummer]

                
                # in pathData[i][0]: punkt koordinaten, 
                JBI_file.write(str(pathData[i][0][j][0]) + "," + str(pathData[i][0][j][1]) + "," + str(pathData[i][0][j][2]))
                # in pathData[i][1]: winkel,
                #JBI_file.write("," + str(pathData[i][1][j][0])  + "," + str(pathData[i][1][j][1])  + "," + str(pathData[i][1][j][2])  + "\r\n")
                JBI_file.write("," + str(pathData[i][1][j][0])  + "," + str(pathData[i][1][j][1])  + "," + str(pathData[i][1][j][2])  + "\r\n")
                
                count_var = count_var+1
            #JBI_file.write("\r\n")

 
        #### ARG Nicht notwendig
        #JBI_file.write("//ARGINFO \r\n")
        #JBI_file.write("///ARGTYPE B,,,,,,, \r\n") 
        #JBI_file.write("///COMMENT \r\n")
        #JBI_file.write("Arg1 \r\n \r\n \r\n \r\n \r\n")
        



        JBI_file.write("//INST" + "\r\n")
        JBI_file.write("///DATE " + str(DATE_str)+"\r\n")
        JBI_file.write("///ATTR SC,RW,RJ\r\n") 
        JBI_file.write("////FRAME " + str(FRAME_string) + "\r\n")
        JBI_file.write("///GROUP1 RB1\r\n") 

        JBI_file.write("NOP\r\n")
        #### 

        # Anfahren der Null Pos
        JBI_file.write("MOVJ ")
        JBI_file.write("C0000" + str(0) + " ")
        JBI_file.write("VJ=" + str(geschwindigkeit_movj) + "\r\n")

        count_var_2 = 1
        for i in range(len(pathData)): # je patch 
            for j in range(len(pathData[i][0])): # je punkt in patch
                if(j == 0):
                    JBI_file.write("TIMER T=" + str(timer) + "\r\n")
                    JBI_file.write("MOVJ ")
                else:
                    JBI_file.write("MOVL ")


                if(count_var_2 < 10):
                    JBI_file.write("C0000" + str(count_var_2) + " ")
                elif(count_var_2< 100):
                    JBI_file.write("C000" + str(count_var_2) + " ")
                elif(count_var_2< 1000):
                    JBI_file.write("C00" + str(count_var_2) + " ")
                elif(count_var_2< 10000):
                    JBI_file.write("C0" + str(count_var_2) + " ")
                elif(count_var_2< 100000):
                    JBI_file.write("C" + str(count_var_2) + " ")

                count_var_2 = count_var_2 + 1
                # Geschwindigkeit und PL angeben ggf.
                if(j == 0): # bei MOVJ
                    JBI_file.write("VJ=" + str(geschwindigkeit_movj) + "\r\n")
                else: # bei MOVL
                    JBI_file.write("V=" + str(geschwindigkeit_movl) + " PL=0" + "\r\n") # mit PL=0
                    #JBI_file.write("V=" + str(geschwindigkeit_movl) + " \r\n") # ohne PL=0, test
                # Timer setzen 
        JBI_file.write("END\r\n")

    print("\r\n list_points written to file ", name_jobDatei)
    return None
        





