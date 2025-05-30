import pandas as pd

# 파일 불러오기
df_population = pd.read_csv("자치구기준_인구밀도.csv", encoding='cp949')
df_living = pd.read_csv("자치구기준_생활인구밀도_long.csv")

# 병합 (자치구명을 기준으로)
merged = pd.merge(df_population, df_living, on="자치구명", how="left")

# 저장
merged.to_csv("자치구기준_인구통합_long.csv", index=False, encoding='utf-8-sig')


# long format 데이터 불러오기
df_long = pd.read_csv("자치구기준_인구통합_long.csv", encoding='utf-8')

# 1. wide format 변환
df_wide = df_long.pivot_table(
    index=["자치구명", "시간대"],
    columns=["국적", "분류"],
    values="생활인구밀도"
).reset_index()

# 2. 컬럼명 정리
df_wide.columns = ['자치구명', '시간대'] + [f"{i}_{j}" for i, j in df_wide.columns[2:]]

# 3. 내국인 인구밀도 평균값 계산 (시간대 무관하게 평균)
df_avg_density = (
    df_long[df_long["국적"] == "내국인"]
    .groupby(["자치구명", "분류"])["생활인구밀도"]
    .mean()
    .unstack()
    .reset_index()
    .rename(columns={
        "총": "총_인구밀도",
        "유소년": "유소년_인구밀도",
        "생산가능": "생산가능_인구밀도",
        "고령": "고령_인구밀도"
    })
)

# 4. 평균 인구밀도를 wide 포맷에 병합
df_final = pd.merge(df_wide, df_avg_density, on="자치구명", how="left")

# 5. 저장
df_final.to_csv("자치구기준_인구통합_wide.csv", index=False, encoding='utf-8-sig')

