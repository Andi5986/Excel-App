import pandas as pd
import streamlit as st
from data_processing import process_dataframe, process_journal, remove_na_accounts
from utils import get_table_download_link, to_excel, load_excel_data
from io import BytesIO
from llm_agent import set_openai_key, init_agent, get_agent_response

st.title('Accounting Fast Close')

# Ask user for OpenAI API key
openai_api_key = st.sidebar.text_input('Enter your OpenAI API Key', type='password')
if openai_api_key:
    set_openai_key(openai_api_key)

# Creating a button to toggle between uploaded documents and findings
view_option = st.selectbox('Choose View', ['Uploaded Documents', 'Findings'])

uploaded_file1 = st.sidebar.file_uploader('Upload your trial balance Excel file', type=['xlsx'])
uploaded_file2 = st.sidebar.file_uploader('Upload your journal entry Excel file', type=['xlsx'])

if uploaded_file1 is not None:
    df1 = load_excel_data(uploaded_file1)
    # Process the DataFrame
    df1 = process_dataframe(df1)

    # AI Agent Section
    if openai_api_key:
        agent = init_agent(openai_api_key)

if uploaded_file2 is not None:
    df2 = load_excel_data(uploaded_file2)
    df2 = process_journal(df2)

if uploaded_file1 is not None and uploaded_file2 is not None:
    # Merge df1 (trial balance) with df2 (journal entries) 
    df1 = pd.merge(df1, df2, on='Account', how='outer')

    # Remove rows with 'Account' as NA
    df1 = remove_na_accounts(df1)

    # Define the columns we want to fill NaN values with 0
    fillna_columns = ['Opening Balance Debit', 'Opening Balance Credit', 
                      'Current Transactions Debit', 'Current Transactions Credit', 
                      'Closing Balance Debit', 'Closing Balance Credit', 
                      'Debit Amount', 'Credit Amount' ]

    # Replace NaN values with 0 in the defined columns
    df1[fillna_columns] = df1[fillna_columns].fillna(0)

    # Compute the differences
    df1['Diff Dr.'] = df1['Current Transactions Debit'] - df1['Debit Amount']
    df1['Diff Cr.'] = df1['Current Transactions Credit'] - df1['Credit Amount']

    excel_data = to_excel(df1)  # Move this line to here

# Uploaded Documents Section
if view_option == 'Uploaded Documents':
    if uploaded_file1 is not None:
        st.write(df1)
#       st.markdown(get_table_download_link(excel_data, 'processed_data.xlsx'), unsafe_allow_html=True)

    if uploaded_file2 is not None:
        # Save the dataframes to an Excel file
        excel_data_combined = BytesIO()
        with pd.ExcelWriter(excel_data_combined, engine='xlsxwriter') as writer:
            df1.to_excel(writer, sheet_name='Trial Balance', index=False)
            df2.to_excel(writer, sheet_name='Journal Entry', index=False)

        st.markdown(get_table_download_link(excel_data_combined.getvalue(), filename='combined.xlsx'), unsafe_allow_html=True)

elif view_option == 'Findings':
    # Logic for findings should be implemented here
    st.write(df1)

    # AI Agent Section
    if openai_api_key and uploaded_file1 is not None:
        # Create a chat box for user questions
        user_input = st.text_input('Ask a question:')
        if user_input:
            response = get_agent_response(agent, df1, user_input)  # pass df1 as an argument
            st.write(response)
            
    if uploaded_file2 is not None:
        # Save the dataframes to an Excel file
        excel_data_combined = BytesIO()
        with pd.ExcelWriter(excel_data_combined, engine='xlsxwriter') as writer:
            df1.to_excel(writer, sheet_name='Trial Balance', index=False)
            df2.to_excel(writer, sheet_name='Journal Entry', index=False)

    st.markdown(get_table_download_link(excel_data_combined.getvalue(), filename='combined.xlsx'), unsafe_allow_html=True)

