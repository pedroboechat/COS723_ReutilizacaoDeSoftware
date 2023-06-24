"""General utilities for the backend"""
# External libraries
import pandas as pd

def load_dataframe(kind: str = "csv", connection_path: (str | None) = None):
    if isinstance(connection_path, type(None)):
        raise ValueError("Invalid connection_path (None).")
    if kind == "csv":
        df = pd.read_csv(connection_path, sep=";")
    elif kind == "excel":
        df = pd.read_excel(connection_path)
    else:
        raise ValueError(f"Invalid kind ({kind}).")
    df["requisitos"] = df["requisitos"].apply(eval)
    return df.loc[
        df["curso_id"].isin(
            df[["curso", "curso_id"]]
            .drop_duplicates()
            .drop_duplicates("curso", keep="last")
            ["curso_id"]
        )
    ]


def get_prerequisites(prerequisites):
    if prerequisites == [""]:
        return []
    return [
        i[:i.index(" (")].strip()
        for i in prerequisites
    ]

def get_blocking_subjects(code, dataframe):
    requisites_df = dataframe.explode("requisitos").dropna(subset=["requisitos"])
    return requisites_df.loc[
        requisites_df["requisitos"].str.startswith(code)
    ]["codigo"].to_list()

def get_syllabus(syllabus):
    if pd.isna(syllabus):
        return "Não cadastrada."
    return syllabus
