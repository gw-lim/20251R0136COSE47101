import pandas as pd

# 1. 데이터 불러오기
df = pd.read_csv("LOCAL_PEOPLE_GU_2022.csv", encoding='cp949')

# 2. 자치구 면적 정보 (단위: km²)
gu_area_km2 = {
    '종로구': 23.91, '중구': 9.96, '용산구': 21.87, '성동구': 16.82, '광진구': 17.06,
    '동대문구': 14.22, '중랑구': 18.5, '성북구': 24.58, '강북구': 23.6, '도봉구': 20.65,
    '노원구': 35.44, '은평구': 29.71, '서대문구': 17.63, '마포구': 23.85, '양천구': 17.41,
    '강서구': 41.45, '구로구': 20.12, '금천구': 13.02, '영등포구': 24.55, '동작구': 16.36,
    '관악구': 29.57, '서초구': 46.97, '강남구': 39.5, '송파구': 33.88, '강동구': 24.59
}

# 3. 연령대별 인구 합산
youth_cols = [...]
working_cols = [...]
elderly_cols = [...]

df['유소년_생활인구수'] = df[youth_cols].sum(axis=1)
df['생산가능_생활인구수'] = df[working_cols].sum(axis=1)
df['고령_생활인구수'] = df[elderly_cols].sum(axis=1)
df['총생활인구수'] = df[['유소년_생활인구수', '생산가능_생활인구수', '고령_생활인구수']].sum(axis=1)

# 4. 시간대 대분류
def classify_time(hour):
    if 7 <= hour <= 18:
        return '주간'
    elif 19 <= hour <= 23:
        return '야간'
    else:
        return '심야'
df['시간대_대분류'] = df['시간대구분'].apply(classify_time)

# 5. 자치구명 매핑
gu_map = {...}
df['자치구명'] = df['자치구코드'].map(gu_map)

# 6. 자치구별 평균 생활인구 수 계산
grouped = df.groupby(['자치구명', '시간대_대분류'])[
    ['총생활인구수', '유소년_생활인구수', '생산가능_생활인구수', '고령_생활인구수']
].mean().reset_index()

# 7. 자치구 면적 매핑 후 밀도 계산
grouped['면적'] = grouped['자치구명'].map(gu_area_km2)
grouped['총생활인구밀도'] = (grouped['총생활인구수'] / grouped['면적']).round(2)
grouped['유소년_생활인구밀도'] = (grouped['유소년_생활인구수'] / grouped['면적']).round(2)
grouped['생산가능_생활인구밀도'] = (grouped['생산가능_생활인구수'] / grouped['면적']).round(2)
grouped['고령_생활인구밀도'] = (grouped['고령_생활인구수'] / grouped['면적']).round(2)

# 8. 최종 열 정리
result = grouped[['자치구명', '시간대_대분류',
                  '총생활인구밀도', '유소년_생활인구밀도',
                  '생산가능_생활인구밀도', '고령_생활인구밀도']]

# 9. 저장 (선택)
result.to_csv("생활인구밀도_내국인.csv", index=False, encoding='utf-8-sig')
