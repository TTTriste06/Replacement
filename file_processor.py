import pandas as pd
from mapping_utils import replace_all_names_with_mapping

def process_uploaded_file(file, mapping_new, mapping_sub):
    df = pd.read_excel(file)
    df.columns = df.columns.astype(str).str.strip()
    if df.empty or df.shape[1] < 1:
        return pd.DataFrame(), None

    # 假设第一列是品名
    name_col = df.columns[0]
    df[name_col] = df[name_col].astype(str).str.strip()

    df[name_col] = replace_all_names_with_mapping(df[name_col], mapping_new, mapping_sub)

    return df, name_col
