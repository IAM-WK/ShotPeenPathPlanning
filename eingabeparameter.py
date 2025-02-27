# eingabeparameter.py

import numpy as np


######################################################

# Eingabe der Eingabeparameter:

# 1. Pfad zur STL-Datei
# Bsp. STL Dateipfade vorgefertigt hier
# !!! !
# EINFÜGEN!!!, die hier in Ordner hinterlegt sind

# 1. path_stl 
#Dateipfad entsprechend anpassen, STL Dateien der Beispiel Geometrien sind im Ordner Geometrien hinterlegt
# path_stl = r"C:\...\zylindrischeBohrung.stl"
# path_stl = r"C:\...\zugprobe.stl"
#path_stl = r"C:\...\cuboid.stl"

# 2. Name der Job Datei wählen, string, ohne endung
name_jobDatei = "NAMEJOBDATEI" 

# 3. Werkzeugnummer
werkzeugnummer = 0

# 4. Abstand Zwischen TCP und und Oberfläche, 
# Angabe in mm
d_offset = 20

# 5. Position des Ursprngs des Proben/ Geometrie KOS bezüglich des Roboter KOS, Koordinaten als Liste, 
# Angaben in mm

# Anm.: 
# NullPos Roboter = [560, 0, 485, 180, -90, 0]

x_koord = 600
y_koord = 0
z_koord = 400

pos_probe = [x_koord, y_koord, z_koord]

# 6. Pfad Linien Abstand, (wichtig für Überdeckung)
# Angabe in mm
ebenenabstand = 5.0

# 7. Geschwindigkeit, linear Bewegung
geschwindigkeit_movl = 30 # Angabe in mm/s, (wichtig für Überdeckung)
# 8. Geschwindigkeit, joint Bewegung
geschwindigkeit_movj = 20 # Angabe in % der Maximalgeschwindigkeit

# 9. Timer
# Angabe in s
timer = 2.00

# 10. hinterschnitte vorliegend, ja = true, nein = false
# Eingab, ob mit Hinderniserkennung oder ohne, boolean: True = mit Hindernis, False = ohne HIndernis
hinterschnitt = False

# 11. Winkel wählen für patch bildung, Grenzwinkel, 
# sinnvolle Wahl: np.pi/4, bzw. 45°
anlge_patches = np.pi/4

# 12. Winkel wählen für die Bestimmung des hindernisfreien Pfades, Feinheit
# Angabe in rad
angle_hindernisAusweichen = np.pi/10



######################################################

# Aufruf der Ausführenden Methode mit den Eingabeparametern in run.py

