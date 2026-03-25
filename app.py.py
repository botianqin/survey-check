import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="问卷矛盾检查", page_icon="📝")

if "data_list" not in st.session_state:
    st.session_state.data_list = []

st.title("📝 问卷打分-备注矛盾识别")

score = st.number_input("打分（1-10）", min_value=1, max_value=10, value=5)
remark = st.text_area("备注内容")

def check_conflict(score, text):
    text = str(text).strip()
    positive = {"好", "满意", "改善", "提升", "进步", "稳定"}
    negative = {"差", "恶化", "下降", "糟糕", "不满", "变差", "问题"}

    has_pos = any(w in text for w in positive)
    has_neg = any(w in text for w in negative)

    if score >= 8 and has_neg:
        return "❌ 矛盾：高分+负面"
    if score <= 3 and has_pos:
        return "❌ 矛盾：低分+正面"
    return "✅ 正常"

if st.button("提交并检查"):
    if not remark:
        st.warning("请输入备注内容")
    else:
        res = check_conflict(score, remark)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.data_list.append({
            "时间": now,
            "打分": score,
            "备注": remark,
            "结果": res
        })
        st.success(f"提交成功！{res}")

st.divider()
st.subheader("📊 查看所有数据")
if st.session_state.data_list:
    df = pd.DataFrame(st.session_state.data_list)
    st.dataframe(df)
    csv = df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("下载数据", csv, "问卷数据.csv")
else:
    st.info("暂无数据")