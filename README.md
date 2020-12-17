# conversation
在HA里使用的官方语音助手修改增强版


> 官方文档：https://www.home-assistant.io/integrations/conversation/

## 云音乐指令（需要配合云音乐播放器使用）

- 我想听xxx的歌
- 播放(电台|歌单|歌曲|专辑)xxx
- 下一曲
- 上一曲
- 播放音乐
- 暂停音乐
- 声音小点、小点声音、小一点声音、声音小一点
- 声音大点、大点声音、大一点声音、声音大一点

## 指令
- `打开|开启|启动|关闭|关掉|关上|切换` `switch名称|input_boolean名称|所有开关|所有的开关|全部开关|全部的开关`
- `打开|开启|启动|关闭|关掉|关上|切换` `x灯xx灯xxx灯`
- `打开|开启|启动|关闭|关掉|关上|切换` `light名称|所有灯|所有的灯|全部灯|全部的灯`
- 把 `light名称` `调成|设为|设置为|调为` `红|橙|黄|绿|青|蓝|紫|粉|白|紫红|橄榄|随机` 色
- 把 `light名称` `调成|设为|设置为|调为` `随机|频闪|闪光|彩虹|颜色流动|扫描|闪烁|随机闪烁|烟火` 模式
- 把 `light名称` 的亮度 `调成|调到|调为|设为` `1-100的数字`
- 执行脚本 `script名称`
- `执行|触发|打开|关闭`自动化`automation名称`
- `查看|查询` `Entity名称`的状态
- `查看|查询` `Entity名称`
- `Entity名称`的状态
- 打开`湖北|湖南|四川|吉林|海南|东南|广东|江苏|东方|云南|北京|浙江|天津|广西|山东|安徽|辽宁|重庆|陕西|北京`卫视
- 打开中央`1-17`台

## 摄像监控
- 查看xxx的画面

## 执行脚本
- 执行脚本（脚本名称=语音文本）

## node-red 和 自动化
- 监听ha_voice_text_event事件
- text: 语音文本

## 更新日志

### v1.3
- 解决不能操作所有灯和开关的问题
- 加入查看摄像监控的画面
- 修复`conversation.process`服务没作用的问题
- 升级`conversation`到官方最新版本
- 添加文本来源，区分内容是从哪里来的
- 当页面版本不一样时，自动跳转到最新版本页面
- 调整开关识别逻辑
- 更换新版图标
- 支持小爱同学自定义技能
- 支持灯光颜色控制（红、橙、黄、绿、青、蓝、紫、粉、白、紫红、橄榄、随机）
- 支持灯光亮度控制
- 支持灯光模式控制
- 支持电视投屏功能
- 记录语音文本
- 支持一次性打开关闭多个设备
- 支持语音结束后是否继续开麦控制
- 支持开启关闭同时操作
- 支持打开关闭空调设备
### v1.2
- 加入单独的聊天界面
- 支持`python_script.conversation`服务，接收`text`参数
- 优化聊天界面登录逻辑

### v1.1
- 优化代码结构
- 增加重载服务（修改配置不用重启）

### v1.0
- 当语音文本与脚本名称一致时，则触发脚本
- 语音文本匹配多个内容时，脚本名称使用=号分隔
- 定义ha_voice_text_event事件发送文本
- 语音支持：添加xxx到我的购物单
- 语音支持：我的购物单上有什么
- 集成聊天机器人