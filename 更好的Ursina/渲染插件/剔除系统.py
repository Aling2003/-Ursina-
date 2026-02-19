from ursina import Vec3, camera, Entity

class 剔除系统:
    def __init__(self, 启用视锥剔除=True, 启用面剔除=True):
        self.启用视锥剔除 = 启用视锥剔除
        self.启用面剔除 = 启用面剔除
        self.对象列表 = []
    
    def 添加对象(self, 实体):
        self.对象列表.append({
            '实体': 实体,
            '原始启用状态': 实体.enabled
        })
        if self.启用面剔除:
            实体.double_sided = False
    
    def 更新(self):
        if not self.启用视锥剔除:
            return
        相机位置 = camera.position
        相机前向 = camera.forward
        for 对象 in self.对象列表:
            实体 = 对象['实体']
            到实体向量 = 实体.position - 相机位置
            距离 = 到实体向量.length()
            if 距离 == 0:
                continue
            归一化方向 = 到实体向量 / 距离
            点积 = 相机前向.dot(归一化方向)
            if 点积 < -0.2:
                实体.enabled = False
            else:
                实体.enabled = 对象['原始启用状态']
    
    def 设置视锥剔除(self, 启用):
        self.启用视锥剔除 = 启用
        if not 启用:
            for 对象 in self.对象列表:
                对象['实体'].enabled = 对象['原始启用状态']
    
    def 设置面剔除(self, 启用):
        self.启用面剔除 = 启用
        for 对象 in self.对象列表:
            对象['实体'].double_sided = not 启用
