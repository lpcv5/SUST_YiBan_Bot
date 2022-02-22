# SUST_YiBan_Bot

使用python自动化脚本来完成一些列操作
部署到服务器上，可利用cron定时任务运行



# Feathers

- ~~验证码采用了自己服务器的api来进行识别~~（0.2.1已经集成到项目中方便大家使用）

- 通过抓包得到了晨午检数据提交的接口，可以无视打卡时间，一键完成晨午检打卡



# changelog 

## [0.2.1] -- 2022.2.23

#### Added

- 将验证码识别集成到项目中

  （识别验证码使用了开源项目 :  [验证码识别 - 部署](https://github.com/kerlomz/captcha_platform) ，因此需要安装tensorflow，亲测python3.9 + tensorflow==2.7.0可以完美运行）

- 采用 yaml 配置文件方式方便多用户使用

## [0.2] -- 2022.1.30

### Fix

- 更新登陆接口

​	

-------



## 项目结构

```
root:[./]
+--account.yaml # 账号存储配置文件
+--captcha.py # 调用 readcaptcha 目录中的模型对进行验证码识别
+--main.py  # 主程序
+--post_data.py # 晨午检数据提交
+--readcaptcha  # tensorflow 识别验证码核心
|      +--captch_crack_service.py
|      +--categorys.py
|      +--config.py
|      +--config.yaml
|      +--event_handler.py
|      +--event_loop.py
|      +--graph
|      |      +--YIBAN-CNN5-GRU-H64-CTC-C1_9900.pb
|      +--graph_session.py
|      +--interface.py
|      +--middleware
|      |      +--constructor
|      |      |      +--color_extractor.py
|      |      +--impl
|      |      |      +--color_extractor.py
|      |      |      +--color_filter.py
|      |      |      +--corp_to_multi.py
|      |      |      +--gif_frames.py
|      |      |      +--rgb_filter.py
|      |      +--resource
|      |      |      +--color_filter.py
|      |      |      +--__init__.py
|      +--model
|      |      +--YIBAN-CNN5-GRU-H64-CTC-C1_model.yaml
|      +--predict.py
|      +--pretreatment.py
|      +--utils.py
+--README.md
+--requirements.txt
+--util.py  # 登录接口相关工具
```



## 使用方法



### 1.安装依赖

```shell
pip install -r requirements.txt
```

### 2.在``` account.yaml```添加你要打卡的个人数据

### 3.运行```main.py```

```py
python main.py
```





## 如果有问题 欢迎邮件联系lpengcheng149@gmail.com 或者 issues
