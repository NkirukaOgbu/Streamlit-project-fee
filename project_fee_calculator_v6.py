import streamlit as st
from fpdf import FPDF
import os

# Fixed Costs
FIXED_COSTS = {
    "Base Plan & Site Layout Details": 1450,
    "Site Inspection and Field Consultation": 3000,
    "Additional Site Visits & Meetings": 2000,  # New additional service
}

# Variable Cost Calculation
def research_bubble_diagram(acres):
    return 8500 if acres > 200 else 6500 if acres > 100 else 5000 if acres > 50 else 3850 if acres > 30 else 3000 if acres > 20 else 2275 if acres > 10 else 1750

def final_master_planning(acres):
    return acres * 7 * 70

def sketch_concept_plan(acres):
    return final_master_planning(acres) * 0.75

def cad_engineer_package(acres):
    return acres * 7 * 30

def additional_revisions(acres):
    return final_master_planning(acres) * 0.4  # New additional service

# Package Details
PACKAGES = {
    "Concept (Sketch) Plan": ["Base Plan & Site Layout Details", "Sketch / Illustrative / Concept Master Plan"],
    "Master Plan (Without Inspection)": ["Base Plan & Site Layout Details", "Research, Bubble Diagram & Site Analysis", "Final / Comprehensive Master Planning"],
    "Comprehensive Master Plan": ["Base Plan & Site Layout Details", "Site Inspection and Field Consultation", "Research, Bubble Diagram & Site Analysis", "Final / Comprehensive Master Planning"],
    "Comprehensive Master Plan & CAD Package": ["Base Plan & Site Layout Details", "Site Inspection and Field Consultation", "Research, Bubble Diagram & Site Analysis", "Final / Comprehensive Master Planning", "CAD (Engineer-ready) Package"]
}

# Streamlit UI
st.title("Nadi Group - Land Planning Fee Calculator")

client_name = st.text_input("Client Name")
client_email = st.text_input("Client Email")
client_address = st.text_area("Client Address")
contact_no = st.text_input("Contact Number")
property_location = st.text_input("Property Location")
property_description = st.text_area("Property Description")
proposal_date = st.date_input("Proposal Date")
acreage = st.number_input("Approximate Developable Area in Acres", min_value=0.1, step=0.1)

st.subheader("Select a Package")
selected_package = None
package_cols = st.columns(len(PACKAGES))

for i, (package, services) in enumerate(PACKAGES.items()):
    with package_cols[i]:
        if st.checkbox(package, key=f"select_{package}"):
            selected_package = package
            for service in services:
                st.checkbox(service, value=True, disabled=True, key=f"{package}_{service}")

# Additional Services Selection
st.subheader("Additional Services (If Requested)")
additional_services = []
if st.checkbox("Additional Site Visits & Meetings ($2,000)"):
    additional_services.append("Additional Site Visits & Meetings")
if st.checkbox("Additional Revisions to Final Master Plan (40% of Final Master Planning)"):
    additional_services.append("Additional Revisions to Final Master Plan")

# Calculate Costs
if selected_package:
    selected_services = PACKAGES[selected_package]
    total_cost = sum(FIXED_COSTS.get(s, 0) for s in selected_services)
    total_cost += research_bubble_diagram(acreage) if "Research, Bubble Diagram & Site Analysis" in selected_services else 0
    total_cost += final_master_planning(acreage) if "Final / Comprehensive Master Planning" in selected_services else 0
    total_cost += sketch_concept_plan(acreage) if "Sketch / Illustrative / Concept Master Plan" in selected_services else 0
    total_cost += cad_engineer_package(acreage) if "CAD (Engineer-ready) Package" in selected_services else 0

    # Include Additional Services in Cost Calculation
    total_cost += FIXED_COSTS["Additional Site Visits & Meetings"] if "Additional Site Visits & Meetings" in additional_services else 0
    total_cost += additional_revisions(acreage) if "Additional Revisions to Final Master Plan" in additional_services else 0

    retainer_fee = total_cost / 2
    
    st.subheader("Cost Breakdown")
    st.write(f"Total Cost: **${total_cost:,.2f}**")
    st.write(f"Retainer Fee (50% of Total): **${retainer_fee:,.2f}**")

    proposal_filename = "nadi_proposal.pdf"
    
    # Generate Proposal PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "PROPOSAL DOCUMENT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Client Name: {client_name}", ln=True)
    pdf.cell(200, 10, f"Email: {client_email}", ln=True)
    pdf.cell(200, 10, f"Address: {client_address}", ln=True)
    pdf.cell(200, 10, f"Contact No: {contact_no}", ln=True)
    pdf.cell(200, 10, f"Property Location: {property_location}", ln=True)
    pdf.cell(200, 10, f"Property Description: {property_description}", ln=True)
    pdf.cell(200, 10, f"Approx. Developable Area: {acreage} acres", ln=True)
    pdf.cell(200, 10, f"Selected Package: {selected_package}", ln=True)
    pdf.cell(200, 10, f"Total Cost: ${total_cost:,.2f}", ln=True)
    pdf.cell(200, 10, f"Retainer Fee (50% of Total): ${retainer_fee:,.2f}", ln=True)

    # Include additional services in the proposal
    if additional_services:
        pdf.ln(10)
        pdf.cell(200, 10, "Additional Services Requested:", ln=True)
        for service in additional_services:
            pdf.cell(200, 10, f"- {service}", ln=True)

    pdf.output(proposal_filename)

    if os.path.exists(proposal_filename) and st.button("Print Proposal"):
        st.write(f"Proposal saved as {proposal_filename}")

