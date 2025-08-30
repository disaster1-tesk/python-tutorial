# Python控制流示例

# 条件语句示例
age = 20
if age < 13:
    print("儿童")
elif age < 20:
    print("青少年")
elif age < 60:
    print("成年人")
else:
    print("老年人")

# 逻辑运算符示例
username = "admin"
password = "123456"

if username == "admin" and password == "123456":
    print("登录成功")
else:
    print("用户名或密码错误")

# for循环示例
print("使用for循环打印数字:")
for i in range(5):
    print(f"数字: {i}")

# 遍历列表
fruits = ["苹果", "香蕉", "橙子"]
print("遍历水果列表:")
for fruit in fruits:
    print(f"我喜欢吃{fruit}")

# while循环示例
print("使用while循环计数:")
count = 0
while count < 5:
    print(f"计数: {count}")
    count += 1

# 循环控制语句示例
print("使用break跳出循环:")
for i in range(10):
    if i == 3:
        break
    print(i)

print("使用continue跳过迭代:")
for i in range(5):
    if i == 2:
        continue
    print(i)

# 三元运算符示例
score = 85
grade = "及格" if score >= 60 else "不及格"
print(f"分数{score}的等级是:{grade}")

# 循环else子句示例
print("循环else子句示例:")
for i in range(3):
    print(i)
else:
    print("循环正常结束")

print("带break的循环else子句:")
for i in range(3):
    if i == 1:
        break
    print(i)
else:
    print("这行不会被打印")