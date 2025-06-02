import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 1. 데이터 로딩
long_df = pd.read_csv("./data/processed/자치구기준_인구통합_long.csv")
gdf = gpd.read_file("./EDA/서울_자치구_경계_2017.geojson")

# 2. 출력 디렉토리 생성
output_dir = "./EDA/maps"
os.makedirs(output_dir, exist_ok=True)

# 3. 총 인구밀도 (long_df에 포함된 경우)
if '총_인구밀도' in long_df.columns:
    district_density = long_df[['자치구명', '총_인구밀도']].drop_duplicates()
    merged = gdf.merge(district_density, left_on='SIG_KOR_NM', right_on='자치구명')

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    merged.plot(column='총_인구밀도', ax=ax, legend=True, cmap='OrRd', edgecolor='black')
    ax.set_title("총 인구밀도 (자치구별)", fontsize=15)
    ax.axis('off')
    plt.savefig(f"{output_dir}/map_1_총인구밀도.png", dpi=300)
    plt.close()

# 4. 총 생활인구밀도
total_living = long_df[long_df['분류'] == '총']
mean_total_living = total_living.groupby('자치구명')['생활인구밀도'].mean().reset_index()
merged = gdf.merge(mean_total_living, left_on='SIG_KOR_NM', right_on='자치구명')

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
merged.plot(column='생활인구밀도', ax=ax, legend=True, cmap='OrRd', edgecolor='black')
ax.set_title("총 생활인구밀도 (자치구별)", fontsize=15)
ax.axis('off')
plt.savefig(f"{output_dir}/map_2_총생활인구밀도.png", dpi=300)
plt.close()

# 5. 분류별 생활인구밀도
mean_by_category = long_df.groupby(['자치구명', '분류'])['생활인구밀도'].mean().reset_index()
categories = mean_by_category['분류'].unique()

for category in categories:
    sub_df = mean_by_category[mean_by_category['분류'] == category]
    merged = gdf.merge(sub_df, left_on='SIG_KOR_NM', right_on='자치구명')

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    merged.plot(column='생활인구밀도', ax=ax, legend=True, cmap='OrRd', edgecolor='black')
    ax.set_title(f"{category} 생활인구밀도 (자치구별)", fontsize=15)
    ax.axis('off')
    plt.savefig(f"{output_dir}/map_3_{category}_생활인구밀도.png", dpi=300)
    plt.close()

# 6. 시간대별 생활인구밀도
mean_by_time = long_df.groupby(['자치구명', '시간대'])['생활인구밀도'].mean().reset_index()
time_slots = mean_by_time['시간대'].unique()

for time in time_slots:
    sub_df = mean_by_time[mean_by_time['시간대'] == time]
    merged = gdf.merge(sub_df, left_on='SIG_KOR_NM', right_on='자치구명')

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    merged.plot(column='생활인구밀도', ax=ax, legend=True, cmap='OrRd', edgecolor='black')
    ax.set_title(f"{time} 생활인구밀도 (자치구별)", fontsize=15)
    ax.axis('off')
    plt.savefig(f"{output_dir}/map_4_{time}_생활인구밀도.png", dpi=300)
    plt.close()
