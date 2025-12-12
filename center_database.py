"""
ADVANCED CENTER DATABASE MODULE
Ready to integrate with real Excel data
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# ============================================================================
# SAMPLE DATA GENERATOR (Replace with your Excel loader)
# ============================================================================

def generate_sample_center_data(center_name: str) -> pd.DataFrame:
    """
    Generate sample data for demonstration.
    Replace this with your actual Excel file loader.
    """
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    programs = ['Islamic Studies', 'Youth Program', 'Community Service', 'Women Empowerment', 'Quran Classes']
    categories = ['Engagement', 'Learning', 'Community', 'Feedback', 'Growth']
    
    data = {
        'Date': np.random.choice(dates, 500),
        'Program': np.random.choice(programs, 500),
        'Participants': np.random.randint(5, 100, 500),
        'Satisfaction': np.random.randint(1, 6, 500),  # 1-5 scale
        'Category': np.random.choice(categories, 500),
        'Attendance_Rate': np.random.uniform(0.6, 1.0, 500),
        'Feedback_Score': np.random.randint(1, 10, 500),
        'Notes': ['Good engagement', 'High participation', 'Good feedback', 'Excellent turnout', 'Need improvement'] * 100
    }
    
    return pd.DataFrame(data).sort_values('Date')


def load_center_data(center_name: str) -> pd.DataFrame:
    """
    Load center data from Excel file.
    Update path to your actual data location.
    """
    try:
        # Try to load from Excel
        file_path = f"data/center_data/{center_name}.xlsx"
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        # Return sample data if file not found
        st.warning(f"Excel file for {center_name} not found. Using sample data for demo.")
        return generate_sample_center_data(center_name)


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def calculate_metrics(df: pd.DataFrame) -> dict:
    """Calculate key metrics from center data"""
    metrics = {
        'total_responses': len(df),
        'total_participants': df['Participants'].sum(),
        'avg_satisfaction': df['Satisfaction'].mean(),
        'avg_attendance': df['Attendance_Rate'].mean() * 100,
        'top_program': df['Program'].value_counts().idxmax() if len(df) > 0 else 'N/A',
        'top_category': df['Category'].value_counts().idxmax() if len(df) > 0 else 'N/A',
    }
    return metrics


def create_satisfaction_chart(df: pd.DataFrame) -> go.Figure:
    """Create satisfaction distribution chart"""
    satisfaction_counts = df['Satisfaction'].value_counts().sort_index()
    
    fig = go.Figure(data=[
        go.Bar(
            x=['Very Poor', 'Poor', 'Neutral', 'Good', 'Excellent'],
            y=[satisfaction_counts.get(i, 0) for i in range(1, 6)],
            marker=dict(
                color=['#ff6b6b', '#ffa726', '#ffd93d', '#6bcf7f', '#4ecdc4'],
                line=dict(color='rgba(0,0,0,0.1)', width=1)
            ),
            text=[satisfaction_counts.get(i, 0) for i in range(1, 6)],
            textposition='outside',
        )
    ])
    
    fig.update_layout(
        title="Response Satisfaction Distribution",
        xaxis_title="Satisfaction Level",
        yaxis_title="Number of Responses",
        hovermode='x unified',
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def create_program_engagement_chart(df: pd.DataFrame) -> go.Figure:
    """Create program engagement chart"""
    program_data = df.groupby('Program').agg({
        'Participants': 'sum',
        'Satisfaction': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=program_data['Program'],
        y=program_data['Participants'],
        name='Total Participants',
        marker=dict(color='#667eea'),
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=program_data['Program'],
        y=program_data['Satisfaction'],
        name='Avg Satisfaction',
        marker=dict(color='#ff6b9d', size=10),
        yaxis='y2',
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title="Program Engagement & Satisfaction",
        xaxis_title="Program Name",
        yaxis=dict(title="Total Participants", side='left'),
        yaxis2=dict(title="Avg Satisfaction (1-5)", overlaying='y', side='right'),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def create_monthly_trend_chart(df: pd.DataFrame) -> go.Figure:
    """Create monthly trend chart"""
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
    monthly_data = df.groupby('Month').agg({
        'Participants': 'sum',
        'Satisfaction': 'mean'
    }).reset_index()
    monthly_data['Month'] = monthly_data['Month'].astype(str)
    
    fig = px.line(
        monthly_data,
        x='Month',
        y='Participants',
        markers=True,
        title='Monthly Participation Trend',
        labels={'Participants': 'Total Participants', 'Month': 'Month'},
        line_shape='spline'
    )
    
    fig.update_traces(line=dict(color='#667eea', width=3), marker=dict(size=8))
    fig.update_layout(hovermode='x unified', plot_bgcolor='rgba(0,0,0,0)')
    
    return fig


def create_category_breakdown(df: pd.DataFrame) -> go.Figure:
    """Create category breakdown pie chart"""
    category_counts = df['Category'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=category_counts.index,
        values=category_counts.values,
        hole=0.3,
        marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'])
    )])
    
    fig.update_layout(
        title="Feedback Categories Distribution",
        showlegend=True,
    )
    return fig


# ============================================================================
# STREAMLIT UI RENDERER
# ============================================================================

def render_center_database():
    """Render the complete Center Database dashboard"""
    
    # Title
    st.markdown('<div class="main-header">🏛️ Center Database Dashboard</div>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Analytics", "📋 Raw Data", "💾 Upload"])
    
    # ========== TAB 1: DASHBOARD ==========
    with tab1:
        # Center selection
        col_select, col_period = st.columns([2, 1])
        
        with col_select:
            centers = ["Aboubakr", "Al-Rashid", "Al-Noor", "Masjid Al-Hana", "Islamic Center"]
            selected_center = st.selectbox(
                "🏛️ Select Centre",
                centers,
                key="center_selector"
            )
        
        with col_period:
            period = st.selectbox(
                "📅 Time Period",
                ["All Time", "Last 12 Months", "Last 6 Months", "Last 3 Months"],
                key="period_selector"
            )
        
        st.markdown("---")
        
        # Load data
        df = load_center_data(selected_center)
        metrics = calculate_metrics(df)
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Total Responses",
                value=f"{metrics['total_responses']:,}",
                delta="responses collected"
            )
        
        with col2:
            st.metric(
                label="👥 Total Participants",
                value=f"{metrics['total_participants']:,}",
                delta="people engaged"
            )
        
        with col3:
            satisfaction_pct = (metrics['avg_satisfaction'] / 5) * 100
            st.metric(
                label="😊 Avg Satisfaction",
                value=f"{satisfaction_pct:.1f}%",
                delta=f"{metrics['avg_satisfaction']:.2f}/5.0"
            )
        
        with col4:
            st.metric(
                label="✓ Attendance Rate",
                value=f"{metrics['avg_attendance']:.1f}%",
                delta="average"
            )
        
        st.markdown("---")
        
        # Key highlights
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"🎯 **Top Program:** {metrics['top_program']}")
        
        with col2:
            st.info(f"📌 **Top Category:** {metrics['top_category']}")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_satisfaction_chart(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_category_breakdown(df), use_container_width=True)
        
        st.plotly_chart(create_program_engagement_chart(df), use_container_width=True)
        st.plotly_chart(create_monthly_trend_chart(df), use_container_width=True)
    
    # ========== TAB 2: ANALYTICS ==========
    with tab2:
        st.subheader("📈 Deep Analytics")
        
        df = load_center_data(selected_center)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Program Performance Ranking")
            program_performance = df.groupby('Program').agg({
                'Participants': 'sum',
                'Satisfaction': 'mean',
                'Attendance_Rate': 'mean'
            }).sort_values('Participants', ascending=False)
            
            st.dataframe(
                program_performance.round(2),
                use_container_width=True,
                column_config={
                    "Participants": st.column_config.NumberColumn("Participants"),
                    "Satisfaction": st.column_config.NumberColumn("Avg Satisfaction", format="%.2f"),
                    "Attendance_Rate": st.column_config.NumberColumn("Attendance Rate", format="%.2%"),
                }
            )
        
        with col2:
            st.markdown("#### Category Performance")
            category_performance = df.groupby('Category').agg({
                'Satisfaction': 'mean',
                'Feedback_Score': 'mean'
            }).sort_values('Satisfaction', ascending=False)
            
            st.dataframe(
                category_performance.round(2),
                use_container_width=True,
            )
        
        st.markdown("---")
        
        # Time-based analysis
        st.markdown("#### Trend Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            df_copy = df.copy()
            df_copy['Week'] = pd.to_datetime(df_copy['Date']).dt.to_period('W')
            weekly_stats = df_copy.groupby('Week').agg({
                'Participants': 'sum',
                'Satisfaction': 'mean'
            }).reset_index()
            weekly_stats['Week'] = weekly_stats['Week'].astype(str)
            
            fig = px.area(
                weekly_stats,
                x='Week',
                y='Participants',
                title='Weekly Participation Trend',
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            satisfaction_by_program = df.groupby('Program')['Satisfaction'].mean().sort_values(ascending=True)
            fig = px.barh(
                satisfaction_by_program,
                title='Satisfaction by Program',
                labels={'value': 'Avg Satisfaction', 'index': 'Program'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== TAB 3: RAW DATA ==========
    with tab3:
        st.subheader("📋 Raw Data View")
        
        df = load_center_data(selected_center)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            program_filter = st.multiselect(
                "Filter by Program",
                df['Program'].unique(),
                default=df['Program'].unique()
            )
        
        with col2:
            category_filter = st.multiselect(
                "Filter by Category",
                df['Category'].unique(),
                default=df['Category'].unique()
            )
        
        with col3:
            satisfaction_filter = st.slider(
                "Min Satisfaction",
                1, 5, 1
            )
        
        # Apply filters
        filtered_df = df[
            (df['Program'].isin(program_filter)) &
            (df['Category'].isin(category_filter)) &
            (df['Satisfaction'] >= satisfaction_filter)
        ]
        
        st.dataframe(
            filtered_df.sort_values('Date', ascending=False),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name=f"{selected_center}_data.csv",
            mime="text/csv"
        )
    
    # ========== TAB 4: UPLOAD ==========
    with tab4:
        st.subheader("💾 Upload Center Data")
        
        st.markdown("""
        Upload Excel files for center data. Expected columns:
        - **Date** - Activity date
        - **Program** - Program name
        - **Participants** - Number of participants
        - **Satisfaction** - Satisfaction rating (1-5)
        - **Category** - Feedback category
        - **Attendance_Rate** - Attendance percentage (0-1)
        - **Feedback_Score** - Feedback score (1-10)
        - **Notes** - Additional notes
        """)
        
        uploaded_file = st.file_uploader(
            "Choose Excel file",
            type=["xlsx", "xls"],
            key="data_upload"
        )
        
        if uploaded_file:
            try:
                df_upload = pd.read_excel(uploaded_file)
                st.success(f"✅ File preview (first 10 rows) - Total rows: {len(df_upload)}")
                st.dataframe(df_upload.head(10), use_container_width=True)
                
                # Summary stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Records", len(df_upload))
                with col2:
                    st.metric("Total Participants", df_upload['Participants'].sum())
                with col3:
                    if 'Satisfaction' in df_upload.columns:
                        st.metric("Avg Satisfaction", f"{df_upload['Satisfaction'].mean():.2f}/5")
                
                if st.button("✅ Confirm & Load"):
                    st.session_state.uploaded_center_data = df_upload
                    st.success("Data loaded successfully!")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# ============================================================================
# RUN FUNCTION (Call this from main app.py)
# ============================================================================

if __name__ == "__main__":
    render_center_database()
