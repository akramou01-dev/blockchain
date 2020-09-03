from vehicle import Vehicle
class Bus(Vehicle):
      # top_speed = 100
    # warnings = []
    def __init__(self,top_speed= 100):
        super().__init__(top_speed)
        self.passengers = []


    def add_group(self,passengers):
        self.passengers.extend(passengers)

 
bus1 = Bus(90)
bus1.add_group(['Akram','Mohamed','Abdel-ileh','ouardas'])
# bus1.add_warning('test')
bus1.drive()
print(bus1.passengers)