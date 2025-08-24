import streamlit as st
import polars as pl
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from whoop_api import refresh

st.title("JOGO")

refresh()

if 'body_measurement' in st.session_state:
    inches = st.session_state.body_measurement['height_meter'] * 39.3701
    st.write(f"Height: {int(inches // 12)}'{int(inches % 12)}\"")
    st.write(f"Weight: {round(st.session_state.body_measurement['weight_kilogram']*2.20462, 2)} lbs")
    workouts_df = pl.DataFrame(st.session_state.workouts).unnest('score')
    workouts_df = pl.DataFrame(workouts_df).unnest('zone_durations')
    workouts_df = workouts_df.with_columns([
        pl.col('start').str.to_datetime().dt.convert_time_zone('America/Los_Angeles').alias('start'),
        pl.col('end').str.to_datetime().dt.convert_time_zone('America/Los_Angeles').alias('end')
    ])

    # Display workout data table
    with st.expander("Workout Data Table", expanded=False):
        st.dataframe(
            (workouts_df
            .select([
                'start',
                'end',
                'sport_name',
                'strain',
                'average_heart_rate',
                'max_heart_rate',
                'kilojoule',
                'zone_zero_milli',
                'zone_one_milli',
                'zone_two_milli',
                'zone_three_milli',
                'zone_four_milli',
                'zone_five_milli'
            ])
            .sort('start', descending=True)
            )
        )

    # Charts for workout data
    st.header("Workout Charts")

    # Convert to pandas for Streamlit charting with time as x-axis
    chart_df = workouts_df.sort('start').to_pandas()
    chart_df = chart_df.set_index('start')

    # Define consistent chart styling
    chart_template = "plotly_white"
    title_font_size = 16
    axis_font_size = 12
    primary_color = '#1f77b4'  # Blue for single series
    secondary_color = '#DC143C'  # Crimson for secondary series

    # Strain over time
    st.subheader("Strain Over Time")
    st.write("Shows the strain score (0-21) for each workout, indicating the cardiovascular load and intensity.")
    fig_strain = px.line(chart_df.reset_index(), x='start', y='strain', 
                        markers=True, title="Workout Strain Over Time",
                        template=chart_template)
    fig_strain.update_traces(line_color=primary_color, marker_color=primary_color)
    fig_strain.update_layout(
        title_font_size=title_font_size,
        xaxis_title_font_size=axis_font_size,
        yaxis_title_font_size=axis_font_size
    )
    st.plotly_chart(fig_strain, use_container_width=True)

    # Heart rate metrics over time
    st.subheader("Heart Rate Over Time")
    st.write("Displays both average and maximum heart rate during workouts to track cardiovascular performance.")
    fig_hr = go.Figure()
    fig_hr.add_trace(go.Scatter(x=chart_df.index, y=chart_df['average_heart_rate'], 
                                mode='lines+markers', name='Average HR',
                                line_color=primary_color, marker_color=primary_color))
    fig_hr.add_trace(go.Scatter(x=chart_df.index, y=chart_df['max_heart_rate'], 
                                mode='lines+markers', name='Max HR',
                                line_color=secondary_color, marker_color=secondary_color))
    fig_hr.update_layout(
        title="Heart Rate Over Time", 
        xaxis_title="Date", 
        yaxis_title="Heart Rate (BPM)",
        template=chart_template,
        title_font_size=title_font_size,
        xaxis_title_font_size=axis_font_size,
        yaxis_title_font_size=axis_font_size
    )
    st.plotly_chart(fig_hr, use_container_width=True)

    # Kilojoule (energy) over time
    st.subheader("Workout Calories Burned Over Time")
    st.write("Total calories burned per day from all workouts, combining multiple sessions if done on the same day.")

    # Group by day and sum calories
    chart_df_daily = chart_df.reset_index()
    chart_df_daily['date'] = pd.to_datetime(chart_df_daily['start']).dt.date
    daily_calories = chart_df_daily.groupby('date')['kilojoule'].sum().reset_index()

    fig_energy = px.bar(daily_calories, x='date', y='kilojoule', 
                        title="Calories Burned During Workouts (Daily Total)",
                        template=chart_template)
    fig_energy.update_traces(marker_color=primary_color)
    fig_energy.update_layout(
        title_font_size=title_font_size,
        xaxis_title="Date",
        yaxis_title="Kilojoules",
        xaxis_title_font_size=axis_font_size,
        yaxis_title_font_size=axis_font_size
    )
    st.plotly_chart(fig_energy, use_container_width=True)

    # Zone durations stacked bar chart
    st.subheader("Heart Rate Zone Durations by Workout")
    st.write("Time spent in each heart rate zone during workouts. Green zones indicate lower intensity, red zones indicate maximum effort.")
    zone_cols = [
        'zone_zero_milli',
        'zone_one_milli', 
        'zone_two_milli',
        'zone_three_milli',
        'zone_four_milli',
        'zone_five_milli'
    ]
    # Create Plotly stacked bar chart for better control over ordering
    fig_zones = go.Figure()
    zone_colors = ['#2E8B57', '#32CD32', '#FFD700', '#FFA500', '#FF4500', '#DC143C']  # Dark green to dark red with better contrast
    zone_names = ['Zone 0', 'Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5']

    # Reset index to get actual dates for x-axis
    chart_df_reset = chart_df.reset_index()

    for i, (col, color, name) in enumerate(zip(zone_cols, zone_colors, zone_names)):
        fig_zones.add_trace(go.Bar(
            x=list(range(len(chart_df_reset))),  # Use index numbers instead of dates
            y=chart_df_reset[col],
            name=name,
            marker_color=color,
            width=0.9  # Make bars even wider
        ))

    # Customize x-axis to show workout numbers instead of dates
    fig_zones.update_layout(
        title="Heart Rate Zone Durations by Workout",
        xaxis_title="Workout Number (Most Recent First)",
        yaxis_title="Duration (milliseconds)",
        barmode='stack',
        bargap=0.05,  # Very small gap between bars
        template=chart_template,
        title_font_size=title_font_size,
        xaxis_title_font_size=axis_font_size,
        yaxis_title_font_size=axis_font_size,
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1,
            tickvals=list(range(0, len(chart_df_reset), max(1, len(chart_df_reset)//10))),  # Show every 10th workout or fewer
            ticktext=[f"#{i+1}" for i in range(0, len(chart_df_reset), max(1, len(chart_df_reset)//10))]
        )
    )
    st.plotly_chart(fig_zones, use_container_width=True)

    # Sport distribution
    st.subheader("Workout Distribution by Sport")
    st.write("Shows the total number of workouts for each sport type to identify your most frequent activities.")
    sport_counts = workouts_df.group_by('sport_name').agg(pl.count('sport_name').alias('count')).to_pandas()
    fig_sports = px.bar(sport_counts, x='sport_name', y='count',
                        title="Workout Distribution by Sport",
                        template=chart_template)
    fig_sports.update_traces(marker_color=primary_color)
    fig_sports.update_layout(
        title_font_size=title_font_size,
        xaxis_title="Sport",
        yaxis_title="Number of Workouts",
        xaxis_title_font_size=axis_font_size,
        yaxis_title_font_size=axis_font_size
    )
    st.plotly_chart(fig_sports, use_container_width=True)

    # Workout intensity scatter plot (Strain vs Average HR)
    st.subheader("Workout Intensity: Strain vs Average Heart Rate")
    st.write("Correlation between strain score and average heart rate. Higher values indicate more intense workouts.")
    fig_intensity = px.scatter(chart_df.reset_index(), x='average_heart_rate', y='strain',
                                title="Workout Intensity: Strain vs Average Heart Rate",
                                template=chart_template)
    fig_intensity.update_traces(marker_color=primary_color, marker_size=8)
    fig_intensity.update_layout(
        title_font_size=title_font_size,
        xaxis_title="Average Heart Rate (BPM)",
        yaxis_title="Strain",
        xaxis_title_font_size=axis_font_size,
        yaxis_title_font_size=axis_font_size
    )
    st.plotly_chart(fig_intensity, use_container_width=True)

    # Workout activity calendar - days with and without workouts
    st.subheader("Daily Workout Activity")
    st.write("Visual calendar showing days with workouts (blue) versus days without workouts (gray) to track consistency.")

    # Get workout dates and convert to date objects
    chart_df_reset = chart_df.reset_index()
    workout_dates = set(pd.to_datetime(chart_df_reset['start']).dt.date)

    # Create a date range from first workout to last workout
    min_date = min(workout_dates)
    max_date = max(workout_dates)
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')

    # Create activity data
    activity_data = []
    for date in date_range:
        date_obj = date.date()
        has_workout = date_obj in workout_dates
        activity_data.append({
            'date': date_obj,
            'workout_activity': 1 if has_workout else 0,
            'status': 'Workout' if has_workout else 'No Workout'
        })

    activity_df = pd.DataFrame(activity_data)

    # Create binary activity chart
    fig_activity = px.bar(activity_df, x='date', y='workout_activity', 
                        color='status',
                        title="Daily Workout Activity",
                        template=chart_template,
                        color_discrete_map={'Workout': primary_color, 'No Workout': '#E8E8E8'})

    fig_activity.update_layout(
        title_font_size=title_font_size,
        xaxis_title="Date",
        yaxis_title="Activity",
        xaxis_title_font_size=axis_font_size,
        yaxis_title_font_size=axis_font_size,
        yaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['Rest', 'Workout']),
        showlegend=True
    )

    st.plotly_chart(fig_activity, use_container_width=True)


