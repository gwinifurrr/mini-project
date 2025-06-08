import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import collections
import plotly.graph_objects as go

st.image('netflixx.jpg')
st.markdown("""
    <h1 style="text-align: center; font-size: 35px;">Welcome to</h1>
""", unsafe_allow_html=True)



#HEADER
st.markdown("""
    <style>
        .gradient-header {
            background: linear-gradient(to right, #660000, #ff2400, #660000);
            color: black;
            padding: 10px;
            text-align: center;
            font-size: 25px;
            font-weight: bold;
            border-radius: 50px;
        }
    </style>
    <div class="gradient-header">Asyiqin & Umi's Dashboard</div>
""", unsafe_allow_html=True)



# READ DATA IMPORTED
df = pd.read_csv(r"C:\Users\umiad\OneDrive\Desktop\mini project data\netflix1.csv")



# VERTICAL GAP
st.write("")
st.write("")



# BORDERED METRICS
# Create columns
col1, col2, col3 = st.columns(3)

# Define custom HTML for bordered metrics
metric_style = """
    <div style="border: 2px solid red; padding: 10px; border-radius: 25px; text-align: center; width: 102%;">
        <h4 style="margin: 0;">{title}</h4>
        <p style="font-size: 20px; font-weight: thin; margin: 5px 0;">{value}</p>
    </div>
"""

# Display metrics inside columns
col1.markdown(metric_style.format(title="Total Movies", value="6, 081"), unsafe_allow_html=True)
col2.markdown(metric_style.format(title="Total TV Shows", value="2, 653"), unsafe_allow_html=True)
col3.markdown(metric_style.format(title="Average Rating", value="8.2 / 10"), unsafe_allow_html=True)

st.write("")

st.markdown("""
    <style>
        div[data-testid="metric-container"] {
            background-color: rgba(28, 131, 225, 0.1);
            border: 2px solid rgba(28, 131, 225, 0.5);
            padding: 10px;
            border-radius: 10px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)



# define shades of red
red_shades = ["#FF0000", "#E60000", "#CC0000", "#B30000", "#990000", "#800000", "#660000", "#4D0000", "#330000", "#5A0000"]



st.write("")
st.write("")



# PIE CHART
# Count occurrences for each type (Movie/TV Show)
type_counts = df["type"].value_counts().reset_index()
type_counts.columns = ["Type", "Count"]

# Count occurrences for each genre
genre_counts = df["listed_in"].str.split(",").explode().value_counts().reset_index()
genre_counts.columns = ["Genre", "Count"]

# Create Streamlit columns
col1, col2 = st.columns(2)



# (1) DOUGHNUT CHART
with col1:
    fig1 = go.Figure(data=[go.Pie(labels=type_counts["Type"], values=type_counts["Count"],
                                  hole=0.6, marker=dict(colors=["#FF0000", "#5A0000"]),
                                  pull=[0.05] * len(type_counts))])  # Adds gap between slices
    
    fig1.update_layout(legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
    st.markdown("""
    <style>
        .gradient-header {
            background: linear-gradient(to right, #660000, #ff2400, #660000);
            color: white;
            padding: 8px;
            text-align: center;
            font-size: 20px;
            font-weight: semi bold;
            border-radius: 50px;
        }
    </style>
    <div class="gradient-header">Content Type</div>
""", unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)

    
    
# (2) DOUGHNUT CHART
with col2:
    fig2 = go.Figure(data=[go.Pie(labels=genre_counts["Genre"].head(5), values=genre_counts["Count"].head(10),
                                  hole=0.6, marker=dict(colors=red_shades),
                                  pull=[0.03] * 10)])  # Adds gap between slices
    fig2.update_layout(legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
    st.markdown("""
    <style>
        .gradient-header {
            background: linear-gradient(to right, #660000, #ff2400, #660000);
            color: white;
            padding: 8px;
            text-align: center;
            font-size: 25px;
            font-weight: semi bold;
            border-radius: 50px;
        }
    </style>
    <div class="gradient-header">Top 5 Genre</div>
""", unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)


    
st.write("")
st.write("")



# BAR CHART
# Filter only movies
df_movies = df[df["type"] == "Movie"]

# Convert duration to numeric (removing " min" and handling missing values)
df_movies["duration"] = df_movies["duration"].str.replace(" min", "", regex=True).astype(float)

# Define duration intervals
bins = [0, 50, 60, 70, 80, 90]  # Define 5 intervals
labels = ["<50", "50 - 60", "60 - 70", "70 - 80", "80 - 90"]

# Categorize movies into intervals (NO automatic sorting)
df_movies["duration_group"] = pd.cut(df_movies["duration"], bins=bins, labels=labels, right=False)

# Count occurrences WITHOUT sorting or rearranging
duration_counts = df_movies.groupby("duration_group").size().reset_index(name="Count")

# Count occurrences for each content rating
rating_counts = df["rating"].value_counts().reset_index().head(5)
rating_counts.columns = ["Rating", "Count"]

# Create Streamlit columns
col1, col2 = st.columns(2)



# (1) BAR CHART
with col1:
    # Create vertical bar chart (Maintain Original Order)
    fig1 = px.bar(duration_counts, x="duration_group", y="Count",
             color="duration_group",
             color_discrete_sequence=["#990000", "#800000", "#660000", "#4D0000", "#330000"])  # Red theme
    
    fig1.update_layout(showlegend=False)
    fig1.update_layout(xaxis_title="( minutes )", yaxis_title="")

# Display in Streamlit
    st.write("")
    st.write("")
    st.markdown("""
    <style>
        .gradient-header {
            background: linear-gradient(to right, #660000, #ff2400, #660000);
            color: white;
            padding: 8px;
            text-align: center;
            font-size: 25px;
            font-weight: semi bold;
            border-radius: 50px;
        }
    </style>
    <div class="gradient-header">Movie Duration Distribution</div>
""", unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)

    
# Red color for 5 bar
custom_colors = ["#330000", "#4D0000", "#660000", "#800000", "#990000"]



# (2) BAR CHART
with col2:
    fig2 = go.Figure(data=[go.Bar(x=rating_counts["Rating"], y=rating_counts["Count"], marker=dict(color=custom_colors))])
    
    st.write("")
    st.write("")
    st.markdown("""
    <style>
        .gradient-header {
            background: linear-gradient(to right, #660000, #ff2400, #660000);
            color: white;
            padding: 8px;
            text-align: center;
            font-size: 25px;
            font-weight: semi bold;
            border-radius: 50px;
        }
    </style>
    <div class="gradient-header">Content Rating Distribution</div>
""", unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)



st.write("")
st.write("")



# (3) LINE CHART
# Convert 'date_added' to datetime
df['date_added'] = pd.to_datetime(df['date_added'])

# Filter data from 2015 onward
df = df[df['date_added'] >= "2015-01-01"]

# Group by month and count occurrences
monthly = df.groupby(df['date_added'].dt.to_period('M')).size().reset_index(name='count')

# Convert period to timestamp for plotting
monthly['date_added'] = monthly['date_added'].dt.to_timestamp()

fig = px.line(monthly, x="date_added", y="count",
              labels={"date_added": "Month", "count": "Title Count"},
              markers=True,
              color_discrete_sequence=["red"])
st.markdown("""
    <style>
        .gradient-header {
            background: linear-gradient(to right, #660000, #ff2400, #660000);
            color: white;
            padding: 8px;
            text-align: center;
            font-size: 25px;
            font-weight: semi bold;
            border-radius: 50px;
        }
    </style>
    <div class="gradient-header">Monthly Netflix Content Additions (From 2015)</div>
""", unsafe_allow_html=True)
st.plotly_chart(fig)



st.write("")
st.write("")



# HORIZONTAL BAR CHART
# Count occurrences for each country
country_counts = df["country"].value_counts().reset_index().head(5)
country_counts.columns = ["Country", "Count"]

# Split genres and count occurrences
genre_counts = collections.Counter(",".join(df["listed_in"].dropna()).split(","))
genre_df = pd.DataFrame(genre_counts.items(), columns=["Genre", "Count"])
genre_df = genre_df.sort_values(by="Count", ascending=True).tail(5)  # Select top 10 genres

# Create Streamlit columns
col1, col2 = st.columns(2)

# (1) HORIZONTAL BAR CHART
with col1:
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=country_counts["Count"], y=country_counts["Country"],
                          orientation="h", marker=dict(color=custom_colors),
                          text=country_counts["Count"], textposition="inside"))  # Labels inside bars
    fig1.update_layout(legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
    st.markdown("""
    <style>
        .gradient-header {
            background: linear-gradient(to right, #660000, #ff2400, #660000);
            color: white;
            padding: 8px;
            text-align: center;
            font-size: 25px;
            font-weight: semi bold;
            border-radius: 50px;
        }
    </style>
    <div class="gradient-header">Content by Top 5 Country</div>
""", unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)

    
    
# (2) HORIZONTAL BAR CHART
with col2:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=genre_df["Count"], y=genre_df["Genre"], orientation="h",
                          marker=dict(color=custom_colors),
                          text=genre_df["Count"], textposition="inside"))  # Labels inside bars
    fig2.update_layout(legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
    st.markdown("""
    <style>
        .gradient-header {
            background: linear-gradient(to right, #660000, #ff2400, #660000);
            color: white;
            padding: 8px;
            text-align: center;
            font-size: 25px;
            font-weight: semi bold;
            border-radius: 50px;
        }
    </style>
    <div class="gradient-header">Top 5 Netflix Genres</div>
""", unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)

    
    
st.write("")
st.write("")



# SHOW DATA
st.markdown("""
    <style>
        .gradient-header {
            background: linear-gradient(to right, #660000, #ff2400, #660000);
            color: white;
            padding: 8px;
            text-align: center;
            font-size: 25px;
            font-weight: semi bold;
            border-radius: 50px;
        }
    </style>
    <div class="gradient-header">Raw Data</div>
""", unsafe_allow_html=True)
st.write("")
st.write(df)


