import streamlit as st
import pandas as pd
from datetime import datetime

# Set page title
st.title("RV Resort Land Planning Fee Calculator")

# User Inputs
st.header("Enter Project Details")

client_name = st.text_input("Client Name")
property_location = st.text_area("Property Location/Description")
proposal_date = st.date_input("Proposal Date", datetime.today())
property_description = st.text_area("Property Description")
project_size = st.number_input("Project Size (in Acres)", min_value=0.1, step=0.1)

# Base Fees
base_plan_fee = 1450
site_inspection_fee = 3000
comprehensive_master_fee = 9800
concept_master_fee = 7350
cad_basic_fee = 2450
cad_engineering_fee = 4200

# Research Fee Calculation Based on Acres
if project_size > 200:
    research_fee = 8500
elif project_size > 100:
    research_fee = 6500
elif project_size > 50:
    research_fee = 5000
elif project_size > 30:
    research_fee = 3850
elif project_size > 20:
    research_fee = 3000
elif project_size > 10:
    research_fee = 2275
else:
    research_fee = 1750

# Ensuring research fee minimum is $1000
research_fee = max(research_fee, 1000)

# 75% and 25% split for concept plan calculations
concept_fee_75 = research_fee * 0.75
concept_fee_25 = research_fee - concept_fee_75

# Ensuring minimum concept fee is $875
concept_fee_25 = max(concept_fee_25, 875)

# Fee Calculations
concept_plan_fee = base_plan_fee + concept_fee_75
master_plan_fee = base_plan_fee + research_fee + comprehensive_master_fee
master_plan_with_inspection_fee = base_plan_fee + site_inspection_fee + research_fee + comprehensive_master_fee
master_plan_cad_fee = master_plan_with_inspection_fee + cad_basic_fee + cad_engineering_fee

# Retainer Fees (50% of each plan)
retainer_concept = concept_plan_fee / 2
retainer_master = master_plan_fee / 2
retainer_master_inspection = master_plan_with_inspection_fee / 2
retainer_master_cad = master_plan_cad_fee / 2

# Display Results
if project_size > 0:
    st.header("Project Fees")
    
    fee_data = {
        "Plan Type": ["Concept Plan", "Master Plan", "Master Plan + Site Inspection", "Master Plan + CAD Package"],
        "Total Fee ($)": [concept_plan_fee, master_plan_fee, master_plan_with_inspection_fee, master_plan_cad_fee],
        "Retainer Fee (50%)": [retainer_concept, retainer_master, retainer_master_inspection, retainer_master_cad]
    }
    
    fee_df = pd.DataFrame(fee_data)
    st.dataframe(fee_df)

    # Option to Download Results
    csv = fee_df.to_csv(index=False).encode("utf-8")
    st.download_button(label="Download Fee Calculation", data=csv, file_name="project_fees.csv", mime="text/csv")
else:
    st.warning("Please enter a valid project size in acres.")
