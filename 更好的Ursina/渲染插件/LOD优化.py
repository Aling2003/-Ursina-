from ursina import Entity, Vec3, camera

class LOD系统:
    def __init__(self, LOD距离=[10, 30, 60]):
        self.LOD距离 = LOD距离
        self.LOD对象列表 = []
    
    def 添加LOD对象(self, 实体, LOD模型列表):
        self.LOD对象列表.append({
            '实体': 实体,
            'LOD模型列表': LOD模型列表,
            '当前LOD': 0
        })
    
    def 更新(self):
        for LOD对象 in self.LOD对象列表:
            距离 = (LOD对象['实体'].position - camera.position).length()
            新LOD = 0
            for i, 距离阈值 in enumerate(self.LOD距离):
                if 距离 > 距离阈值:
                    新LOD = i + 1
            新LOD = min(新LOD, len(LOD对象['LOD模型列表']))
            if 新LOD != LOD对象['当前LOD']:
                LOD对象['当前LOD'] = 新LOD
                if 新LOD == 0:
                    LOD对象['实体'].visible = True
                    LOD对象['实体'].model = LOD对象['LOD模型列表'][0]
                elif 新LOD <= len(LOD对象['LOD模型列表']):
                    LOD对象['实体'].model = LOD对象['LOD模型列表'][新LOD - 1]
                else:
                    LOD对象['实体'].visible = False
