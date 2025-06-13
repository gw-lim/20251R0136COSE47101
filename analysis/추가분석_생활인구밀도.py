import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 한글 폰트 설정 (Windows 환경)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 데이터 로딩
df = pd.read_csv("./data/processed/(최종) feature 통합 데이터셋.csv")

# 2. Type 그룹 정의 및 매핑
type_dict = {
    "TypeA": ["강남구", "금천구", "서초구", "성동구", "영등포구", "용산구", "종로구", "중구", "마포구", "서대문구"],
    "TypeB": ["강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "노원구", "도봉구", "동작구",
              "성북구", "양천구", "은평구", "중랑구"],
    "TypeC": ["동대문구"],
    "TypeD": ["송파구"]
}
type_map = {gu: t for t, gu_list in type_dict.items() for gu in gu_list}
df["유동인구유형"] = df["자치구명"].map(type_map)

# 3. 시각화
plt.figure(figsize=(10, 5))
sns.boxplot(data=df, x="유동인구유형", y="범죄밀도")
plt.title("유형별 범죄밀도 분포")
plt.grid(True)
plt.show()

# 4. 정규성 검정 (Shapiro-Wilk)
print("Shapiro-Wilk 정규성 검정:")
for t in df["유동인구유형"].unique():
    group_data = df[df["유동인구유형"] == t]["범죄밀도"]
    if len(group_data) >= 3:
        stat, p = shapiro(group_data)
        print(f"{t}: p-value={p:.4f} → {'정규분포 가정 충족' if p > 0.05 else '정규성 X'}")
    else:
        print(f"{t}: 샘플 수 부족 (n={len(group_data)}) → 정규성 검정 불가")

# 5. 등분산성 및 ANOVA 검정은 2개 이상 샘플 가진 그룹만 사용
valid_types = [t for t in df["유동인구유형"].unique() if df[df["유동인구유형"] == t].shape[0] > 1]
group_values = [df[df["유동인구유형"] == t]["범죄밀도"] for t in valid_types]

# 6. 등분산성 검정
if len(group_values) >= 2:
    stat, p = levene(*group_values)
    print(f"\nLevene 등분산성 검정: p-value={p:.4f} → {'등분산성 만족' if p > 0.05 else '등분산성 X'}")

# 7. ANOVA 검정
print("\n(ANOVA):")
df_anova = df[df["유동인구유형"].isin(valid_types)]
model = ols('범죄밀도 ~ C(유동인구유형)', data=df_anova).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

# 8. Tukey HSD 사후 분석
print("\nTukey HSD 사후 분석:")
if df_anova["유동인구유형"].nunique() >= 2:
    tukey = pairwise_tukeyhsd(endog=df_anova["범죄밀도"],
                              groups=df_anova["유동인구유형"],
                              alpha=0.05)
    print(tukey)
else:
    print("Tukey HSD 수행 불가: 유효한 그룹 수 부족")
