class Car:
    #__init__方法是初始化的方法，会在创建对象时自动调用 可以在该方法中为对象设置对应的属性
    #self参数 无实际意义
    def __init__(self, car_name, car_price):
        self.car_name = car_name
        self.car_price = car_price
    #魔法方法 __init__ __str__ __eq__ 自动调用

    #类属性和实例属性 先访问实例属性
    car_name="los"


benz=Car("Benz", "10")
print(benz.car_name)
print(Car.car_name)

#异常
try:
    print(Car.car_name)
except Exception as e:
    print("有问题")
