# MonitorApkAdd
monitor an apk file new create
> 监控中转站中apk文件改变，自动安装apk到手机中，并打开指定应用
## 环境配置
1. 安装python3---自行安装
2. python3安装成功，环境变量配置成功之后，安装watchdog库
   命令行执行
   
   ```
   $ pip install watchdog
   ```
   
3. 修改脚本中的自定义文件
   DIRECTORY_NAME 修改为自己的中转站文件夹名称
   appStartCmd 修改为需要启动的应用主入口
4. 命令行运行python 脚本
```
 python .\monitorFile.py
 ```
  
5.  Ctrl+C 结束运行 
  
