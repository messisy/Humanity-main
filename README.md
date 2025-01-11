Humanity Protocol 脚本

[点击注册➡](testnet.humanity.org/login?ref=messisy)

介绍
脚本每天自动 Humanity Protocol 签到领取 $RWT 奖励。

使用方法

按照以下步骤设置并运行脚本。

1. 克隆存储库

首先，使用 Git 将此存储库克隆到本地计算机：

git clone https://github.com/messisy/Humanity-main.git


2. 导航到克隆存储库的文件夹：

cd Humanity-main


3. 填写private_keys.txt
将私钥填入private_keys.txt文件。每行应包含一个私钥

private_key_1

private_key_2

private_key_3

...

代理功能

格式 


http://user:password@ip:port


4. 安装依赖项


pip install -r requirements.txt


5. 运行脚本



python main.py

