import streamlit as st
import pandas as pd
from transformers import pipeline

# Page Configuration
st.set_page_config(
    page_title="AI Customer Feedback Analyzer",
    page_icon="📊",
    layout="wide"
)

# Sidebar Design
st.sidebar.title("Navigation")
st.sidebar.markdown("### AI Customer Sentiment Tool")
st.sidebar.write("Ready to deploy, clean code, zero maintenance.")

# Load AI Model for Sentiment Analysis (Multilingual)
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

with st.spinner("Loading AI model... Please wait."):
    sentiment_analyzer = load_sentiment_model()

# Main Page UI
st.title("📊 AI Customer Feedback Analyzer")
st.markdown("Easily analyze customer sentiment instantly. Perfect for instant feedback analysis.")

# Tab 1: Single Text Analysis
st.subheader("1️⃣ Single Review Analysis")
user_input = st.text_area("Enter customer review (English or Arabic):", placeholder="Type or paste feedback here...")

if st.button("Analyze Sentiment"):
    if user_input.strip() != "":
        with st.spinner("Analyzing..."):
            result = sentiment_analyzer(user_input[:512])[0]
            label = result['label']
            score = result['score']
            
            # Map stars to sentiment
            if "5" in label or "4" in label:
                st.success(f"**Result:** Positive Sentiment ({label}) - Score: {score:.2f}")
            elif "3" in label:
                st.info(f"**Result:** Neutral Sentiment ({label}) - Score: {score:.2f}")
            else:
                st.error(f"**Result:** Negative Sentiment ({label}) - Score: {score:.2f}")
    else:
        st.warning("Please enter some text to analyze.")

st.markdown("---")

# Tab 2: Batch File Analysis (Excel / CSV)
st.subheader("2️⃣ Batch File Analysis (Excel / CSV)")
uploaded_file = st.file_uploader("Upload your file containing reviews:", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.write("Preview of uploaded data:", df.head())
    
    # Select column containing text
    text_column = st.selectbox("Select the column containing reviews:", df.columns)
    
    if st.button("Run Batch Analysis"):
        with st.spinner("Analyzing all comments and generating insights..."):
            results = []
            for text in df[text_column].astype(str):
                res = sentiment_analyzer(text[:512])[0]
                results.append(res['label'])
            
            df['Sentiment Result'] = results
            st.success("Batch analysis completed successfully!")
            
            # Display charts and summary
            st.subheader("Customer Sentiment Overview")
            sentiment_counts = df['Sentiment Result'].value_counts()
            st.bar_chart(sentiment_counts)
            
            st.write("Full data with results:", df)

