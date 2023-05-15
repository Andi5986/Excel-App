from app import load_excel_data, process_dataframe, process_journal, remove_na_accounts, to_excel, get_table_download_link
import pandas as pd

## Test 1 - test_load_excel_data

def test_load_excel_data():
    uploaded_file = 'test_data.xlsx'
    df = pd.read_excel(uploaded_file)
    assert isinstance(load_excel_data(uploaded_file), pd.DataFrame)
    assert df.equals(load_excel_data(uploaded_file))


## Test 2 - test_process_dataframe

def test_process_dataframe():
    df = pd.DataFrame({'Account': ['A', 'B', 'C'], 
                       'Debit Amount': [100, 200, 300], 
                       'Credit Amount': [50, 100, 150]})
    expected_df = pd.DataFrame({'Account': ['A', 'B', 'C'], 
                                 'Opening Balance Debit': [0, 0, 0], 
                                 'Opening Balance Credit': [0, 0, 0], 
                                 'Current Transactions Debit': [100, 200, 300], 
                                 'Current Transactions Credit': [50, 100, 150], 
                                 'Closing Balance Debit': [100, 200, 300], 
                                 'Closing Balance Credit': [50, 100, 150]})
    assert expected_df.equals(process_dataframe(df))


## Test 3 - test_process_journal

def test_process_journal():
    df = pd.DataFrame({'Account': ['A', 'B', 'C'], 
                       'Debit Amount': [100, 200, 300], 
                       'Credit Amount': [50, 100, 150]})
    expected_df = pd.DataFrame({'Account': ['A', 'B', 'C'], 
                                 'Debit Amount': [100, 200, 300], 
                                 'Credit Amount': [50, 100, 150]})
    assert expected_df.equals(process_journal(df))


## Test 4 - test_remove_na_accounts

def test_remove_na_accounts():
    df = pd.DataFrame({'Account': ['A', 'B', 'C', pd.NA], 
                       'Debit Amount': [100, 200, 300, 400], 
                       'Credit Amount': [50, 100, 150, 200]})
    expected_df = pd.DataFrame({'Account': ['A', 'B', 'C'], 
                                 'Debit Amount': [100, 200, 300], 
                                 'Credit Amount': [50, 100, 150]})
    assert expected_df.equals(remove_na_accounts(df))


## Test 5 - test_get_table_download_link

def test_get_table_download_link():
    df = pd.DataFrame({'Account': ['A', 'B', 'C'], 
                       'Debit Amount': [100, 200, 300], 
                       'Credit Amount': [50, 100, 150]})
    excel_data = to_excel(df)
    expected_output = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_data}" download="processed_data.xlsx">Download Excel file</a>'
    assert expected_output == get_table_download_link(excel_data, 'processed_data.xlsx')


## Test 6 - test_load_excel_data_cache

def test_load_excel_data_cache():
    uploaded_file = 'test_data.xlsx'
    df = pd.read_excel(uploaded_file)
    assert isinstance(load_excel_data.cache_info(), tuple)
    assert load_excel_data.cache_info().hits == 0
    assert load_excel_data.cache_info().misses == 0
    load_excel_data(uploaded_file)
    assert load_excel_data.cache_info().hits == 0
    assert load_excel_data.cache_info().misses == 1
    load_excel_data(uploaded_file)
    assert load_excel_data.cache_info().hits == 1
    assert load_excel_data.cache_info().misses == 1
