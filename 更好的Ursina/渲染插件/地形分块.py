from ursina import Entity, Vec3, camera, Mesh, destroy

class 地形分块:
    def __init__(self, 位置, 大小=16):
        self.位置 = 位置
        self.大小 = 大小
        self.实体 = None
        self.是否加载 = False
        self.是否可见 = False
    
    def 加载(self, 模型, 纹理=None):
        self.实体 = Entity(
            position=self.位置,
            model=模型,
            texture=纹理
        )
        self.是否加载 = True
        self.是否可见 = True
    
    def 卸载(self):
        if self.实体:
            destroy(self.实体)
            self.实体 = None
        self.是否加载 = False
        self.是否可见 = False
    
    def 设置可见(self, 可见):
        if self.实体:
            self.实体.visible = 可见
        self.是否可见 = 可见

class 地形分块管理器:
    def __init__(self, 分块大小=16, 视野距离=5, 生成器=None):
        self.分块大小 = 分块大小
        self.视野距离 = 视野距离
        self.生成器 = 生成器
        self.分块字典 = {}
        self.当前分块位置 = Vec3(0,0,0)
    
    def 获取分块键(self, x, z):
        return f"{x},{z}"
    
    def 更新分块(self, 玩家位置):
        分块x = int(玩家位置.x // self.分块大小)
        分块z = int(玩家位置.z // self.分块大小)
        新位置 = Vec3(分块x, 0, 分块z)
        if 新位置 == self.当前分块位置:
            return
        self.当前分块位置 = 新位置
        self._加载可见分块(分块x, 分块z)
        self._卸载远分块(分块x, 分块z)
    
    def _加载可见分块(self, 中心x, 中心z):
        for x in range(中心x - self.视野距离, 中心x + self.视野距离 + 1):
            for z in range(中心z - self.视野距离, 中心z + self.视野距离 + 1):
                键 = self.获取分块键(x, z)
                if 键 not in self.分块字典:
                    分块位置 = Vec3(x * self.分块大小, 0, z * self.分块大小)
                    分块 = 地形分块(分块位置, self.分块大小)
                    if self.生成器:
                        模型 = self.生成器(x, z, self.分块大小)
                        分块.加载(模型)
                    self.分块字典[键] = 分块
                else:
                    self.分块字典[键].设置可见(True)
    
    def _卸载远分块(self, 中心x, 中心z):
        for 键 in list(self.分块字典.keys()):
            x, z = map(int, 键.split(','))
            距离 = max(abs(x - 中心x), abs(z - 中心z))
            if 距离 > self.视野距离:
                self.分块字典[键].卸载()
                del self.分块字典[键]
            elif 距离 > self.视野距离 - 1:
                self.分块字典[键].设置可见(False)
