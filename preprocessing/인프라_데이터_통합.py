import pandas as pd
import csv

# 데이터 로드
df_crime = pd.read_csv("./data/processed/강력범죄율_기준.csv", encoding='utf-8', dtype={'자치구명': str})
df_cctv = pd.read_csv("./data/processed/CCTV.csv", encoding='utf-8', dtype={'자치구명': str})[['자치구명', 'CCTV_밀도']]
df_safety_agency = pd.read_csv("./data/processed/주요기관.csv", encoding='utf-8', dtype={'자치구명': str})[['자치구명', '주요기관_밀도']]
df_entertainment_venue = pd.read_csv("./data/processed/유흥주점.csv", encoding='utf-8', dtype={'자치구명': str})[['자치구명', '유흥주점_밀도']]

# 자치구명 기준으로 데이터 통합
df_all = df_crime.merge(df_cctv, on='자치구명', how='outer')
df_all = df_all.merge(df_safety_agency, on='자치구명', how='outer')
df_all = df_all.merge(df_entertainment_venue, on='자치구명', how='outer')

# 필요한 칼럼만 선택
df_all = df_all[['자치구명', '면적당강력범죄건수', 'CCTV_밀도', '주요기관_밀도', '유흥주점_밀도']]

# 결과 저장
output_path = "./data/processed/인프라_통합.csv"
df_all['자치구명'] = df_all['자치구명'].astype(str)
df_all.to_csv(output_path, index=False, encoding='utf-8')

print("\n저장된 파일 내용:")
saved_df = pd.read_csv(output_path, encoding='utf-8', dtype={'자치구명': str})
print(saved_df)

