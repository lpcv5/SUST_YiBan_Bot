from utils.sql import Sql
import os


def menu():
    flag = 1
    while flag:
        print("----------------------------SUST晨午检小助手----------------------------")
        print("1、添加用户")
        print("2、查看服务运行状态")
        print("3、启动自动晨午检服务")
        print("4、添加晨午检反馈邮箱")
        print("0、退出菜单")
        aim = int(input())
        if aim == 1:
            add_user()
        elif aim == 2:
            show_service_state()
        elif aim == 3:
            pass
        elif aim == 4:
            pass
        elif aim == 0:
            flag = 0
            print("准备退出")
        else:
            print("请输入正确的选项")


def start_service():
    command = '10 7,12 * * * python ./auto_check_service.py'
    p = os.system(command)
    if p == 1:
        print(p, "开启成功")


def show_service_state():
    print("正在运行")


def add_user():
    print("请依次输入要添加的账户、密码、信息上报地址")
    account = input()
    passwd = input()
    address = input()
    Sql.add_user(Sql(), account, passwd, address)


def main():
    menu()
    print("退出成功")


if __name__ == '__main__':
    main()
