import pandas as pd

# 두 파일 불러오기
df_korean = pd.read_csv("생활인구밀도_내국인.csv")
df_foreigner = pd.read_csv("생활인구밀도_외국인.csv")

# 컬럼 순서를 맞추기 위한 정렬
common_columns = ['자치구명', '시간대', '국적', '분류', '생활인구밀도']
df_korean = df_korean[common_columns]
df_foreigner = df_foreigner[common_columns]

# 병합
df_all = pd.concat([df_korean, df_foreigner], ignore_index=True)

# 저장
df_all.to_csv("자치구기준_생활인구밀도_long.csv", index=False, encoding='utf-8-sig')
