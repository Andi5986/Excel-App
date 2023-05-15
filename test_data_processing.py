import pandas as pd
import unittest
from data_processing import remove_nulls, remove_na_accounts, remove_empty_columns, handle_unknown_columns, rename_columns, convert_to_float, process_dataframe, rename_columns_je, process_journal
                             

class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({'Account': [1, 2, 3, 4, 5], 
                                'Description': ['a', 'b', 'c', 'd', 'e'], 
                                'Opening Balance Debit': [100, 200, None, 400, 500], 
                                'Opening Balance Credit': [None, 200, 300, 400, 500], 
                                'Current Transactions Debit': [100, 200, 300, 400, 500], 
                                'Current Transactions Credit': [100, 200, 300, 400, 500], 
                                'Total Transactions Debit': [100, 200, 300, 400, 500], 
                                'Total Transactions Credit': [100, 200, 300, 400, 500], 
                                'Closing Balance Debit': [100, 200, 300, 400, 500], 
                                'Closing Balance Credit': [100, 200, 300, 400, 500]})
        self.df_je = pd.DataFrame({'Cont debitor': [1, 2, 3, 4, 5], 
                                   'Cont creditor': [6, 7, 8, 9, 10], 
                                   'Suma': [100, 200, 300, 400, 500]})

    def test_remove_nulls(self):
        df = remove_nulls(self.df, ['Opening Balance Debit'])
        self.assertEqual(len(df), 4)

    def test_remove_na_accounts(self):
        df = remove_na_accounts(self.df)
        self.assertEqual(len(df), 5)

    def test_remove_empty_columns(self):
        df = remove_empty_columns(self.df)
        self.assertEqual(len(df.columns), 10)

    def test_handle_unknown_columns(self):
        df = handle_unknown_columns(self.df)
        self.assertEqual(len(df), 5)

    def test_rename_columns(self):
        df = rename_columns(self.df)
        self.assertEqual(len(df.columns), 10)

    def test_convert_to_float(self):
        df = convert_to_float(self.df, ['Account'])
        self.assertEqual(df['Opening Balance Debit'].dtype, 'float64')

    def test_process_dataframe(self):
        df = process_dataframe(self.df, 'Opening Balance Debit')
        self.assertEqual(len(df.columns), 10)

    def test_rename_columns_je(self):
        df = rename_columns_je(self.df_je)
        self.assertEqual(len(df.columns), 3)

    def test_process_journal(self):
        df = process_journal(self.df_je)
        self.assertEqual(len(df), 10)

if __name__ == '__main__':
    unittest.main()
