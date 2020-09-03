from vehicle import Vehicle


class Car(Vehicle):
    # top_speed = 100
    # warnings = []
    def breg(self):
        print('look how cool my car is !')

car_1 = Car()
car_1.drive() 
car_1.add_warning('new warnings! ')
car_1.add_warning('this the second warning')

# print(car_1.__dict__)
print(car_1)
car_2 = Car(200)
car_2.drive()




car_3 = Car(300)
car_3.drive()
print(car_1.get_warning())
