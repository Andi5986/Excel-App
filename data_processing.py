import pandas as pd
from typing import List

def remove_nulls(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    for column in columns:
        df = df[df[column].notnull() & df[column].astype(str).str[0].str.isdigit()]
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
    df = handle_unknown_columns(df)
    df = rename_columns(df)
    df = convert_to_float(df, ['Account', 'Description'])
    return df

def find_account_columns(df: pd.DataFrame) -> List[int]:
    return [col for col in df.columns if 'cont' in col.lower() or 'account' in col.lower() and 'debit' in col.lower() or 'credit' in col.lower()]

def find_amount_columns(df: pd.DataFrame) -> List[int]:
    return [col for col in df.columns if 'suma' in col.lower()]

def process_journal(df: pd.DataFrame) -> pd.DataFrame:
    account_columns = [col for col in df.columns if any(account_key in col.lower() for account_key in ['cont', 'account'])]
    if len(account_columns) != 2:
        raise ValueError("Journal entry format is not as expected")

    transactions_dr = df.groupby(account_columns[0]).sum().reset_index().rename(columns={0: 'Debit Amount'})
    transactions_cr = df.groupby(account_columns[1]).sum().reset_index().rename(columns={0: 'Credit Amount'})

    df_out = pd.merge(transactions_dr, transactions_cr, on='Account', how='outer')

    df_out.fillna(0, inplace=True)

    df_out['Diff Dr.'] = df_out['Total Transactions Debit'] - df_out['Debit Amount']
    df_out['Diff Cr.'] = df_out['Total Transactions Credit'] - df_out['Credit Amount']

    return df_out
