from io import BytesIO
import streamlit as st
import pandas as pd
from datetime import datetime

from ui import setup_sidebar, get_uploaded_files
from mapping_utils import clean_mapping_headers, replace_all_names_with_mapping, apply_mapping_and_merge, apply_extended_substitute_mapping
from excel_utils import adjust_column_width

def main():
    st.set_page_config(page_title="料号替换合并工具", layout="wide")
    setup_sidebar()

    uploaded_files, mapping_file, start = get_uploaded_files()

    if start:
        if not uploaded_files or mapping_file is None:
            st.warning("请上传替换文件和新旧料号表")
            return

        # 加载映射表
        try:
            mapping_df = pd.read_excel(mapping_file)
            mapping_df = clean_mapping_headers(mapping_df)
            
            # 去除“品名”为空的行
            mapping_new = mapping_df[
                ["旧晶圆品名", "旧规格", "旧品名", "新晶圆品名", "新规格", "新品名"]
            ]
            mapping_new = mapping_new[~mapping_df["新品名"].astype(str).str.strip().replace("nan", "").eq("")].copy()
            mapping_new = mapping_new[~mapping_new["旧品名"].astype(str).str.strip().replace("nan", "").eq("")].copy()
            
            # 去除“替代品名”为空的行，并保留指定字段
            mapping_sub1 = mapping_df[
                ["新晶圆品名", "新规格", "新品名", "替代晶圆1", "替代规格1", "替代品名1"]
            ]
            mapping_sub1 = mapping_sub1[~mapping_df["替代品名1"].astype(str).str.strip().replace("nan", "").eq("")].copy()
            mapping_sub1.columns = [
                "新晶圆品名", "新规格", "新品名", 
                "替代晶圆", "替代规格", "替代品名"
            ]
    
    
            mapping_sub2 = mapping_df[
                ["新晶圆品名", "新规格", "新品名", "替代晶圆2", "替代规格2", "替代品名2"]
            ]
            mapping_sub2 = mapping_sub2[~mapping_df["替代品名2"].astype(str).str.strip().replace("nan", "").eq("")].copy()
            mapping_sub2.columns = [
                "新晶圆品名", "新规格", "新品名",
                "替代晶圆", "替代规格", "替代品名"
            ]
    
            mapping_sub3 = mapping_df[
                ["新晶圆品名", "新规格", "新品名", "替代晶圆3", "替代规格3", "替代品名3"]
            ]
            mapping_sub3 = mapping_sub3[~mapping_df["替代品名3"].astype(str).str.strip().replace("nan", "").eq("")].copy()
            mapping_sub3.columns = [
                "新晶圆品名", "新规格", "新品名",
                "替代晶圆", "替代规格", "替代品名"
            ]
            
            mapping_sub4 = mapping_df[
                ["新晶圆品名", "新规格", "新品名", "替代晶圆4", "替代规格4", "替代品名4"]
            ]
            mapping_sub4 = mapping_sub4[~mapping_df["替代品名4"].astype(str).str.strip().replace("nan", "").eq("")].copy()
            mapping_sub4.columns = [
                "新晶圆品名", "新规格", "新品名",
                "替代晶圆", "替代规格", "替代品名"
            ]
        
        except Exception as e:
            st.error(f"❌ 映射表加载失败：{e}")
            return

        # 处理所有上传的文件
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            for file in uploaded_files:
                try:
                    df = pd.read_excel(file)
                    df.columns = df.columns.astype(str).str.strip()

                    if df.empty or df.shape[1] < 1:
                        st.warning(f"⚠️ 文件 `{file.name}` 内容为空，跳过")
                        continue

                    name_col = df.columns[0]
                    
                    # 替换品名
                    df = apply_mapping_and_merge(df, mapping_new)
                    df = apply_extended_substitute_mapping(df, mapping_sub1)
                    df = apply_extended_substitute_mapping(df, mapping_sub2)
                    df = apply_extended_substitute_mapping(df, mapping_sub3)
                    df = apply_extended_substitute_mapping(df, mapping_sub4)

                    # 将相同品名合并（数值列相加）
                    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
                    df = df.groupby(name_col, as_index=False)[numeric_cols].sum()


                    sheet_name = file.name[:31]  # Excel sheet 名最长 31 字符

                    with pd.ExcelWriter(output_buffer, engine="openpyxl") as writer:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        
                        #写入主计划
                        ws = writer.book[sheet_name]
                        adjust_column_width(ws)

                except Exception as e:
                    st.warning(f"❌ 处理文件 `{file.name}` 失败：{e}")

        buffer.seek(0)
        filename = f"替换结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        st.success("✅ 所有文件处理完毕！你可以下载结果：")
        st.download_button("📥 下载合并 Excel", data=buffer, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print("❌ 应用崩溃:", e)
        traceback.print_exc()
