# SUST_YiBan_Bot

使用python自动化脚本来完成一些列操作
部署到服务器上，可利用cron定时任务运行
验证码采用了自己服务器的api来进行识别

## 项目结构

```
├─ auto_check_service.py				# 在这里面填入你的登陆信息一键晨午检
├─ README.md
├─ requirements.txt
├─ util.py										  # 和登陆有关的模块
├─ captcha.py								    # 获取验证码，并对验证码进行识别
└─ post_data.py								  # 信息上报数据提交模块



```



## 使用方法



### 1.安装依赖

```shell
pip install -r requirements.txt
```

### 2.添加你要打卡的个人数据

> 运行main.py

```shell
python main.py
```

> 运行结果如下

<img src=".\mdimg\Snipaste_2021-09-19_12-05-34.png" alt="image-20210919120135069" style="zoom:50%;" />

按照选项操作即可

### 3.关于自动晨午检

​	如果你是在windows上使用，可以参照这篇文章[使用Windows任务计划自动运行Python程序_若如初见-CSDN博客_任务计划程序运行python脚本](https://blog.csdn.net/Artificial_idiots/article/details/108570387)

​	如果你是部署到自己的linux服务器上，直接使用crond脚本自动执行



## 如果有问题 欢迎邮件联系lpengcheng149@gmail.com 或者 issues
