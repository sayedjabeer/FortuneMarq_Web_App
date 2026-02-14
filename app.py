import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
from parser import parse_semrush_html

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="FortuneMarq SEO Tool", page_icon="📈", layout="wide")

st.title("📈 FortuneMarq SEO Metrics Extractor")
st.markdown("---")

# Sidebar for instructions
with st.sidebar:
    st.header("Instructions")
    st.write("1. Export your Semrush Domain Overview as an HTML file.")
    st.write("2. Upload it here.")
    st.write("3. Get a numbers-focused analysis for your scripts.")

# File uploader
uploaded_file = st.file_uploader("Upload Semrush HTML File", type="html")

if uploaded_file is not None:
    # Read the file content
    html_content = uploaded_file.read().decode("utf-8")
    
    if st.button("Generate Metrics Report"):
        with st.spinner('FortuneMarq AI is extracting numeric insights...'):
            try:
                # Parse the HTML
                clean_text = parse_semrush_html(html_content)
                
                # Updated Prompt for a numbers-focused output
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "You are a senior SEO analyst at FortuneMarq. "
                                "Your task is to extract exact numerical data from the text. "
                                "Format the output using Markdown tables only. "
                                "Do not use conversational fillers or long paragraphs. "
                                "Focus on: Domain Metrics, Keyword Performance (Volume, Position, Traffic %), "
                                "Intent Distribution, and Competitor Keyword Overlap."
                            )
                        },
                        {
                            "role": "user", 
                            "content": f"Extract all key metrics from the following SEO data into structured tables:\n\n{clean_text}"
                        }
                    ]
                )
                
                report = response.choices[0].message.content
                
                # Display Report
                st.success("Metrics Extracted Successfully!")
                st.markdown("### 📊 Structured Market Insights")
                st.markdown(report)
                
                # Option to download as text (useful for parsing in other scripts)
                st.download_button("Download Raw Report", report, file_name="SEO_Metrics_Report.txt")
                
            except Exception as e:
                st.error(f"Error: {e}")
