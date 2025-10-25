from sklearn.cluster import KMeans
import pandas as pd

def perform_clustering(df, x_col, y_col):
    data = df.dropna(subset=[x_col, y_col]).copy()
    if len(data) < 2:
        data['Cluster'] = -1
        return data

    n_clusters = min(3, len(data))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    data['Cluster'] = kmeans.fit_predict(data[[x_col, y_col]])
    return data
