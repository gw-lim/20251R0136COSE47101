from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
import pandas as pd

df = pd.read_csv("./correlation/linear-regression/final_dataset.csv", encoding='cp949', dtype={'자치구명': str})


# 독립 변수와 종속 변수 정의
# VIF 반영 전
# X = df.drop(columns=['자치구명', '범죄밀도'])
# VIF 반영 후
X = df.drop(columns=['자치구명', '범죄밀도', '12-18시_생산가능_인구밀도', '행복지수_가정생활', '조도 평균(lux)'])
y = df['범죄밀도']

# 1. 다중공선성 제거 (VIF 계산)
def calculate_vif(X):
    vif_data = pd.DataFrame()
    vif_data['변수'] = X.columns
    vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return vif_data

initial_vif = calculate_vif(X)

# 2. 다변량 회귀분석 (다중선형회귀)
# statsmodels 사용: 회귀식 도출을 위해
X_const = sm.add_constant(X)  # 상수항 추가
model = sm.OLS(y, X_const).fit()

# 3. 평가
y_pred = model.predict(X_const)
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

print({
    "1. VIF (다중공선성 확인)": initial_vif,
    "2. 회귀분석 요약": model.summary().as_text(),
    "3. 평가 지표": {
        "MSE": mse,
        "R2": r2
    }
})
