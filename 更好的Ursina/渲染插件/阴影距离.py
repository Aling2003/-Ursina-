from ursina import camera, Entity

class 阴影距离控制器:
    def __init__(self, 阴影距离=50, 阴影投射距离=100):
        self.阴影距离 = 阴影距离
        self.阴影投射距离 = 阴影投射距离
        self.阴影投射体列表 = []
    
    def 添加阴影投射体(self, 实体):
        self.阴影投射体列表.append(实体)
        实体.cast_shadow = True
    
    def 更新(self, 相机位置):
        for 投射体 in self.阴影投射体列表:
            距离 = (投射体.position - 相机位置).length()
            if 距离 > self.阴影投射距离:
                投射体.cast_shadow = False
            elif 距离 > self.阴影距离:
                投射体.cast_shadow = True
                投射体.shadow_resolution = 'low'
            else:
                投射体.cast_shadow = True
                投射体.shadow_resolution = 'high'
    
    def 设置阴影距离(self, 距离):
        self.阴影距离 = 距离
    
    def 设置阴影投射距离(self, 距离):
        self.阴影投射距离 = 距离
