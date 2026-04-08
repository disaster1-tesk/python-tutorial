class User:
    """用户类"""

    def __init__(self, name, chineseScore=0, mathScore=0, englishScore=0):
        self.name = name
        self.chineseScore = chineseScore
        self.mathScore = mathScore
        self.englishScore = englishScore

    def __str__(self):
        return f"{self.name} 的成绩是：语文 {self.chineseScore}，数学 {self.mathScore}，英语 {self.englishScore},总分为：{self.chineseScore + self.mathScore + self.englishScore}"

    def _get_chinese_score(self):
        return self.chineseScore

    def update_score(self, chineseScore, mathScore, englishScore):
        if chineseScore is not None:
            self.chineseScore = chineseScore
        if mathScore is not None:
            self.mathScore = mathScore
        if englishScore is not None:
            self.englishScore = englishScore


class EduManagementSystem:
    """教育管理系统"""
    system_version = "1.0.0"
    system_name = "教育管理系统"

    def __init__(self, users=None):
        if users is None:
            users = []
        self.users = users

    def verify_user(self, user):
        """验证用户成绩是否在有效范围内 (0-100)"""
        scores = [user.chineseScore, user.mathScore, user.englishScore]
        return all(0 <= score <= 100 for score in scores)

    def add_user(self, user):
        """添加用户，先验证成绩"""
        if not self.verify_user(user):
            print("添加失败：用户成绩无效")
            return
        self.users.append(user)

    def update_user(self, user):
        """更新用户信息，先验证成绩"""
        if not self.verify_user(user):
            print("更新失败：用户成绩无效")
            return

        for i, u in enumerate(self.users):
            if u.name == user.name:
                print(f"当前{u.name}成绩：中文成绩{u.chineseScore},英文成绩{u.englishScore},数学成绩{u.mathScore}")
                self.users[i] = user
                print(
                    f"{u.name}更新成功：中文成绩{user.chineseScore},英文成绩{user.englishScore},数学成绩{user.mathScore}")
                return

        print("没有该用户")

    def delete_user(self, name):
        """删除指定名称的用户"""
        for i, u in enumerate(self.users):
            if u.name == name:
                self.users.pop(i)
                return

        print("没有该用户")

    def show_all_users(self):
        """显示所有用户信息"""
        for user in self.users:
            print(user)


if __name__ == "__main__":
    ems = EduManagementSystem()
    print("欢迎使用教育管理系统")
    print("当前版本：", EduManagementSystem.system_version)
    print("当前系统名称：", EduManagementSystem.system_name)
    while True:
        flag = input("请选择操作：1. 添加用户 2. 更新用户 3. 删除用户 4.查询所有用户 5. 退出\n")
        if flag == "1":
            name = input("请输入学生姓名：")
            try:
                chineseScore = int(input("请输入学生语文成绩："))
                mathScore = int(input("请输入学生数学成绩："))
                englishScore = int(input("请输入学生英语成绩："))
                user = User(name, chineseScore, mathScore, englishScore)
                ems.add_user(user)
            except ValueError:
                print("输入错误：成绩必须是整数。")

        if flag == "2":
            name = input("请输入学生姓名：")
            try:
                chineseScore = int(input("请输入学生语文成绩："))
                mathScore = int(input("请输入学生数学成绩："))
                englishScore = int(input("请输入学生英语成绩："))
                user = User(name, chineseScore, mathScore, englishScore)
                ems.update_user(user)
            except ValueError:
                print("输入错误：成绩必须是整数。")

        if flag == "3":
            name = input("请输入学生姓名：")
            ems.delete_user(name)
            print("删除成功")

        if flag == "4":
            ems.show_all_users()

        if flag == "5":
            print("退出系统")
            exit()
