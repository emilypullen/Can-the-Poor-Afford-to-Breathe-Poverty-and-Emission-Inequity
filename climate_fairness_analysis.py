#!/usr/bin/env python3
"""
climate_fairness_analysis.py

Standalone script to compute and visualize the Climate Fairness Index (CFI)
and cluster countries into actionable groups for policy insights.

Usage:
    1. Place your CSV files in the same directory or update the paths below.
    2. Install required packages:
         pip install pandas numpy scikit-learn plotly folium
    3. Run:
         python climate_fairness_analysis.py
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px
import folium
import os

# === CONFIGURATION ===
CO2_PATH = 'co2_emissions.csv'       # columns: country, year, co2_per_capita
POVERTY_PATH = 'poverty.csv'         # columns: country, year, extreme_poverty_share
REVENUE_PATH = 'revenue_gap.csv'     # columns: country, year, revenue_gap_pct
OUTPUT_DIR = 'output'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_and_merge(latest_year=None):
    """
    Load datasets, filter to a common year, merge on country, and drop missing values.
    If latest_year is None, use the maximum year present in all three datasets.
    Returns merged DataFrame and the year used.
    """
    co2 = pd.read_csv(CO2_PATH)
    poverty = pd.read_csv(POVERTY_PATH)
    revenue = pd.read_csv(REVENUE_PATH)

    # Determine the latest common year
    years = [co2['year'].unique(), poverty['year'].unique(), revenue['year'].unique()]
    max_common = min(co2['year'].max(), poverty['year'].max(), revenue['year'].max())
    year = latest_year or max_common

    # Filter to that year
    co2_y = co2[co2['year'] == year][['country', 'co2_per_capita']]
    pov_y = poverty[poverty['year'] == year][['country', 'extreme_poverty_share']]
    rev_y = revenue[revenue['year'] == year][['country', 'revenue_gap_pct']]

    # Merge DataFrames
    df = co2_y.merge(pov_y, on='country').merge(rev_y, on='country')
    df = df.dropna().reset_index(drop=True)
    return df, year


def normalize(df):
    """
    Add Min-Max scaled columns for index calculation and Z-score columns for clustering.
    """
    mm = MinMaxScaler()
    ss = StandardScaler()

    df[['co2_mm', 'poverty_mm', 'revenue_mm']] = mm.fit_transform(
        df[['co2_per_capita', 'extreme_poverty_share', 'revenue_gap_pct']]
    )
    df[['co2_z', 'poverty_z', 'revenue_z']] = ss.fit_transform(
        df[['co2_per_capita', 'extreme_poverty_share', 'revenue_gap_pct']]
    )
    return df


def compute_cfi(df):
    """
    Compute the Climate Fairness Index (CFI), rank countries, and assign deciles.
    """
    epsilon = 1e-6
    df['CFI'] = (df['poverty_mm'] * df['revenue_mm']) / (df['co2_mm'] + epsilon)
    df['CFI_rank'] = df['CFI'].rank(ascending=False)
    df['CFI_decile'] = pd.qcut(df['CFI'], 10, labels=False) + 1
    return df


def cluster_countries(df, n_clusters=4):
    """
    Apply K-means clustering on Z-score features and label clusters.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(df[['co2_z', 'poverty_z', 'revenue_z']])

    names = {
        0: 'Justice Priorities',
        1: 'High-Responsibility',
        2: 'Transitional',
        3: 'Outliers'
    }
    df['cluster_label'] = df['cluster'].map(names)
    return df


def create_visualizations(df, year):
    """
    Generate and save interactive charts:
      - HTML choropleth map of CFI
      - HTML bubble plot (emissions vs poverty)
      - Folium map saved as HTML
    """
    # Choropleth
    fig1 = px.choropleth(
        df,
        locations='country',
        locationmode='country names',
        color='CFI',
        hover_name='country',
        title=f'Climate Fairness Index ({year})',
        color_continuous_scale='RdYlBu_r'
    )
    fig1.write_html(os.path.join(OUTPUT_DIR, f'cfi_choropleth_{year}.html'))

    # Bubble plot
    fig2 = px.scatter(
        df,
        x='co2_per_capita',
        y='extreme_poverty_share',
        size='revenue_gap_pct',
        color='cluster_label',
        hover_name='country',
        title='Emissions vs. Poverty by Cluster'
    )
    fig2.write_html(os.path.join(OUTPUT_DIR, 'bubble_plot.html'))

    # Folium cluster map (requires lat/lon; add your own in df)
    m = folium.Map(location=[20, 0], zoom_start=2)
    for _, row in df.iterrows():
        # Replace with actual latitude/longitude columns if available
        lat, lon = row.get('latitude'), row.get('longitude')
        if pd.notnull(lat) and pd.notnull(lon):
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                fill=True,
                fill_color=px.colors.qualitative.Plotly[row['cluster'] % 10],
                fill_opacity=0.7,
                popup=f"{row['country']}: {row['cluster_label']}"
            ).add_to(m)
    m.save(os.path.join(OUTPUT_DIR, 'cluster_map.html'))


def main():
    df, year = load_and_merge()
    df = normalize(df)
    df = compute_cfi(df)
    df = cluster_countries(df)
    create_visualizations(df, year)
    print(f"Analysis complete. Outputs saved in '{OUTPUT_DIR}' folder.")


if __name__ == '__main__':
    main()
