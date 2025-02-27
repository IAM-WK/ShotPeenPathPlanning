#


""""""
class Obstacle_Info:
    def __init__(self, b_liegtInEbeneTriangle, parameter):
        self.b_liegtInEbeneTriangle = b_liegtInEbeneTriangle
        self.parameter = parameter
        self.b_isObstacle = None

    def setObstacle(self, b_isObstacle):
        self.b_isObstacle = b_isObstacle

    def spExists(self):
        if(not self.b_liegtInEbeneTriangle):
            if(self.parameter is not None): 
                return True
            else: 
                return False
        else:
            return False
                
#


""""""
class LineIntersection_Info:
    def __init__(self, b_linesIdentisch, parameter):
        self.b_linesIdentisch = b_linesIdentisch
        self.parameter = parameter

                
    def isObstacle_inPlane(self):
        # prüfen, ob liste eintrag, bzw ob geraden windschief, parallel, keinen schnitt auf weisen.#
        if(not self.b_linesIdentisch):
            if(self.parameter is not None):
                return True
            else:
                return False
        else: 
            return True



