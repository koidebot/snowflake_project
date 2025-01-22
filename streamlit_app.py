import streamlit as st
import pandas as pd
import snowflake.connector

conn = st.connection("snowflake")
cursor = conn.cursor()

# Create the table in Snowflake
create_table_query = """
CREATE OR REPLACE TABLE fin_sales_data AS 
SELECT STORE, 
       TO_DATE(Date, 'DD/MM/YYYY') AS new_date, 
       WEEKLY_SALES, 
       ISHOLIDAY 
FROM sales_data;
"""

# Execute the query
cursor.execute(create_table_query)

# query = "SELECT * FROM fin_sales_data LIMIT 10;"
# df = pd.read_sql(query, conn)

store_id = st.number_input("ENTER STORE ID: ", min_value=1, max_value=45, step=1)

store_query = f"""
    SELECT Store, 
           DATE_TRUNC('month', new_date) AS sales_month, 
           SUM(WEEKLY_SALES) AS total_sales
    FROM fin_sales_data
    WHERE Store = {store_id}
    GROUP BY Store, sales_month
    ORDER BY sales_month;
    """

if st.button("Get Store Data"):
    df = pd.read_sql(store_query, conn)
    st.dataframe(df)



