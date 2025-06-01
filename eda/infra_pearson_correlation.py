import pandas as pd

df_infra = pd.read_csv("./data/processed/인프라_통합.csv", encoding='utf-8', dtype={'자치구명': str})

# 피어슨 상관계수 계산
correlation = df_infra[["면적당강력범죄건수", "CCTV_밀도", "주요기관_밀도", "유흥주점_밀도"]].corr(method="pearson")
print(correlation["면적당강력범죄건수"])
