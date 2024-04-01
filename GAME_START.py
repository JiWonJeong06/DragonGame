#pip install pygame --pre (python: 3.11.0)
import pygame
import os
import random
import time
from datetime import datetime
# 1. 게임초기화-------------------------------------------------
pygame.init()
# 2. 게임 창 옵션----------------------------------------
size = [540, 960]
screen = pygame.display.set_mode(size)
#제목
title = '드래곤 잡기'
pygame.display.set_caption(title)



# 3. 게임 필요 설정------------------------------------------------
clock = pygame.time.Clock()

class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    def put_img(self, address):
        current_path = os.path.dirname(__file__)
        self.img = pygame.image.load(os.path.join(current_path,address)).convert_alpha()
        self.sx, self.sy = self.img.get_size()
    def change_size(self, sx,sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()
    def show(self):
        screen.blit(self.img, (self.x, self.y))
    
def crash(a,b):
    if (a.x-b.sx <= b.x) and (b.x <= a.x+a.sx):
        if (a.y-b.sy <= b.y) and (b.y <= a.y+a.sy):
            return True
        else:
            return False
    else: 
        return False
   



#object 1-
ob1 = obj()
ob1.put_img('object1.png')
ob1.change_size(80, 100)
ob1.x = round(size[0]/2)
ob1.y = size[1] -ob1.y -100
ob1.move = 3
left_go = False
right_go = False
shoot = False
up_go = False
down_go = False







# 4-0 대기 화면
current_path = os.path.dirname(__file__)
bg = pygame.image.load(os.path.join(current_path, 'background.png'))
run = True
while run == True:
    clock.tick(60) 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run =  False
    screen.blit(bg, (0, 0))
    font = pygame.font.Font("Maplestory Bold.ttf", 25)
    text = font.render('스페이스바를 누르세요 ', True,(0,0,0))
    screen.blit(text,(170, round(size[1]/2-50)))
    pygame.display.update()
    
# 4. 메인 이벤트----------------------------------------------------
run = True
# 배경화면
time_start = datetime.now()
bg =pygame.image.load(os.path.join(current_path, 'background.png'))
ob3_list = []
ob2_list = []
k = 0
kill = 0
loss = 0
GAME_OVER = True

while run:

    # 4-1 FPS설정----------------------------------------------------
    clock.tick(60)
    # 4-2 각종 입력감지-------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:#왼
                left_go = True
            elif event.key == pygame.K_RIGHT:#오
                right_go = True
            elif event.key == pygame.K_SPACE:#발사
                shoot = True
            elif event.key == pygame.K_UP:
                up_go = True
            elif event.key == pygame.K_DOWN:
                down_go = True
                k = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_SPACE:
                shoot = False   
            elif event.key == pygame.K_UP:
                up_go = False
            elif event.key == pygame.K_DOWN:
                down_go = False 
    # 4-3 입력,시간에 따른 변화-----------------------------------------
    time_now = datetime.now()
    delta_time = round((time_now - time_start).total_seconds())
    # 오른쪽, 왼쪽 움직이기
    if left_go == True:
        ob1.x -= ob1.move
        if ob1.x <= 0: #벽나가기 금지
            ob1.x = 0
    elif right_go == True: 
        ob1.x += ob1.move
        if ob1.x >= size[0] -ob1.sx: #벽나가기 금지
            ob1.x = size[0] -ob1.sx

    #--------- new 설정-------------------
    elif up_go == True:
        ob1.y -= ob1.move
        if ob1.y <= 0:
            ob1.y = 0
    elif down_go == True:
        ob1.y += ob1.move
        if ob1.y >= size[1] -ob1.sy:
            ob1.y = size[1] -ob1.sy


    # object 3 ------------------------------------------------
    if shoot == True and k % 20 == 0:
        ob3 = obj()
        ob3.put_img('object3.png')
        ob3.change_size(20, 20)
        ob3.x = round(ob1.x + ob1.sx/2 -ob3.sx/2)
        ob3.y = ob1.y - ob3.sy -10
        ob3.move = 5
        ob3_list.append(ob3)
    k += 1
    d_list = []
    for i in range(len(ob3_list)):
        sh = ob3_list[i]
        sh.y -= sh.move
        if sh.y <= -sh.sy:
            d_list.append(i)
    for d in d_list:
        del ob3_list[d]
    # object 2
    if random.random() > 0.98:
        ob2 = obj()
        ob2.put_img('object2.png')
        ob2_size = random.randint(40,70)
        ob2.change_size(ob2_size, ob2_size)
        ob2.x = random.randrange(0,size[0]-ob2.sx-round(ob1.sx/2))
        ob2.y = 10
        ob2.move = 1
        ob2_list.append(ob2)
    d_list = []
    for i in range(len(ob2_list)):
        o2 = ob2_list[i]
        o2.y += o2.move
        if o2.y >= size[1]:
            d_list.append(i)
    for d in d_list:
        del ob2_list[d]
        loss += 1

# 총알과 돌과 충돌 하는 부분
    dm_list = []
    da_list = []
    for i in range(len(ob3_list)):
        for j in range(len(ob2_list)):
            m = ob3_list[i]
            a = ob2_list[j]
            if crash(m,a) == True:
                dm_list.append(i)
                da_list.append(j)
    dm_list = list(set(dm_list))
    da_list = list(set(da_list))

    for dm in dm_list:
        del ob3_list[dm]
    for da in da_list:
        del ob2_list[da]    
        kill += 1
        dm_list = []
        da_list = []
    for i in range(len(ob2_list)):
        a = ob2_list[i]
        if crash(a, ob1) == True:
            run = False
            GAME_OVER = False


    # 4-4 그리기---------------------------------------------------------
    screen.blit(bg, (0, 0))

    ob1.show()
    for sh in ob3_list:
        sh.show()
    for o2 in ob2_list:
        o2.show()

    font = pygame.font.Font("Maplestory Bold.ttf",20)
    text = font.render(f'죽인 수:{kill} 킬 놓친 수:{loss} 회 ', True,(0,0,0))
    screen.blit(text,(10, 5))
    text2 = font.render(f'시간: {delta_time} 초', True,(0,0,0))
    screen.blit(text2,(440, 5))
    # 4-5 업데이트------------------------------------------------------------------
    pygame.display.update()
    
# 5. 게임 종료 --------------------------------------------------------
current_path = os.path.dirname(__file__)
bg = pygame.image.load(os.path.join(current_path, 'background.png'))
run = True

while GAME_OVER == False:
    clock.tick(60) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                GAME_OVER = True
    screen.blit(bg, (0, 0))
    font = pygame.font.Font("Maplestory Bold.ttf",40)
    text = font.render('게임 종료 ', True,(0,0,0))
    screen.blit(text,(170, round(size[1]/2-50)))
    pygame.display.update() 








pygame.quit()