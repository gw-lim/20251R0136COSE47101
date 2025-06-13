import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 데이터 불러오기
df = pd.read_csv("./data/processed/자치구기준_범죄_인구통합_wide.csv")

# 자치구명, 타겟 분리
gu_names = df['자치구명']
target = df['범죄밀도']
features = df.drop(columns=['자치구명', '범죄밀도'], errors='ignore')

# 수치형 feature만 필터링
numeric_features = features.select_dtypes(include='number')

# 상관계수 계산
correlations = numeric_features.corrwith(target).abs()

# 상관계수 기준 필터링 (|r| ≥ 0.5)
selected_columns = correlations[correlations >= 0.5].index.tolist()
selected_features = numeric_features[selected_columns]

# 스케일링
scaler = StandardScaler()
scaled_features = scaler.fit_transform(selected_features)

# PCA 수행 (90% 분산 유지)
pca = PCA(n_components=0.9)
pca_features = pca.fit_transform(scaled_features)

# 주성분 결과 → DataFrame
pca_df = pd.DataFrame(pca_features, columns=[f'PC{i+1}' for i in range(pca_features.shape[1])])
pca_df['자치구명'] = gu_names.values
pca_df['범죄밀도'] = target.values

# 결과 저장
pca_df.to_csv("./correlation/PCA_자치구별_상관기반_결과.csv", index=False, encoding='utf-8-sig')

# 주성분 loading matrix 저장
loadings = pd.DataFrame(
    pca.components_.T,
    index=selected_columns,
    columns=[f'PC{i+1}' for i in range(pca.n_components_)]
)
loadings.to_csv("./correlation/PCA_상관기반_성분별_선형결합계수.csv", encoding='utf-8-sig')
