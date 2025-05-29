import pandas as pd
import csv
from datetime import datetime

# 데이터 로드
df = pd.read_csv("./data/raw/환경데이터.csv", encoding='cp949', dtype={'자치구': str}, quoting=csv.QUOTE_ALL, usecols=range(58))

EN_KR_MAP = {
    'Jung-gu': '중구',
    'Yongsan-gu': '용산구',
    'Seongdong-gu': '성동구',
    'Gwangjin-gu': '광진구',
    'Dongdaemun-gu': '동대문구',
    'Jongno-gu': '종로구',
    'Jungnang-gu': '중랑구',
    'Seongbuk-gu': '성북구',
    'Dobong-gu': '도봉구',
    'Nowon-gu': '노원구',
    'Eunpyeong-gu': '은평구',
    'Seodaemun-gu': '서대문구',
    'Mapo-gu': '마포구',
    'Yangcheon-gu': '양천구',
    'Gangseo-gu': '강서구',
    'Guro-gu': '구로구',
    'Geumcheon-gu': '금천구',
    'Yeongdeungpo-gu': '영등포구',
    'Dongjak-gu': '동작구',
    'Gwanak-gu': '관악구',
    'Seocho-gu': '서초구',
    'Gangnam-gu': '강남구',
    'Songpa-gu': '송파구',
    'Gangdong-gu': '강동구',
    'Gangbuk-gu': '강북구',
}

df['자치구'] = df['자치구'].map(EN_KR_MAP)

# 측정시간을 datetime 형식으로 변환 (YYYY-MM-DD_HH:MM:SS 형식)
df['측정시간'] = pd.to_datetime(df['측정시간'], format='%Y-%m-%d_%H:%M:%S')
df['시간'] = df['측정시간'].dt.hour

# 시간대 구분 함수
def get_time_period(hour):
    if 0 <= hour < 6:
        return '00시-06시'
    elif 6 <= hour < 12:
        return '06시-12시'
    elif 12 <= hour < 18:
        return '12시-18시'
    else:
        return '18시-24시'

# 시간대 컬럼 추가
df['시간대'] = df['시간'].apply(get_time_period)

# 자치구와 시간대별 조도와 소음 평균 계산
result = df.groupby(['자치구', '시간대'], as_index=False).agg({
    '조도 평균(lux)': 'mean',
    '소음 평균(dB)': 'mean'
})

# 전체 시간대(00시~24시) 평균 계산
total_avg = df.groupby('자치구', as_index=False).agg({
    '조도 평균(lux)': 'mean',
    '소음 평균(dB)': 'mean'
})
total_avg['시간대'] = '00시-24시'

# 결과 합치기
result = pd.concat([result, total_avg], ignore_index=True)

# 시간대 순서 지정
time_order = ['00시-06시', '06시-12시', '12시-18시', '18시-24시', '00시-24시']
result['시간대'] = pd.Categorical(result['시간대'], categories=time_order, ordered=True)
result = result.sort_values(['자치구', '시간대'])

print("\n시간대별 계산된 결과:")
print(result)

# 결과 저장
output_path = "./data/processed/자치구_및_시간대별_환경데이터.csv"
result['자치구'] = result['자치구'].astype(str)
result.to_csv(output_path, index=False, encoding='cp949')

print("\n저장된 파일 내용:")
saved_df = pd.read_csv(output_path, encoding='cp949', dtype={'자치구': str})
print(saved_df)

