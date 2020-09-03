class Vehicle:
    def __init__(self,starting_top_speed=100):
        # initializing the attributs
        self.top_speed = starting_top_speed
        self.__warnings = []
        self.passengers = []


    def drive(self):
           print("I'am drinving but certainly not faster than {} ".format(self.top_speed))


    def add_warning(self,warning_txt): 
        if len(warning_txt) > 0:
            self.__warnings.append(warning_txt)


    def __repr__(self):
        print(" printing !")
        return "Top speed is :{} warnings are : {} ".format(self.top_speed, len(self.__warnings))
      
    def get_warning(self):
        return self.__warnings