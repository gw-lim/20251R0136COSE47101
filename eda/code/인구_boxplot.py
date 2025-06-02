import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
long_df = pd.read_csv("./data/processed/자치구기준_인구통합_long.csv")  # 인코딩 필요시

# 1. 자치구별 분류별 평균 생활인구밀도
avg_df = long_df.groupby(['분류', '자치구명'])['생활인구밀도'].mean().reset_index()

# 2. 분류별로 Min-Max 정규화
def minmax_group_norm(x):
    scaler = MinMaxScaler()
    x['정규화된_생활인구밀도'] = scaler.fit_transform(x[['생활인구밀도']])
    return x

avg_df = avg_df.groupby('분류').apply(minmax_group_norm).reset_index(drop=True)

# 3. 분류별 정규화된 생활인구밀도의 자치구 간 표준편차 계산
category_std_by_district = avg_df.groupby('분류')['정규화된_생활인구밀도'].std().sort_values(ascending=False).reset_index()
category_std_by_district.columns = ['분류', '자치구_간_표준편차(MinMax 기준)']

# 4. 시각화 ①: Barplot
plt.figure(figsize=(10, 5))
sns.barplot(x='분류', y='자치구_간_표준편차(MinMax 기준)', data=category_std_by_district, palette='coolwarm')
plt.title("분류별 자치구 간 생활인구밀도 표준편차 (Min-Max 정규화 기준)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. 시각화 ②: Boxplot (정규화된 값 기반)
plt.figure(figsize=(12, 6))
sns.boxplot(x='분류', y='생활인구밀도', data=avg_df)
plt.title("분류별 자치구 간 생활인구밀도 분포")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
