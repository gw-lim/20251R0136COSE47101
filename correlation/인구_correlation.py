import pandas as pd

# 병합된 데이터 불러오기
merged_path = './data/processed/자치구기준_범죄_인구통합_wide.csv'
merged = pd.read_csv(merged_path, encoding='utf-8-sig')

# 수치형 컬럼만 선택
numeric_df = merged.select_dtypes(include='number')

# 상관계수 분석
correlations = numeric_df.corr()['범죄밀도'].drop('범죄밀도').sort_values(ascending=False)

# 결과 출력
print("범죄밀도와의 전체 상관관계 분석 결과:\n")
for var, corr in correlations.items():
    print(f"{var:<25} : {corr:.3f}")

# 결과 저장용 데이터프레임으로 변환
correlation_df = correlations.reset_index()
correlation_df.columns = ['변수명', '상관계수']

# 파일로 저장
correlation_df.to_csv('./correlation/인구_범죄밀도_상관관계.csv', index=False, encoding='utf-8-sig')
