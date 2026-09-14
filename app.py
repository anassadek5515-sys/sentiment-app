import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="محلل آراء العملاء", page_icon="🤖")
st.title("🤖 أداة تحليل آراء العملاء بالذكاء الاصطناعي")
st.write("أدخل رأي العميل لتحديد ما إذا كان إيجابياً أم سلبياً:")

@st.cache_resource
def load_analyzer():
    return pipeline("sentiment-analysis")

analyzer = load_analyzer()
user_input = st.text_area("رأي العميل:", "This app is really amazing and super fast!")

if st.button("تحليل النص 🚀"):
    if user_input.strip() != "":
        with st.spinner("جاري التحليل..."):
            result = analyzer(user_input)[0]
            label = result['label']
            score = round(result['score'] * 100, 1)
            if label == "POSITIVE":
                st.success(f"النتيجة: إيجابي 👍 (نسبة التأكد: {score}%)")
            else:
                st.error(f"النتيجة: سلبي 👎 (نسبة التأكد: {score}%)")
    else:
        st.warning("يرجى كتابة نص أولاً!")
