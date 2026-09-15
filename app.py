import streamlit as st
from transformers import pipeline
import pandas as pd

# إعدادات صفحة الويب
st.set_page_config(page_title="منصة تحليل آراء العملاء", page_icon="📊", layout="wide")

# تصميم القائمة الجانبية (Sidebar) للاحترافية
st.sidebar.title("🛠️ لوحة التحكم")
app_mode = st.sidebar.selectbox("اختر وضع الاستخدام:", ["تحليل نص فردي", "تحليل ملف عملاء (Excel/CSV)"])

# تحميل نموذج الذكاء الاصطناعي متعدد اللغات (يدعم العربية والإنجليزية ببراعة)
@st.cache_resource
def load_analyzer():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

with st.spinner("جاري تهيئة نموذج الذكاء الاصطناعي..."):
    analyzer = load_analyzer()

# الوضع الأول: تحليل تعليق فردي
if app_mode == "تحليل نص فردي":
    st.title("🤖 أداة تحليل آراء العملاء الذكية")
    st.write("أدخل رأي العميل (بالعربية أو الإنجليزية) لمعرفة انطباعه بدقة:")

    user_input = st.text_area("رأي العميل:", "الخدمة ممتازة جداً والتوصيل سريع / This app is amazing!")

    if st.button("تحليل النص 🚀"):
        if user_input.strip() != "":
            with st.spinner("جاري التحليل..."):
                result = analyzer(user_input)[0]
                label = result['label'] # نجوم من 1 لـ 5
                score = round(result['score'] * 100, 1)
                
                # تصنيف النتيجة وتلوينها
                if "4" in label or "5" in label:
                    st.success(f"النتيجة: إيجابي 👍 (التقييم: {label} - نسبة التأكد: {score}%)")
                elif "1" in label or "2" in label:
                    st.error(f"النتيجة: سلبي 👎 (التقييم: {label} - نسبة التأكد: {score}%)")
                else:
                    st.warning(f"النتيجة: محايد 😐 (التقييم: {label} - نسبة التأكد: {score}%)")
        else:
            st.warning("يرجى كتابة نص أولاً!")

# الوضع الثاني: تحليل ملفات كاملة ورسوم بيانية (Dashboard)
elif app_mode == "تحليل ملف عملاء (Excel/CSV)":
    st.title("📈 لوحة إحصائيات آراء العملاء المتقدمة")
    st.write("ارفع ملف يحتوي على تعليقات العملاء لتحليلها دفعة واحدة وعمل رسوم بيانية:")

    uploaded_file = st.file_uploader("اختر ملف (CSV أو Excel)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.write("📋 عينة من البيانات المرفوعة:", df.head())
        
        text_column = st.selectbox("حدد عمود النص (التعليقات) في الملف:", df.columns)
        
        if st.button("بدء تحليل الملف الشامل 🚀"):
            with st.spinner("جاري تحليل كافة التعليقات ورسم الإحصائيات..."):
                results = []
                for text in df[text_column].astype(str):
                    res = analyzer(text[:512])[0]  # تحليل أول 512 حرف لكل تعليق
                    results.append(res['label'])
                
                df['التقييم'] = results
                st.success("تم الانتهاء من التحليل بنجاح!")
                
                # عرض رسم بياني للإحصائيات
                st.subheader("📊 توزيع آراء العملاء (رسوم بيانية)")
                sentiment_counts = df['التقييم'].value_counts()
                st.bar_chart(sentiment_counts)
                
                st.dataframe(df)

