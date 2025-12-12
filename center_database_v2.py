"""
CENTER DATABASE MODULE - PROGRAMS ANALYTICS
Designed for MAC ICCO Programs Database Structure
Supports 17 centres with dynamic centre selection
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# ============================================================================
# CONFIGURATION
# ============================================================================

# Path to your master Excel file with all centres and programs
DATA_PATH = "data/MAC_ICCO_Programs_Database_2025.xlsx"

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================

@st.cache_data
def load_all_centers_data():
    """
    Load all centres data from Excel file.
    Works with multiple sheets or a single master sheet.
    Automatically detects and normalizes column names.
    """
    try:
        # Try to read the Excel file
        df = pd.read_excel(DATA_PATH, sheet_name=0)  # Read first sheet
        
        # Normalize column names (handle variations)
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
        
        # Create Centre column if not exists
        if "Location Name" in df.columns:
            df["Centre"] = df["Location Name"]
        elif "Location" in df.columns:
            df["Centre"] = df["Location"]
        elif "Center" in df.columns:
            df["Centre"] = df["Center"]
        else:
            # Fallback: use first text column as centre
            df["Centre"] = "ICCO"
        
        # Create Program column if not exists
        if "Program Name" in df.columns:
            df["Program"] = df["Program Name"]
        elif "Course Name" in df.columns:
            df["Program"] = df["Course Name"]
        elif "Program" not in df.columns:
            df["Program"] = "Program"
        
        # Handle dates
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        
        # Handle participants (if not exists, count as 1 per row/program)
        if "Participants" not in df.columns:
            df["Participants"] = 1
        else:
            df["Participants"] = pd.to_numeric(df["Participants"], errors="coerce").fillna(1)
        
        # Handle satisfaction/rating (if not exists, set neutral)
        if "Satisfaction" not in df.columns:
            df["Satisfaction"] = 4  # Neutral default (1-5 scale)
        else:
            df["Satisfaction"] = pd.to_numeric(df["Satisfaction"], errors="coerce").fillna(4)
        
        # Handle target audience/category
        if "Target Audience" in df.columns:
            df["Category"] = df["Target Audience"]
        elif "Category" not in df.columns:
            df["Category"] = "General"
        
        # Remove completely empty rows
        df = df.dropna(how="all")
        
        st.success(f"✅ Loaded {len(df)} programs from {len(df['Centre'].unique())} centres")
        
        return df
    
    except FileNotFoundError:
        st.error(f"❌ File not found: {DATA_PATH}")
        st.info("📌 Place your Excel file in: data/MAC_ICCO_Programs_Database_2025.xlsx")
        return pd.DataFrame()
    
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        return pd.DataFrame()


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def calculate_metrics(df):
    """Calculate key metrics for selected centre"""
    if df.empty:
        return {
            'total_programs': 0,
            'total_participants': 0,
            'avg_satisfaction': 0,
            'unique_programs': 0,
            'target_audiences': 0,
        }
    
    return {
        'total_programs': len(df),
        'total_participants': int(df['Participants'].sum()),
        'avg_satisfaction': df['Satisfaction'].mean(),
        'unique_programs': df['Program'].nunique(),
        'target_audiences': df['Category'].nunique(),
    }


def create_program_distribution(df):
    """Create program type distribution chart"""
    if df.empty:
        return go.Figure()
    
    program_counts = df['Program'].value_counts().head(10).reset_index()
    program_counts.columns = ['Program', 'Count']
    
    fig = go.Figure(data=[
        go.Bar(
            x=program_counts['Count'],
            y=program_counts['Program'],
            orientation='h',
            marker=dict(color='#667eea'),
            text=program_counts['Count'],
            textposition='outside',
        )
    ])
    
    fig.update_layout(
        title="Top 10 Programs by Frequency",
        xaxis_title="Number of Entries",
        yaxis_title="Program",
        hovermode='y unified',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig


def create_target_audience_breakdown(df):
    """Create target audience distribution pie chart"""
    if df.empty:
        return go.Figure()
    
    audience_counts = df['Category'].value_counts()
    
    colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#6bcf7f', '#ffa726']
    
    fig = go.Figure(data=[go.Pie(
        labels=audience_counts.index,
        values=audience_counts.values,
        hole=0.3,
        marker=dict(colors=colors[:len(audience_counts)])
    )])
    
    fig.update_layout(
        title="Target Audience Distribution",
        height=400,
        showlegend=True,
    )
    
    return fig


def create_participants_trend(df):
    """Create participants trend over time (if dates available)"""
    if df.empty or 'Date' not in df.columns:
        return go.Figure()
    
    df_with_dates = df.dropna(subset=['Date'])
    
    if df_with_dates.empty:
        return go.Figure()
    
    df_with_dates = df_with_dates.copy()
    df_with_dates['Month'] = df_with_dates['Date'].dt.to_period('M')
    
    trend = df_with_dates.groupby('Month')['Participants'].sum().reset_index()
    trend['Month'] = trend['Month'].astype(str)
    
    fig = px.line(
        trend,
        x='Month',
        y='Participants',
        markers=True,
        title='Participants Trend Over Time',
        line_shape='spline'
    )
    
    fig.update_traces(line=dict(color='#667eea', width=3), marker=dict(size=8))
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig


def create_satisfaction_distribution(df):
    """Create satisfaction score distribution"""
    if df.empty:
        return go.Figure()
    
    satisfaction_counts = df['Satisfaction'].value_counts().sort_index()
    
    satisfaction_labels = {
        1: 'Very Poor',
        2: 'Poor',
        3: 'Neutral',
        4: 'Good',
        5: 'Excellent'
    }
    
    colors_map = {
        1: '#ff6b6b',
        2: '#ffa726',
        3: '#ffd93d',
        4: '#6bcf7f',
        5: '#4ecdc4'
    }
    
    x_labels = [satisfaction_labels.get(i, f'Score {i}') for i in satisfaction_counts.index]
    
    fig = go.Figure(data=[
        go.Bar(
            x=x_labels,
            y=satisfaction_counts.values,
            marker=dict(
                color=[colors_map.get(i, '#667eea') for i in satisfaction_counts.index],
            ),
            text=satisfaction_counts.values,
            textposition='outside',
        )
    ])
    
    fig.update_layout(
        title="Satisfaction Score Distribution",
        xaxis_title="Satisfaction Level",
        yaxis_title="Count",
        hovermode='x unified',
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig


def create_program_participants(df):
    """Create participants by program chart"""
    if df.empty:
        return go.Figure()
    
    program_data = df.groupby('Program').agg({
        'Participants': 'sum',
        'Satisfaction': 'mean'
    }).reset_index().sort_values('Participants', ascending=False).head(10)
    
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
        title="Top 10 Programs: Participants & Satisfaction",
        xaxis_title="Program",
        yaxis=dict(title="Total Participants", side='left'),
        yaxis2=dict(title="Avg Satisfaction (1-5)", overlaying='y', side='right'),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig


# ============================================================================
# UI RENDERER
# ============================================================================

def render_center_database():
    """Main Centre Database Dashboard Renderer"""
    
    st.markdown('<div class="main-header">🏛️ Center Database Dashboard</div>', unsafe_allow_html=True)
    
    # Load all data
    df_all = load_all_centers_data()
    
    if df_all.empty:
        st.warning("No data available. Please upload your MAC Programs Excel file.")
        return
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Analytics", "📋 Raw Data", "💾 Data Upload"])
    
    # ========== TAB 1: DASHBOARD ==========
    with tab1:
        # Centre selection
        col_select, col_period = st.columns([2, 1])
        
        with col_select:
            centre_list = sorted(df_all['Centre'].dropna().unique())
            selected_centre = st.selectbox(
                "🏛️ Select Centre",
                centre_list,
                key="centre_selector"
            )
        
        with col_period:
            period = st.selectbox(
                "📅 Filter By",
                ["All Time", "Target Audience"],
                key="period_selector"
            )
        
        # Filter data for selected centre
        df_centre = df_all[df_all['Centre'] == selected_centre].copy()
        
        # Additional filter by target audience if selected
        if period != "All Time":
            audiences = sorted(df_centre['Category'].unique())
            if audiences:
                selected_audience = st.selectbox("Target Audience", audiences)
                df_centre = df_centre[df_centre['Category'] == selected_audience]
        
        st.markdown("---")
        
        # Calculate metrics
        metrics = calculate_metrics(df_centre)
        
        # Metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="📊 Total Programs",
                value=f"{metrics['total_programs']:,}",
                delta="entries"
            )
        
        with col2:
            st.metric(
                label="👥 Total Participants",
                value=f"{metrics['total_participants']:,}",
                delta="people"
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
                label="🎯 Unique Programs",
                value=f"{metrics['unique_programs']:,}",
                delta="types"
            )
        
        with col5:
            st.metric(
                label="👨‍👩‍👧‍👦 Audiences",
                value=f"{metrics['target_audiences']:,}",
                delta="groups"
            )
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_program_distribution(df_centre), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_target_audience_breakdown(df_centre), use_container_width=True)
        
        st.plotly_chart(create_participants_trend(df_centre), use_container_width=True)
        st.plotly_chart(create_program_participants(df_centre), use_container_width=True)
    
    # ========== TAB 2: ANALYTICS ==========
    with tab2:
        st.subheader("📈 Deep Analytics")
        
        df_centre = df_all[df_all['Centre'] == selected_centre].copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Program Performance")
            program_perf = df_centre.groupby('Program').agg({
                'Participants': 'sum',
                'Satisfaction': 'mean'
            }).sort_values('Participants', ascending=False).head(10)
            
            st.dataframe(
                program_perf.round(2),
                use_container_width=True,
                column_config={
                    "Participants": st.column_config.NumberColumn("Participants"),
                    "Satisfaction": st.column_config.NumberColumn("Avg Satisfaction", format="%.2f"),
                }
            )
        
        with col2:
            st.markdown("#### Target Audience Performance")
            audience_perf = df_centre.groupby('Category').agg({
                'Participants': 'sum',
                'Satisfaction': 'mean'
            }).sort_values('Participants', ascending=False)
            
            st.dataframe(
                audience_perf.round(2),
                use_container_width=True,
            )
        
        st.markdown("---")
        st.plotly_chart(create_satisfaction_distribution(df_centre), use_container_width=True)
    
    # ========== TAB 3: RAW DATA ==========
    with tab3:
        st.subheader("📋 Raw Data View")
        
        df_centre = df_all[df_all['Centre'] == selected_centre].copy()
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            program_filter = st.multiselect(
                "Filter by Program",
                df_centre['Program'].unique(),
                default=df_centre['Program'].unique()[:5] if len(df_centre) > 0 else []
            )
        
        with col2:
            category_filter = st.multiselect(
                "Filter by Target Audience",
                df_centre['Category'].unique(),
                default=df_centre['Category'].unique()
            )
        
        with col3:
            satisfaction_filter = st.slider(
                "Min Satisfaction",
                1.0, 5.0, 1.0
            )
        
        # Apply filters
        filtered_df = df_centre[
            (df_centre['Program'].isin(program_filter)) &
            (df_centre['Category'].isin(category_filter)) &
            (df_centre['Satisfaction'] >= satisfaction_filter)
        ]
        
        st.dataframe(
            filtered_df.sort_values('Date', ascending=False) if 'Date' in filtered_df.columns else filtered_df,
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name=f"{selected_centre}_programs_data.csv",
            mime="text/csv"
        )
    
    # ========== TAB 4: UPLOAD ==========
    with tab4:
        st.subheader("💾 Upload MAC Programs Database")
        
        st.markdown("""
        Upload your MAC Centers Excel file. Expected structure:
        
        **Required Columns:**
        - **Location / Location Name** - Centre name (will be auto-detected)
        - **Program Name / Course Name** - Program/Activity name
        - **Participants** - Number of participants (optional, defaults to 1)
        - **Target Audience** - Target group (optional)
        - **Date** - Program date (optional, for trend analysis)
        - **Satisfaction** - Satisfaction rating 1-5 (optional)
        
        **Supported Sheets:**
        - Regular Programs
        - Courses & Classes
        - Youth Programs
        - Special Events
        - (Any sheet with the above columns)
        """)
        
        uploaded_file = st.file_uploader(
            "Choose Excel file",
            type=["xlsx", "xls"],
            key="programs_upload"
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
                    if 'Participants' in df_upload.columns:
                        st.metric("Total Participants", df_upload['Participants'].sum())
                with col3:
                    if 'Satisfaction' in df_upload.columns:
                        st.metric("Avg Satisfaction", f"{df_upload['Satisfaction'].mean():.2f}/5")
                
                if st.button("✅ Use This Data"):
                    # Save to data folder
                    os.makedirs("data", exist_ok=True)
                    output_path = "data/MAC_ICCO_Programs_Database_2025.xlsx"
                    df_upload.to_excel(output_path, index=False)
                    st.success(f"✅ Data saved to {output_path}")
                    st.info("Refresh the page to see updated data")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# ============================================================================
# STANDALONE EXECUTION
# ============================================================================

if __name__ == "__main__":
    import os
    import streamlit as st
    
    st.set_page_config(page_title="Center Database", layout="wide")
    render_center_database()
