import streamlit as st
import pandas as pd
from functions import (
    generate_behavioral_data,
    generate_preference_data,
    generate_inventory_data,
    check_data_consistency,
    CATEGORIES,
    BRANDS
)

# Page settings
st.set_page_config(layout="wide", page_title="Customer Data Analysis")

# Custom CSS for bigger section headers
st.markdown("""
    <style>
    .big-header {
        font-size: 2em !important;
        font-weight: bold !important;
        margin-bottom: 1em !important;
    }
    .load-button button {
        background-color: #ff9933 !important;
        color: white !important;
    }
    .loaded-button button {
        background-color: #00cc00 !important;
        color: white !important;
    }
    .custom-message {
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
    }
    .custom-message.success {
        border-left: 4px solid #00cc00;
    }
    .custom-message.info {
        border-left: 4px solid #0077cc;
    }
    .custom-message.warning {
        border-left: 4px solid #ff9933;
    }
    div[data-testid="stHorizontalBlock"] button {
        width: 100%;
        padding: 0.5rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar menu
menu_selection = st.sidebar.radio(
    "Navigation",
    ["Instructions", "Data", "Clustering", "Inventory Selection", "Email Design"]
)

if menu_selection == "Instructions":
    st.title("📚 Instructions")
    st.write("Welcome to the Customer Data Analysis Tool!")
    st.write("Use the sidebar menu to navigate between different sections:")
    st.markdown("""
    - **Data**: View and analyze customer behavioral data
    - **Clustering**: Customer segmentation analysis (Coming soon)
    - **Inventory Selection**: Product inventory optimization (Coming soon)
    - **Email Design**: Email campaign designer (Coming soon)
    """)

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
                    # Generate Behavioral Dataset
                    st.session_state.data = generate_behavioral_data(num_customers=2000)
                    
                    # Generate Preference Dataset
                    st.session_state.preference_data = generate_preference_data(num_customers=2000)
                    
                    # Generate Inventory Dataset
                    st.session_state.inventory_data = generate_inventory_data(num_products=1000)
                    
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
            
            show_data = st.toggle("Show Data", value=False)
            
            if show_data:
                # Display Behavioral Data
                st.subheader(f"Behavioral Data -- Number of records: {len(st.session_state.clean_data)}")
                # Pagination for Behavioral Data
                records_per_page = 10
                if 'page_behavioral' not in st.session_state:
                    st.session_state.page_behavioral = 0

                total_pages = len(st.session_state.clean_data) // records_per_page + (1 if len(st.session_state.clean_data) % records_per_page > 0 else 0)
                start_idx = st.session_state.page_behavioral * records_per_page
                end_idx = min(start_idx + records_per_page, len(st.session_state.clean_data))

                # Display data table
                st.dataframe(
                    st.session_state.clean_data.iloc[start_idx:end_idx],
                    use_container_width=True,
                    hide_index=True,
                    height=400,
                    column_config={
                        "customer_id": "ID",
                        "email": "Email",
                        "total_spent": st.column_config.NumberColumn("Total Spent", format="€%.2f"),
                        "total_orders": "Total Orders",
                        "avg_order_value": st.column_config.NumberColumn("Avg Order Value", format="€%.2f"),
                        "last_purchase_days_ago": "Days Since Last Purchase",
                        "categories_bought": "Categories",
                        "brands_bought": "Brands"
                    }
                )
                
                # Pagination controls
                col1, col2, col3 = st.columns([2, 6, 2])
                with col1:
                    cols = st.columns(2)
                    with cols[0]:
                        if st.button("⬅️", key="prev_behavioral", disabled=st.session_state.page_behavioral == 0, use_container_width=True, help="Previous page"):
                            st.session_state.page_behavioral -= 1
                    with cols[1]:
                        if st.button("➡️", key="next_behavioral", disabled=st.session_state.page_behavioral >= total_pages - 1, use_container_width=True, help="Next page"):
                            st.session_state.page_behavioral += 1
                with col2:
                    st.markdown(f"<div style='text-align: center'>Page {st.session_state.page_behavioral + 1} of {total_pages}</div>", unsafe_allow_html=True)
                
                # Display Preference Data
                st.subheader(f"Preference Data -- Number of records: {len(st.session_state.preference_data)}")
                # Pagination for Preference Data
                if 'page_preference' not in st.session_state:
                    st.session_state.page_preference = 0

                total_pages_pref = len(st.session_state.preference_data) // records_per_page + (1 if len(st.session_state.preference_data) % records_per_page > 0 else 0)
                start_idx_pref = st.session_state.page_preference * records_per_page
                end_idx_pref = min(start_idx_pref + records_per_page, len(st.session_state.preference_data))

                st.dataframe(
                    st.session_state.preference_data.iloc[start_idx_pref:end_idx_pref],
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )

                # Pagination controls for Preference Data
                col1, col2, col3 = st.columns([2, 6, 2])
                with col1:
                    cols = st.columns(2)
                    with cols[0]:
                        if st.button("⬅️", key="prev_preference", disabled=st.session_state.page_preference == 0, use_container_width=True):
                            st.session_state.page_preference -= 1
                    with cols[1]:
                        if st.button("➡️", key="next_preference", disabled=st.session_state.page_preference >= total_pages_pref - 1, use_container_width=True):
                            st.session_state.page_preference += 1
                with col2:
                    st.markdown(f"<div style='text-align: center'>Page {st.session_state.page_preference + 1} of {total_pages_pref}</div>", unsafe_allow_html=True)
                
                # Display Inventory Data
                st.subheader(f"Inventory Data -- Number of records: {len(st.session_state.inventory_data)}")
                # Pagination for Inventory Data
                if 'page_inventory' not in st.session_state:
                    st.session_state.page_inventory = 0

                total_pages_inv = len(st.session_state.inventory_data) // records_per_page + (1 if len(st.session_state.inventory_data) % records_per_page > 0 else 0)
                start_idx_inv = st.session_state.page_inventory * records_per_page
                end_idx_inv = min(start_idx_inv + records_per_page, len(st.session_state.inventory_data))

                st.dataframe(
                    st.session_state.inventory_data.iloc[start_idx_inv:end_idx_inv],
                    use_container_width=True,
                    hide_index=True,
                    height=400,
                    column_config={
                        "product_id": "ID",
                        "product_name": "Product Name",
                        "category": "Category",
                        "brand": "Brand",
                        "stock_quantity": "Stock",
                        "retail_price": st.column_config.NumberColumn("Retail Price", format="€%.2f"),
                        "cost_price": st.column_config.NumberColumn("Cost Price", format="€%.2f"),
                        "profit_margin": st.column_config.NumberColumn("Profit Margin", format="%.1f%%")
                    }
                )

                # Pagination controls for Inventory Data
                col1, col2, col3 = st.columns([2, 6, 2])
                with col1:
                    cols = st.columns(2)
                    with cols[0]:
                        if st.button("⬅️", key="prev_inventory", disabled=st.session_state.page_inventory == 0, use_container_width=True):
                            st.session_state.page_inventory -= 1
                    with cols[1]:
                        if st.button("➡️", key="next_inventory", disabled=st.session_state.page_inventory >= total_pages_inv - 1, use_container_width=True):
                            st.session_state.page_inventory += 1
                with col2:
                    st.markdown(f"<div style='text-align: center'>Page {st.session_state.page_inventory + 1} of {total_pages_inv}</div>", unsafe_allow_html=True)
    
    if 'data_loaded' in st.session_state:
        # Data Consistency Check section
        with st.expander("🔍 Data Consistency Check ✅ PASSED", expanded=False):
            st.markdown('<p class="big-header">Data Consistency Check</p>', unsafe_allow_html=True)
            
            problems, problem_rows = check_data_consistency(st.session_state.data)
            
            # Remove problematic rows and save clean data
            if problem_rows:
                st.session_state.clean_data = st.session_state.data.drop(problem_rows).reset_index(drop=True)
            else:
                st.session_state.clean_data = st.session_state.data
            
            # Display problems and their resolution
            for problem in problems:
                st.warning(f"• {problem} --- ✅ fixed")
            
            if not problems:
                st.success("✅ No problems found in the dataset")
            
            st.success(f"📊 Number of records after cleaning: {len(st.session_state.clean_data)}")

        # Data Privacy section
        with st.expander("🔒 Data Privacy & Anonymization ✅ PASSED", expanded=False):
            st.markdown('<p class="big-header">Data Privacy & Anonymization</p>', unsafe_allow_html=True)
            
            if 'anonymized_data' not in st.session_state:
                # Create anonymized dataset by removing email column
                st.session_state.anonymized_data = st.session_state.clean_data.drop(columns=['email'])
            st.success("✅ Email addresses have been removed from the dataset for AI analysis")
            st.success("ℹ️ The anonymized dataset is now ready for AI processing and analysis")

        # Data Normalization section
        with st.expander("📊 Data Normalization (for K-means) ✅ PASSED", expanded=False):
            st.markdown('<p class="big-header">Data Normalization</p>', unsafe_allow_html=True)
            
            if 'normalized_preference_data' not in st.session_state:
                # Create mapping tables for 'top_category' and 'top_brand'
                category_mapping = {category: idx for idx, category in enumerate(CATEGORIES)}
                brand_mapping = {brand: idx for idx, brand in enumerate(BRANDS)}
                
                # Create a copy of preference data for normalization
                st.session_state.normalized_preference_data = st.session_state.preference_data.copy()
                
                # Convert categorical columns to numeric
                st.session_state.normalized_preference_data["top_category"] = st.session_state.preference_data["top_category"].map(category_mapping)
                st.session_state.normalized_preference_data["top_brand"] = st.session_state.preference_data["top_brand"].map(brand_mapping)
                
                # Save mappings for reference
                st.session_state.category_mapping = pd.DataFrame(list(category_mapping.items()), columns=["category_name", "category_id"])
                st.session_state.brand_mapping = pd.DataFrame(list(brand_mapping.items()), columns=["brand_name", "brand_id"])
            
            st.success("✅ Preference dataset has been normalized for K-means clustering")
            
            show_details = st.toggle("Show Normalization Details", value=False)
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

        # Debug section
        with st.expander("🔧 DEBUG - Dataset Overview ✅ PASSED", expanded=False):
            st.markdown('<p class="big-header">Dataset Overview</p>', unsafe_allow_html=True)
            
            st.subheader("Final Datasets Status:")
            
            # Behavioral Dataset (cleaned)
            st.markdown("**1. Behavioral Dataset** (cleaned, emails removed)")
            st.success(f"• Number of records: {len(st.session_state.clean_data)}")
            st.success("• Status: ✅ Cleaned, invalid records removed")
            st.success("• Status: ✅ Emails removed for privacy")
            
            # Preference Dataset (normalized)
            st.markdown("**2. Preference Dataset** (normalized for K-means)")
            st.success(f"• Number of records: {len(st.session_state.normalized_preference_data)}")
            st.success("• Status: ✅ Categorical values converted to numeric")
            st.success("• Status: ✅ Ready for K-means clustering")
            
            # Inventory Dataset (original)
            st.markdown("**3. Inventory Dataset** (original)")
            st.success(f"• Number of records: {len(st.session_state.inventory_data)}")
            st.success("• Status: ✅ Original data, no modifications needed")

        # Final Datasets section
        with st.expander("📋 Final Datasets Overview ✅ PASSED", expanded=False):
            st.markdown('<p class="big-header">Final Datasets</p>', unsafe_allow_html=True)
            
            # Merge datasets for K-means
            if 'combined_dataset' not in st.session_state:
                st.session_state.combined_dataset = pd.merge(
                    st.session_state.normalized_preference_data,
                    st.session_state.anonymized_data,
                    on="customer_id",
                    how="inner"
                )
            
            st.success("✅ Behavioral and Preference datasets have been merged for K-means analysis")
            st.success(f"✅ Combined dataset contains {len(st.session_state.combined_dataset)} records")
            
            show_final_data = st.toggle("Show Final Datasets", value=False)
            if show_final_data:
                # Display Combined Data first
                st.subheader(f"Combined Dataset (for K-means) -- Number of records: {len(st.session_state.combined_dataset)}")
                if 'page_combined' not in st.session_state:
                    st.session_state.page_combined = 0

                records_per_page = 10
                total_pages_comb = len(st.session_state.combined_dataset) // records_per_page + (1 if len(st.session_state.combined_dataset) % records_per_page > 0 else 0)
                start_idx_comb = st.session_state.page_combined * records_per_page
                end_idx_comb = min(start_idx_comb + records_per_page, len(st.session_state.combined_dataset))

                st.dataframe(
                    st.session_state.combined_dataset.iloc[start_idx_comb:end_idx_comb],
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )

                # Pagination controls for Combined Data
                col1, col2, col3 = st.columns([2, 6, 2])
                with col1:
                    cols = st.columns(2)
                    with cols[0]:
                        if st.button("⬅️", key="prev_combined", disabled=st.session_state.page_combined == 0, use_container_width=True):
                            st.session_state.page_combined -= 1
                    with cols[1]:
                        if st.button("➡️", key="next_combined", disabled=st.session_state.page_combined >= total_pages_comb - 1, use_container_width=True):
                            st.session_state.page_combined += 1
                with col2:
                    st.markdown(f"<div style='text-align: center'>Page {st.session_state.page_combined + 1} of {total_pages_comb}</div>", unsafe_allow_html=True)

                st.markdown("---")  # Separator

                # Display Final Behavioral Data
                st.subheader(f"Final Behavioral Data (Cleaned & Anonymized) -- Number of records: {len(st.session_state.anonymized_data)}")
                # Pagination
                records_per_page = 10
                if 'page_final_behavioral' not in st.session_state:
                    st.session_state.page_final_behavioral = 0

                total_pages = len(st.session_state.anonymized_data) // records_per_page + (1 if len(st.session_state.anonymized_data) % records_per_page > 0 else 0)
                start_idx = st.session_state.page_final_behavioral * records_per_page
                end_idx = min(start_idx + records_per_page, len(st.session_state.anonymized_data))

                st.dataframe(
                    st.session_state.anonymized_data.iloc[start_idx:end_idx],
                    use_container_width=True,
                    hide_index=True,
                    height=400,
                    column_config={
                        "customer_id": "ID",
                        "total_spent": st.column_config.NumberColumn("Total Spent", format="€%.2f"),
                        "total_orders": "Total Orders",
                        "avg_order_value": st.column_config.NumberColumn("Avg Order Value", format="€%.2f"),
                        "last_purchase_days_ago": "Days Since Last Purchase",
                        "categories_bought": "Categories",
                        "brands_bought": "Brands"
                    }
                )
                
                # Pagination controls
                col1, col2, col3 = st.columns([2, 6, 2])
                with col1:
                    cols = st.columns(2)
                    with cols[0]:
                        if st.button("⬅️", key="prev_final_behavioral", disabled=st.session_state.page_final_behavioral == 0, use_container_width=True):
                            st.session_state.page_final_behavioral -= 1
                    with cols[1]:
                        if st.button("➡️", key="next_final_behavioral", disabled=st.session_state.page_final_behavioral >= total_pages - 1, use_container_width=True):
                            st.session_state.page_final_behavioral += 1
                with col2:
                    st.markdown(f"<div style='text-align: center'>Page {st.session_state.page_final_behavioral + 1} of {total_pages}</div>", unsafe_allow_html=True)

                # Display Final Preference Data
                st.subheader(f"Final Preference Data (Normalized) -- Number of records: {len(st.session_state.normalized_preference_data)}")
                if 'page_final_preference' not in st.session_state:
                    st.session_state.page_final_preference = 0

                total_pages_pref = len(st.session_state.normalized_preference_data) // records_per_page + (1 if len(st.session_state.normalized_preference_data) % records_per_page > 0 else 0)
                start_idx_pref = st.session_state.page_final_preference * records_per_page
                end_idx_pref = min(start_idx_pref + records_per_page, len(st.session_state.normalized_preference_data))

                st.dataframe(
                    st.session_state.normalized_preference_data.iloc[start_idx_pref:end_idx_pref],
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )

                # Pagination controls
                col1, col2, col3 = st.columns([2, 6, 2])
                with col1:
                    cols = st.columns(2)
                    with cols[0]:
                        if st.button("⬅️", key="prev_final_preference", disabled=st.session_state.page_final_preference == 0, use_container_width=True):
                            st.session_state.page_final_preference -= 1
                    with cols[1]:
                        if st.button("➡️", key="next_final_preference", disabled=st.session_state.page_final_preference >= total_pages_pref - 1, use_container_width=True):
                            st.session_state.page_final_preference += 1
                with col2:
                    st.markdown(f"<div style='text-align: center'>Page {st.session_state.page_final_preference + 1} of {total_pages_pref}</div>", unsafe_allow_html=True)

                # Display Final Inventory Data
                st.subheader(f"Final Inventory Data -- Number of records: {len(st.session_state.inventory_data)}")
                if 'page_final_inventory' not in st.session_state:
                    st.session_state.page_final_inventory = 0

                total_pages_inv = len(st.session_state.inventory_data) // records_per_page + (1 if len(st.session_state.inventory_data) % records_per_page > 0 else 0)
                start_idx_inv = st.session_state.page_final_inventory * records_per_page
                end_idx_inv = min(start_idx_inv + records_per_page, len(st.session_state.inventory_data))

                st.dataframe(
                    st.session_state.inventory_data.iloc[start_idx_inv:end_idx_inv],
                    use_container_width=True,
                    hide_index=True,
                    height=400,
                    column_config={
                        "product_id": "ID",
                        "product_name": "Product Name",
                        "category": "Category",
                        "brand": "Brand",
                        "stock_quantity": "Stock",
                        "retail_price": st.column_config.NumberColumn("Retail Price", format="€%.2f"),
                        "cost_price": st.column_config.NumberColumn("Cost Price", format="€%.2f"),
                        "profit_margin": st.column_config.NumberColumn("Profit Margin", format="%.1f%%")
                    }
                )

                # Pagination controls
                col1, col2, col3 = st.columns([2, 6, 2])
                with col1:
                    cols = st.columns(2)
                    with cols[0]:
                        if st.button("⬅️", key="prev_final_inventory", disabled=st.session_state.page_final_inventory == 0, use_container_width=True):
                            st.session_state.page_final_inventory -= 1
                    with cols[1]:
                        if st.button("➡️", key="next_final_inventory", disabled=st.session_state.page_final_inventory >= total_pages_inv - 1, use_container_width=True):
                            st.session_state.page_final_inventory += 1
                with col2:
                    st.markdown(f"<div style='text-align: center'>Page {st.session_state.page_final_inventory + 1} of {total_pages_inv}</div>", unsafe_allow_html=True)

elif menu_selection == "Clustering":
    st.title("🎯 Customer Clustering")
    st.success("This feature is coming soon!")
    
elif menu_selection == "Inventory Selection":
    st.title("📦 Inventory Selection")
    st.success("This feature is coming soon!")
    
elif menu_selection == "Email Design":
    st.title("✉️ Email Campaign Design")
    st.success("This feature is coming soon!")
