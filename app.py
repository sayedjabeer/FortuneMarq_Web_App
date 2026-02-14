import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
from parser import parse_semrush_html

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="FortuneMarq SEO Tool", page_icon="📈", layout="wide")

st.title("📈 FortuneMarq SEO Report Generator")
st.markdown("---")

# Sidebar for instructions
with st.sidebar:
    st.header("Instructions")
    st.write("1. Export your Semrush Domain Overview as an HTML file.")
    st.write("2. Upload it here.")
    st.write("3. Get your AI-powered executive summary.")

# File uploader
uploaded_file = st.file_uploader("Upload Semrush HTML File", type="html")

if uploaded_file is not None:
    # Read the file content
    html_content = uploaded_file.read().decode("utf-8")
    
    if st.button("Generate Executive Report"):
        with st.spinner('FortuneMarq AI is analyzing your data...'):
            try:
                # Parse the HTML
                clean_text = parse_semrush_html(html_content)
                
                # AI Prompt
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a senior SEO analyst for FortuneMarq agency. Provide a professional, client-ready market insight report based on the provided data."},
                        {"role": "user", "content": f"Analyze this SEO data and provide insights on traffic, keywords, and competition:\n\n{clean_text}"}
                    ]
                )
                
                report = response.choices[0].message.content
                
                # Display Report
                st.success("Report Generated Successfully!")
                st.markdown("### Executive Summary")
                st.markdown(report)
                
                # Option to download as text
                st.download_button("Download Report", report, file_name="SEO_Report.txt")
                
            except Exception as e:
                st.error(f"Error: {e}")
