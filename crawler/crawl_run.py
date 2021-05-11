import sys
import urllib.request
import urllib.parse
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup

seconds=0 #모든 맵의 플레이 타임의 합
seconds_length=0
score=0 #모든 맵의 점수의 합
score_length=0
top=150
victors_sum=0 #모든 맵의 클리어 인원 수의 합
victors_list=[]
playtime_list=[]
score_list=[]

#[mapname, value, rank]
most_victors=['null',0,-1]
least_victors=['null',sys.maxsize,-1]
longest=['null',0,-1]
shortest=['null',sys.maxsize,-1]

for rank in range(1,top+1):
    print("Analyzing Rank "+str(rank)+'...') # 크롤링 진행 과정을 콘솔창에서 확인하기 위한 용도
    with urllib.request.urlopen('https://pointercrate.com/demonlist/'+str(rank)+'/') as response:
        html = response.read()
        soup = BeautifulSoup(html,'html.parser')

        #해당 맵의 이름 데이터 추출
        mapname = soup.select_one('div.underlined h1')

        #해당 맵의 유저 기록 데이터 추출
        records = soup.select('tbody tr td:nth-child(2)')
        victors=0
        for record in records:
            if record.text=='100%': # 100% = 클리어
                victors+=1
        victors_sum+=victors
        victors_list.append(victors)
        if(victors>most_victors[1]): #최댓값 갱신
            most_victors[0]=mapname.text
            most_victors[1]=victors
            most_victors[2]=rank
        if(victors<least_victors[1]): #최솟값 갱신
            least_victors[0]=mapname.text
            least_victors[1]=victors
            least_victors[2]=rank

        #해당 맵의 플레이 타임,클리어 점수 정보 추출
        infotexts = soup.select('#level-info span')
        for infotext in infotexts:
            splited_elements = str(infotext.text).split(':')
            if splited_elements[0].find('Level length')!=-1: #플레이 타임 정보 추출
                sec=int(splited_elements[1][1:-1])*60+int(splited_elements[2][:-1])
                seconds+=sec
                playtime_list.append(sec)
                if(sec>longest[1]): #최댓값 갱신
                    longest[0]=mapname.text
                    longest[1]=sec
                    longest[2]=rank
                if(sec<shortest[1]): #최솟값 갱신
                    shortest[0]=mapname.text
                    shortest[1]=sec
                    shortest[2]=rank
                seconds_length+=1
            elif splited_elements[0].find('100%')!=-1: #클리어 점수 정보 추출
                score+=float(splited_elements[1])
                score_list.append(float(splited_elements[1]))
                score_length+=1

#크롤링 결과 출력
print('\n<Top '+str(top)+' Maps Analyzer>')
print('\n[Longest Map] #'+ str(longest[2]) + ' '+ longest[0]+' - '+str(int(longest[1]/60))+'m '+str(longest[1]%60)+'s')
print('[Shortest Map] #'+str(shortest[2]) + ' '+ shortest[0]+' - '+str(int(shortest[1]/60))+'m '+str(shortest[1]%60)+'s')
print('[Average Playtime] '+str(int(int(seconds/seconds_length)/60))+'m '+str(int(seconds/seconds_length)%60)+'s')
print('[Most Victors] #'+ str(most_victors[2]) + ' '+ most_victors[0]+' - '+str(most_victors[1]) +' Victors')
print('[Least Victors] #'+ str(least_victors[2]) + ' '+ least_victors[0]+ ' - '+str(least_victors[1]) +' Victors')
print('[Average Victors] '+str(round(victors_sum/top,1))+' Victors')
print('[Total Score] '+str(round(score,2))+'\n')

#맵 난이도 순위와 클리어 인원 수의 관계를 그래프로 시각화
plt.figure(1)
plt.plot(np.arange(1,top+1),victors_list)
plt.xlabel('Rank')
plt.ylabel('Victors')

#맵 난이도 순위와 플레이 타임의 관계를 그래프로 시각화
plt.figure(2)
plt.plot(np.arange(1,len(playtime_list)+1), playtime_list,'r')
plt.xticks([],[]) # 눈금 표시 안하기
plt.xlabel('Rank')
plt.ylabel('Playtime')

#맵 난이도 순위와 점수의 관계를 그래프로 시각화
plt.figure(3)
plt.plot(np.arange(1,top+1),score_list,'g')
plt.xlabel('Rank')
plt.ylabel('Score')

plt.show()