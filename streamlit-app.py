from matplotlib import projections
import streamlit as st
import pymongo
import pandas as pd

MONGO_CLIENT = pymongo.MongoClient("mongodb://localhost:27017", username='root', password = 'example')

DB = MONGO_CLIENT["customer-events"]
COL = DB["invoice-items"]

customer_id = st.sidebar.text_input("Customer ID: ")

if customer_id:
    st.header(f"Customer: {customer_id}")
    query = {"CustomerID": customer_id}
    result = COL.find(query, {'_id': 0, "Description": 0, "UnitPrice": 0,"StockCode":0, "Quantity": 0, "Country": 0})
    df = pd.DataFrame(result)
    df.drop_duplicates(subset = 'InvoiceNo', keep= 'first', inplace = True)
    st.dataframe(df)



invoice_no = st.sidebar.text_input("Invoice No: ")

if invoice_no:
    st.header(f"Invoice No: {invoice_no}")
    query = {"InvoiceNo" : invoice_no}
    result = COL.find(query, {'_id': 0, 'Country': 0, 'InvoiceNo': 0})
    df = pd.DataFrame(result)
    st.dataframe(df)