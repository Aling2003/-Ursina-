from ursina import Entity, Vec3, destroy

class 对象池:
    def __init__(self, 预制体, 初始大小=100, 最大大小=1000):
        self.预制体 = 预制体
        self.初始大小 = 初始大小
        self.最大大小 = 最大大小
        self.池 = []
        self.活跃对象 = []
        self._初始化池()
    
    def _初始化池(self):
        for _ in range(self.初始大小):
            对象 = self._创建对象()
            对象.enabled = False
            self.池.append(对象)
    
    def _创建对象(self):
        if isinstance(self.预制体, Entity):
            对象 = Entity(parent=self.预制体.parent, model=self.预制体.model, texture=self.预制体.texture, color=self.预制体.color)
            对象.scale = self.预制体.scale
            对象.enabled = False
            return 对象
        return Entity(enabled=False)
    
    def 获取(self, 位置=Vec3(0,0,0), 旋转=Vec3(0,0,0)):
        if self.池:
            对象 = self.池.pop()
        else:
            if len(self.活跃对象) >= self.最大大小:
                return None
            对象 = self._创建对象()
        对象.position = 位置
        对象.rotation = 旋转
        对象.enabled = True
        self.活跃对象.append(对象)
        return 对象
    
    def 归还到池(self, 对象):
        if 对象 in self.活跃对象:
            self.活跃对象.remove(对象)
            对象.enabled = False
            对象.position = Vec3(0,0,0)
            对象.rotation = Vec3(0,0,0)
            if len(self.池) < self.最大大小:
                self.池.append(对象)
            else:
                destroy(对象)
    
    def 归还全部(self):
        for 对象 in list(self.活跃对象):
            self.归还到池(对象)
