# app.py
import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="AI Data Analyzer Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for advanced styling
# Custom CSS for advanced styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #2c3e50;
        margin-bottom: 1.2rem;
        font-weight: 600;
        border-left: 5px solid #667eea;
        padding-left: 12px;
        background: rgba(255,255,255,0.7);
        padding: 12px;
        border-radius: 0 8px 8px 0;
    }
    
    .card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.8rem;
        border-radius: 12px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-top: 4px solid #667eea;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(102, 126, 234, 0.4);
    }
    
    .success-box {
        background: linear-gradient(to right, #d4edda, #c3e6cb);
        color: #155724;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin-bottom: 1rem;
        box-shadow: 0 3px 6px rgba(0,0,0,0.05);
    }
    
    .warning-box {
        background: linear-gradient(to right, #fff3cd, #ffeaa7);
        color: #856404;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin-bottom: 1rem;
        box-shadow: 0 3px 6px rgba(0,0,0,0.05);
    }
    
    .info-box {
        background: linear-gradient(to right, #d1ecf1, #bee5eb);
        color: #0c5460;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 5px solid #17a2b8;
        margin-bottom: 1rem;
        box-shadow: 0 3px 6px rgba(0,0,0,0.05);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.7rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4b6cb7 0%, #182848 100%);
        color: white;
    }
    
    .css-1d391kg, .css-12oz5g7 {
        padding: 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
    }
    
    /* Sidebar text color fixes - changed to black for visibility */
    section[data-testid="stSidebar"] div:not(.stButton) {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] p {
        color: #000000 !important;
        font-weight: 500;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5,
    section[data-testid="stSidebar"] h6 {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] label {
        color: #000000 !important;
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] .stCheckbox label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #000000 !important;
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] .stCheckbox span,
    section[data-testid="stSidebar"] .stSelectbox span,
    section[data-testid="stSidebar"] .stSlider span {
        color: #000000 !important;
    }
    
    /* Change sidebar background to lighter color for black text */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #a7bfe8 0%, #a7bfe8 100%) !important;
    }
    
    /* File uploader text color */
    section[data-testid="stSidebar"] .stFileUploader label {
        color: #000000 !important;
        font-weight: 600;
    }
    
    .tab-container {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(5px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .feature-pill {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .data-preview {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        background: white;
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        backdrop-filter: blur(5px);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Streamlit element specific styling */
    .stDataFrame {
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox, .stSlider, .stTextInput {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header with enhanced design
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">📊 AI Data Analyzer Pro</h1>', unsafe_allow_html=True)
        st.markdown("### Advanced Insights with Automated Visualization and Machine Learning")
    
    # Sidebar with improved design
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png" width="100" style="margin-bottom: 1rem;">
            <h2 style="color: white;">AI Data Analyzer</h2>
            <p style="color: rgba(255,255,255,0.8);">Upload your data and get instant insights</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "📁 Choose a file", 
            type=['csv', 'xlsx', 'xls'],
            help="Supported formats: CSV, Excel"
        )
        
        # Advanced options
        st.markdown("---")
        st.markdown("### ⚙️ Analysis Options")
        
        analysis_depth = st.select_slider(
            "Analysis Depth",
            options=["Basic", "Standard", "Comprehensive"]
        )
        
        auto_visualize = st.checkbox("Auto Visualize All Charts", value=True)
        show_correlations = st.checkbox("Show Correlation Matrix", value=True)
        show_outliers = st.checkbox("Detect Outliers", value=True)
        
        if uploaded_file:
            st.success("File uploaded successfully!")
            if st.button("🔄 Analyze Data", use_container_width=True):
                st.rerun()

    # Main content
    if uploaded_file is not None:
        try:
            # Read file with progress indicator
            with st.spinner("Loading data..."):
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
            
            # Display success message with animation
            st.success(f"✅ Successfully loaded data with {df.shape[0]:,} rows and {df.shape[1]} columns")
            
            # Analysis with tabs for better organization
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Overview", "📊 Visualizations", "🧠 Insights", "📈 Advanced", "📄 Report"])
            
            with tab1:
                overview_tab(df, uploaded_file.name)
            
            with tab2:
                visualization_tab(df, auto_visualize, show_correlations)
            
            with tab3:
                insights_tab(df, show_outliers)
            
            with tab4:
                advanced_analysis_tab(df)
            
            with tab5:
                report_tab(df, uploaded_file.name)
            
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    else:
        # Show welcome message and features
        st.markdown("""
        <div style="text-align: center; margin-bottom: 3rem;">
            <h2>Transform Your Data into Actionable Insights</h2>
            <p>Powerful automated analysis with machine learning capabilities</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="card">
                <h3>📈 Advanced Analytics</h3>
                <p>Get comprehensive statistical analysis with detailed metrics and distributions</p>
                <div>
                    <span class="feature-pill">Trend Analysis</span>
                    <span class="feature-pill">Correlation</span>
                    <span class="feature-pill">Outlier Detection</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card">
                <h3>📊 Interactive Visualizations</h3>
                <p>Automatically generated interactive charts and graphs with export capabilities</p>
                <div>
                    <span class="feature-pill">Histograms</span>
                    <span class="feature-pill">Heatmaps</span>
                    <span class="feature-pill">Scatter Plots</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="card">
                <h3>🤖 ML-Powered Insights</h3>
                <p>Receive actionable recommendations powered by machine learning algorithms</p>
                <div>
                    <span class="feature-pill">Pattern Recognition</span>
                    <span class="feature-pill">Predictive Insights</span>
                    <span class="feature-pill">Anomaly Detection</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Usage instructions
        st.markdown("""
        <div class="info-box">
            <h4>🚀 How to get started:</h4>
            <ol>
                <li>Upload your CSV or Excel file using the sidebar</li>
                <li>Customize your analysis using the options panel</li>
                <li>Explore the insights across multiple tabs</li>
                <li>Download comprehensive reports</li>
                <li>Implement the AI-powered suggestions</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample data section
        st.markdown("---")
        st.markdown("### 🧪 Try with sample data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Generate Sample Data", use_container_width=True):
                sample_data = create_sample_data()
                st.session_state.sample_data = sample_data
                st.rerun()
        
        if 'sample_data' in st.session_state:
            st.dataframe(st.session_state.sample_data, use_container_width=True)
            if st.button("Analyze Sample Data", use_container_width=True):
                uploaded_file = io.BytesIO()
                st.session_state.sample_data.to_csv(uploaded_file, index=False)
                uploaded_file.name = "sample_data.csv"
                st.session_state.uploaded_file = uploaded_file
                st.rerun()

def overview_tab(df, filename):
    """Data overview tab"""
    st.markdown('<h2 class="sub-header">Data Overview</h2>', unsafe_allow_html=True)
    
    # Metrics in a grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Rows</h3>
            <h2>{df.shape[0]:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Columns</h3>
            <h2>{df.shape[1]}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        missing_values = df.isnull().sum().sum()
        missing_percent = (missing_values / df.size) * 100
        st.markdown(f"""
        <div class="metric-card">
            <h3>Missing Values</h3>
            <h2>{missing_values:,}</h2>
            <p>{missing_percent:.2f}% of data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        duplicates = df.duplicated().sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>Duplicates</h3>
            <h2>{duplicates}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Data preview with style
    st.markdown("#### 🔍 Data Preview")
    st.dataframe(df.head(10), use_container_width=True, height=300)
    
    # Column information with expander
    with st.expander("📊 Detailed Column Information", expanded=True):
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes.values,
            'Missing Values': df.isnull().sum().values,
            'Missing %': [(df[col].isnull().sum() / len(df)) * 100 for col in df.columns],
            'Unique Values': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)
    
    # Data quality assessment
    st.markdown("#### 🧰 Data Quality Assessment")
    
    completeness_score = 100 - (df.isnull().sum().sum() / df.size) * 100
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"**Data Completeness Score: {completeness_score:.2f}%**")
        st.progress(completeness_score / 100)
    
    with col2:
        st.metric("Uniqueness Score", f"{(1 - (df.duplicated().sum() / len(df))) * 100:.2f}%")

def visualization_tab(df, auto_visualize, show_correlations):
    """Visualization tab with automatic chart generation"""
    st.markdown('<h2 class="sub-header">Data Visualizations</h2>', unsafe_allow_html=True)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    if auto_visualize:
        # Automatic visualization of all possible charts
        st.info("🔍 Automatically generating all possible visualizations for your data...")
        
        # 1. Numeric columns distributions
        if numeric_cols:
            st.markdown("#### 📊 Distributions of Numeric Variables")
            cols = st.columns(2)
            for i, col in enumerate(numeric_cols):
                with cols[i % 2]:
                    with st.expander(f"Distribution of {col}", expanded=True):
                        fig = px.histogram(df, x=col, title=f'Distribution of {col}', marginal="box")
                        st.plotly_chart(fig, use_container_width=True)
        
        # 2. Categorical columns distributions
        if categorical_cols:
            st.markdown("#### 📈 Categorical Variables Distribution")
            cols = st.columns(2)
            for i, col in enumerate(categorical_cols):
                with cols[i % 2]:
                    with st.expander(f"Value counts for {col}", expanded=True):
                        value_counts = df[col].value_counts().head(10)
                        fig = px.bar(x=value_counts.index, y=value_counts.values, 
                                    title=f'Top 10 Values for {col}')
                        st.plotly_chart(fig, use_container_width=True)
        
        # 3. Correlation matrix for numeric columns
        if show_correlations and len(numeric_cols) > 1:
            st.markdown("#### 🔗 Correlation Matrix")
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(corr_matrix, title='Correlation Heatmap', 
                           aspect="auto", color_continuous_scale='RdBu_r')
            st.plotly_chart(fig, use_container_width=True)
        
        # 4. Scatter plots for all numeric column pairs
        if len(numeric_cols) >= 2:
            st.markdown("#### 📍 Scatter Plots (Numeric Variables)")
            num_pairs = min(6, len(numeric_cols))  # Limit to 6 plots to avoid overload
            cols = st.columns(2)
            pair_count = 0
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    if pair_count >= num_pairs:
                        break
                    with cols[pair_count % 2]:
                        col1, col2 = numeric_cols[i], numeric_cols[j]
                        with st.expander(f"{col1} vs {col2}", expanded=True):
                            fig = px.scatter(df, x=col1, y=col2, title=f'{col1} vs {col2}', 
                                           trendline="lowess")
                            st.plotly_chart(fig, use_container_width=True)
                            pair_count += 1
                    if pair_count >= num_pairs:
                        break
        
        # 5. Time series plots if date columns exist
        if date_cols and numeric_cols:
            st.markdown("#### 📅 Time Series Analysis")
            date_col = date_cols[0]  # Use first date column
            cols = st.columns(2)
            for i, num_col in enumerate(numeric_cols[:4]):  # Limit to 4 time series plots
                with cols[i % 2]:
                    with st.expander(f"{num_col} over Time", expanded=True):
                        time_df = df[[date_col, num_col]].dropna()
                        if not time_df.empty:
                            fig = px.line(time_df, x=date_col, y=num_col, title=f'{num_col} over Time')
                            st.plotly_chart(fig, use_container_width=True)
        
        # 6. Box plots for numeric vs categorical
        if numeric_cols and categorical_cols:
            st.markdown("#### 📦 Box Plots (Numeric vs Categorical)")
            num_plots = min(4, len(numeric_cols) * len(categorical_cols))
            cols = st.columns(2)
            plot_count = 0
            for num_col in numeric_cols:
                for cat_col in categorical_cols:
                    if plot_count >= num_plots:
                        break
                    if df[cat_col].nunique() <= 10:  # Only if reasonable number of categories
                        with cols[plot_count % 2]:
                            with st.expander(f"{num_col} by {cat_col}", expanded=True):
                                fig = px.box(df, x=cat_col, y=num_col, title=f'{num_col} by {cat_col}')
                                st.plotly_chart(fig, use_container_width=True)
                                plot_count += 1
        
        # 7. Pie charts for categorical variables with few categories
        if categorical_cols:
            st.markdown("#### 🥧 Pie Charts (Categorical Variables)")
            cols = st.columns(2)
            pie_count = 0
            for cat_col in categorical_cols:
                if df[cat_col].nunique() <= 6 and df[cat_col].nunique() >= 2:  # Reasonable for pie chart
                    with cols[pie_count % 2]:
                        with st.expander(f"Distribution of {cat_col}", expanded=True):
                            value_counts = df[cat_col].value_counts()
                            fig = px.pie(values=value_counts.values, names=value_counts.index, 
                                        title=f'Distribution of {cat_col}')
                            st.plotly_chart(fig, use_container_width=True)
                            pie_count += 1
                    if pie_count >= 4:  # Limit to 4 pie charts
                        break
    
    else:
        # Manual chart selection (original functionality)
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Histogram", "Box Plot", "Scatter Plot", "Bar Chart", "Line Chart", "Heatmap"]
        )
        
        if chart_type == "Histogram" and numeric_cols:
            selected_col = st.selectbox("Select column:", numeric_cols)
            if selected_col:
                fig = px.histogram(df, x=selected_col, title=f'Distribution of {selected_col}',
                                  marginal="box", nbins=50)
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Box Plot" and numeric_cols:
            selected_col = st.selectbox("Select column:", numeric_cols)
            if selected_col:
                fig = px.box(df, y=selected_col, title=f'Box Plot of {selected_col}')
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Scatter Plot" and len(numeric_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("X-axis:", numeric_cols)
            with col2:
                y_col = st.selectbox("Y-axis:", numeric_cols)
            
            if x_col and y_col:
                color_col = st.selectbox("Color by (optional):", [None] + categorical_cols)
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col, 
                                title=f'{y_col} vs {x_col}', trendline="lowess")
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Bar Chart" and categorical_cols:
            selected_col = st.selectbox("Select column:", categorical_cols)
            if selected_col:
                value_counts = df[selected_col].value_counts().head(10)
                fig = px.bar(x=value_counts.index, y=value_counts.values, 
                             title=f'Top 10 Values for {selected_col}')
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Line Chart" and numeric_cols:
            if date_cols:
                date_col = st.selectbox("Select date column:", date_cols)
                value_col = st.selectbox("Select value column:", numeric_cols)
                
                if date_col and value_col:
                    fig = px.line(df, x=date_col, y=value_col, title=f'{value_col} over Time')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No datetime columns found for line chart. Try another visualization.")
        
        elif chart_type == "Heatmap" and show_correlations and len(numeric_cols) > 1:
            st.subheader("📊 Correlation Matrix")
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(corr_matrix, title='Correlation Heatmap', 
                           aspect="auto", color_continuous_scale='RdBu_r')
            st.plotly_chart(fig, use_container_width=True)

def insights_tab(df, show_outliers):
    """Insights and suggestions tab"""
    st.markdown('<h2 class="sub-header">AI-Powered Insights</h2>', unsafe_allow_html=True)
    
    suggestions = generate_insights(df, show_outliers)
    
    # Display suggestions in tabs
    tab1, tab2, tab3 = st.tabs(["🚀 Recommendations", "⚠️ Warnings", "ℹ️ Information"])
    
    with tab1:
        success_suggestions = [s for s in suggestions if s['type'] == 'success']
        if success_suggestions:
            for suggestion in success_suggestions:
                st.markdown(f'<div class="success-box">✅ {suggestion["message"]}</div>', unsafe_allow_html=True)
        else:
            st.info("No recommendations at this time.")
    
    with tab2:
        warning_suggestions = [s for s in suggestions if s['type'] == 'warning']
        if warning_suggestions:
            for suggestion in warning_suggestions:
                st.markdown(f'<div class="warning-box">⚠️ {suggestion["message"]}</div>', unsafe_allow_html=True)
        else:
            st.info("No critical issues found.")
    
    with tab3:
        info_suggestions = [s for s in suggestions if s['type'] == 'info']
        if info_suggestions:
            for suggestion in info_suggestions:
                st.markdown(f'<div class="info-box">ℹ️ {suggestion["message"]}</div>', unsafe_allow_html=True)
        else:
            st.info("No additional information.")

def advanced_analysis_tab(df):
    """Advanced analysis tab"""
    st.markdown('<h2 class="sub-header">Advanced Analysis</h2>', unsafe_allow_html=True)
    
    # Outlier detection
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        st.subheader("🔍 Outlier Detection")
        selected_col = st.selectbox("Select numeric column for outlier detection:", numeric_cols)
        
        if selected_col:
            # Calculate outliers using IQR method
            Q1 = df[selected_col].quantile(0.25)
            Q3 = df[selected_col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[selected_col] < lower_bound) | (df[selected_col] > upper_bound)]
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Lower Bound", f"{lower_bound:.2f}")
            col2.metric("Upper Bound", f"{upper_bound:.2f}")
            col3.metric("Outliers Found", len(outliers))
            
            if len(outliers) > 0:
                st.dataframe(outliers, use_container_width=True)
    
    # Time series analysis (if date columns exist)
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    if date_cols:
        st.subheader("📈 Time Series Analysis")
        date_col = st.selectbox("Select date column:", date_cols)
        value_col = st.selectbox("Select value column:", numeric_cols)
        
        if date_col and value_col:
            # Resample time series data
            resample_freq = st.selectbox("Resampling frequency:", 
                                        ["D", "W", "M", "Q", "Y"])
            
            try:
                time_series = df.set_index(date_col)[value_col]
                resampled = time_series.resample(resample_freq).mean()
                
                fig = px.line(resampled, title=f'{value_col} over Time ({resample_freq} average)')
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.warning("Could not process time series with selected parameters.")
    
    # Data transformation options
    st.subheader("🛠️ Data Transformation")
    
    transform_option = st.selectbox(
        "Select transformation:",
        ["None", "Normalize", "Standardize", "Log Transform"]
    )
    
    if transform_option != "None" and numeric_cols:
        col_to_transform = st.selectbox("Select column to transform:", numeric_cols)
        
        if st.button("Apply Transformation"):
            if transform_option == "Normalize":
                # Min-max normalization
                min_val = df[col_to_transform].min()
                max_val = df[col_to_transform].max()
                df[col_to_transform + "_normalized"] = (df[col_to_transform] - min_val) / (max_val - min_val)
                st.success(f"Normalized {col_to_transform} (0-1 range)")
                
            elif transform_option == "Standardize":
                # Z-score standardization
                mean_val = df[col_to_transform].mean()
                std_val = df[col_to_transform].std()
                df[col_to_transform + "_standardized"] = (df[col_to_transform] - mean_val) / std_val
                st.success(f"Standardized {col_to_transform} (mean=0, std=1)")
                
            elif transform_option == "Log Transform":
                # Log transformation
                if (df[col_to_transform] > 0).all():
                    df[col_to_transform + "_log"] = np.log(df[col_to_transform])
                    st.success(f"Applied log transformation to {col_to_transform}")
                else:
                    st.error("Log transformation requires all values to be positive")

def report_tab(df, filename):
    """Report generation tab"""
    st.markdown('<h2 class="sub-header">Analysis Report</h2>', unsafe_allow_html=True)
    
    # Generate comprehensive report
    report_text = generate_report(df, filename)
    
    # Display report in expandable sections
    with st.expander("📋 Executive Summary", expanded=True):
        st.write(report_text["executive_summary"])
    
    with st.expander("📊 Data Overview"):
        st.write(report_text["data_overview"])
    
    with st.expander("📈 Key Findings"):
        for finding in report_text["key_findings"]:
            st.write(f"- {finding}")
    
    with st.expander("🚀 Recommendations"):
        for recommendation in report_text["recommendations"]:
            st.write(f"- {recommendation}")
    
    # Download options
    st.markdown("---")
    st.subheader("📥 Download Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Text report
        st.download_button(
            label="📄 Download Text Report",
            data=report_text["full_report"],
            file_name=f"data_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        # CSV export of cleaned data
        csv = df.to_csv(index=False)
        st.download_button(
            label="💾 Download Cleaned Data (CSV)",
            data=csv,
            file_name=f"cleaned_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

def generate_insights(df, show_outliers):
    """Generate AI-powered insights"""
    suggestions = []
    
    # Missing values suggestion
    missing_values = df.isnull().sum().sum()
    if missing_values > 0:
        missing_percent = (missing_values / df.size) * 100
        suggestions.append({
            'type': 'warning',
            'message': f"Your data has {missing_values} missing values ({missing_percent:.2f}%). Consider imputation techniques like mean/median replacement or model-based imputation."
        })
    
    # Duplicates suggestion
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        suggestions.append({
            'type': 'warning',
            'message': f"Found {duplicates} duplicate rows ({duplicates/len(df)*100:.2f}%). Consider removing duplicates to avoid bias in analysis."
        })
    
    # Data type suggestions
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].nunique() < 10:
            suggestions.append({
                'type': 'info',
                'message': f"Column '{col}' has few unique values ({df[col].nunique()}). Consider converting to categorical for better memory usage and analysis."
            })
    
    # High cardinality detection
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].nunique() > 50:
            suggestions.append({
                'type': 'warning',
                'message': f"Column '{col}' has high cardinality ({df[col].nunique()} unique values). Consider grouping similar values or using encoding techniques for machine learning."
            })
    
    # Outlier detection
    if show_outliers:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_percent = (len(outliers) / len(df)) * 100
            
            if outlier_percent > 5:  # If more than 5% outliers
                suggestions.append({
                    'type': 'warning',
                    'message': f"Column '{col}' has {len(outliers)} potential outliers ({outlier_percent:.2f}%). Consider investigating these values for data quality issues."
                })
    
    # Add general suggestions
    suggestions.extend([
        {
            'type': 'success',
            'message': "Consider feature engineering to create new variables that might better capture patterns in your data."
        },
        {
            'type': 'info',
            'message': "For machine learning applications, remember to scale numeric features and encode categorical variables appropriately."
        },
        {
            'type': 'success',
            'message': "Based on your data structure, tree-based models might perform well for predictive tasks."
        }
    ])
    
    return suggestions

def generate_report(df, filename):
    """Generate a comprehensive report"""
    # Basic metrics
    missing_values = df.isnull().sum().sum()
    missing_percent = (missing_values / df.size) * 100
    duplicates = df.duplicated().sum()
    completeness_score = 100 - missing_percent
    
    # Numeric columns summary
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_summary = pd.DataFrame()
    if numeric_cols:
        numeric_summary = df[numeric_cols].describe()
    
    # Executive summary
    executive_summary = f"""
    AI Data Analysis Report
    Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    File: {filename}
    
    EXECUTIVE SUMMARY:
    This dataset contains {df.shape[0]:,} records with {df.shape[1]} variables.
    Overall data quality is {completeness_score:.1f}% complete with {duplicates} duplicate records.
    """
    
    # Data overview
    data_overview = f"""
    DATA OVERVIEW:
    - Records: {df.shape[0]:,}
    - Variables: {df.shape[1]}
    - Missing Values: {missing_values} ({missing_percent:.2f}%)
    - Duplicate Records: {duplicates}
    - Data Completeness Score: {completeness_score:.2f}%
    
    DATA TYPES:
    {df.dtypes.value_counts().to_string()}
    """
    
    # Key findings
    key_findings = [
        f"The dataset has {len(numeric_cols)} numeric columns and {len(df.columns) - len(numeric_cols)} categorical columns.",
        f"The most complete column is {df.isnull().sum().idxmin()} with {df[df.isnull().sum().idxmin()].isnull().sum()} missing values.",
        f"The column with the most unique values is {df.nunique().idxmax()} with {df.nunique().max()} distinct values."
    ]
    
    # Recommendations
    recommendations = [
        "Address missing values before performing advanced analysis or modeling.",
        "Remove duplicate records to ensure data quality.",
        "Consider normalizing numeric variables if they have significantly different scales.",
        "Encode categorical variables appropriately for machine learning applications."
    ]
    
    # Full report
    full_report = executive_summary + "\n\n" + data_overview + "\n\nKEY FINDINGS:\n"
    for finding in key_findings:
        full_report += f"- {finding}\n"
    
    full_report += "\nRECOMMENDATIONS:\n"
    for recommendation in recommendations:
        full_report += f"- {recommendation}\n"
    
    if not numeric_summary.empty:
        full_report += f"\nNUMERIC SUMMARY STATISTICS:\n{numeric_summary.to_string()}"
    
    return {
        "executive_summary": executive_summary,
        "data_overview": data_overview,
        "key_findings": key_findings,
        "recommendations": recommendations,
        "full_report": full_report
    }

def create_sample_data():
    """Create sample data for demonstration"""
    np.random.seed(42)
    n_samples = 1000
    
    # Generate sample data
    dates = pd.date_range('2020-01-01', periods=n_samples, freq='D')
    sales = np.random.normal(1000, 200, n_samples).cumsum() + np.random.normal(0, 50, n_samples)
    customers = np.random.poisson(50, n_samples) + np.random.randint(0, 20, n_samples)
    revenue = sales * np.random.uniform(0.8, 1.2, n_samples)
    product_categories = np.random.choice(['Electronics', 'Clothing', 'Home', 'Books', 'Sports'], n_samples)
    regions = np.random.choice(['North', 'South', 'East', 'West'], n_samples)
    
    # Create some missing values
    for col in [sales, customers, revenue]:
        idx = np.random.choice(n_samples, size=int(n_samples*0.05), replace=False)
        col[idx] = np.nan
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Sales': sales,
        'Customers': customers,
        'Revenue': revenue,
        'Product_Category': product_categories,
        'Region': regions
    })
    
    # Add some duplicates
    df = pd.concat([df, df.iloc[:10]], ignore_index=True)
    
    return df

if __name__ == "__main__":
    main()