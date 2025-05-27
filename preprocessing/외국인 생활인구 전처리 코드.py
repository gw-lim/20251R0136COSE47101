import pandas as pd

# 1. 데이터 불러오기
temp_df = pd.read_csv("TEMP_FOREIGNER_GU_2022.csv", encoding='cp949')
long_df = pd.read_csv("LONG_FOREIGNER_GU_2022.csv", encoding='cp949')

# 2. 시간대 대분류 분류 함수 정의
def classify_time(hour):
    if 7 <= hour <= 18:
        return '주간'
    elif 19 <= hour <= 23:
        return '야간'
    else:
        return '심야'

# 3. 시간대 대분류 컬럼 추가
temp_df['시간대_대분류'] = temp_df['시간대구분'].apply(classify_time)
long_df['시간대_대분류'] = long_df['시간대구분'].apply(classify_time)

# 4. 자치구 면적 정보 (자치구코드 기준)
gu_area_km2 = {
    11110: 23.91, 11140: 9.96, 11170: 21.87, 11200: 16.82, 11215: 17.06,
    11230: 14.22, 11260: 18.5, 11290: 24.58, 11305: 23.6, 11320: 20.65,
    11350: 35.44, 11380: 29.71, 11410: 17.63, 11440: 23.85, 11470: 17.41,
    11500: 41.45, 11530: 20.12, 11545: 13.02, 11560: 24.55, 11590: 16.36,
    11620: 29.57, 11650: 46.97, 11680: 39.5, 11710: 33.88, 11740: 24.59
}

# 5. 자치구코드 → 자치구명 매핑
gu_map = {
    11110: '종로구', 11140: '중구', 11170: '용산구', 11200: '성동구', 11215: '광진구',
    11230: '동대문구', 11260: '중랑구', 11290: '성북구', 11305: '강북구', 11320: '도봉구',
    11350: '노원구', 11380: '은평구', 11410: '서대문구', 11440: '마포구', 11470: '양천구',
    11500: '강서구', 11530: '구로구', 11545: '금천구', 11560: '영등포구', 11590: '동작구',
    11620: '관악구', 11650: '서초구', 11680: '강남구', 11710: '송파구', 11740: '강동구'
}

# 6. TEMP 처리 (중국인 제외, 총생활인구수 사용)
temp_grouped = temp_df.groupby(['자치구코드', '시간대_대분류'])['총생활인구수'].mean().reset_index()
temp_grouped['자치구명'] = temp_grouped['자치구코드'].map(gu_map)
temp_grouped['면적'] = temp_grouped['자치구코드'].map(gu_area_km2)
temp_grouped['TEMP_생활인구밀도'] = (temp_grouped['총생활인구수'] / temp_grouped['면적']).round(2)

# 7. LONG 처리
long_grouped = long_df.groupby(['자치구코드', '시간대_대분류'])['총생활인구수'].mean().reset_index()
long_grouped['자치구명'] = long_grouped['자치구코드'].map(gu_map)
long_grouped['면적'] = long_grouped['자치구코드'].map(gu_area_km2)
long_grouped['LONG_생활인구밀도'] = (long_grouped['총생활인구수'] / long_grouped['면적']).round(2)

# 8. TEMP와 LONG 병합
df_foreign_density = pd.merge(
    temp_grouped[['자치구명', '시간대_대분류', 'TEMP_생활인구밀도']],
    long_grouped[['자치구명', '시간대_대분류', 'LONG_생활인구밀도']],
    on=['자치구명', '시간대_대분류'],
    how='outer'
)

# 9. 결과 저장 (선택)
df_foreign_density.to_csv("생활인구밀도_외국인.csv", index=False, encoding='utf-8-sig')
