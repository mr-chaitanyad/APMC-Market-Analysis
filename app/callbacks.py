import folium
import plotly.express as px
from dash.dependencies import Input, Output
from models.clustering import perform_clustering
from src.utils import load_data

# Load data once
district_geodata, merged_gdf, numeric_cols = load_data()

def register_callbacks(app):
    @app.callback(
        [Output('map-display', 'srcDoc'),
         Output('cluster-scatter-chart', 'figure')],
        [Input('commodity-selector', 'value'),
         Input('metric-x-selector', 'value'),
         Input('metric-y-selector', 'value')]
    )
    def update_map(selected_commodity, x_metric, y_metric):
        # Filter data
        filtered = merged_gdf[merged_gdf['Commodity'] == selected_commodity].copy()
        clustered = perform_clustering(filtered, x_metric, y_metric)

        # --- Folium Map with Tooltip ---
        m = folium.Map(location=[19.5, 76.5], zoom_start=7, tiles='OpenStreetMap')

        choropleth = folium.Choropleth(
            geo_data=district_geodata.to_json(),
            data=clustered,
            columns=['district', x_metric],
            key_on='feature.properties.district',
            fill_color='YlGnBu',
            line_weight=1,
            fill_opacity=0.8,
            legend_name=f'{x_metric.replace("_"," ").title()} of {selected_commodity}'
        ).add_to(m)

        # Create tooltip info for hover display
        tooltip_cols = ['district', 'APMC', 'min_price', 'max_price', 'modal_price', 'arrivals_in_qtl', 'Cluster']
        available_cols = [col for col in tooltip_cols if col in clustered.columns]

        # Join the tooltip info with GeoJSON layer
        for _, r in clustered.iterrows():
            district = r['district']
            info = '<br>'.join([f"<b>{col.replace('_',' ').title()}:</b> {r[col]}" for col in available_cols])
            folium.GeoJsonTooltip(
                fields=[],
                aliases=[],
                labels=False,
                sticky=True
            )
            folium.Marker(
                location=[r.geometry.centroid.y, r.geometry.centroid.x],
                popup=folium.Popup(f"<b>{district}</b><br>{info}", max_width=250)
            ).add_to(m)

        # --- Scatter Plot with Hover Info ---
        hover_data = {
            'district': True,
            'APMC': True,
            'min_price': True,
            'max_price': True,
            'modal_price': True,
            'arrivals_in_qtl': True,
            'Cluster': True
        }

        fig = px.scatter(
            clustered, 
            x=x_metric, 
            y=y_metric, 
            color=clustered['Cluster'].astype(str),
            hover_name='district',
            hover_data=hover_data,
            template='plotly_white',
            title=f'{x_metric.replace("_"," ").title()} vs {y_metric.replace("_"," ").title()} ({selected_commodity})'
        )

        fig.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')))
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=50, r=30, t=80, b=50),
            title_x=0.5
        )

        return m.get_root().render(), fig
