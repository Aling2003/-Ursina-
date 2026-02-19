from ursina import Vec3, mouse, application, Entity, Text, Button, camera, color, destroy
from ursina.prefabs.first_person_controller import FirstPersonController
import configparser

class 玩家控制器:
    def __init__(self, 移动速度=8, 跳跃高度=2, 配置文件路径=None):
        self.玩家 = None
        self.移动速度 = 移动速度
        self.跳跃高度 = 跳跃高度
        self.是否暂停 = False
        self.暂停界面元素 = []
        self.控制已激活 = False
        self.配置文件路径 = 配置文件路径
        self.提示文本 = None
        self.准星 = None
        
        if 配置文件路径:
            self.加载配置(配置文件路径)
    
    def 加载配置(self, 配置文件路径):
        config = configparser.ConfigParser()
        config.read(配置文件路径, encoding='utf-8')
        
        if config.has_section('物理设置'):
            物理设置 = config['物理设置']
            try:
                self.移动速度 = float(物理设置.get('移动速度', self.移动速度))
            except:
                pass
            try:
                self.跳跃高度 = float(物理设置.get('跳跃高度', self.跳跃高度))
            except:
                pass
    
    def 初始化(self):
        self.玩家 = FirstPersonController(
            y=2,
            speed=self.移动速度,
            jump_height=self.跳跃高度
        )
        self.玩家.disable()
        mouse.locked = False
    
    def 激活控制(self):
        self.控制已激活 = True
        self.玩家.enable()
        mouse.locked = True
        if self.提示文本:
            self.提示文本.visible = False
        if self.准星:
            self.准星.visible = True
    
    def 暂停控制(self):
        self.控制已激活 = False
        self.玩家.disable()
        mouse.locked = False
        self.是否暂停 = True
        self._显示暂停界面()
        if self.准星:
            self.准星.visible = False
    
    def 继续控制(self):
        self.是否暂停 = False
        self._隐藏暂停界面()
        self.激活控制()
    
    def 切换暂停(self):
        if self.是否暂停:
            self.继续控制()
        else:
            self.暂停控制()
    
    def 处理输入(self, 键):
        if 键 == 'escape':
            if self.控制已激活 or self.是否暂停:
                self.切换暂停()
            return True
        
        if 键 == 'left mouse down':
            if not self.控制已激活 and not self.是否暂停:
                self.激活控制()
            return True
        
        return False
    
    def _显示暂停界面(self):
        背景 = Entity(
            parent=camera.ui,
            model='quad',
            scale=(3, 2),
            color=color.black66,
            z=1
        )
        
        标题 = Text(
            text='游戏暂停',
            position=(0, 0.2),
            origin=(0, 0),
            scale=2,
            parent=camera.ui
        )
        
        继续按钮 = Button(
            text='继续',
            position=(0, -0.1),
            scale=(0.2, 0.1),
            parent=camera.ui,
            on_click=self.继续控制
        )
        
        退出按钮 = Button(
            text='退出',
            position=(0, -0.25),
            scale=(0.2, 0.1),
            parent=camera.ui,
            on_click=application.quit
        )
        
        self.暂停界面元素 = [背景, 标题, 继续按钮, 退出按钮]
    
    def _隐藏暂停界面(self):
        for 元素 in self.暂停界面元素:
            destroy(元素)
        self.暂停界面元素 = []
    
    def 设置提示文本(self, 文本):
        self.提示文本 = 文本
    
    def 设置准星(self, 准星):
        self.准星 = 准星
    
    def 获取玩家位置(self):
        if self.玩家:
            return self.玩家.position
        return Vec3(0, 0, 0)
    
    def 设置玩家位置(self, 位置):
        if self.玩家:
            self.玩家.position = 位置
