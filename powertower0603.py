import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

powerline_x = []
powerline_y = []
powerline_z = []
# 송전탑 현수선 방정식
def catenary(x,a=0.00001):
    return (np.exp(a*x)+np.exp(-a*x)) / 2*a

# 거리 계산하기 (추후에 전자기파 계산식으로 변경할 것)
def cal_EMWave(x, y, z=0):
    val_x_list = []; val_y_list = []; val_z_list = []; r_list = []; EM_list = []
    for px in powerline_x:
        val_x_list.append((px - x)**2)
    for py in powerline_y:
        val_y_list.append((py - y)**2)
    for pz in powerline_z:
        val_z_list.append((pz - z)**2)
    for i in range(len(val_x_list)):
        r = np.sqrt(val_x_list[i] + val_y_list[i] + val_z_list[i])
        r_list.append(r)
        EM_list.append(1/r**2)
    # print(type(np.sum(EM_list)),np.sum(EM_list))
    return np.sum(EM_list)
    


# 송전타워 class
class Tower:
    total_towers = 0
    global tower_list
    tower_list = []             # 총 타워 list
    def __init__(self, x, y, height=100, elevation=0, previous_tower=None): #송전타워 설치 위치 (x,y), 높이, 지형고도
        Tower.total_towers += 1     # 총 타워 개수 증가
        self.x = x              # 송전타워 x
        self.y = y              # 송전타워 y
        self.height = height        # 송전타워 높이
        self.elevation = elevation  # 해발 고도
        self.z = self.height + self.elevation # 송전타워 꼭대기 높이
        self.previous_tower = previous_tower  # 이전 탑과의 연결 정보를 유지
        tower_list.append(self)

    def plot_tower(self):
        x = self.x
        y = self.y
        z = self.z
        ax.plot([x-13, x], [y-13, y], [0, z], linewidth=5)
        ax.plot([x-13, x], [y+13, y], [0, z], linewidth=5)
        ax.plot([x+13, x], [y-13, y], [0, z], linewidth=5)
        ax.plot([x+13, x], [y+13, y], [0, z], linewidth=5)

    # 현수선 그리기
    def plot_powerline(self):
        if self.previous_tower is not None:
            powerline_x.append(np.linspace(self.previous_tower.x, self.x, 1000))  # x 값 추가
            powerline_y.append(np.linspace(self.previous_tower.y, self.y, 1000))  # y 값 추가

            x = np.linspace(-(self.previous_tower.x+self.x)/2, (self.previous_tower.x+self.x)/2, 1000)
            y = np.linspace(-(self.previous_tower.y+self.y)/2, (self.previous_tower.y+self.y)/2, 1000)
            z = catenary(np.sqrt((x)**2 + (y)**2)) - catenary(np.sqrt((x)**2 + (y)**2))[0]+self.z
            powerline_z.append(z)                                                 # z 값 추가
            # 현수선 그리기
            ax.scatter(np.linspace(self.previous_tower.x, self.x, 1000), np.linspace(self.previous_tower.y, self.y, 1000), z)

# 집 class
class House:
    global house_list
    house_list = []
    def __init__(self, x, y, story=5):
        house_list.append(self)         # 총 건물 list
        self.x = x
        self.y = y
        self.story = story              # 건물 층 수
        self.height = self.story * 3    # 건물 높이

        # scatter the corner of house
    def plot_house(self):
        ax.scatter(self.x, self.y, 0, s=30)
        ax.scatter(self.x+14, self.y, 0, s=30)
        ax.scatter(self.x, self.y+14, 0, s=30)
        ax.scatter(self.x+14, self.y+14, 0, s=30)
        
        ax.scatter(self.x, self.y, self.height, s=30)
        ax.scatter(self.x+14, self.y, self.height, s=30)
        ax.scatter(self.x, self.y+14, self.height, s=30)
        ax.scatter(self.x+14, self.y+14, self.height, s=30)

        ax.plot([self.x, self.x], [self.y, self.y], [0, self.height], linewidth=5)
        ax.plot([self.x+14, self.x+14], [self.y, self.y], [0, self.height], linewidth=5)
        ax.plot([self.x, self.x], [self.y+14, self.y+14], [0, self.height], linewidth=5)
        ax.plot([self.x+14, self.x+14], [self.y+14, self.y+14], [0, self.height], linewidth=5)
        


# tower 선언
tower1 = Tower(0,0)
tower2 = Tower(60,400,previous_tower=tower1)
tower3 = Tower(0,800,previous_tower=tower2)

# house 선언
# house1 = House(600, 200)
# house2 = House(1000, 600)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection='3d')

# 바닥 색칠하기
x_range = np.arange(-100, 200,4)
y_range = np.arange(-100, 1000,20)
for i in x_range:
    for j in y_range:
        # a = cal_EMWave(i,j,0)
        print("\r",i,j,end="")
        # print(type(cal_EMWave(i,j,0)))
        ax.scatter(i,j,0, c=cal_EMWave(i,j,0)*12000,s=10)
        # ax.colorbar()
        # ax.scatter(i,j,0, c=0,s=10)

for i in tower_list:
    ax.scatter(i.x, i.y, i.z,s=100)
    i.plot_tower()

for i in house_list:
    i.plot_house()

for i in tower_list:
    i.plot_powerline()

plt.show()