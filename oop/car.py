class Car:
    # top_speed = 100
    # warnings = []
    def __init__(self,starting_top_speed=100):
        # initializing the attributs
        self.top_speed = starting_top_speed
        self.warnings = []

    def drive(self):
        print("I'am drinving but certainly not faster than {} ".format(self.top_speed))


car_1 = Car()
car_1.drive() 
car_1.warnings.append('new warnings! ')
print(car_1.warnings)
car_2 = Car(200)
car_2.drive()
car_2.warnings.append('new warning 2 !')

print(car_2.warnings)

car_3 = Car(300)
car_3.drive()
print(car_3.warnings)
