import streamlit as st
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date
from config import CONFIG


def setup_sidebar():
    with st.sidebar:
        st.title("欢迎使用新旧料号替换工具")
        st.markdown("---")
        st.markdown("### 功能简介：")

def get_uploaded_files():
    st.header("📤 新旧料号替换")
   
    # ✅ 合并上传框：所有主+明细文件统一上传
    upload_file = st.file_uploader("🔁 上传新旧料号对照表", type="xlsx", key="uploading")

    # 📁 上传辅助文件（可选）
    st.subheader("📁 上传辅助文件（如无更新可跳过）")
    mapping_file = st.file_uploader("🔁 上传新旧料号对照表", type="xlsx", key="mapping")

    # 🚀 生成按钮
    start = st.button("🚀 生成汇总 Excel")

    return upload_file, mapping_file
