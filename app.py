import streamlit as st
import pandas as pd
from PIL import Image
import os

# Set page configuration
st.set_page_config(
    page_title="Customer Feedback Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 500;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .header-section {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and header
st.markdown("""
    <div class="header-section">
        <h1>📊 Customer Feedback Analytics Dashboard</h1>
        <p>Comprehensive analysis of customer feedback, sentiment distribution, and business insights</p>
    </div>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    analysis_df = pd.read_csv("analysis_results.csv")
    with open("overall_report.txt", "r") as f:
        report_text = f.read()
    sentiment_img = Image.open("sentiment_distribution.png")
    return analysis_df, report_text, sentiment_img

analysis_df, report_text, sentiment_img = load_data()

# SECTION 1: Executive Summary
with st.expander("📋 Executive Summary", expanded=True):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Sentiment Distribution")
        st.image(sentiment_img, use_container_width=True)
    
    with col2:
        st.subheader("Key Metrics")
        
        # Calculate metrics
        total_feedback = len(analysis_df)
        positive_count = len(analysis_df[analysis_df["sentiment"] == "Positive"])
        negative_count = len(analysis_df[analysis_df["sentiment"] == "Negative"])
        neutral_count = len(analysis_df[analysis_df["sentiment"] == "Neutral"])
        
        positive_pct = (positive_count / total_feedback * 100) if total_feedback > 0 else 0
        negative_pct = (negative_count / total_feedback * 100) if total_feedback > 0 else 0
        neutral_pct = (neutral_count / total_feedback * 100) if total_feedback > 0 else 0
        
        st.metric("Total Feedback", total_feedback)
        st.metric("Positive", f"{positive_count} ({positive_pct:.1f}%)", delta="✓")
        st.metric("Negative", f"{negative_count} ({negative_pct:.1f}%)", delta="✗")
        st.metric("Neutral", f"{neutral_count} ({neutral_pct:.1f}%)")

st.divider()

# SECTION 2: Detailed Business Report
with st.expander("📝 Detailed Business Report", expanded=True):
    report_lines = report_text.split("\n")
    for line in report_lines:
        if line.startswith("#"):
            if line.startswith("##"):
                st.subheader(line.replace("## ", ""))
            else:
                st.title(line.replace("# ", ""))
        elif line.startswith("-"):
            st.write(line)
        elif line.strip():
            st.write(line)
    
    # Add a download button for the full report
    st.download_button(
        label="📥 Download Full Report",
        data=report_text,
        file_name="customer_feedback_report.txt",
        mime="text/plain"
    )

st.divider()

# SECTION 3: Sentiment Distribution Analysis
with st.expander("📊 Sentiment Distribution Analysis", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(sentiment_img, use_container_width=True)
    
    with col2:
        st.subheader("Sentiment Breakdown")
        sentiment_counts = analysis_df["sentiment"].value_counts()
        st.bar_chart(sentiment_counts)
        
        st.subheader("Statistics")
        for sentiment, count in sentiment_counts.items():
            percentage = (count / len(analysis_df)) * 100
            st.write(f"**{sentiment}:** {count} ({percentage:.1f}%)")

st.divider()

# SECTION 4: Raw Data
with st.expander("🗂️ Raw Analysis Data", expanded=False):
    # Display dataframe with better formatting
    st.subheader("Analysis Results Table")
    st.dataframe(analysis_df, use_container_width=True, height=400)
    
    # Sentiment filter
    st.subheader("Filter by Sentiment")
    sentiment_filter = st.multiselect(
        "Select sentiments to display:",
        options=analysis_df["sentiment"].unique(),
        default=analysis_df["sentiment"].unique(),
        key="sentiment_filter"
    )
    
    filtered_df = analysis_df[analysis_df["sentiment"].isin(sentiment_filter)]
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download button for CSV
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="analysis_results_filtered.csv",
        mime="text/csv"
    )

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #999; font-size: 0.9rem;'>
        <p>Customer Feedback Analytics Dashboard | Data-Driven Insights for Business Growth</p>
    </div>
    """, unsafe_allow_html=True)
