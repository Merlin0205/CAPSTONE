import streamlit as st

# Page settings must be the first Streamlit command
st.set_page_config(layout="wide", page_title="Customer Data Analysis")

import pandas as pd
from functions import (
    generate_behavioral_data,
    generate_preference_data,
    generate_inventory_data,
    check_data_consistency,
    CATEGORIES,
    BRANDS
)
import toml
from components.section import create_section
from components.template_loader import load_template

# Load CSS
with open("styles/main.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Handle navigation from buttons
if 'go_to_clustering' in st.session_state and st.session_state['go_to_clustering']:
    st.session_state['go_to_clustering'] = False
    st.session_state['menu_selection'] = "Clustering"

if 'go_to_data' in st.session_state and st.session_state['go_to_data']:
    st.session_state['go_to_data'] = False
    st.session_state['menu_selection'] = "Data"

# Load config file
try:
    with open('.streamlit/config.toml', 'r') as f:
        config = toml.load(f)
        debug_mode = config.get('debug', {}).get('developerMode', False)
except Exception as e:
    print(f"Error loading config: {e}")
    debug_mode = False

# Print debug mode status for verification
print(f"Debug mode is: {debug_mode}")

# Sidebar menu
if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = "Instructions"

menu_selection = st.sidebar.radio(
    "Navigation",
    ["Instructions", "Data", "Clustering", "Inventory Selection", "Email Design"],
    key="menu_selection"
)

if menu_selection == "Instructions":
    st.title("📚 User Guide")
    st.write("Welcome to the Customer Data Analysis Tool!")
    
    # Application Goal section
    application_goal_content = load_template("application-goal")
    st.markdown(create_section(
        "APPLICATION GOAL",
        application_goal_content,
        "🎯"
    ), unsafe_allow_html=True)
    
    # Workflow section
    workflow_content = load_template("workflow")
    st.markdown(create_section(
        "WORKFLOW",
        workflow_content,
        "📋"
    ), unsafe_allow_html=True)
    
    # Getting Started section
    getting_started_content = load_template("getting-started")
    st.markdown(create_section(
        "GETTING STARTED",
        getting_started_content,
        "🚀"
    ), unsafe_allow_html=True)
    
    # Navigation button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Start with Data Section ➡️", type="primary", use_container_width=True):
            st.session_state['go_to_data'] = True
            st.rerun()

elif menu_selection == "Data":
    st.title("📊 Customer Data Analysis")

    # Load Data section
    with st.expander("📥 Load Data" + (" ✅ PASSED" if 'data_loaded' in st.session_state else ""), expanded=True):
        st.markdown('<p class="big-header">Load Data</p>', unsafe_allow_html=True)
        
        load_col = st.container()
        with load_col:
            if 'data_loaded' not in st.session_state:
                st.markdown('<div class="load-button">', unsafe_allow_html=True)
                if st.button("Load Datasets"):
                    # Generate and store original datasets
                    st.session_state.original_behavioral_data = generate_behavioral_data(num_customers=2000)
                    st.session_state.original_preference_data = generate_preference_data(num_customers=2000)
                    st.session_state.original_inventory_data = generate_inventory_data(num_products=1000)
                    
                    st.session_state.data_loaded = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="loaded-button">', unsafe_allow_html=True)
                st.button("✅ Load Datasets")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Show success messages if data is loaded
        if 'data_loaded' in st.session_state:
            st.success("✅ Behavioral dataset successfully loaded")
            st.success("✅ Preference dataset successfully loaded")
            st.success("✅ Inventory dataset successfully loaded")
            
            show_data = st.toggle("Show Original Data", value=False)
            
            if show_data:
                st.subheader("Original Datasets:")
                
                # Display Original Behavioral Data
                st.subheader(f"Original Behavioral Data -- Number of records: {len(st.session_state.original_behavioral_data)}")
                st.dataframe(
                    st.session_state.original_behavioral_data,
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
                
                # Display Original Preference Data
                st.subheader(f"Original Preference Data -- Number of records: {len(st.session_state.original_preference_data)}")
                st.dataframe(
                    st.session_state.original_preference_data,
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
                
                # Display Original Inventory Data
                st.subheader(f"Original Inventory Data -- Number of records: {len(st.session_state.original_inventory_data)}")
                st.dataframe(
                    st.session_state.original_inventory_data,
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
    
    if 'data_loaded' in st.session_state:
        # Data Consistency Check section
        with st.expander("🔍 Data Consistency Check ✅ PASSED", expanded=False):
            st.markdown('<p class="big-header">Data Consistency Check</p>', unsafe_allow_html=True)
            
            problems, problem_rows = check_data_consistency(st.session_state.original_behavioral_data)
            
            # Remove problematic rows and save clean data
            if problem_rows:
                st.session_state.clean_behavioral_data = st.session_state.original_behavioral_data.drop(problem_rows).reset_index(drop=True)
            else:
                st.session_state.clean_behavioral_data = st.session_state.original_behavioral_data.copy()
            
            # Display problems and their resolution
            for problem in problems:
                st.warning(f"• {problem} --- ✅ fixed")
            
            if not problems:
                st.success("✅ No problems found in the dataset")
            
            st.success(f"📊 Number of records after cleaning: {len(st.session_state.clean_behavioral_data)}")

        # Data Privacy section
        with st.expander("🔒 Data Privacy & Anonymization ✅ PASSED", expanded=False):
            st.markdown('<p class="big-header">Data Privacy & Anonymization</p>', unsafe_allow_html=True)
            
            # Create anonymized dataset by removing email column
            st.session_state.anonymized_behavioral_data = st.session_state.clean_behavioral_data.drop(columns=['email'])
            st.success("✅ Email addresses have been removed from the dataset for AI analysis")
            st.success("ℹ️ The anonymized dataset is now ready for AI processing and analysis")

        # String to Numeric Conversion section
        with st.expander("🔢 String to Numeric Conversion ✅ PASSED", expanded=False):
            st.markdown('<p class="big-header">String to Numeric Conversion</p>', unsafe_allow_html=True)
            
            # Create mapping tables for 'top_category' and 'top_brand'
            category_mapping = {category: idx for idx, category in enumerate(CATEGORIES)}
            brand_mapping = {brand: idx for idx, brand in enumerate(BRANDS)}
            
            # Create a copy of preference data for conversion
            st.session_state.numeric_preference_data = st.session_state.original_preference_data.copy()
            
            # Convert categorical columns to numeric
            st.session_state.numeric_preference_data["top_category"] = st.session_state.original_preference_data["top_category"].map(category_mapping)
            st.session_state.numeric_preference_data["top_brand"] = st.session_state.original_preference_data["top_brand"].map(brand_mapping)
            
            # Save mappings for reference
            st.session_state.category_mapping = pd.DataFrame(list(category_mapping.items()), columns=["category_name", "category_id"])
            st.session_state.brand_mapping = pd.DataFrame(list(brand_mapping.items()), columns=["brand_name", "brand_id"])
            
            st.success("✅ Categorical values have been converted to numeric")
            
            show_details = st.toggle("Show Conversion Details", value=False)
            if show_details:
                st.subheader("Category Mapping")
                st.dataframe(
                    st.session_state.category_mapping,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.subheader("Brand Mapping")
                st.dataframe(
                    st.session_state.brand_mapping,
                    use_container_width=True,
                    hide_index=True
                )

        # Final Datasets section
        with st.expander("📋 Final Datasets Overview ✅ PASSED", expanded=False):
            st.markdown('<p class="big-header">Final Datasets</p>', unsafe_allow_html=True)
            
            # Merge datasets
            st.session_state.combined_raw_data = pd.merge(
                st.session_state.numeric_preference_data,
                st.session_state.anonymized_behavioral_data,
                on="customer_id",
                how="inner"
            )
            
            # Normalize data for K-means
            from sklearn.preprocessing import StandardScaler
            
            # Select numeric columns for normalization
            numeric_columns = ['price_preference_range', 'discount_sensitivity', 'luxury_preference_score',
                             'total_spent', 'total_orders', 'avg_order_value', 'last_purchase_days_ago',
                             'categories_bought', 'brands_bought']
            
            # Create scaler
            scaler = StandardScaler()
            
            # Create copy for normalization
            st.session_state.normalized_kmeans_data = st.session_state.combined_raw_data.copy()
            
            # Normalize numeric columns
            st.session_state.normalized_kmeans_data[numeric_columns] = scaler.fit_transform(
                st.session_state.combined_raw_data[numeric_columns]
            )
            
            st.success("✅ Datasets have been merged and normalized for K-means analysis")
            st.success(f"✅ Final dataset contains {len(st.session_state.normalized_kmeans_data)} records")
            
            show_final_data = st.toggle("Show Final Dataset", value=False)
            if show_final_data:
                st.subheader(f"Final Dataset for K-means Clustering -- Number of records: {len(st.session_state.normalized_kmeans_data)}")
                st.dataframe(
                    st.session_state.normalized_kmeans_data,
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )

        # Final success message and next step
        st.markdown("---")  # Separator
        st.markdown("""
            <div style='text-align: center; padding: 2rem; margin: 2rem 0; background-color: #1a1a1a; border-radius: 10px; border: 1px solid #333;'>
                <h2 style='color: #00cc00; margin-bottom: 1rem;'>✅ All Data Successfully Processed</h2>
                <p style='color: #ffffff; font-size: 1.2rem; margin-bottom: 1.5rem;'>
                    All datasets have been loaded, cleaned, and prepared for analysis. You can now proceed to customer segmentation.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Center the button using columns
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Continue to Clustering Analysis ➡️", type="primary", use_container_width=True):
                # Instead of directly modifying menu_selection, set a flag
                st.session_state['go_to_clustering'] = True
                st.rerun()

elif menu_selection == "Clustering":
    st.title("🎯 Customer Clustering")
    st.success("This feature is coming soon!")
    
elif menu_selection == "Inventory Selection":
    st.title("📦 Inventory Selection")
    st.success("This feature is coming soon!")
    
elif menu_selection == "Email Design":
    st.title("✉️ Email Campaign Design")
    st.success("This feature is coming soon!")
