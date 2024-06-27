import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
zorder_index=20
powerline_x = []
powerline_y = []
powerline_z = []
# 송전탑 현수선 방정식
def catenary(x,a=0.027):
    return (np.exp(a*x)+np.exp(-a*x)) / 2*a

# 거리 계산하기 (추후에 전자기파 계산식으로 변경할 것)
def cal_EMWave(x, y, z=0):
    val_x_list = np.array([(px - x)**2 for px in powerline_x])
    val_y_list = np.array([(py - y)**2 for py in powerline_y])
    val_z_list = np.array([(pz - z)**2 for pz in powerline_z])
    EM_list = 1/np.sqrt(val_x_list + val_y_list + val_z_list)**2
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
        if self.previous_tower is not None:
            print(self.previous_tower.x,self.x,self.previous_tower.y,self.y)

    def plot_tower(self):
        global zorder_index
        x = self.x
        y = self.y
        z = self.z
        ax.plot([x-13, x]+[x-13, x]+[x+13, x]+[x+13, x], [y-13, y]+[y+13, y]+[y-13, y]+[y+13, y], [0, z]*4, linewidth=5,zorder=zorder_index)
        zorder_index+=1

    # 현수선 그리기
    def plot_powerline(self):
        if self.previous_tower is not None:
            powerline_x.append(np.linspace(self.previous_tower.x, self.x, 1000))  # x 값 추가
            powerline_y.append(np.linspace(self.previous_tower.y, self.y, 1000))  # y 값 추가

            x = np.linspace(-(self.previous_tower.x-self.x)/2, (self.previous_tower.x-self.x)/2, 1000)
            y = np.linspace(-(self.previous_tower.y-self.y)/2, (self.previous_tower.y-self.y)/2, 1000)
            z = catenary(np.sqrt((x)**2 + (y)**2)) - catenary(np.sqrt((x)**2 + (y)**2))[0]+self.z
            powerline_z.append(z)                                                 # z 값 추가
            # 현수선 그리기
            ax.scatter(np.linspace(self.previous_tower.x, self.x, 1000), np.linspace(self.previous_tower.y, self.y, 1000), z)
# 집 class
class House:
    global house_list
    house_list = []
    def __init__(self, x, y, width=30,length=30 ,story=5):
        house_list.append(self)         # 총 건물 list
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.story = story              # 건물 층 수
        self.height = self.story * 3    # 건물 높이
        self.x_range = np.linspace(self.x, self.x+self.width ,20)
        self.y_range = np.linspace(self.y, self.y+self.length,20)
        self.z_range = np.linspace(0, self.height,20)
        print(self.x_range)
        print(self.y_range)
        print(self.z_range)
        
        # print(self.surface)
        # scatter the corner of house
    def plot_house(self):
        X, Y, Z = np.meshgrid(self.x_range, self.y_range,self.z_range)
        result = [[[cal_EMWave(i,j,k) for i in self.x_range] for j in self.y_range]for k in self.z_range]
        print(result)
        q = ax.scatter(X,Y,Z,c = result ,cmap = 'jet',zorder = 1000)

# tower 선언
tower1 = Tower(100,100)
tower2 = Tower(100,600,previous_tower=tower1)
tower3 = Tower(300,100,previous_tower=tower2)
tower4 = Tower(300,600,previous_tower=tower3)

# house 선언
house1 = House(260, 200)
house2 = House(100, 300,100,100,23)
house3 = House(700, 1500, 100, 200, 30)
# house2 = House(60, 600)
fig = plt.figure(figsize=(10, 10))
# ax = fig.add_subplot(projection='3d')
ax = plt.axes(projection='3d',computed_zorder=False)

for i in tower_list:
    ax.scatter(i.x, i.y, i.z,s=100)
    i.plot_tower()
for i in tower_list:
    i.plot_powerline()

for i in house_list:
    i.plot_house()
# 바닥 색칠하기
x_range = np.arange(0, 800,4)
y_range = np.arange(-100, 2000,20)
X, Y = np.meshgrid(x_range, y_range)
c_range=np.array([[cal_EMWave(i,j,0) for i in x_range] for j in y_range])
print(np.array(c_range).shape)

# p = ax.plot_surface(X, Y, c_range,cmap = 'jet',linewidth=0, antialiased=False,zorder = 0)
p = ax.scatter(X,Y,c=c_range,s=10,cmap='jet',alpha=1,zorder=0)
# ax.set_zorder = 1
cbar=fig.colorbar(p)



plt.show()
