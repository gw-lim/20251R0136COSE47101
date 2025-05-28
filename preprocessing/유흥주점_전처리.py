import pandas as pd

# 데이터 로드
df = pd.read_csv("서울시_유흥주점영업_인허가_정보.csv")
area_df = pd.read_csv("자치구_면적.csv")

# '지번주소'가 결측이 아닌 행만 선택
df_filtered = df[df['지번주소'].notna()].copy()

# '인허가일자'가 2023년 1월 1일 이전인 경우만 선택
df_filtered['인허가일자'] = pd.to_datetime(df_filtered['인허가일자'], errors='coerce')
df_filtered = df_filtered[df_filtered['인허가일자'] < pd.to_datetime("2023-01-01")]

# '자치구명' 추출: 지번주소에서 두 번째 토큰
df_filtered['자치구명'] = df_filtered['지번주소'].apply(lambda x: x.split()[1] if len(x.split()) > 1 else None)

# 자치구명별 유흥주점 수 세기
gu_counts = df_filtered['자치구명'].value_counts().reset_index()
gu_counts.columns = ['자치구명', '유흥주점_수']

# 면적 데이터와 병합하여 밀도 계산
gu_counts = pd.merge(gu_counts, area_df, on='자치구명', how='left')
gu_counts['유흥주점_밀도'] = gu_counts['유흥주점_수'] / gu_counts['면적']

# 결과 저장
output_path = "유흥주점.csv"
gu_counts.to_csv(output_path, index=False, encoding='utf-8-sig')

