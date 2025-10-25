import pandas as pd
import geopandas as gpd

def load_data():
    geo_path = 'data/maharashtra_districts.geojson'
    csv_path = 'data/data.csv'

    district_geodata = gpd.read_file(geo_path)
    district_geodata['district'] = district_geodata['district'].str.strip().str.title()

    df = pd.read_csv(csv_path)
    df['district_name'] = df['district_name'].str.strip().str.title()

    merged_gdf = district_geodata.merge(df, left_on='district', right_on='district_name', how='left')
    numeric_cols = ['min_price', 'max_price', 'modal_price', 'arrivals_in_qtl']
    return district_geodata, merged_gdf, numeric_cols
