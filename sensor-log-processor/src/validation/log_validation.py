import pandas as pd

def validation_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df["is_valid"]
        .value_counts()
        .reindex([True, False], fill_value=0)
        .rename_axis("is_valid")
        .reset_index(name="records")
    )