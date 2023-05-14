import base64
import pandas as pd
from io import BytesIO
import os

def get_table_download_link(excel_data: bytes, filename: str = 'data.xlsx') -> str:
    """Generates a link allowing the data in a given pandas dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    b64 = base64.b64encode(excel_data).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:application/octet-stream;base64,{b64}" download={filename}>Download Excel File</a>'
    return href

def convert_and_save_as_csv(uploaded_file) -> str:
    # Check if the uploaded file is not None
    if uploaded_file is not None:
        try:
            # Read the file with pandas
            df = pd.read_excel(uploaded_file)
            # Save the file as a CSV file
            csv_file_path = os.path.splitext(uploaded_file.name)[0] + '.csv'
            df.to_csv(csv_file_path, index=False)
            return csv_file_path
        except Exception as e:
            print("Error: ", e)
            return None
    else:
        print("No file uploaded.")
        return None

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    return output.getvalue()

def load_data(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None
