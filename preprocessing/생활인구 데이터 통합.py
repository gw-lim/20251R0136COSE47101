import pandas as pd

# 1. 파일 불러오기
df_domestic = pd.read_csv("생활인구밀도_내국인.csv", encoding='cp949')
df_foreign = pd.read_csv("생활인구밀도_외국인.csv", encoding='cp949')

# 2. 내국인 데이터: wide → long 변환
df_domestic_long = df_domestic.melt(
    id_vars=['자치구명', '시간대_대분류'],
    var_name='분류',
    value_name='생활인구밀도'
)
df_domestic_long['국적'] = '내국인'

# 분류명 앞의 '생활인구밀도_' 제거
df_domestic_long['분류'] = df_domestic_long['분류'].str.replace('생활인구밀도_', '').str.replace('_', '')

# 3. 외국인 데이터: TEMP, LONG 구분 포함하여 long 변환
df_foreign_long = df_foreign.melt(
    id_vars=['자치구명', '시간대_대분류'],
    var_name='분류',
    value_name='생활인구밀도'
)

# TEMP/LONG 추출
df_foreign_long['국적'] = '외국인'
df_foreign_long['분류'] = df_foreign_long['분류'].str.extract(r'(TEMP|LONG)')

# 4. 컬럼 이름 정리
df_domestic_long.rename(columns={'시간대_대분류': '시간대'}, inplace=True)
df_foreign_long.rename(columns={'시간대_대분류': '시간대'}, inplace=True)

# 5. 두 데이터프레임 합치기
df_final = pd.concat([df_domestic_long, df_foreign_long], ignore_index=True)

# 6. 컬럼 순서 정리
df_final = df_final[['자치구명', '시간대', '국적', '분류', '생활인구밀도']]

# 7. 결과 저장 (선택)
df_final.to_csv("자치구기준_생활인구밀도_longformat.csv", index=False, encoding='utf-8-sig')
