import pandas as pd

# 파일 불러오기
long_df = pd.read_csv("./data/processed/자치구기준_인구통합_long.csv", encoding = 'utf-8')


### 기준별 기술통계분석

# 자치구별 총 생활인구밀도 평균
living_pop_by_district = long_df.groupby('자치구명')['생활인구밀도'].mean().sort_values(ascending=False)

# 시간대별 생활인구밀도 평균
living_pop_by_time = long_df.groupby('시간대')['생활인구밀도'].mean().sort_values(ascending=False)

# 국적별 생활인구밀도 평균
living_pop_by_nationality = long_df.groupby('국적')['생활인구밀도'].mean().sort_values(ascending=False)

# 분류별(유소년/생산가능/고령/외국인 등) 생활인구밀도 평균
living_pop_by_category = long_df.groupby('분류')['생활인구밀도'].mean().sort_values(ascending=False)

# 인구 구성별 인구밀도 평균
density_by_age_group = long_df[['유소년_인구밀도', '생산가능_인구밀도', '고령_인구밀도', '총_인구밀도']].mean()

# 각 분류별 생활인구밀도 편차 (표준편차)
living_pop_std_by_category = long_df.groupby('분류')['생활인구밀도'].std()

# 결과 출력 (선택적으로 DataFrame 형태로 보기)
print("▶ 자치구별 생활인구밀도 평균:\n", living_pop_by_district, "\n")
print("▶ 시간대별 생활인구밀도 평균:\n", living_pop_by_time, "\n")
print("▶ 국적별 생활인구밀도 평균:\n", living_pop_by_nationality, "\n")
print("▶ 분류별 생활인구밀도 평균:\n", living_pop_by_category, "\n")
print("▶ 인구 구성별 인구밀도 평균:\n", density_by_age_group, "\n")
print("▶ 분류별 생활인구밀도 표준편차:\n", living_pop_std_by_category, "\n")



#### 자치구별 기술통계분석

# 총 인구밀도 상위 출력
if '총_인구밀도' in long_df.columns:
    district_density = long_df[['자치구명', '총_인구밀도']].drop_duplicates()
    print("[총 인구밀도 상위 10 자치구]")
    print(district_density.sort_values(by='총_인구밀도', ascending=False).head(10), "\n")

# 총 생활인구밀도 상위 출력
print("[총 생활인구밀도 상위 10 자치구]")
total_living = long_df[long_df['분류'] == '총']
mean_total_living = total_living.groupby('자치구명')['생활인구밀도'].mean().reset_index()
print(mean_total_living.sort_values(by='생활인구밀도', ascending=False).head(10), "\n")

# 분류별 생활인구밀도 상위 출력
mean_by_category = long_df.groupby(['자치구명', '분류'])['생활인구밀도'].mean().reset_index()
categories = mean_by_category['분류'].unique()

for category in categories:
    print(f"[{category} 생활인구밀도 상위 10 자치구]")
    sub_df = mean_by_category[mean_by_category['분류'] == category]
    print(sub_df.sort_values(by='생활인구밀도', ascending=False).head(10), "\n")

# 시간대별 생활인구밀도 상위 출력
mean_by_time = long_df.groupby(['자치구명', '시간대'])['생활인구밀도'].mean().reset_index()
time_slots = mean_by_time['시간대'].unique()

for time in time_slots:
    print(f"[{time} 생활인구밀도 상위 10 자치구]")
    sub_df = mean_by_time[mean_by_time['시간대'] == time]
    print(sub_df.sort_values(by='생활인구밀도', ascending=False).head(10), "\n")