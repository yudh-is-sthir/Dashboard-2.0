import pandas as pd

def get_data_for_role(role: str):
    df = pd.read_csv("mock_data.csv")

    if role == "admin":
        return df
    elif role == "viewer":
        return df[["name", "email", "department"]]
    elif role == "finance":
        return df[["name", "department", "salary"]]
    else:
        return pd.DataFrame({"message": ["Unauthorized role"]})
