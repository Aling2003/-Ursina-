from ursina import Entity, Mesh, Vec3, color, destroy

class 实例化渲染器:
    def __init__(self, 模型, 最大实例数=10000):
        self.模型 = 模型
        self.最大实例数 = 最大实例数
        self.实例列表 = []
        self.实例实体列表 = []
    
    def 添加实例(self, 位置, 旋转=Vec3(0,0,0), 缩放=Vec3(1,1,1), 颜色=color.white):
        if len(self.实例列表) >= self.最大实例数:
            return False
        实体 = Entity(
            model=self.模型,
            position=位置,
            rotation=旋转,
            scale=缩放,
            color=颜色
        )
        self.实例列表.append(实体)
        self.实例实体列表.append(实体)
        return True
    
    def 构建(self):
        pass
    
    def 清空(self):
        for 实体 in self.实例实体列表:
            destroy(实体)
        self.实例列表 = []
        self.实例实体列表 = []
