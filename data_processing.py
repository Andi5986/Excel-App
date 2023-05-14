import pandas as pd
from typing import List

def remove_nulls(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    for column in columns:
        df = df[df[column].notnull() & df[column].astype(str).str[0].str.isdigit()]
    return df

def remove_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(how='all', axis=1)
    return df

def handle_unknown_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.apply(lambda x: x[x.astype(str).str[0].str.isdigit()] if x.dtype in ['object', 'int64'] else x)
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    if len(df.columns) == 10:
        df.columns = ['Account', 'Description', 'Opening Balance Debit', 'Opening Balance Credit',  
                      'Current Transactions Debit', 'Current Transactions Credit',
                      'Total Transactions Debit', 'Total Transactions Credit', 
                      'Closing Balance Debit', 'Closing Balance Credit']
    elif len(df.columns) == 8:
        df.columns = ['Account', 'Description', 'Opening Balance Debit', 'Opening Balance Credit', 
                      'Current Transactions Debit', 'Current Transactions Credit', 
                      'Closing Balance Debit', 'Closing Balance Credit']
    return df

def convert_to_float(df: pd.DataFrame, skip_columns: List[str]) -> pd.DataFrame:
    df = df.apply(lambda x: x.astype(str).str.replace(',', '').astype(float) if x.name not in skip_columns else x)
    return df

def process_dataframe(df: pd.DataFrame, *args) -> pd.DataFrame:
    df = remove_nulls(df, args)
    df = remove_empty_columns(df)
    df = handle_unknown_columns(df)
    df = rename_columns(df)
    df = convert_to_float(df, ['Account', 'Description'])
    return df


def rename_columns_je(df):
    column_mapping = {
        'Cont debitor': 'Account Debit',
        'Cont creditor': 'Account Credit',
        'Suma': 'Amount' 
    }
    
    df.rename(columns=column_mapping, inplace=True)
    return df

def process_journal(df: pd.DataFrame) -> pd.DataFrame:
    df = rename_columns_je(df)

    transactions_dr = df.groupby('Account Debit').agg({'Amount': 'sum'}).reset_index().rename(columns={'Amount': 'Debit Amount'})
    transactions_cr = df.groupby('Account Credit').agg({'Amount': 'sum'}).reset_index().rename(columns={'Amount': 'Credit Amount'})

    df_out = pd.merge(transactions_dr, transactions_cr, left_on='Account Debit', right_on='Account Credit', how='outer')

    df_out.fillna(0, inplace=True)

    df_out = df_out.rename(columns={'Account Debit': 'Account'}).drop('Account Credit', axis=1)
    
    return df_out

