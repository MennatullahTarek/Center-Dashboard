"""
STAKEHOLDER DASHBOARDS - MAIN APPLICATION (UPDATED)
Multi-dashboard platform for MAC centers with programs database
Designed for 17 MAC/ICCO centres
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from center_database_v2 import render_center_database

# ============================================================================
# PAGE CONFIGURATION & THEME
# ============================================================================
st.set_page_config(
    page_title="MAC Stakeholder Dashboards",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f3a93;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d5aa3;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
st.sidebar.title("📊 MAC Dashboards")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "🏠 Main",
        "📈 All Centers Summary",
        "🏛️ Center Database",
        "🌙 All Ramadan Summary",
        "📚 Ramadan Database",
        "🎯 OKR & Strategic Alignment"
    ],
    key="page_selector"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Dashboard Version:** 2.0.0")
st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.sidebar.markdown("**System:** Programs Database")
st.sidebar.markdown("**Centers:** 17 MAC/ICCO")
st.sidebar.markdown("---")

# Clear cache option
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.success("✅ Data refreshed!")

# ============================================================================
# PAGE 1: MAIN
# ============================================================================
if page == "🏠 Main":
    st.markdown('<div class="main-header">📊 MAC Stakeholder Dashboards</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Platform Overview
        
        Comprehensive dashboard suite for MAC (Muslim Association of Canada) and ICCO (Islamic Community 
        Centre of Ontario) to track programs, activities, and centre engagement across 17 locations.
        
        #### ✨ Key Features
        
        - **📊 Programs Database Analytics** - Track all programs across 17 centres
        - **👥 Participant Tracking** - Monitor engagement and participation
        - **🎯 Target Audience Analysis** - Segment programs by audience groups
        - **📈 Performance Metrics** - KPIs and trend analysis
        - **📥 Easy Data Upload** - Upload Excel files for instant analytics
        - **☁️ Cloud Deployment** - Hosted on Streamlit Cloud
        
        #### 📑 Available Dashboards
        
        1. **🏛️ Center Database** ← **START HERE** - Full programs analytics by centre
        2. **📈 All Centers Summary** - Aggregate view across all 17 centres
        3. **🌙 All Ramadan Summary** - Ramadan campaign tracking
        4. **📚 Ramadan Database** - Detailed Ramadan analytics
        5. **🎯 OKR & Strategic Alignment** - Strategic objectives tracking
        
        #### 🚀 Quick Start (2 Minutes)
        
        1. **Click** 🏛️ Center Database in the sidebar
        2. **Select** your centre from the dropdown
        3. **View** all programs, participants, and analytics
        4. **Export** data as CSV for reports
        
        #### 📊 What You Can See
        
        - **Program Distribution** - Most common programs
        - **Participant Trends** - Participation over time
        - **Target Audiences** - Who programs are for
        - **Satisfaction Scores** - Program quality ratings
        - **Raw Data** - Full details with filtering
        
        #### 💾 Upload Your Data
        
        Go to Center Database → Upload tab to add/update your programs database.
        """)
    
    with col2:
        st.info("""
        ### 📌 System Info
        
        - **Total Centers:** 17 MAC/ICCO
        - **Data Source:** Excel files
        - **Update Mode:** Real-time upload
        - **Version:** 2.0.0
        
        ### 🎯 Supported Centres
        
        - ICCO (Main)
        - Mississauga
        - Toronto
        - Brampton
        - Ajax
        - Markham
        - Richmond Hill
        - Scarborough
        - Etobicoke
        - North York
        - Vaughan
        - Oshawa
        - Hamilton
        - Oakville
        - Burlington
        - Milton
        - Guelph
        
        ### 💡 Pro Tips
        
        ✓ Use centre dropdown to filter  
        ✓ Use filters to refine data  
        ✓ Download CSV for Excel  
        ✓ Refresh data when updated  
        ✓ Check raw data tab for details
        """)
    
    st.markdown("---")
    
    # Features showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🏛️ Centre Database
        
        Complete programs analytics for each centre with:
        - Program distribution
        - Participant numbers
        - Target audience breakdown
        - Satisfaction ratings
        """)
    
    with col2:
        st.markdown("""
        ### 📈 National View
        
        Aggregate analytics across all centres:
        - Top programs nationally
        - Total participants
        - Most served audiences
        - Trend analysis
        """)
    
    with col3:
        st.markdown("""
        ### 🌙 Ramadan Focus
        
        Dedicated Ramadan tracking:
        - Campaign performance
        - Donor analytics
        - Event attendance
        - Impact metrics
        """)
    
    st.markdown("---")
    st.markdown("""
    ### 📖 Getting Started
    
    **Step 1:** Click **🏛️ Center Database** in sidebar  
    **Step 2:** Select your centre name from dropdown  
    **Step 3:** View interactive charts and analytics  
    **Step 4:** Use Raw Data tab to filter and export  
    
    **For support:** Check README.md in project files
    """)

# ============================================================================
# PAGE 2: ALL CENTERS SUMMARY
# ============================================================================
elif page == "📈 All Centers Summary":
    st.markdown('<div class="main-header">📈 All Centers Summary Dashboard</div>', unsafe_allow_html=True)
    
    st.info("🔄 This dashboard is under development. National-level centre aggregation coming soon.")
    
    st.markdown("""
    ### 📊 Planned Features
    
    - Comparison across all 17 centres
    - Top programs nationally
    - Participant statistics
    - Target audience reach
    - Geographic distribution
    - Performance benchmarking
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Centers", "17", "MAC/ICCO")
    with col2:
        st.metric("Total Programs", "—", "Pending data")
    with col3:
        st.metric("Total Participants", "—", "Pending data")

# ============================================================================
# PAGE 3: CENTER DATABASE (FUNCTIONAL)
# ============================================================================
elif page == "🏛️ Center Database":
    render_center_database()

# ============================================================================
# PAGE 4: ALL RAMADAN SUMMARY
# ============================================================================
elif page == "🌙 All Ramadan Summary":
    st.markdown('<div class="main-header">🌙 All Ramadan Summary Dashboard</div>', unsafe_allow_html=True)
    
    st.info("🔄 This dashboard is under development. National Ramadan campaign aggregation coming soon.")
    
    st.markdown("""
    ### 📊 Planned Features
    
    - Donation tracking across all centres
    - Campaign reach and engagement
    - Donor demographics
    - Year-over-year comparisons
    - Regional performance
    - Impact metrics
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Donations", "—", "Pending data")
    with col2:
        st.metric("Campaign Reach", "—", "Pending data")
    with col3:
        st.metric("Engagement Rate", "—", "Pending data")

# ============================================================================
# PAGE 5: RAMADAN DATABASE
# ============================================================================
elif page == "📚 Ramadan Database":
    st.markdown('<div class="main-header">📚 Ramadan Database</div>', unsafe_allow_html=True)
    
    st.info("🔄 This dashboard is under development. Detailed Ramadan analytics coming soon.")
    
    tab1, tab2 = st.tabs(["📊 Analytics", "💾 Data Management"])
    
    with tab1:
        st.markdown("### 📊 Ramadan Campaign Performance")
        st.markdown("""
        **Planned Analytics:**
        - Daily donation tracking
        - Donor demographics and retention
        - Campaign effectiveness metrics
        - Channel performance (Online, In-person, etc.)
        - Program attendance during Ramadan
        """)
    
    with tab2:
        st.markdown("### 💾 Upload Ramadan Data")
        st.markdown("Upload Excel file with Ramadan campaign data.")
        
        uploaded_file = st.file_uploader(
            "Choose Ramadan Excel file",
            type=["xlsx", "xls"],
            key="ramadan_upload"
        )
        
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file)
                st.success(f"✅ File preview - Total rows: {len(df)}")
                st.dataframe(df.head(10), use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============================================================================
# PAGE 6: OKR & STRATEGIC ALIGNMENT
# ============================================================================
elif page == "🎯 OKR & Strategic Alignment":
    st.markdown('<div class="main-header">🎯 OKR & Strategic Alignment</div>', unsafe_allow_html=True)
    
    st.info("🔄 This dashboard is under development. Strategic objectives and KR tracking coming soon.")
    
    st.markdown("""
    ### 📌 Strategic Framework
    
    This dashboard will track:
    - **Objectives** - High-level organizational goals
    - **Key Results (KRs)** - Measurable outcomes
    - **Initiatives** - Programs supporting OKRs
    - **Progress Tracking** - Real-time status updates
    - **Risk Assessment** - Potential blockers
    - **Cross-functional Alignment** - Centre coordination
    
    #### OKR Structure by Quarter
    
    - Q1: January - March (Ramadan Focus)
    - Q2: April - June (Summer Programs)
    - Q3: July - September (Youth Programs)
    - Q4: October - December (Year-End Reviews)
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active OKRs", "—", "Pending configuration")
    with col2:
        st.metric("Average Progress", "—%", "Pending configuration")
    with col3:
        st.metric("On-Track KRs", "—%", "Pending configuration")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
    <small>
    MAC Stakeholder Dashboards v2.0.0 | © 2025 Muslim Association of Canada | 
    Built with Streamlit
    </small>
    </div>
    """, unsafe_allow_html=True)
