import pandas as pd
import matplotlib.pyplot as plt
import os

# 한글 폰트 설정 (Windows 기준: Malgun Gothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 1. 데이터 불러오기
long_df = pd.read_csv("./data/processed/자치구기준_인구통합_long.csv")  # 파일 경로는 상황에 맞게 수정

# 2. 출력 디렉토리 생성
output_dir = "./EDA/lineplots"
os.makedirs(output_dir, exist_ok=True)

# 3. 자치구별, 시간대별 평균 생활인구밀도 계산
mean_by_time = long_df.groupby(['자치구명', '시간대'])['생활인구밀도'].mean().reset_index()

# ⏱4. 시간대 정렬 순서 지정
time_order = ['00-06시', '06-12시', '12-18시', '18-24시']
mean_by_time['시간대'] = pd.Categorical(mean_by_time['시간대'], categories=time_order, ordered=True)
mean_by_time = mean_by_time.sort_values(['자치구명', '시간대'])

# 5. 자치구 목록
districts = mean_by_time['자치구명'].unique()

# 6. 꺾은선 그래프 생성 및 저장
for district in districts:
    sub_df = mean_by_time[mean_by_time['자치구명'] == district]
    
    plt.figure(figsize=(8, 5))
    plt.plot(sub_df['시간대'], sub_df['생활인구밀도'], marker='o', linestyle='-', color='teal')
    plt.title(f"{district}", fontsize=14)
    plt.xlabel("시간대")
    plt.ylabel("생활인구밀도")
    plt.grid(True)
    plt.tight_layout()
    
    filename = f"{output_dir}/{district}_생활인구_시간대_변화.png"
    plt.savefig(filename, dpi=300)
    plt.close()
