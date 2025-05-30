import pandas as pd

# 데이터 불러오기
df = pd.read_csv("LOCAL_PEOPLE_GU_2022.csv", encoding='cp949')

# 자치구 코드 → 자치구명 매핑
gu_code_to_name = {
    11110:'종로구',11140:'중구',11170:'용산구',11200:'성동구',11215:'광진구',
    11230:'동대문구',11260:'중랑구',11290:'성북구',11305:'강북구',11320:'도봉구',
    11350:'노원구',11380:'은평구',11410:'서대문구',11440:'마포구',11470:'양천구',
    11500:'강서구',11530:'구로구',11545:'금천구',11560:'영등포구',11590:'동작구',
    11620:'관악구',11650:'서초구',11680:'강남구',11710:'송파구',11740:'강동구'
}
df['자치구명'] = df['자치구코드'].map(gu_code_to_name)

# 시간대 6시간 단위로 변환
def classify_time_6hour(hour):
    if 0 <= hour < 6:
        return '00-06시'
    elif 6 <= hour < 12:
        return '06-12시'
    elif 12 <= hour < 18:
        return '12-18시'
    else:
        return '18-24시'

df['시간대'] = df['시간대구분'].apply(classify_time_6hour)

# 연령대별 컬럼 정의
youth_cols = [col for col in df.columns if '0세부터' in col or '10세부터' in col or '15세부터' in col]
working_cols = [col for col in df.columns if '20세부터' in col or '30세부터' in col or '40세부터' in col or '50세부터' in col]
elderly_cols = [col for col in df.columns if '60세부터' in col or '65세부터' in col or '70세이상' in col]

# 유소년, 생산가능, 고령, 총합 계산
df['유소년'] = df[youth_cols].sum(axis=1)
df['생산가능'] = df[working_cols].sum(axis=1)
df['고령'] = df[elderly_cols].sum(axis=1)
df['총'] = df[['유소년', '생산가능', '고령']].sum(axis=1)

# 자치구 면적
gu_area = {
    '종로구': 23.91, '중구': 9.96, '용산구': 21.87, '성동구': 16.82, '광진구': 17.06,
    '동대문구': 14.22, '중랑구': 18.5, '성북구': 24.58, '강북구': 23.6, '도봉구': 20.65,
    '노원구': 35.44, '은평구': 29.71, '서대문구': 17.63, '마포구': 23.85, '양천구': 17.41,
    '강서구': 41.45, '구로구': 20.12, '금천구': 13.02, '영등포구': 24.55, '동작구': 16.36,
    '관악구': 29.57, '서초구': 46.97, '강남구': 39.5, '송파구': 33.88, '강동구': 24.59
}

# 그룹별 평균 후 밀도 계산
grouped = df.groupby(['자치구명', '시간대'])[['유소년', '생산가능', '고령', '총']].mean().reset_index()
for col in ['유소년', '생산가능', '고령', '총']:
    grouped[col] = grouped[col] / grouped['자치구명'].map(gu_area)

# long format 변환
melted = grouped.melt(id_vars=['자치구명', '시간대'], var_name='분류', value_name='생활인구밀도')
melted['국적'] = '내국인'
melted = melted[['자치구명', '시간대', '국적', '분류', '생활인구밀도']]

# 저장
melted.to_csv("생활인구밀도_내국인.csv", index=False, encoding='utf-8-sig')
