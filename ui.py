import streamlit as st
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date


def setup_sidebar():
    with st.sidebar:
        st.title("欢迎使用新旧料号替换工具")
        st.markdown("---")
        st.markdown("### 功能简介：")

def get_uploaded_files():
    st.header("📤 新旧料号替换")

    # ✅ 支持多个主文件上传
    uploaded_files = st.file_uploader("🔁 上传需要替换的文件（第一列为品名）", type="xlsx", accept_multiple_files=True, key="uploading")

    # 📁 上传新旧料号表
    st.subheader("📁 上传辅助文件")
    mapping_file = st.file_uploader("📌 上传新旧料号对照表", type="xlsx", key="mapping")

    start = st.button("🚀 开始替换并导出")

    return uploaded_files, mapping_file, start
