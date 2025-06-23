import streamlit as st
import pandas as pd
from io import BytesIO
from file_processor import process_uploaded_file
from mapping_utils import clean_mapping_headers

st.set_page_config(page_title="料号替换软件", layout="wide")
st.title("📦 文件新旧料号替换工具")

# 上传主文件
uploaded_files = st.file_uploader("📤 上传 Excel 文件（第一列为品名）", type="xlsx", accept_multiple_files=True)

# 上传映射表
mapping_file = st.file_uploader("🔁 上传新旧料号映射表", type="xlsx")

if st.button("🚀 开始替换") and uploaded_files and mapping_file:
    try:
        mapping_df = pd.read_excel(mapping_file)
        mapping_df = clean_mapping_headers(mapping_df)

        mapping_new = mapping_df[["旧品名", "新品名"]].dropna()
        mapping_sub = mapping_df[["新品名"] + [f"替代品名{i}" for i in range(1, 5) if f"替代品名{i}" in mapping_df.columns]]

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            for file in uploaded_files:
                df, name_col = process_uploaded_file(file, mapping_new, mapping_sub)
                if name_col:
                    df.to_excel(writer, sheet_name=file.name[:31], index=False)

        buffer.seek(0)
        st.success("✅ 所有文件已替换并合并完成！")
        st.download_button(
            label="📥 下载结果 Excel 文件",
            data=buffer,
            file_name="料号替换结果.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ 替换失败：{e}")
