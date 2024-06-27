import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# 송전탑 현수선 방정식
def catenary(x,a=0.00001):  # a값에 따라 현수선 모양이 바뀐다.
    return (np.exp(a*x)+np.exp(-a*x)) / 2*a

### 송전타워 class ###
class Tower:
    total_towers = 0            # 총 타워 개수
    global tower_list
    tower_list = []             # 총 타워 list
    def __init__(self, x, y, height=100, elevation=0, previous_tower=None): #송전타워 설치 위치 (x,y), 높이, 지형고도를 받아와서 초기화
        Tower.total_towers += 1     # 총 타워 개수 증가
        self.x = x                  # 송전타워 x
        self.y = y                  # 송전타워 y
        self.height = height        # 송전타워 높이
        self.elevation = elevation  # 해발 고도
        self.z = self.height + self.elevation # 송전타워 꼭대기 높이
        self.previous_tower = previous_tower  # 이전 탑과의 연결 정보를 유지
        tower_list.append(self)     # 타워 리스트에 현재 타워 추가

    def plot_tower(self):       # 송전타워 그리기
        x = self.x
        y = self.y
        z = self.z
        ax.plot([x-13, x], [y-13, y], [0, z], linewidth=5)  # 송전탑 다리들
        ax.plot([x-13, x], [y+13, y], [0, z], linewidth=5)  # 송전탑 다리들
        ax.plot([x+13, x], [y-13, y], [0, z], linewidth=5)  # 송전탑 다리들
        ax.plot([x+13, x], [y+13, y], [0, z], linewidth=5)  # 송전탑 다리들

    # 현수선 그리기
    def plot_powerline(self):
        if self.previous_tower is not None:
            x = np.linspace(-(self.previous_tower.x+self.x)/2, (self.previous_tower.x+self.x)/2, 1000)  # 현수선의 x값 계산 (1000등분)
            y = np.linspace(-(self.previous_tower.y+self.y)/2, (self.previous_tower.y+self.y)/2, 1000)  # 현수선의 y값 계산 (1000등분)
            """print(self.previous_tower.z)"""
            ax.scatter(np.linspace(self.previous_tower.x, self.x, 1000),                                # 이전 타워와 현재 타워를 잇는
                    np.linspace(self.previous_tower.y, self.y, 1000),                                   # 현수선을 그린다.
                    catenary(np.sqrt((x)**2 + (y)**2)) -                                                # (방정식)
                    catenary(np.sqrt((x)**2 + (y)**2))[0]+self.z)

### 집 class ###
class House:
    global house_list
    house_list = []         # 총 집 list
    def __init__(self, x, y, story=5):  # x, y, 층 수를 받아와 초기화
        house_list.append(self)         # 총 집 list
        self.x = x                      # 집 x
        self.y = y                      # 집 y
        self.story = story
        self.height = self.story * 3    # 집 높이 = (층 수) X (한 층 당 높이 (3m))

    def plot_house(self):   # 집 그리기 함수
        # scatter the corner of house   
        ax.scatter(self.x, self.y, 0, s=30)
        ax.scatter(self.x+14, self.y, 0, s=30)
        ax.scatter(self.x, self.y+14, 0, s=30)
        ax.scatter(self.x+14, self.y+14, 0, s=30) # 14는 집 가로 및 세로 길이 (m)
        
        ax.scatter(self.x, self.y, self.height, s=30) # 30은 찍는 점 크기
        ax.scatter(self.x+14, self.y, self.height, s=30)
        ax.scatter(self.x, self.y+14, self.height, s=30)
        ax.scatter(self.x+14, self.y+14, self.height, s=30)

        ax.plot([self.x, self.x], [self.y, self.y], [0, self.height], linewidth=5)      # 모서리를 이어준다.
        ax.plot([self.x+14, self.x+14], [self.y, self.y], [0, self.height], linewidth=5)
        ax.plot([self.x, self.x], [self.y+14, self.y+14], [0, self.height], linewidth=5)
        ax.plot([self.x+14, self.x+14], [self.y+14, self.y+14], [0, self.height], linewidth=5)
        


### tower 만들기 ###
# Tower() 안에 x, y, '이전 타워' 를 넣어주면 됩니다.
tower1 = Tower(0,0)
tower2 = Tower(60,400,previous_tower=tower1)
tower3 = Tower(0,800,previous_tower=tower2)

### house 만들기 ###
# House() 안에 x, y, '층 수'(선택)를 넣어주면 됩니다.
house1 = House(600, 200)
house2 = House(1000, 600)

# 밑은 자동으로 그림 그려주는 코드
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection='3d')
for i in tower_list:
    ax.scatter(i.x, i.y, i.z,s=100)
    i.plot_tower()

for i in house_list:
    i.plot_house()

for i in tower_list:
    i.plot_powerline()

plt.show()