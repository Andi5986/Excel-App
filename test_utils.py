import unittest
from io import BytesIO
import os
import pandas as pd
import base64
from unittest.mock import MagicMock, patch
from typing import List

class TestExcelDownload(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        self.excel_data = to_excel(self.df)
        self.filename = 'data.xlsx'

    def test_get_table_download_link(self):
        expected_output = f'<a href="data:application/octet-stream;base64,{base64.b64encode(self.excel_data).decode()}" download={self.filename}>Download Excel File</a>'
        self.assertEqual(get_table_download_link(self.excel_data, self.filename), expected_output)

    def test_convert_and_save_as_csv(self):
        # Test with a valid file
        uploaded_file = MagicMock(name='uploaded_file')
        uploaded_file.name = 'test.xlsx'
        uploaded_file.read.return_value = self.excel_data
        csv_file_path = convert_and_save_as_csv(uploaded_file)
        self.assertIsNotNone(csv_file_path)
        self.assertTrue(os.path.exists(csv_file_path))
        os.remove(csv_file_path)

        # Test with a None file
        self.assertIsNone(convert_and_save_as_csv(None))

        # Test with an invalid file
        uploaded_file = MagicMock(name='uploaded_file')
        uploaded_file.name = 'test.txt'
        self.assertIsNone(convert_and_save_as_csv(uploaded_file))

    def test_to_excel(self):
        expected_output = pd.read_excel(BytesIO(self.excel_data))
        self.assertTrue(self.df.equals(pd.read_excel(BytesIO(to_excel(self.df)))))

    def test_load_data(self):
        # Test with a valid file
        csv_file_path = 'test.csv'
        self.df.to_csv(csv_file_path, index=False)
        expected_output = pd.read_csv(csv_file_path)
        self.assertTrue(expected_output.equals(load_data(csv_file_path)))
        os.remove(csv_file_path)

        # Test with a None file
        self.assertIsNone(load_data(None))

        # Test with an invalid file
        self.assertIsNone(load_data('invalid_file.csv'))

if __name__ == '__main__':
    unittest.main()
