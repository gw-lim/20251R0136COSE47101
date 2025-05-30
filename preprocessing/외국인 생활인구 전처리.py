import pandas as pd

# 데이터 불러오기
temp_df = pd.read_csv("TEMP_FOREIGNER_GU_2022.csv", encoding='cp949')
long_df = pd.read_csv("LONG_FOREIGNER_GU_2022.csv", encoding='cp949')

# 자치구 코드 → 자치구명 매핑
gu_code_to_name = {
    11110:'종로구',11140:'중구',11170:'용산구',11200:'성동구',11215:'광진구',
    11230:'동대문구',11260:'중랑구',11290:'성북구',11305:'강북구',11320:'도봉구',
    11350:'노원구',11380:'은평구',11410:'서대문구',11440:'마포구',11470:'양천구',
    11500:'강서구',11530:'구로구',11545:'금천구',11560:'영등포구',11590:'동작구',
    11620:'관악구',11650:'서초구',11680:'강남구',11710:'송파구',11740:'강동구'
}

# 자치구 면적 정보
gu_area = {
    '종로구': 23.91, '중구': 9.96, '용산구': 21.87, '성동구': 16.82, '광진구': 17.06,
    '동대문구': 14.22, '중랑구': 18.5, '성북구': 24.58, '강북구': 23.6, '도봉구': 20.65,
    '노원구': 35.44, '은평구': 29.71, '서대문구': 17.63, '마포구': 23.85, '양천구': 17.41,
    '강서구': 41.45, '구로구': 20.12, '금천구': 13.02, '영등포구': 24.55, '동작구': 16.36,
    '관악구': 29.57, '서초구': 46.97, '강남구': 39.5, '송파구': 33.88, '강동구': 24.59
}

# 시간대를 6시간 단위로 분류하는 함수
def classify_time_6hour(hour):
    if 0 <= hour < 6:
        return '00-06시'
    elif 6 <= hour < 12:
        return '06-12시'
    elif 12 <= hour < 18:
        return '12-18시'
    else:
        return '18-24시'

# 외국인 데이터 처리 함수
def process_foreigner_data(df, 분류명):
    df['자치구명'] = df['자치구코드'].map(gu_code_to_name)
    df['시간대'] = df['시간대구분'].apply(classify_time_6hour)
    grouped = df.groupby(['자치구명', '시간대'])['총생활인구수'].mean().reset_index()
    grouped['생활인구밀도'] = grouped['총생활인구수'] / grouped['자치구명'].map(gu_area)
    grouped['국적'] = '외국인'
    grouped['분류'] = 분류명
    return grouped[['자치구명', '시간대', '국적', '분류', '생활인구밀도']]

# 각각 처리
temp_processed = process_foreigner_data(temp_df, 'TEMP')
long_processed = process_foreigner_data(long_df, 'LONG')

# 통합
final_df = pd.concat([temp_processed, long_processed], ignore_index=True)

# 저장
final_df.to_csv("생활인구밀도_외국인.csv", index=False, encoding='utf-8-sig')
