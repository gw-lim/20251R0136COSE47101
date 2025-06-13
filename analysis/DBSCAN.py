import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows 환경)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 데이터 불러오기
df = pd.read_csv("./data/processed/(최종) feature 통합 데이터셋.csv")

# 2. 범죄밀도 제외한 수치형 feature만 추출
features = df.drop(columns=["자치구명", "범죄밀도"])

# 3. 정규화
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# 4. min_samples 후보
min_samples_list = [3, 4, 5, 6]

# 5. k-distance plot (min_samples마다 1개씩)
plt.figure(figsize=(14, 10))
for idx, k in enumerate(min_samples_list):
    neighbors = NearestNeighbors(n_neighbors=k)
    neighbors_fit = neighbors.fit(scaled_features)
    distances, _ = neighbors_fit.kneighbors(scaled_features)
    k_distances = np.sort(distances[:, k - 1])

    plt.subplot(2, 2, idx + 1)
    plt.plot(k_distances)
    plt.title(f"k-distance plot (min_samples={k})")
    plt.xlabel("Data Points sorted by distance")
    plt.ylabel(f"{k}th Nearest Neighbor Distance")
    plt.grid(True)

plt.tight_layout()
plt.show()

eps_fixed = 2.5

# 6. DBSCAN 수행 및 시각화
results = []
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, min_samples in enumerate(min_samples_list):
    dbscan = DBSCAN(eps=eps_fixed, min_samples=min_samples)
    labels = dbscan.fit_predict(scaled_features)

    temp_df = df[["자치구명"]].copy()
    temp_df["클러스터"] = labels
    temp_df["min_samples"] = min_samples
    temp_df["eps"] = eps_fixed
    results.append(temp_df)

    # 시각화
    ax = axes[idx]
    clusters = temp_df["클러스터"].value_counts().sort_index()
    clusters.plot(kind="bar", ax=ax)
    ax.set_title(f"min_samples={min_samples}, eps={eps_fixed}")
    ax.set_xlabel("클러스터")
    ax.set_ylabel("자치구 수")
    ax.grid(True)

plt.tight_layout()
plt.show()

# 7. 결과 병합 및 저장
final_results = pd.concat(results, ignore_index=True)
final_results.to_csv("./analysis/DBSCAN결과_eps2.5_min_samples_3to6.csv", index=False, encoding="utf-8-sig")
