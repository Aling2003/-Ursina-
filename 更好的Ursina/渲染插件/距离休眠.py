from ursina import Vec3, camera

class 距离休眠系统:
    def __init__(self, 休眠距离=50, 检查间隔=0.5):
        self.休眠距离 = 休眠距离
        self.检查间隔 = 检查间隔
        self.对象列表 = []
        self.距离上次检查时间 = 0
    
    def 添加对象(self, 实体, 休眠回调=None, 唤醒回调=None):
        self.对象列表.append({
            '实体': 实体,
            '休眠回调': 休眠回调,
            '唤醒回调': 唤醒回调,
            '是否休眠': False
        })
    
    def 更新(self, 时间增量):
        self.距离上次检查时间 += 时间增量
        if self.距离上次检查时间 < self.检查间隔:
            return
        self.距离上次检查时间 = 0
        for 对象 in self.对象列表:
            距离 = (对象['实体'].position - camera.position).length()
            if 距离 > self.休眠距离 and not 对象['是否休眠']:
                对象['实体'].enabled = False
                对象['是否休眠'] = True
                if 对象['休眠回调']:
                    对象['休眠回调'](对象['实体'])
            elif 距离 <= self.休眠距离 and 对象['是否休眠']:
                对象['实体'].enabled = True
                对象['是否休眠'] = False
                if 对象['唤醒回调']:
                    对象['唤醒回调'](对象['实体'])
