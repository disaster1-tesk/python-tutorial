# Python类与对象示例

# 基本类定义
class Person:
    """人类"""
    # 类属性
    species = "Homo sapiens"
    
    def __init__(self, name, age):
        """构造方法"""
        # 实例属性
        self.name = name
        self.age = age
    
    def introduce(self):
        """自我介绍方法"""
        return f"我是{self.name}，今年{self.age}岁。"
    
    def have_birthday(self):
        """过生日"""
        self.age += 1
        print(f"{self.name}现在{self.age}岁了！")

# 创建对象
person1 = Person("张三", 25)
person2 = Person("李四", 30)

print(person1.introduce())
print(person2.introduce())

person1.have_birthday()

# 类方法和静态方法
class MathUtils:
    """数学工具类"""
    
    @classmethod
    def circle_area(cls, radius):
        """计算圆面积的类方法"""
        return 3.14159 * radius ** 2
    
    @staticmethod
    def add(x, y):
        """加法静态方法"""
        return x + y

print("圆面积:", MathUtils.circle_area(5))
print("加法结果:", MathUtils.add(3, 4))

# 继承示例
class Student(Person):
    """学生类，继承自Person类"""
    
    def __init__(self, name, age, student_id):
        """构造方法"""
        super().__init__(name, age)  # 调用父类构造方法
        self.student_id = student_id
        self.courses = []
    
    def enroll_course(self, course):
        """选课"""
        self.courses.append(course)
        print(f"{self.name}选修了{course}")
    
    def introduce(self):
        """重写父类的自我介绍方法"""
        base_info = super().introduce()
        return f"{base_info}我的学号是{self.student_id}。"

# 创建学生对象
student = Student("王五", 20, "2023001")
print(student.introduce())
student.enroll_course("Python编程")
student.enroll_course("数据结构")

# 属性装饰器示例
class Temperature:
    """温度类"""
    
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """摄氏度属性"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """摄氏度属性的setter"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """华氏度属性"""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        """华氏度属性的setter"""
        self.celsius = (value - 32) * 5/9

# 使用属性装饰器
temp = Temperature(25)
print(f"摄氏度: {temp.celsius}")
print(f"华氏度: {temp.fahrenheit}")

temp.fahrenheit = 100
print(f"华氏100度等于摄氏{temp.celsius:.2f}度")