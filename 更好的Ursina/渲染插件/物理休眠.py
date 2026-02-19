from ursina import Vec3

class 物理休眠系统:
    def __init__(self, 休眠速度=0.1, 休眠时间=2.0):
        self.休眠速度 = 休眠速度
        self.休眠时间 = 休眠时间
        self.对象列表 = []
    
    def 添加对象(self, 实体):
        self.对象列表.append({
            '实体': 实体,
            '速度向量': Vec3(0,0,0),
            '静止时间': 0,
            '是否休眠': False
        })
    
    def 更新(self, 时间增量):
        for 对象 in self.对象列表:
            if 对象['是否休眠']:
                continue
            速度 = getattr(对象['实体'], 'velocity', Vec3(0,0,0))
            速率 = 速度.length()
            if 速率 < self.休眠速度:
                对象['静止时间'] += 时间增量
                if 对象['静止时间'] >= self.休眠时间:
                    对象['是否休眠'] = True
                    if hasattr(对象['实体'], 'sleep'):
                        对象['实体'].sleep()
            else:
                对象['静止时间'] = 0
                对象['速度向量'] = 速度
    
    def 唤醒(self, 实体):
        for 对象 in self.对象列表:
            if 对象['实体'] == 实体:
                对象['是否休眠'] = False
                对象['静止时间'] = 0
                if hasattr(实体, 'wake_up'):
                    实体.wake_up()
                break
