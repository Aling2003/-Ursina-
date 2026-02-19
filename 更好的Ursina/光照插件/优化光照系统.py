from ursina import Entity, DirectionalLight, AmbientLight, PointLight, SpotLight, Vec3, camera, time, color
import configparser

class 优化光照系统:
    def __init__(self, 配置文件路径=None):
        self.光源列表 = []
        self.主光源 = None
        self.环境光 = None
        self.阴影投射体列表 = []
        self.更新间隔 = 0.1
        self.距离上次更新 = 0
        self.最大光源距离 = 100
        self.最大阴影距离 = 50
        self.主光源强度 = 1.0
        self.环境光强度 = 0.5
        self.阴影分辨率 = 1024
        
        if 配置文件路径:
            self.加载配置(配置文件路径)
    
    def 加载配置(self, 配置文件路径):
        config = configparser.ConfigParser()
        config.read(配置文件路径, encoding='utf-8')
        
        if config.has_section('光照设置'):
            光照设置 = config['光照设置']
            try:
                self.主光源强度 = float(光照设置.get('主光源强度', self.主光源强度))
            except:
                pass
            try:
                self.环境光强度 = float(光照设置.get('环境光强度', self.环境光强度))
            except:
                pass
            try:
                self.最大光源距离 = float(光照设置.get('最大光源距离', self.最大光源距离))
            except:
                pass
            try:
                self.最大阴影距离 = float(光照设置.get('最大阴影距离', self.最大阴影距离))
            except:
                pass
            try:
                self.阴影分辨率 = int(光照设置.get('阴影分辨率', self.阴影分辨率))
            except:
                pass
    
    def 设置默认光照(self):
        self.环境光 = AmbientLight(color=color.rgba(80*self.环境光强度, 80*self.环境光强度, 80*self.环境光强度, 0.5*self.环境光强度))
        self.主光源 = DirectionalLight(
            y=50,
            rotation=(45, 45, 0),
            shadows=True,
            shadow_resolution=self.阴影分辨率,
            color=color.rgba(255*self.主光源强度, 250*self.主光源强度, 240*self.主光源强度, 1)
        )
        self.光源列表.append(self.主光源)
        self.光源列表.append(self.环境光)
    
    def 添加点光源(self, 位置, 颜色=color.white, 半径=20, 强度=1, 带阴影=False):
        光源 = PointLight(
            position=位置,
            color=颜色,
            radius=半径,
            intensity=强度
        )
        if 带阴影:
            光源.shadows = True
            光源.shadow_resolution = 512
        self.光源列表.append(光源)
        return 光源
    
    def 添加聚光灯(self, 位置, 旋转, 颜色=color.white, 半径=30, 角度=45, 带阴影=False):
        光源 = SpotLight(
            position=位置,
            rotation=旋转,
            color=颜色,
            radius=半径,
            angle=角度
        )
        if 带阴影:
            光源.shadows = True
            光源.shadow_resolution = 512
        self.光源列表.append(光源)
        return 光源
    
    def 添加阴影投射体(self, 实体):
        实体.cast_shadow = True
        self.阴影投射体列表.append(实体)
    
    def 更新(self):
        self.距离上次更新 += time.dt
        if self.距离上次更新 < self.更新间隔:
            return
        self.距离上次更新 = 0
        
        相机位置 = camera.position
        for 光源 in self.光源列表:
            if isinstance(光源, (PointLight, SpotLight)):
                距离 = (光源.position - 相机位置).length()
                if 距离 > self.最大光源距离:
                    光源.enabled = False
                else:
                    光源.enabled = True
                    光源.intensity = max(0, 1 - (距离 / self.最大光源距离))
        
        for 投射体 in self.阴影投射体列表:
            距离 = (投射体.position - 相机位置).length()
            if 距离 > self.最大阴影距离:
                投射体.cast_shadow = False
            else:
                投射体.cast_shadow = True
                if 距离 > self.最大阴影距离 * 0.5:
                    投射体.shadow_resolution = 256
                else:
                    投射体.shadow_resolution = self.阴影分辨率
    
    def 设置主光源旋转(self, 旋转):
        if self.主光源:
            self.主光源.rotation = 旋转
    
    def 设置主光源强度(self, 强度):
        self.主光源强度 = 强度
        if self.主光源:
            self.主光源.color = color.rgba(255*强度, 250*强度, 240*强度, 1)
    
    def 设置环境光强度(self, 强度):
        self.环境光强度 = 强度
        if self.环境光:
            self.环境光.color = color.rgba(80*强度, 80*强度, 80*强度, 0.5*强度)
    
    def 移除光源(self, 光源):
        if 光源 in self.光源列表:
            self.光源列表.remove(光源)
            destroy(光源)
    
    def 清空全部光源(self):
        for 光源 in self.光源列表:
            destroy(光源)
        self.光源列表 = []
        self.阴影投射体列表 = []
