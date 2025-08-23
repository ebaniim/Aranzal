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
    page_title="🏇 Наадам 2025 Уралдааны Самбар",
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
    """CSV файлууд байхгүй үед үзүүлэлтийн өгөгдөл үүсгэх"""
    
    # Морины өгөгдөл үүсгэх
    np.random.seed(42)
    aimags = ['Улаанбаатар', 'Дархан-Уул', 'Орхон', 'Сэлэнгэ', 'Төв', 'Архангай']
    sums = ['Төв', 'Хойд', 'Урд', 'Зүүн', 'Баруун']
    colors = ['Хээр', 'Шар', 'Хар', 'Саарал', 'Бор', 'Алаг']
    
    horses_data = []
    for i in range(300):
        age_group = (i // 50) + 2  # 2-7 нас
        horses_data.append({
            'horse_id': f'М{str(i+1).zfill(3)}',
            'color': np.random.choice(colors),
            'age': age_group,
            'trainer': f'Сургагч_{np.random.randint(1, 51)}',
            'trainer_id': f'С{str(np.random.randint(1, 51)).zfill(3)}',
            'aimag': np.random.choice(aimags),
            'sum': np.random.choice(sums),
            'rider_name': f'Унаач_{i+1}',
            'rider_age': np.random.randint(8, 16),
            'aimgiin_airag': np.random.randint(0, 5),
            'ulsiin_airag': np.random.randint(0, 10),
            'aimgiin_turuu': np.random.randint(0, 3),
            'ulsiin_turuu': np.random.randint(0, 8),
            'racing_group': f'Нас_{age_group}',
            'total_achievement': np.random.randint(0, 20)
        })
    
    horses_df = pd.DataFrame(horses_data)
    
    # Сургагчийн өгөгдөл үүсгэх
    trainers_data = []
    for i in range(50):
        trainers_data.append({
            'trainer_id': f'С{str(i+1).zfill(3)}',
            'trainer_name': f'Сургагч_{i+1}',
            'aimag': np.random.choice(aimags),
            'sum': np.random.choice(sums),
            'national_achievement': np.random.randint(0, 15),
            'provincial__achievement': np.random.randint(0, 25),
            'total_trained_horses': np.random.randint(1, 10),
            'phone_number': f'+976-{np.random.randint(80000000, 99999999)}'
        })
    
    trainers_df = pd.DataFrame(trainers_data)
    
    # Уралдааны бичлэгийн өгөгдөл (Даага - 2 настай)
    daaga_horses = horses_df[horses_df['age'] == 2].head(50)
    record_data = []
    
    for i, horse in enumerate(daaga_horses.itertuples()):
        finish_time_minutes = np.random.randint(25, 35)
        finish_time_seconds = np.random.randint(0, 60)
        distance_km = 15.0
        
        record_data.append({
            'horse_id': horse.horse_id,
            'racing_group': 'Даага',
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
            'weather': np.random.choice(['Нартай', 'Үүлэрхэг', 'Салхитай']),
            'temperature_celsius': np.random.randint(20, 30),
            'wind_speed_kmh': np.random.randint(0, 20),
            'humidity_percent': np.random.randint(30, 70),
            'track_condition': np.random.choice(['Сайн', 'Зөөлөн', 'Хатуу']),
            'prize_money_tugrik': max(0, 10000000 - (i * 200000)),
            'injury': np.random.choice(['Байхгүй', 'Бага зэрэг', 'Байхгүй', 'Байхгүй', 'Байхгүй']),
            'fatigue_level': np.random.choice(['Бага', 'Дунд', 'Өндөр']),
            'rider_experience_years': np.random.randint(1, 8)
        })
    
    record_df = pd.DataFrame(record_data)
    
    # Шилдэг 5 морьдын шууд өгөгдөл үүсгэх
    top_5_horses = record_df.head(5)['horse_id'].tolist()
    live_data = []
    
    # Монголын тал нутгийн координат
    base_lat, base_lon = 47.9184, 106.9177
    
    for timestamp in range(0, 1800, 60):  # 30 минут, 60 секунд тутамд
        for i, horse_id in enumerate(top_5_horses):
            progress = timestamp / 1800  # Уралдааны явц (0-с 1 хүртэл)
            
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
                'rider_commands': np.random.choice(['Тогтвортой', 'Түлхэх', 'Барих', 'Гүйлт', 'Амрах'])
            })
    
    live_df = pd.DataFrame(live_data)
    
    return horses_df, trainers_df, record_df, live_df

@st.cache_data
def load_data():
    """CSV файлаас өгөгдөл ачаалах эсвэл үзүүлэлтийн өгөгдөл үүсгэх"""
    try:
        horses_df = pd.read_csv(r"data/horse.csv")
        trainers_df = pd.read_csv(r"data/trainer.csv")
        record_df = pd.read_csv(r"data/record.csv")
        live_df = pd.read_csv(r"data/live.csv")
        return horses_df, trainers_df, record_df, live_df
    except FileNotFoundError:
        st.info("📁 CSV файлууд олдсонгүй. Үзүүлэлтийн өгөгдлийг ашиглаж байна.")
        return generate_demo_data()

# Dashboard functions
def overview_dashboard(horses_df, trainers_df, record_df):
    """Ерөнхий самбар - гол үзүүлэлт болон тархалт"""
    
    st.markdown('<h2 class="sub-header">🏇 Уралдааны Ерөнхий Мэдээлэл</h2>', unsafe_allow_html=True)
    
    # Гол үзүүлэлтүүд
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Нийт Морь", len(horses_df), delta="Идэвхтэй")
    with col2:
        st.metric("Нийт Уяач", len(trainers_df), delta="Бүртгэлтэй")
    with col3:
        st.metric("Дууссан Уралдаан", 1, delta="Наадам 2025")
    with col4:
        total_prize = record_df['prize_money_tugrik'].sum()
        st.metric("Нийт Шагналын Мөнгө", f"₮{total_prize:,.0f}", delta="Хуваарилсан")
    
    # Диаграмууд 1-р эгнээ
    col1, col2 = st.columns(2)
    
    with col1:
        # Насны ангиллаар морьд
        age_dist = horses_df['age'].value_counts().sort_index()
        fig_age = px.bar(
            x=age_dist.index,
            y=age_dist.values,
            title="🐎 Насны Ангиллаар Морьд",
            labels={'x': 'Нас (Жил)', 'y': 'Морины Тоо'},
            color=age_dist.values,
            color_continuous_scale='viridis'
        )
        fig_age.update_layout(showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        # Аймгаар морьдын тархалт
        aimag_dist = horses_df['aimag'].value_counts()
        fig_aimag = px.pie(
            values=aimag_dist.values,
            names=aimag_dist.index,
            title="🗺️ Аймгаар Морины Тархалт"
        )
        fig_aimag.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_aimag, use_container_width=True)
    
    # Диаграмууд 2-р эгнээ
    col1, col2 = st.columns(2)
    
    with col1:
        # Сургагчийн амжилт
        fig_trainers = px.scatter(
            trainers_df,
            x='provincial__achievement',
            y='national_achievement',
            size='total_trained_horses',
            color='aimag',
            title="🏆 Уяачийн Амжилт",
            labels={'provincial__achievement': 'Аймгийн Амжилт', 
                   'national_achievement': 'Үндэсний Амжилт'},
            hover_data=['trainer_name']
        )
        st.plotly_chart(fig_trainers, use_container_width=True)
    
    with col2:
        # Морины өнгөний тархалт
        color_dist = horses_df['color'].value_counts()
        fig_colors = px.bar(
            x=color_dist.values,
            y=color_dist.index,
            orientation='h',
            title="🎨 Морины Өнгөний Тархалт",
            labels={'x': 'Морины Тоо', 'y': 'Өнгө'},
            color=color_dist.values,
            color_continuous_scale='rainbow'
        )
        st.plotly_chart(fig_colors, use_container_width=True)

def race_record_dashboard(record_df, horses_df):
    """Уралдааны бичлэгийн самбар - дэлгэрэнгүй шинжилгээ"""
    
    st.markdown('<h2 class="sub-header">🏁 Уралдааны Бичлэгийн Шинжилгээ - Наадам 2025 Даага</h2>', unsafe_allow_html=True)
    
    # Уралдааны хураангуй
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Оролцогчид", len(record_df))
    with col2:
        avg_speed = record_df['average_speed_kmh'].mean()
        st.metric("Дундаж Хурд", f"{avg_speed:.1f} км/ц")
    with col3:
        max_speed = record_df['max_speed_kmh'].max()
        st.metric("Хамгийн Өндөр Хурд", f"{max_speed:.1f} км/ц")
    with col4:
        race_distance = record_df['distance_km'].iloc[0]
        st.metric("Зай", f"{race_distance:.0f} км")
    
    # Байрлал болон хурдны шинжилгээ
    col1, col2 = st.columns(2)
    
    with col1:
        # Эцсийн байрлал ба хурд
        fig_pos = px.scatter(
            record_df,
            x='final_position',
            y='average_speed_kmh',
            size='max_speed_kmh',
            color='final_position',
            title="🏃 Байрлал ба Хурдны Шинжилгээ",
            labels={'final_position': 'Эцсийн Байрлал', 'average_speed_kmh': 'Дундаж Хурд (км/ц)'},
            hover_data=['horse_id', 'finish_time_minutes', 'finish_time_seconds'],
            color_continuous_scale='RdYlBu_r'
        )
        st.plotly_chart(fig_pos, use_container_width=True)
    
    with col2:
        # Барианы цагийн тархалт
        record_df['total_time'] = record_df['finish_time_minutes'] + record_df['finish_time_seconds']/60
        fig_time = px.histogram(
            record_df,
            x='total_time',
            nbins=20,
            title="⏱️ Барианы Цагийн Тархалт",
            labels={'total_time': 'Барианы Цаг (минут)', 'count': 'Морины Тоо'},
            color_discrete_sequence=['#FF6B35']
        )
        st.plotly_chart(fig_time, use_container_width=True)
    
    # Зүрхний цохилт болон унаачийн шинжилгээ
    col1, col2 = st.columns(2)
    
    with col1:
        # Зүрхний цохилтын шинжилгээ
        fig_hr = go.Figure()
        fig_hr.add_trace(go.Scatter(
            x=record_df['final_position'],
            y=record_df['heart_rate_start'],
            mode='markers',
            name='Эхлэлийн Зц',
            marker=dict(color='blue', size=8)
        ))
        fig_hr.add_trace(go.Scatter(
            x=record_df['final_position'],
            y=record_df['heart_rate_end'],
            mode='markers',
            name='Төгсгөлийн Зц',
            marker=dict(color='red', size=8)
        ))
        fig_hr.update_layout(
            title="💓 Байрлалаар Зүрхний Цохилт",
            xaxis_title="Эцсийн Байрлал",
            yaxis_title="Зүрхний Цохилт (мин-д)"
        )
        st.plotly_chart(fig_hr, use_container_width=True)
    
    with col2:
        # Шагналын мөнгөний тархалт
        fig_prize = px.bar(
            record_df.head(10),
            x='final_position',
            y='prize_money_tugrik',
            title="💰 Шагналын Мөнгө (Эхний 10)",
            labels={'final_position': 'Байрлал', 'prize_money_tugrik': 'Шагналын Мөнгө (₮)'},
            color='prize_money_tugrik',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_prize, use_container_width=True)
    
    # Дэлгэрэнгүй уралдааны үр дүнгийн хүснэгт
    st.markdown("### 📊 Дэлгэрэнгүй Уралдааны Үр Дүн")
    
    # Шүүлтүүр нэмэх
    col1, col2, col3 = st.columns(3)
    with col1:
        position_filter = st.selectbox("Байрлалаар Шүүх", 
                                     ["Бүгд", "Эхний 10", "Эхний 20", "Сүүлийн 10"])
    with col2:
        speed_filter = st.slider("Хамгийн Багадаа Дундаж Хурд (км/ц)", 
                               float(record_df['average_speed_kmh'].min()),
                               float(record_df['average_speed_kmh'].max()),
                               float(record_df['average_speed_kmh'].min()))
    with col3:
        weather_filter = st.selectbox("Цаг Агаарын Нөхцөл", 
                                    ["Бүгд"] + list(record_df['weather'].unique()))
    
    # Шүүлтүүр хэрэглэх
    filtered_df = record_df.copy()
    
    if position_filter == "Эхний 10":
        filtered_df = filtered_df[filtered_df['final_position'] <= 10]
    elif position_filter == "Эхний 20":
        filtered_df = filtered_df[filtered_df['final_position'] <= 20]
    elif position_filter == "Сүүлийн 10":
        filtered_df = filtered_df[filtered_df['final_position'] > 40]
    
    filtered_df = filtered_df[filtered_df['average_speed_kmh'] >= speed_filter]
    
    if weather_filter != "Бүгд":
        filtered_df = filtered_df[filtered_df['weather'] == weather_filter]
    
    # Үр дүнг харуулах
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
    """Шууд уралдааны дүрслэл - анимацитай"""
    
    st.markdown('<h2 class="sub-header">📡 Шууд Уралдааны Дүрслэл - Шилдэг 5 Морь</h2>', unsafe_allow_html=True)
    
    # Удирдлагын самбар
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Дүрслэл Эхлүүлэх", type="primary"):
            st.session_state.simulation_running = True
            st.session_state.current_timestamp = 0
    
    with col2:
        if st.button("⏸️ Зогсоох"):
            st.session_state.simulation_running = False
    
    with col3:
        if st.button("🔄 Дахин Эхлэх"):
            st.session_state.simulation_running = False
            st.session_state.current_timestamp = 0
    
    # Session state эхлүүлэх
    if 'simulation_running' not in st.session_state:
        st.session_state.simulation_running = False
    if 'current_timestamp' not in st.session_state:
        st.session_state.current_timestamp = 0
    
    # Цагийн сонголт
    max_time = live_df['timestamp_seconds'].max()
    current_time = st.slider(
        "Уралдааны Цаг (секунд)", 
        0, int(max_time), 
        int(st.session_state.current_timestamp),
        step=60
    )
    
    # Одоогийн өгөгдөл авах
    current_data = live_df[live_df['timestamp_seconds'] == current_time]
    
    if len(current_data) > 0:
        # Уралдааны явц
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Байрлалын хяналт
            fig_pos = px.bar(
                current_data.sort_values('position'),
                x='horse_id',
                y='distance_covered_km',
                color='position',
                title=f"🏁 Одоогийн Байрлал (Цаг: {current_time//60}:{current_time%60:02d})",
                labels={'distance_covered_km': 'Туулсан Зай (км)'},
                color_continuous_scale='RdYlBu'
            )
            fig_pos.update_layout(showlegend=False)
            st.plotly_chart(fig_pos, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Шууд Үзүүлэлт")
            for _, horse in current_data.iterrows():
                with st.container():
                    st.markdown(f"**{horse['horse_id']}** (Байр: {horse['position']})")
                    st.metric(
                        "Хурд", 
                        f"{horse['current_speed_kmh']:.1f} км/ц",
                        delta=f"{horse['current_speed_kmh'] - 30:.1f}"
                    )
                    st.progress(horse['energy_level']/100)
                    st.markdown("---")
        
        # Хурд болон зүрхний цохилт цаг хугацаагаар
        col1, col2 = st.columns(2)
        
        with col1:
            # Хурдны хяналт
            time_data = live_df[live_df['timestamp_seconds'] <= current_time]
            fig_speed = px.line(
                time_data,
                x='timestamp_seconds',
                y='current_speed_kmh',
                color='horse_id',
                title="🚀 Цаг Хугацаагаар Хурд",
                labels={'timestamp_seconds': 'Цаг (секунд)', 'current_speed_kmh': 'Хурд (км/ц)'}
            )
            st.plotly_chart(fig_speed, use_container_width=True)
        
        with col2:
            # Зүрхний цохилтын хяналт
            fig_hr = px.line(
                time_data,
                x='timestamp_seconds',
                y='heart_rate',
                color='horse_id',
                title="💓 Цаг Хугацаагаар Зүрхний Цохилт",
                labels={'timestamp_seconds': 'Цаг (секунд)', 'heart_rate': 'Зүрхний Цохилт (мин-д)'}
            )
            st.plotly_chart(fig_hr, use_container_width=True)
        
        # Уралдааны газрын зураг
        if 'latitude' in current_data.columns and 'longitude' in current_data.columns:
            st.markdown("### 🗺️ Шууд Уралдааны Газрын Зураг")
            
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
                title="Замд Морьдын Байрлал"
            )
            
            # Уралдааны замын шугам нэмэх
            if len(time_data) > 0:
                for horse_id in time_data['horse_id'].unique():
                    horse_path = time_data[time_data['horse_id'] == horse_id]
                    fig_map.add_trace(go.Scattermapbox(
                        lat=horse_path['latitude'],
                        lon=horse_path['longitude'],
                        mode='lines',
                        name=f"{horse_id} зам",
                        line=dict(width=2),
                        showlegend=False
                    ))
            
            st.plotly_chart(fig_map, use_container_width=True)
        
        # Автомат дүрслэлийн үргэлжлэл
        if st.session_state.simulation_running and current_time < max_time:
            time.sleep(2)
            st.session_state.current_timestamp = min(current_time + 60, max_time)
            st.rerun()
    
    else:
        st.warning("Сонгосон цагт өгөгдөл байхгүй байна.")

def horse_trainer_profile(horses_df, trainers_df, record_df):
    """Морь ба Сургагчийн Хувийн Мэдээллийн Самбар"""
    
    st.markdown('<h2 class="sub-header">🐎 Морь ба Уяачийн Хувийн Мэдээлэл</h2>', unsafe_allow_html=True)
    
    profile_type = st.selectbox("Хувийн Мэдээллийн Төрөл", ["Морины Хувийн Мэдээлэл", "Уяачийн Хувийн Мэдээлэл"])
    
    if profile_type == "Морины Хувийн Мэдээлэл":
        # Морь сонгох
        horse_options = horses_df['horse_id'].tolist()
        selected_horse = st.selectbox("Морь Сонгох", horse_options)
        
        if selected_horse:
            horse_info = horses_df[horses_df['horse_id'] == selected_horse].iloc[0]
            
            # Морины дэлгэрэнгүй мэдээлэл
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="race-card">
                <h3>🐎 {selected_horse}</h3>
                <p><strong>Нас:</strong> {horse_info['age']} жил</p>
                <p><strong>Өнгө:</strong> {horse_info['color']}</p>
                <p><strong>Уралдааны Бүлэг:</strong> {horse_info['racing_group']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="race-card">
                <h3>📍 Байршил</h3>
                <p><strong>Аймаг:</strong> {horse_info['aimag']}</p>
                <p><strong>Сум:</strong> {horse_info['sum']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="race-card">
                <h3>🏆 Амжилт</h3>
                <p><strong>Аймгийн:</strong> {horse_info['aimgiin_airag']}</p>
                <p><strong>Үндэсний:</strong> {horse_info['ulsiin_airag']}</p>
                <p><strong>Нийт:</strong> {horse_info['total_achievement']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Унаачийн мэдээлэл
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="race-card">
                <h3>🤠 Унаачийн Мэдээлэл</h3>
                <p><strong>Нэр:</strong> {horse_info['rider_name']}</p>
                <p><strong>Нас:</strong> {horse_info['rider_age']} жил</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Сургагчийн мэдээлэл
                trainer_info = trainers_df[trainers_df['trainer_id'] == horse_info['trainer_id']]
                if not trainer_info.empty:
                    trainer = trainer_info.iloc[0]
                    st.markdown(f"""
                    <div class="race-card">
                    <h3>👨‍🏫 Уяачийн Мэдээлэл</h3>
                    <p><strong>Нэр:</strong> {trainer['trainer_name']}</p>
                    <p><strong>Утас:</strong> {trainer['phone_number']}</p>
                    <p><strong>Нийт Морь:</strong> {trainer['total_trained_horses']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Уралдааны гүйцэтгэл (боломжтой бол)
            race_performance = record_df[record_df['horse_id'] == selected_horse]
            if not race_performance.empty:
                st.markdown("### 🏁 Уралдааны Гүйцэтгэл")
                perf = race_performance.iloc[0]
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Эцсийн Байрлал", f"#{perf['final_position']}")
                with col2:
                    st.metric("Дундаж Хурд", f"{perf['average_speed_kmh']:.2f} км/ц")
                with col3:
                    st.metric("Хамгийн Өндөр Хурд", f"{perf['max_speed_kmh']:.2f} км/ц")
                with col4:
                    st.metric("Хожсон Шагнал", f"₮{perf['prize_money_tugrik']:,.0f}")
    
    else:  # Сургагчийн Хувийн Мэдээлэл
        trainer_options = trainers_df['trainer_name'].tolist()
        selected_trainer = st.selectbox("Уяач Сонгох", trainer_options)
        
        if selected_trainer:
            trainer_info = trainers_df[trainers_df['trainer_name'] == selected_trainer].iloc[0]
            
            # Сургагчийн дэлгэрэнгүй мэдээлэл
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="race-card">
                <h3>👨‍🏫 {selected_trainer}</h3>
                <p><strong>ID:</strong> {trainer_info['trainer_id']}</p>
                <p><strong>Утас:</strong> {trainer_info['phone_number']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="race-card">
                <h3>📍 Байршил</h3>
                <p><strong>Аймаг:</strong> {trainer_info['aimag']}</p>
                <p><strong>Сум:</strong> {trainer_info['sum']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="race-card">
                <h3>🏆 Амжилт</h3>
                <p><strong>Үндэсний:</strong> {trainer_info['national_achievement']}</p>
                <p><strong>Аймгийн:</strong> {trainer_info['provincial__achievement']}</p>
                <p><strong>Нийт Морь:</strong> {trainer_info['total_trained_horses']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Сургагчийн морьд
            trainer_horses = horses_df[horses_df['trainer_id'] == trainer_info['trainer_id']]
            
            if not trainer_horses.empty:
                st.markdown("### 🐎 Сургасан Морьд")
                
                # Морины гүйцэтгэлийн хураангуй
                col1, col2 = st.columns(2)
                
                with col1:
                    # Сургасан морьдын насны тархалт
                    age_dist = trainer_horses['age'].value_counts().sort_index()
                    fig_age = px.bar(
                        x=age_dist.index,
                        y=age_dist.values,
                        title="Сургасан Морьдын Насны Тархалт",
                        labels={'x': 'Нас (Жил)', 'y': 'Морины Тоо'}
                    )
                    st.plotly_chart(fig_age, use_container_width=True)
                
                with col2:
                    # Амжилтын тархалт
                    fig_achievements = px.scatter(
                        trainer_horses,
                        x='aimgiin_airag',
                        y='ulsiin_airag',
                        size='total_achievement',
                        color='age',
                        title="Морьдын Амжилт",
                        labels={'aimgiin_airag': 'Аймгийн Шагнал', 'ulsiin_airag': 'Үндэсний Шагнал'},
                        hover_data=['horse_id']
                    )
                    st.plotly_chart(fig_achievements, use_container_width=True)
                
                # Дэлгэрэнгүй морьдын жагсаалт
                st.dataframe(
                    trainer_horses[['horse_id', 'age', 'color', 'racing_group', 'total_achievement']],
                    use_container_width=True
                )

def geospatial_dashboard(live_df, record_df):
    """Газарзүйн уралдааны шинжилгээний самбар"""
    
    st.markdown('<h2 class="sub-header">🗺️ Газарзүйн Уралдааны Шинжилгээ</h2>', unsafe_allow_html=True)
    
    if 'latitude' not in live_df.columns or 'longitude' not in live_df.columns:
        st.warning("Одоогийн өгөгдлийн санд газарзүйн өгөгдөл байхгүй байна.")
        return
    
    # Газрын зургийн удирдлага
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_horses = st.multiselect(
            "Харуулах Морьдыг Сонгох",
            live_df['horse_id'].unique(),
            default=live_df['horse_id'].unique()[:3]
        )
    
    with col2:
        map_style = st.selectbox(
            "Газрын Зургийн Загвар",
            ["open-street-map", "satellite-raster", "stamen-terrain"]
        )
    
    with col3:
        show_elevation = st.checkbox("Өндрийн Профайл Харуулах", value=True)
    
    if selected_horses:
        filtered_live = live_df[live_df['horse_id'].isin(selected_horses)]
        
        # Үндсэн уралдааны замын газрын зураг
        st.markdown("### 🏁 Бүрэн Уралдааны Зам")
        
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
            title="Морьдын Хөдөлгөөнтэй Уралдааны Зам"
        )
        
        # Уралдааны замын шугам нэмэх
        for horse_id in selected_horses:
            horse_data = filtered_live[filtered_live['horse_id'] == horse_id].sort_values('timestamp_seconds')
            fig_map.add_trace(go.Scattermapbox(
                lat=horse_data['latitude'],
                lon=horse_data['longitude'],
                mode='lines',
                name=f"{horse_id} зам",
                line=dict(width=3),
                showlegend=True
            ))
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Хурд болон өндрийн шинжилгээ
        if show_elevation:
            col1, col2 = st.columns(2)
            
            with col1:
                # Морь тус бүрийн хурд ба цаг
                fig_speed_time = px.line(
                    filtered_live,
                    x='timestamp_seconds',
                    y='current_speed_kmh',
                    color='horse_id',
                    title="Цаг Хугацаагаар Хурд",
                    labels={'timestamp_seconds': 'Цаг (секунд)', 'current_speed_kmh': 'Хурд (км/ц)'}
                )
                st.plotly_chart(fig_speed_time, use_container_width=True)
            
            with col2:
                # Өндрийн профайл
                fig_elevation = px.line(
                    filtered_live,
                    x='distance_covered_km',
                    y='elevation_m',
                    color='horse_id',
                    title="Өндрийн Профайл",
                    labels={'distance_covered_km': 'Зай (км)', 'elevation_m': 'Өндөр (м)'}
                )
                st.plotly_chart(fig_elevation, use_container_width=True)
        
        # Статистикийн шинжилгээ
        st.markdown("### 📊 Газарзүйн Статистик")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Нийт Зай", f"{filtered_live['distance_covered_km'].max():.1f} км")
        with col2:
            elevation_gain = filtered_live['elevation_m'].max() - filtered_live['elevation_m'].min()
            st.metric("Өндрийн Өсөлт", f"{elevation_gain:.0f} м")
        with col3:
            avg_speed = filtered_live['current_speed_kmh'].mean()
            st.metric("Дундаж Хурд", f"{avg_speed:.1f} км/ц")

# Үндсэн програм
def main():
    # CSS болон өгөгдөл ачаалах
    load_css()
    
    st.markdown('<h1 class="main-header">🏇 Наадам 2025 Уралдааны Самбар</h1>', unsafe_allow_html=True)
    
    # Өгөгдөл ачаалах
    horses_df, trainers_df, record_df, live_df = load_data()
    
    # Хажуугийн навигаци
    try:
        st.sidebar.image(r"data/logo.png", use_container_width=True)
    except:
        st.sidebar.markdown("## 🏇 Наадам 2025")
    #st.sidebar.markdown("## 🚀 Навигаци")
    
    # Самбарын сонголт
    dashboard = st.sidebar.selectbox(
        "Самбар Сонгох",
        ["🏇 Ерөнхий", "🏁 Уралдааны рэкорд", "📡 Шууд Дүрслэл", "👤 Хувийн Мэдээлэл", "🗺️ Газарзүйн"]
    )
    
    # Хажуугийн өгөгдлийн хураангуй
    st.sidebar.markdown("## 📊 Өгөгдлийн Хураангуй")
    st.sidebar.metric("Нийт Морь", len(horses_df))
    st.sidebar.metric("Нийт Уяач", len(trainers_df))
    st.sidebar.metric("Уралдааны Оролцогч", len(record_df))
    #st.sidebar.metric("Шууд Өгөгдлийн Цэг", len(live_df))
    
    # Үндсэн самбарын агуулга
    if dashboard == "🏇 Ерөнхий":
        overview_dashboard(horses_df, trainers_df, record_df)
    
    elif dashboard == "🏁 Уралдааны Бичлэг":
        race_record_dashboard(record_df, horses_df)
    
    elif dashboard == "📡 Шууд Дүрслэл":
        live_race_simulation(live_df, record_df)
    
    elif dashboard == "👤 Хувийн Мэдээлэл":
        horse_trainer_profile(horses_df, trainers_df, record_df)
    
    elif dashboard == "🗺️ Газарзүйн":
        geospatial_dashboard(live_df, record_df)
    
    # Доод талын мэдээлэл
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🏇 Наадам 2025 Самбар**")
    st.sidebar.markdown(f"Сүүлд шинэчлэгдсэн: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()





