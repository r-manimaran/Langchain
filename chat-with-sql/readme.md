# Query MS SQL Server table data using OpenAI LLM
---------------------------------------------------

Uses the MS SQL Server table which contains 1 table GasExpenses
To connect to Database I am using ODBC and Sqlalchemy engine

contins the below columns
- Id
- DateFilled
- Price
- Quantity
- Total
### Below is the UI to perform the Query
![alt text](image.png)

### Below is the output from the table using the Agent
![alt text](image-1.png)


### Background agent processing
![alt text](image-2.png)


# Environment file
create a .env file and add the OPEN AI API as below
OPENAI_API_KEY = sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Run the App
To run the application use
> streamlit run main.py