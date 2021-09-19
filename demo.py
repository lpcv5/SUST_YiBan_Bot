from utils.sql import Sql
import os


def menu():
    flag = 1
    while flag:
        print("----------------------------SUST晨午检小助手----------------------------")
        print("1、管理用户")
        print("2、查看服务运行状态")
        print("3、启动自动晨午检服务")
        print("4、添加晨午检反馈邮箱")
        print("0、退出菜单")
        aim = int(input())
        if aim == 1:
            manage_user()
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


def manage_user():
    flag = True
    while flag:
        print("----------------------------用户管理----------------------------")
        print("1、查询用户")
        print("2、添加用户")
        print("3、删除用户")
        print("4、更改地址")
        print("5、返回上一级")
        aim = int(input())
        if aim == 1:
            print(Sql.list_user(Sql()))
        elif aim == 2:
            add_user()
        elif aim == 3:
            delete_user()
        elif aim == 4:
            acc = input('请输入你要更改地址的账户')
            while True:
                address = input('请输入你要更改的新地址：')
                if 'yes' == input('输入yes并回车确认更改：'):
                    break
            Sql.update_user(Sql(), address, acc)
        elif aim == 5:
            return


def delete_user():
    account = input('请输入删除的账户名称')
    if Sql.delete_user(Sql(), account):
        print('删除成功')


def add_user():
    print("请依次输入要添加的账户、密码、信息上报地址、上报结果通知邮件")
    account = input('账户:')
    passwd = input('密码')
    address = input('地址')
    mail = input('通知邮件')
    Sql.add_user(Sql(), account, passwd, address, mail)


def main():
    menu()
    print("退出成功")


if __name__ == '__main__':
    main()
