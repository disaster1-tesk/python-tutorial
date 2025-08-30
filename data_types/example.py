# Python数据类型示例

# 数字类型
integer_num = 42
float_num = 3.14159
complex_num = 3 + 4j

print("整数:", integer_num, type(integer_num))
print("浮点数:", float_num, type(float_num))
print("复数:", complex_num, type(complex_num))

# 布尔类型
is_python_fun = True
is_java_better = False

print("Python有趣吗?", is_python_fun, type(is_python_fun))
print("Java更好吗?", is_java_better, type(is_java_better))

# 字符串类型
single_quote = '单引号字符串'
double_quote = "双引号字符串"
multi_line = """多行
字符串
示例"""

print("单引号:", single_quote)
print("双引号:", double_quote)
print("多行字符串:", multi_line)

# 列表类型
fruits = ["苹果", "香蕉", "橙子"]
numbers = [1, 2, 3, 4, 5]

print("水果列表:", fruits, type(fruits))
fruits.append("葡萄")  # 添加元素
print("添加葡萄后:", fruits)

# 元组类型
coordinates = (10, 20)
rgb_color = (255, 128, 0)

print("坐标:", coordinates, type(coordinates))
# coordinates[0] = 15  # 这会报错，因为元组不可变

# 字典类型
person = {
    "name": "张三",
    "age": 30,
    "city": "北京"
}

print("个人信息:", person, type(person))
print("姓名:", person["name"])  # 访问字典值
person["job"] = "程序员"  # 添加新的键值对
print("更新后:", person)

# 集合类型
unique_numbers = {1, 2, 3, 3, 2, 1}  # 重复元素会被自动去除
print("集合:", unique_numbers, type(unique_numbers))

# 类型检查
print("42是整数吗?", isinstance(42, int))
print("3.14是字符串吗?", isinstance(3.14, str))