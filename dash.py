import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import time
from datetime import datetime, timedelta
import base64

# Page config
st.set_page_config(
    page_title="🏇 Naadam 2025 Racing Dashboard",
    page_icon="🏇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2E86C1;
        margin-bottom: 1rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .race-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Data loading and generation functions
@st.cache_data
def generate_demo_data():
    """Generate demo data for testing when CSV files are not available"""
    
    # Generate horses data
    np.random.seed(42)
    aimags = ['Ulaanbaatar', 'Darkhan-Uul', 'Orkhon', 'Selenge', 'Tuv', 'Arkhangai']
    sums = ['Center', 'North', 'South', 'East', 'West']
    colors = ['Bay', 'Chestnut', 'Black', 'Gray', 'Brown', 'Palomino']
    
    horses_data = []
    for i in range(300):
        age_group = (i // 50) + 2  # Ages 2-7
        horses_data.append({
            'horse_id': f'M{str(i+1).zfill(3)}',
            'color': np.random.choice(colors),
            'age': age_group,
            'trainer': f'Trainer_{np.random.randint(1, 51)}',
            'trainer_id': f'T{str(np.random.randint(1, 51)).zfill(3)}',
            'aimag': np.random.choice(aimags),
            'sum': np.random.choice(sums),
            'rider_name': f'Rider_{i+1}',
            'rider_age': np.random.randint(8, 16),
            'aimgiin_airag': np.random.randint(0, 5),
            'ulsiin_airag': np.random.randint(0, 10),
            'aimgiin_turuu': np.random.randint(0, 3),
            'ulsiin_turuu': np.random.randint(0, 8),
            'racing_group': f'Age_{age_group}',
            'total_achievement': np.random.randint(0, 20)
        })
    
    horses_df = pd.DataFrame(horses_data)
    
    # Generate trainers data
    trainers_data = []
    for i in range(50):
        trainers_data.append({
            'trainer_id': f'T{str(i+1).zfill(3)}',
            'trainer_name': f'Trainer_{i+1}',
            'aimag': np.random.choice(aimags),
            'sum': np.random.choice(sums),
            'national_achievement': np.random.randint(0, 15),
            'provincial__achievement': np.random.randint(0, 25),
            'total_trained_horses': np.random.randint(1, 10),
            'phone_number': f'+976-{np.random.randint(80000000, 99999999)}'
        })
    
    trainers_df = pd.DataFrame(trainers_data)
    
    # Generate race record data (Daaga - age 2)
    daaga_horses = horses_df[horses_df['age'] == 2].head(50)
    record_data = []
    
    for i, horse in enumerate(daaga_horses.itertuples()):
        finish_time_minutes = np.random.randint(25, 35)
        finish_time_seconds = np.random.randint(0, 60)
        distance_km = 15.0
        
        record_data.append({
            'horse_id': horse.horse_id,
            'racing_group': 'Daaga',
            'final_position': i + 1,
            'finish_time_minutes': finish_time_minutes,
            'finish_time_seconds': finish_time_seconds,
            'average_speed_kmh': distance_km / ((finish_time_minutes + finish_time_seconds/60) / 60),
            'max_speed_kmh': np.random.uniform(35, 55),
            'stride_length_m': np.random.uniform(4.5, 6.5),
            'heart_rate_start': np.random.randint(60, 80),
            'heart_rate_end': np.random.randint(120, 180),
            'weight_kg': np.random.uniform(280, 350),
            'rider_weight_kg': np.random.uniform(25, 40),
            'race_name': 'Наадам 2025 - даага',
            'date': '2025-07-11',
            'distance_km': distance_km,
            'weather': np.random.choice(['Sunny', 'Cloudy', 'Windy']),
            'temperature_celsius': np.random.randint(20, 30),
            'wind_speed_kmh': np.random.randint(0, 20),
            'humidity_percent': np.random.randint(30, 70),
            'track_condition': np.random.choice(['Good', 'Soft', 'Hard']),
            'prize_money_tugrik': max(0, 10000000 - (i * 200000)),
            'injury': np.random.choice(['None', 'Minor', 'None', 'None', 'None']),
            'fatigue_level': np.random.choice(['Low', 'Medium', 'High']),
            'rider_experience_years': np.random.randint(1, 8)
        })
    
    record_df = pd.DataFrame(record_data)
    
    # Generate live data for top 5 horses
    top_5_horses = record_df.head(5)['horse_id'].tolist()
    live_data = []
    
    # Base coordinates for Mongolian steppe
    base_lat, base_lon = 47.9184, 106.9177
    
    for timestamp in range(0, 1800, 60):  # 30 minutes, every 60 seconds
        for i, horse_id in enumerate(top_5_horses):
            progress = timestamp / 1800  # Race progress (0 to 1)
            
            live_data.append({
                'id': len(live_data),
                'timestamp_seconds': timestamp,
                'horse_id': horse_id,
                'distance_covered_km': progress * 15 + np.random.uniform(-0.5, 0.5),
                'current_speed_kmh': 30 + np.random.uniform(-10, 15) + (5 * np.sin(progress * np.pi)),
                'heart_rate': 80 + int(progress * 60) + np.random.randint(-10, 10),
                'position': i + 1 + np.random.randint(-1, 2) if timestamp > 300 else i + 1,
                'gap_to_leader_seconds': i * 5 + np.random.randint(0, 10) if i > 0 else 0,
                'cumulative_time_seconds': timestamp + (i * 2),
                'latitude': base_lat + (progress * 0.1) + np.random.uniform(-0.01, 0.01),
                'longitude': base_lon + (progress * 0.15) + np.random.uniform(-0.01, 0.01),
                'elevation_m': 1350 + np.random.randint(-50, 100),
                'stride_frequency': 2.2 + np.random.uniform(-0.3, 0.3),
                'energy_level': max(20, 100 - int(progress * 60) + np.random.randint(-10, 10)),
                'rider_commands': np.random.choice(['Steady', 'Push', 'Hold', 'Sprint', 'Easy'])
            })
    
    live_df = pd.DataFrame(live_data)
    
    return horses_df, trainers_df, record_df, live_df

@st.cache_data
def load_data():
    """Load data from CSV files or generate demo data"""
    try:
        horses_df = pd.read_csv(r"C:\Users\enkhb\Downloads\gwg_project\mongolian_datasets\horse.csv")
        trainers_df = pd.read_csv(r"C:\Users\enkhb\Downloads\gwg_project\mongolian_datasets\trainer.csv")
        record_df = pd.read_csv(r"C:\Users\enkhb\Downloads\gwg_project\mongolian_datasets\record.csv")
        live_df = pd.read_csv(r"C:\Users\enkhb\Downloads\gwg_project\mongolian_datasets\live.csv")
        return horses_df, trainers_df, record_df, live_df
    except FileNotFoundError:
        st.info("📁 CSV files not found. Using demo data for presentation.")
        return generate_demo_data()

# Dashboard functions
def overview_dashboard(horses_df, trainers_df, record_df):
    """Overview Dashboard with key metrics and distributions"""
    
    st.markdown('<h2 class="sub-header">🏇 Racing Overview</h2>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Horses", len(horses_df), delta="Active")
    with col2:
        st.metric("Total Trainers", len(trainers_df), delta="Registered")
    with col3:
        st.metric("Races Completed", 1, delta="Naadam 2025")
    with col4:
        total_prize = record_df['prize_money_tugrik'].sum()
        st.metric("Total Prize Money", f"₮{total_prize:,.0f}", delta="Distributed")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Horses by age group
        age_dist = horses_df['age'].value_counts().sort_index()
        fig_age = px.bar(
            x=age_dist.index,
            y=age_dist.values,
            title="🐎 Horses by Age Group",
            labels={'x': 'Age (Years)', 'y': 'Number of Horses'},
            color=age_dist.values,
            color_continuous_scale='viridis'
        )
        fig_age.update_layout(showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        # Horses by Aimag
        aimag_dist = horses_df['aimag'].value_counts()
        fig_aimag = px.pie(
            values=aimag_dist.values,
            names=aimag_dist.index,
            title="🗺️ Horse Distribution by Aimag"
        )
        fig_aimag.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_aimag, use_container_width=True)
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Trainer achievements
        fig_trainers = px.scatter(
            trainers_df,
            x='provincial__achievement',
            y='national_achievement',
            size='total_trained_horses',
            color='aimag',
            title="🏆 Trainer Achievements",
            labels={'provincial__achievement': 'Provincial Achievements', 
                   'national_achievement': 'National Achievements'},
            hover_data=['trainer_name']
        )
        st.plotly_chart(fig_trainers, use_container_width=True)
    
    with col2:
        # Horse colors distribution
        color_dist = horses_df['color'].value_counts()
        fig_colors = px.bar(
            x=color_dist.values,
            y=color_dist.index,
            orientation='h',
            title="🎨 Horse Color Distribution",
            labels={'x': 'Number of Horses', 'y': 'Color'},
            color=color_dist.values,
            color_continuous_scale='rainbow'
        )
        st.plotly_chart(fig_colors, use_container_width=True)

def race_record_dashboard(record_df, horses_df):
    """Race Record Dashboard with detailed race analysis"""
    
    st.markdown('<h2 class="sub-header">🏁 Race Record Analysis - Наадам 2025 Даага</h2>', unsafe_allow_html=True)
    
    # Race summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Participants", len(record_df))
    with col2:
        avg_speed = record_df['average_speed_kmh'].mean()
        st.metric("Avg Speed", f"{avg_speed:.1f} km/h")
    with col3:
        max_speed = record_df['max_speed_kmh'].max()
        st.metric("Top Speed", f"{max_speed:.1f} km/h")
    with col4:
        race_distance = record_df['distance_km'].iloc[0]
        st.metric("Distance", f"{race_distance:.0f} km")
    
    # Position and speed analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Final positions with speed
        fig_pos = px.scatter(
            record_df,
            x='final_position',
            y='average_speed_kmh',
            size='max_speed_kmh',
            color='final_position',
            title="🏃 Position vs Speed Analysis",
            labels={'final_position': 'Final Position', 'average_speed_kmh': 'Average Speed (km/h)'},
            hover_data=['horse_id', 'finish_time_minutes', 'finish_time_seconds'],
            color_continuous_scale='RdYlBu_r'
        )
        st.plotly_chart(fig_pos, use_container_width=True)
    
    with col2:
        # Finish time distribution
        record_df['total_time'] = record_df['finish_time_minutes'] + record_df['finish_time_seconds']/60
        fig_time = px.histogram(
            record_df,
            x='total_time',
            nbins=20,
            title="⏱️ Finish Time Distribution",
            labels={'total_time': 'Finish Time (minutes)', 'count': 'Number of Horses'},
            color_discrete_sequence=['#FF6B35']
        )
        st.plotly_chart(fig_time, use_container_width=True)
    
    # Heart rate and rider analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Heart rate analysis
        fig_hr = go.Figure()
        fig_hr.add_trace(go.Scatter(
            x=record_df['final_position'],
            y=record_df['heart_rate_start'],
            mode='markers',
            name='Start HR',
            marker=dict(color='blue', size=8)
        ))
        fig_hr.add_trace(go.Scatter(
            x=record_df['final_position'],
            y=record_df['heart_rate_end'],
            mode='markers',
            name='End HR',
            marker=dict(color='red', size=8)
        ))
        fig_hr.update_layout(
            title="💓 Heart Rate by Position",
            xaxis_title="Final Position",
            yaxis_title="Heart Rate (BPM)"
        )
        st.plotly_chart(fig_hr, use_container_width=True)
    
    with col2:
        # Prize money distribution
        fig_prize = px.bar(
            record_df.head(10),
            x='final_position',
            y='prize_money_tugrik',
            title="💰 Prize Money (Top 10)",
            labels={'final_position': 'Position', 'prize_money_tugrik': 'Prize Money (₮)'},
            color='prize_money_tugrik',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_prize, use_container_width=True)
    
    # Detailed race results table
    st.markdown("### 📊 Detailed Race Results")
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    with col1:
        position_filter = st.selectbox("Filter by Position Range", 
                                     ["All", "Top 10", "Top 20", "Bottom 10"])
    with col2:
        speed_filter = st.slider("Minimum Average Speed (km/h)", 
                               float(record_df['average_speed_kmh'].min()),
                               float(record_df['average_speed_kmh'].max()),
                               float(record_df['average_speed_kmh'].min()))
    with col3:
        weather_filter = st.selectbox("Weather Condition", 
                                    ["All"] + list(record_df['weather'].unique()))
    
    # Apply filters
    filtered_df = record_df.copy()
    
    if position_filter == "Top 10":
        filtered_df = filtered_df[filtered_df['final_position'] <= 10]
    elif position_filter == "Top 20":
        filtered_df = filtered_df[filtered_df['final_position'] <= 20]
    elif position_filter == "Bottom 10":
        filtered_df = filtered_df[filtered_df['final_position'] > 40]
    
    filtered_df = filtered_df[filtered_df['average_speed_kmh'] >= speed_filter]
    
    if weather_filter != "All":
        filtered_df = filtered_df[filtered_df['weather'] == weather_filter]
    
    # Display results
    display_cols = ['final_position', 'horse_id', 'finish_time_minutes', 'finish_time_seconds', 
                   'average_speed_kmh', 'max_speed_kmh', 'prize_money_tugrik']
    
    st.dataframe(
        filtered_df[display_cols].style.format({
            'average_speed_kmh': '{:.2f}',
            'max_speed_kmh': '{:.2f}',
            'prize_money_tugrik': '₮{:,.0f}'
        }),
        use_container_width=True
    )

def live_race_simulation(live_df, record_df):
    """Live Race Simulation Dashboard with animations"""
    
    st.markdown('<h2 class="sub-header">📡 Live Race Simulation - Top 5 Horses</h2>', unsafe_allow_html=True)
    
    # Control panel
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Start Simulation", type="primary"):
            st.session_state.simulation_running = True
            st.session_state.current_timestamp = 0
    
    with col2:
        if st.button("⏸️ Pause"):
            st.session_state.simulation_running = False
    
    with col3:
        if st.button("🔄 Reset"):
            st.session_state.simulation_running = False
            st.session_state.current_timestamp = 0
    
    # Initialize session state
    if 'simulation_running' not in st.session_state:
        st.session_state.simulation_running = False
    if 'current_timestamp' not in st.session_state:
        st.session_state.current_timestamp = 0
    
    # Time selector
    max_time = live_df['timestamp_seconds'].max()
    current_time = st.slider(
        "Race Time (seconds)", 
        0, int(max_time), 
        int(st.session_state.current_timestamp),
        step=60
    )
    
    # Get current data
    current_data = live_df[live_df['timestamp_seconds'] == current_time]
    
    if len(current_data) > 0:
        # Race progress
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Position tracking
            fig_pos = px.bar(
                current_data.sort_values('position'),
                x='horse_id',
                y='distance_covered_km',
                color='position',
                title=f"🏁 Current Positions (Time: {current_time//60}:{current_time%60:02d})",
                labels={'distance_covered_km': 'Distance Covered (km)'},
                color_continuous_scale='RdYlBu'
            )
            fig_pos.update_layout(showlegend=False)
            st.plotly_chart(fig_pos, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Live Metrics")
            for _, horse in current_data.iterrows():
                with st.container():
                    st.markdown(f"**{horse['horse_id']}** (Pos: {horse['position']})")
                    st.metric(
                        "Speed", 
                        f"{horse['current_speed_kmh']:.1f} km/h",
                        delta=f"{horse['current_speed_kmh'] - 30:.1f}"
                    )
                    st.progress(horse['energy_level']/100)
                    st.markdown("---")
        
        # Speed and heart rate over time
        col1, col2 = st.columns(2)
        
        with col1:
            # Speed tracking
            time_data = live_df[live_df['timestamp_seconds'] <= current_time]
            fig_speed = px.line(
                time_data,
                x='timestamp_seconds',
                y='current_speed_kmh',
                color='horse_id',
                title="🚀 Speed Over Time",
                labels={'timestamp_seconds': 'Time (seconds)', 'current_speed_kmh': 'Speed (km/h)'}
            )
            st.plotly_chart(fig_speed, use_container_width=True)
        
        with col2:
            # Heart rate tracking
            fig_hr = px.line(
                time_data,
                x='timestamp_seconds',
                y='heart_rate',
                color='horse_id',
                title="💓 Heart Rate Over Time",
                labels={'timestamp_seconds': 'Time (seconds)', 'heart_rate': 'Heart Rate (BPM)'}
            )
            st.plotly_chart(fig_hr, use_container_width=True)
        
        # Race map
        if 'latitude' in current_data.columns and 'longitude' in current_data.columns:
            st.markdown("### 🗺️ Live Race Map")
            
            fig_map = px.scatter_mapbox(
                current_data,
                lat='latitude',
                lon='longitude',
                size='current_speed_kmh',
                color='position',
                hover_name='horse_id',
                hover_data=['current_speed_kmh', 'heart_rate', 'energy_level'],
                mapbox_style='open-street-map',
                zoom=10,
                title="Horse Positions on Track"
            )
            
            # Add race track path
            if len(time_data) > 0:
                for horse_id in time_data['horse_id'].unique():
                    horse_path = time_data[time_data['horse_id'] == horse_id]
                    fig_map.add_trace(go.Scattermapbox(
                        lat=horse_path['latitude'],
                        lon=horse_path['longitude'],
                        mode='lines',
                        name=f"{horse_id} path",
                        line=dict(width=2),
                        showlegend=False
                    ))
            
            st.plotly_chart(fig_map, use_container_width=True)
        
        # Auto-advance simulation
        if st.session_state.simulation_running and current_time < max_time:
            time.sleep(2)
            st.session_state.current_timestamp = min(current_time + 60, max_time)
            st.rerun()
    
    else:
        st.warning("No data available for selected timestamp.")

def horse_trainer_profile(horses_df, trainers_df, record_df):
    """Horse and Trainer Profile Dashboard"""
    
    st.markdown('<h2 class="sub-header">🐎 Horse & Trainer Profiles</h2>', unsafe_allow_html=True)
    
    profile_type = st.selectbox("Select Profile Type", ["Horse Profile", "Trainer Profile"])
    
    if profile_type == "Horse Profile":
        # Horse selection
        horse_options = horses_df['horse_id'].tolist()
        selected_horse = st.selectbox("Select Horse", horse_options)
        
        if selected_horse:
            horse_info = horses_df[horses_df['horse_id'] == selected_horse].iloc[0]
            
            # Horse details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="race-card">
                <h3>🐎 {selected_horse}</h3>
                <p><strong>Age:</strong> {horse_info['age']} years</p>
                <p><strong>Color:</strong> {horse_info['color']}</p>
                <p><strong>Racing Group:</strong> {horse_info['racing_group']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="race-card">
                <h3>📍 Location</h3>
                <p><strong>Aimag:</strong> {horse_info['aimag']}</p>
                <p><strong>Sum:</strong> {horse_info['sum']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="race-card">
                <h3>🏆 Achievements</h3>
                <p><strong>Provincial:</strong> {horse_info['aimgiin_airag']}</p>
                <p><strong>National:</strong> {horse_info['ulsiin_airag']}</p>
                <p><strong>Total:</strong> {horse_info['total_achievement']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Rider information
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="race-card">
                <h3>🤠 Rider Information</h3>
                <p><strong>Name:</strong> {horse_info['rider_name']}</p>
                <p><strong>Age:</strong> {horse_info['rider_age']} years</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Trainer information
                trainer_info = trainers_df[trainers_df['trainer_id'] == horse_info['trainer_id']]
                if not trainer_info.empty:
                    trainer = trainer_info.iloc[0]
                    st.markdown(f"""
                    <div class="race-card">
                    <h3>👨‍🏫 Trainer Information</h3>
                    <p><strong>Name:</strong> {trainer['trainer_name']}</p>
                    <p><strong>Phone:</strong> {trainer['phone_number']}</p>
                    <p><strong>Total Horses:</strong> {trainer['total_trained_horses']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Race performance (if available)
            race_performance = record_df[record_df['horse_id'] == selected_horse]
            if not race_performance.empty:
                st.markdown("### 🏁 Race Performance")
                perf = race_performance.iloc[0]
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Final Position", f"#{perf['final_position']}")
                with col2:
                    st.metric("Avg Speed", f"{perf['average_speed_kmh']:.2f} km/h")
                with col3:
                    st.metric("Max Speed", f"{perf['max_speed_kmh']:.2f} km/h")
                with col4:
                    st.metric("Prize Won", f"₮{perf['prize_money_tugrik']:,.0f}")
    
    else:  # Trainer Profile
        trainer_options = trainers_df['trainer_name'].tolist()
        selected_trainer = st.selectbox("Select Trainer", trainer_options)
        
        if selected_trainer:
            trainer_info = trainers_df[trainers_df['trainer_name'] == selected_trainer].iloc[0]
            
            # Trainer details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="race-card">
                <h3>👨‍🏫 {selected_trainer}</h3>
                <p><strong>ID:</strong> {trainer_info['trainer_id']}</p>
                <p><strong>Phone:</strong> {trainer_info['phone_number']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="race-card">
                <h3>📍 Location</h3>
                <p><strong>Aimag:</strong> {trainer_info['aimag']}</p>
                <p><strong>Sum:</strong> {trainer_info['sum']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="race-card">
                <h3>🏆 Achievements</h3>
                <p><strong>National:</strong> {trainer_info['national_achievement']}</p>
                <p><strong>Provincial:</strong> {trainer_info['provincial__achievement']}</p>
                <p><strong>Total Horses:</strong> {trainer_info['total_trained_horses']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Trainer's horses
            trainer_horses = horses_df[horses_df['trainer_id'] == trainer_info['trainer_id']]
            
            if not trainer_horses.empty:
                st.markdown("### 🐎 Trained Horses")
                
                # Horse performance summary
                col1, col2 = st.columns(2)
                
                with col1:
                    # Age distribution of trainer's horses
                    age_dist = trainer_horses['age'].value_counts().sort_index()
                    fig_age = px.bar(
                        x=age_dist.index,
                        y=age_dist.values,
                        title="Age Distribution of Trained Horses",
                        labels={'x': 'Age (Years)', 'y': 'Number of Horses'}
                    )
                    st.plotly_chart(fig_age, use_container_width=True)
                
                with col2:
                    # Achievement distribution
                    fig_achievements = px.scatter(
                        trainer_horses,
                        x='aimgiin_airag',
                        y='ulsiin_airag',
                        size='total_achievement',
                        color='age',
                        title="Horse Achievements",
                        labels={'aimgiin_airag': 'Provincial Awards', 'ulsiin_airag': 'National Awards'},
                        hover_data=['horse_id']
                    )
                    st.plotly_chart(fig_achievements, use_container_width=True)
                
                # Detailed horse list
                st.dataframe(
                    trainer_horses[['horse_id', 'age', 'color', 'racing_group', 'total_achievement']],
                    use_container_width=True
                )

def geospatial_dashboard(live_df, record_df):
    """Geospatial Dashboard with race track mapping"""
    
    st.markdown('<h2 class="sub-header">🗺️ Geospatial Race Analysis</h2>', unsafe_allow_html=True)
    
    if 'latitude' not in live_df.columns or 'longitude' not in live_df.columns:
        st.warning("Geospatial data not available in the current dataset.")
        return
    
    # Map controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_horses = st.multiselect(
            "Select Horses to Display",
            live_df['horse_id'].unique(),
            default=live_df['horse_id'].unique()[:3]
        )
    
    with col2:
        map_style = st.selectbox(
            "Map Style",
            ["open-street-map", "satellite-raster", "stamen-terrain"]
        )
    
    with col3:
        show_elevation = st.checkbox("Show Elevation Profile", value=True)
    
    if selected_horses:
        filtered_live = live_df[live_df['horse_id'].isin(selected_horses)]
        
        # Main race track map
        st.markdown("### 🏁 Complete Race Track")
        
        fig_map = px.scatter_mapbox(
            filtered_live,
            lat='latitude',
            lon='longitude',
            color='horse_id',
            size='current_speed_kmh',
            hover_data=['timestamp_seconds', 'current_speed_kmh', 'heart_rate', 'position'],
            mapbox_style=map_style,
            zoom=10,
            height=600,
            title="Race Track with Horse Movements"
        )
        
        # Add race paths
        for horse_id in selected_horses:
            horse_data = filtered_live[filtered_live['horse_id'] == horse_id].sort_values('timestamp_seconds')
            fig_map.add_trace(go.Scattermapbox(
                lat=horse_data['latitude'],
                lon=horse_data['longitude'],
                mode='lines',
                name=f"{horse_id} path",
                line=dict(width=3),
                showlegend=True
            ))
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Speed and elevation analysis
        if show_elevation:
            col1, col2 = st.columns(2)
            
            with col1:
                # Speed vs time for each horse
                fig_speed_time = px.line(
                    filtered_live,
                    x='timestamp_seconds',
                    y='current_speed_kmh',
                    color='horse_id',
                    title="Speed Over Time",
                    labels={'timestamp_seconds': 'Time (seconds)', 'current_speed_kmh': 'Speed (km/h)'}
                )
                st.plotly_chart(fig_speed_time, use_container_width=True)
            
            with col2:
                # Elevation profile
                fig_elevation = px.line(
                    filtered_live,
                    x='distance_covered_km',
                    y='elevation_m',
                    color='horse_id',
                    title="Elevation Profile",
                    labels={'distance_covered_km': 'Distance (km)', 'elevation_m': 'Elevation (m)'}
                )
                st.plotly_chart(fig_elevation, use_container_width=True)
        
        # Statistical analysis
        st.markdown("### 📊 Geospatial Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Distance", f"{filtered_live['distance_covered_km'].max():.1f} km")
        with col2:
            elevation_gain = filtered_live['elevation_m'].max() - filtered_live['elevation_m'].min()
            st.metric("Elevation Gain", f"{elevation_gain:.0f} m")
        with col3:
            avg_speed = filtered_live['current_speed_kmh'].mean()
            st.metric("Average Speed", f"{avg_speed:.1f} km/h")

# Main application
def main():
    # Load CSS and data
    load_css()
    
    st.markdown('<h1 class="main-header">🏇 Naadam 2025 Racing Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    horses_df, trainers_df, record_df, live_df = load_data()
    
    # Sidebar navigation
    st.sidebar.image("https://via.placeholder.com/300x150/FF6B35/FFFFFF?text=Naadam+2025", use_column_width=True)
    st.sidebar.markdown("## 🚀 Navigation")
    
    # Dashboard selection
    dashboard = st.sidebar.selectbox(
        "Select Dashboard",
        ["🏇 Overview", "🏁 Race Records", "📡 Live Simulation", "👤 Profiles", "🗺️ Geospatial"]
    )
    
    # Data summary in sidebar
    st.sidebar.markdown("## 📊 Data Summary")
    st.sidebar.metric("Total Horses", len(horses_df))
    st.sidebar.metric("Total Trainers", len(trainers_df))
    st.sidebar.metric("Race Participants", len(record_df))
    st.sidebar.metric("Live Data Points", len(live_df))
    
    # Main dashboard content
    if dashboard == "🏇 Overview":
        overview_dashboard(horses_df, trainers_df, record_df)
    
    elif dashboard == "🏁 Race Records":
        race_record_dashboard(record_df, horses_df)
    
    elif dashboard == "📡 Live Simulation":
        live_race_simulation(live_df, record_df)
    
    elif dashboard == "👤 Profiles":
        horse_trainer_profile(horses_df, trainers_df, record_df)
    
    elif dashboard == "🗺️ Geospatial":
        geospatial_dashboard(live_df, record_df)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🏇 Naadam 2025 Dashboard**")
    st.sidebar.markdown("Built with Streamlit & Plotly")
    st.sidebar.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()