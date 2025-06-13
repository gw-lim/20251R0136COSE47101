import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import networkx as nx


# 한글 폰트 설정 (Windows 환경)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


### [1] 범죄율 상위 25% 자치구: Frequent Itemsets 저장

# 데이터 로딩
df = pd.read_csv('./data/processed/(최종) feature 통합 데이터셋.csv')

# 상위 25% 범죄율 자치구 필터링
top_25_threshold = df['범죄밀도'].quantile(0.75)
high_crime_df = df[df['범죄밀도'] >= top_25_threshold]

# 수치형 → 범주형
features = high_crime_df.drop(columns=['자치구명', '범죄밀도'])
binner = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile')
binned = binner.fit_transform(features)
binned_df = pd.DataFrame(binned, columns=features.columns).astype(int)

# 트랜잭션 구성
transactions = [
    [f"{col}_{['Low', 'Mid', 'High'][val]}" for col, val in row.items()]
    for _, row in binned_df.iterrows()
]

# One-hot 인코딩
te = TransactionEncoder()
te_data = te.fit_transform(transactions)
te_df = pd.DataFrame(te_data, columns=te.columns_)

# Frequent itemsets 저장
frequent_itemsets = apriori(te_df, min_support=0.3, use_colnames=True)
frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False)
frequent_itemsets.to_csv('./analysis/frequent_itemsets.csv', index=False, encoding='utf-8-sig')
print("frequent_itemsets.csv 저장 완료")

### [2] 전체 데이터: 범죄율 등급을 결과로 한 연관규칙 분석

# 범죄율 등급화
crime_bins = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile')
df['범죄밀도_등급'] = crime_bins.fit_transform(df[['범죄밀도']]).astype(int)
df['범죄밀도_등급'] = df['범죄밀도_등급'].map({0: '범죄밀도_Low', 1: '범죄밀도_Mid', 2: '범죄밀도_High'})

# 나머지 변수 범주화
full_features = df.drop(columns=['자치구명', '범죄밀도', '범죄밀도_등급'])
full_binned = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile').fit_transform(full_features)
full_binned_df = pd.DataFrame(full_binned, columns=full_features.columns).astype(int)

# 트랜잭션 구성 (범죄밀도 등급 포함)
transactions = []
for idx, row in full_binned_df.iterrows():
    items = [f"{col}_{['Low', 'Mid', 'High'][val]}" for col, val in row.items()]
    items.append(df.loc[idx, '범죄밀도_등급'])
    transactions.append(items)

# One-hot 인코딩
te2 = TransactionEncoder()
te_data2 = te2.fit_transform(transactions)
te_df2 = pd.DataFrame(te_data2, columns=te2.columns_)

# 연관규칙 추출
frequent_itemsets_full = apriori(te_df2, min_support=0.3, use_colnames=True)
rules = association_rules(frequent_itemsets_full, metric='confidence', min_threshold=0.6)

# 범죄 관련 후건만 필터링
rules = rules[rules['consequents'].apply(lambda x: any('범죄밀도' in item for item in x))]

# 예외 처리 포함
if rules.empty:
    print("[경고] 연관 규칙이 없습니다. min_support 또는 min_confidence를 낮춰보세요.")
else:
    rules = rules.sort_values(by='confidence', ascending=False)
    rules.to_csv('./analysis/crime_rules.csv', index=False, encoding='utf-8-sig')
    print("crime_rules.csv 저장 완료")

    ### [3] 시각화 (상위 10개 규칙)
    top_rules = rules.head(10)
    G = nx.DiGraph()
    for _, row in top_rules.iterrows():
        for antecedent in row['antecedents']:
            for consequent in row['consequents']:
                G.add_edge(antecedent, consequent, weight=row['confidence'])

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray', font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f"{v:.2f}" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("상위 10개 범죄율 연관규칙 그래프")
    plt.tight_layout()
    plt.show()
