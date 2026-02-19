from ursina import Entity, Mesh, Vec3, color, destroy

class 合批渲染器:
    def __init__(self):
        self.批次字典 = {}
        self.批次实体字典 = {}
    
    def 添加到批次(self, 实体, 批次键='default'):
        if 批次键 not in self.批次字典:
            self.批次字典[批次键] = []
        self.批次字典[批次键].append(实体)
    
    def 构建批次(self, 批次键='default'):
        if 批次键 not in self.批次字典 or not self.批次字典[批次键]:
            return None
        return self.批次实体字典.get(批次键, None)
    
    def 构建全部批次(self):
        for 批次键 in list(self.批次字典.keys()):
            self.构建批次(批次键)
    
    def 清空批次(self, 批次键='default'):
        if 批次键 in self.批次字典:
            for 实体 in self.批次字典[批次键]:
                实体.enabled = True
            self.批次字典[批次键] = []
        if 批次键 in self.批次实体字典:
            destroy(self.批次实体字典[批次键])
            del self.批次实体字典[批次键]
    
    def 清空全部批次(self):
        for 批次键 in list(self.批次字典.keys()):
            self.清空批次(批次键)
