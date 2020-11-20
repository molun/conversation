import logging, re, aiohttp
from homeassistant.helpers import intent
import homeassistant.config as conf_util
from homeassistant.helpers import template
from homeassistant.helpers.network import get_url

from .xiaoai_view import XiaoaiGateView

_LOGGER = logging.getLogger(__name__)

VERSION = '1.6'
DOMAIN = "conversation"
DATA_AGENT = "conversation_agent"
DATA_CONFIG = "conversation_config"

def text_start(findText, text):
    return text.find(findText,0,len(findText)) >= 0

class Voice():

    def __init__(self, hass):
        self.hass = hass
        hass.services.async_register(DOMAIN, 'reload', self.reload)
        # 显示插件信息
        _LOGGER.info('''
    -------------------------------------------------------------------
        语音小助手【作者QQ：635147515】
        
        版本：''' + VERSION + '''
        
        介绍：官方语音助手修改增强版
        
        项目地址：https://github.com/shaonianzhentan/conversation

    -------------------------------------------------------------------''')
        local = hass.config.path("custom_components/conversation/local")
        hass.http.register_static_path('/conversation', local, False)
        hass.http.register_view(XiaoaiGateView)

    # 解析模板
    def template(self, message):
        tpl = template.Template(message, self.hass)
        return tpl.async_render(None)

    # 返回意图结果
    def intent_result(self, message):
        intent_result = intent.IntentResponse()
        intent_result.async_set_speech(message)
        return intent_result

    # 重新加载配置
    async def reload(self, service):
        hass = self.hass
        # 读取配置
        hass.data[DATA_CONFIG] = await conf_util.async_hass_config_yaml(hass)
        # 清除agent
        hass.data[DATA_AGENT] = None

    # 异步调用服务
    def call_service(self, service, data):
        arr = service.split('.')
        self.hass.async_create_task(self.hass.services.async_call(arr[0], arr[1], data))

    # 语音服务处理
    async def async_process(self, text):
        # 去掉前后标点符号
        _text = self.fire_text(text)
        # 执行自定义语句
        intent_result = await self.execute_action(_text)
        if intent_result is not None:
            return intent_result
        
        # 开关控制
        intent_result = await self.execute_switch(_text)
        if intent_result is not None:
            return intent_result

        # 灯光颜色控制
        intent_result = await self.execute_light_color(_text)
        if intent_result is not None:
            return intent_result

        # 调用聊天机器人
        message = await self.chat_robot(text)
        return self.intent_result(message)

    # 触发事件
    def fire_text(self, text):
        hass = self.hass
        # 去掉前后标点符号
        _text = text.strip(' 。，、＇：∶；?‘’“”〝〞ˆˇ﹕︰﹔﹖﹑·¨….¸;！´？！～—ˉ｜‖＂〃｀@﹫¡¿﹏﹋﹌︴々﹟#﹩$﹠&﹪%*﹡﹢﹦﹤‐￣¯―﹨ˆ˜﹍﹎+=<­­＿_-\ˇ~﹉﹊（）〈〉‹›﹛﹜『』〖〗［］《》〔〕{}「」【】︵︷︿︹︽_﹁﹃︻︶︸﹀︺︾ˉ﹂﹄︼')
        # 预处理文本结果
        command = ''
        command_data = ''
        
        matchObj = re.match(r'.*(下一曲|下一首|下一集).*', text)
        if matchObj is not None:
            command = 'next'

        if matchObj is None:
            matchObj = re.match(r'.*(上一曲|上一首|上一集).*', text)
            if matchObj is not None:
                command = 'prev'
        
        if matchObj is None:
            matchObj = re.match(r'.*(音量调到|音量设置到|设置音量到)(.*)', text)
            if matchObj is not None:
                command = 'set_volume'
                command_data = matchObj.group(2)

        # 发送事件，共享给其他组件
        text_data = {
            'text': _text,
            'command': command,
            'command_data': command_data
        }
        hass.bus.fire('ha_voice_text_event', text_data)
        # 调用python_script.conversation
        if hass.services.has_service('python_script', 'conversation'):
            hass.async_create_task(hass.services.async_call('python_script', 'conversation', text_data))
        return _text

    # 根据名称查询设备
    def find_device(self, name):
        # 遍历所有实体
        states = self.hass.states.async_all()
        for state in states:
            attributes = state.attributes
            friendly_name = attributes.get('friendly_name')
            # 查询对应的设备名称
            if friendly_name is not None and friendly_name.lower() == name.lower():
                return state
        return None

    # 查看设备
    def query_device(self, text):
        hass = self.hass
        device_type = None
        if text == '查看全部设备':
            device_type = ''
        elif text == '查看全部灯':
            device_type = '.light'
        elif text == '查看全部传感器':
            device_type = '.sensor'
        elif text == '查看全部开关':
            device_type = '.switch'
        elif text == '查看全部脚本':
            device_type = '.script'
        elif text == '查看全部自动化':
            device_type = '.automation'
        elif text == '查看全部场景':
            device_type = '.scene'

        if device_type is not None:
            return self.intent_result(self.template('''
                <table border cellpadding="5" style="border-collapse: collapse;">
                    <tr><th>名称</th><th>状态</th><th>操作</th></tr>
                    {% for state in states''' + device_type + ''' -%}
                    <tr>
                        <td>{{state.attributes.friendly_name}}</td>
                        <td>{{state.state}}</td>                        
                        <td>
                            {% if 'light.' in state.entity_id or 
                                  'switch.' in state.entity_id or
                                  'script.' in state.entity_id or
                                  'automation.' in state.entity_id or
                                  'scene.' in state.entity_id -%}
                                <a onclick="triggerDevice('{{state.entity_id}}', '正在执行', `{{state.attributes.friendly_name}}`)" style="color:#03a9f4;">触发</a>
                            {%- else -%}
                 
                            {%- endif %}
                        </td>
                    </tr>
                    {%- endfor %}
                </table>
            '''))
        return None

    # 执行动作
    async def execute_action(self, text):
        hass = self.hass
        if text == '重新加载配置':
            self.reload()
            return self.intent_result("重新加载配置成功")

        # 如果有查询到设备，则返回
        device_result = self.query_device(text)
        if device_result is not None:
            return device_result

        # 遍历所有实体
        states = hass.states.async_all()
        for state in states:
            entity_id = state.entity_id
            attributes = state.attributes
            state_value = state.state
            friendly_name = attributes.get('friendly_name')
            # 执行自定义脚本
            if entity_id.find('script.') == 0:
                cmd = friendly_name.split('=')
                if cmd.count(text) > 0:
                    arr = entity_id.split('.')
                    _LOGGER.info('执行脚本：' + entity_id)
                    await hass.services.async_call(arr[0], arr[1])
                    return self.intent_result("正在执行自定义脚本：" + entity_id)
            # 查询设备状态
            if friendly_name is not None:
                friendly_name_lower = friendly_name.lower()
                if text.lower() == friendly_name_lower + '的状态':
                    return self.intent_result(friendly_name + '的状态：' + state.state)
                # 查询设备属性
                if text.lower() == friendly_name_lower + '的属性':
                    message = self.template('''
                    {% set entity_id = "''' + entity_id + '''" -%}
                    <table border cellpadding="5" style="border-collapse: collapse;">
                        <tr>
                            <th>{{entity_id}}</th>
                            <th>{{states(entity_id)}}</th>
                        </tr>
                        {% for state in states[entity_id].attributes -%}
                        <tr>
                            <td>{{state}}</td>
                            <td>{{states[entity_id].attributes[state]}}</td>
                        </tr>  
                        {%- endfor %}
                    </table>
                    ''')
                    return self.intent_result(message)
                # 查询摄像监控画面
                if text.lower() == '查看' + friendly_name_lower + '的画面':
                    return self.intent_result(self.template('''
                    {% set image = states['camera.generic_camera'].attributes['entity_picture'] %}
                    <a href="{{ image }}" target="_blank">  <img src="{{ image }}" style="max-width:100%;" /> </a>
                    '''))

        return None
    
    # 执行灯光调色
    async def execute_light_color(self, text):
        matchObj = re.match(r'(.+)(调成|设为|调为)(.*)色', text)
        if matchObj is not None:
            name = matchObj.group(1) 
            color = matchObj.group(3)
            colorObj = {
                '红': 'red',
                '橙': 'orange',
                '黄': 'yellow',
                '绿': 'green',
                '青': 'red',
                '蓝': 'blue',
                '紫': 'red',
                '粉': 'pink',
                '白': 'white'
            }            
            # 设备
            if name[0:1] == '把':
                name = name[1:]
            # print(name)
            state = self.find_device(name)
            if state is not None:
                # 颜色
                if color in colorObj:
                    self.call_service('light.turn_on', {
                        'entity_id': state.entity_id,
                        'color_name': colorObj[color]
                    })
                    return self.intent_result(f"已经设置为{color}色")

    # 执行开关
    async def execute_switch(self, _text):
        hass = self.hass
        intent_type = ''
        service_type = ''

        matchObj = re.match(r'.*((打开|开启|启动)(.+))', _text)
        if matchObj is not None:
            intent_type = 'HassTurnOn'
            service_type = 'turn_on'
            _name = matchObj.group(3)
        
        if matchObj is None:
            matchObj = re.match(r'.*((关闭|关掉|关上)(.+))', _text)
            if matchObj is not None:
                intent_type = 'HassTurnOff'
                service_type = 'turn_off'
                _name = matchObj.group(3)

        if matchObj is None:
            matchObj = re.match(r'.*((切换)(.+))', _text)
            if matchObj is not None:
                intent_type = 'HassToggle'
                service_type = 'toggle'
                _name = matchObj.group(3)
        
        # 默认的开关操作
        if intent_type != '':
            # 操作所有灯和开关
            if _name == '所有灯' or _name == '所有的灯' or _name == '全部灯' or _name == '全部的灯':
                await hass.services.async_call('light', service_type, {
                    'entity_id': self.template('{% for state in states.light -%}{{ state.entity_id }},{%- endfor %}').strip(',')
                })
                return self.intent_result("正在" + _text + self.template('''
                    <hr />
                    <table border cellpadding="5" style="border-collapse: collapse;">
                        <tr><th>名称</th><th>状态</th></tr>
                        {% for state in states.light -%}
                        <tr>
                            <td>{{state.attributes.friendly_name}}</td>
                            <td>{{state.state}}</td>  
                        </tr>
                        {%- endfor %}
                    </table>
                '''))
            elif _name == '所有开关' or _name == '所有的开关' or _name == '全部开关' or _name == '全部的开关':
                await hass.services.async_call('switch', service_type, {
                    'entity_id': self.template('{% for state in states.switch -%}{{ state.entity_id }},{%- endfor %}').strip(',')
                })
                await hass.services.async_call('input_boolean', service_type, {
                    'entity_id': self.template('{% for state in states.switch -%}{{ state.entity_id }},{%- endfor %}').strip(',')
                })
                return self.intent_result("正在" + _text + self.template('''
                    <hr />
                    <table border cellpadding="5" style="border-collapse: collapse;">
                        <tr><th>名称</th><th>状态</th></tr>
                        {% for state in states.switch -%}
                        <tr>
                            <td>{{state.attributes.friendly_name}}</td>
                            <td>{{state.state}}</td>  
                        </tr>
                        {%- endfor %}
                        {% for state in states.input_boolean -%}
                        <tr>
                            <td>{{state.attributes.friendly_name}}</td>
                            <td>{{state.state}}</td>  
                        </tr>
                        {%- endfor %}
                    </table>
                '''))
            else:
                # 如果没有这个设备，则返回为空
                if self.find_device(_name) is None:
                    return None

                await intent.async_handle(hass, DOMAIN, intent_type, {'name': {'value': _name}})
            return self.intent_result("正在" + _text)
        return None

    # 聊天机器人
    async def chat_robot(self, text):
        message = "对不起，我不明白"
        try:
            async with aiohttp.request('GET','https://api.ownthink.com/bot?appid=xiaosi&spoken=' + text) as r:
                res = await r.json(content_type=None)
                _LOGGER.info(res)
                message = res['data']['info']['text']
        except Exception as e:
            _LOGGER.info(e)        
        return message

    # 记录语音识别语句
    async def set_state(self, text=VERSION, source = '', timestamp = ''):
        hass = self.hass
        try:
            base_url = get_url(hass)
        except Exception as ex:
            base_url = 'http://localhost:8123'
        hass.states.async_set('conversation.voice', text, {
            "icon": "mdi:account-voice",
            "friendly_name": "语音助手",
            "timestamp": timestamp,
            "source": source,
            "version": VERSION,
            'link': base_url + '/conversation/index.html?ver=' + VERSION,
            'github': 'https://github.com/shaonianzhentan/conversation'
        })