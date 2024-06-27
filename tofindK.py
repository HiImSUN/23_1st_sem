import numpy as np
import matplotlib.pyplot as plt
vmax=0.1
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
    r_list = []
    for i in range(len(val_x_list)):
        r = np.sqrt(val_x_list[i]+val_y_list[i]+val_z_list[i])
        r_list.append(r)
    a = 1
    b = 1
    EM_list = [a*np.exp(-b * r**2) for r in r_list]
    return np.sum(EM_list)
    
def cal_r(x, y, z=0):
    val_x_list = np.array([(px - x)**2 for px in powerline_x])
    val_y_list = np.array([(py - y)**2 for py in powerline_y])
    val_z_list = np.array([(pz - z)**2 for pz in powerline_z])
    r_list = []
    for i in range(len(val_x_list)):
        r = np.sqrt(val_x_list[i]+val_y_list[i]+val_z_list[i])
        r_list.append(r)
    return r_list


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
        ax.plot([x-13, x]+[x-13, x]+[x+13, x]+[x+13, x], [y-13, y]+[y+13, y]+[y-13, y]+[y+13, y], [0, z]*4, linewidth=5,zorder=zorder_index,c='dimgrey')
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
            ax.scatter(np.linspace(self.previous_tower.x, self.x, 1000), np.linspace(self.previous_tower.y, self.y, 1000), z,zorder=10000, c='orange')
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
        self.x_range = np.linspace(self.x, self.x+self.width ,10)
        self.y_range = np.linspace(self.y, self.y+self.length,10)
        self.z_range = np.linspace(0, self.height,story*2)
        
        # print(self.surface)
        # scatter the corner of house
    def plot_house(self):
        X, Y = np.meshgrid(self.x_range, self.y_range,indexing='xy')
        for k in self.z_range:
            result = [[cal_EMWave(i,j,k) for i in self.x_range] for j in self.y_range]
            p = ax.scatter(X,Y,k,c = 'grey' ,vmin=0., vmax=vmax,cmap = 'jet',zorder = 1000)
        

# tower 선언
tower1 = Tower(0, 0)
tower2 = Tower(0, 500, previous_tower=tower1)
tower3 = Tower(0, 1000, previous_tower=tower2)

# house 선언




fig = plt.figure(figsize=(15, 10))
ax = plt.axes(projection='3d',computed_zorder=False)

for i in tower_list:
    ax.scatter(i.x, i.y, i.z,s=100, c='dimgrey')
    i.plot_tower()
for i in tower_list:
    i.plot_powerline()

for i in house_list:
    i.plot_house()
# 바닥 색칠하기
x_range = np.arange(0, 1200,20)
y_range = np.arange(0, 800,20)
X, Y = np.meshgrid(x_range, y_range)
c_range=np.array([[cal_EMWave(i,j,0) for i in x_range] for j in y_range])
print("max:", np.max(c_range))
print("min:", np.min(c_range))
###
x_list = np.arange(0,1000,100)
r_list = [cal_r(i,500) for i in x_list]
em_list = [cal_EMWave(i,500) for i in x_list]
#print('r_list', r_list) ###
print(em_list)




p = ax.plot_surface(X, Y, c_range,cmap = 'jet',linewidth=0, antialiased=False,zorder = 0)
p = ax.scatter(X,Y,c=c_range,s=10,cmap='jet',vmin=0., vmax=vmax,alpha=1,zorder=0)
cbar=fig.colorbar(p)
ax.scatter(1000,1000,1000,s=1000,c='red')
ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.set_axis_off()



#plt.show()