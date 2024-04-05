import pandas as pd
import sqlalchemy

# read the excel file into a df
df = pd.read_excel('Retail_Sales_Data.xlsx')
df_names = df["name"].str.split("_", expand = True) # splits the name column into two columns

df['first_name'] = df_names[0]
df['last_name'] = df_names[1]
df.drop(columns =["name"], inplace = True) # drop the original name column modifies original df

# fix the product and category columns

productCategoriesDict = {
        'Camera': 'Technology',
        'Laptop': 'Technology',
        'Gloves': 'Apparel',
        'Smartphone': 'Technology',
        'Watch': 'Accessories',
        'Backpack': 'Accessories',
        'Water Bottle': 'Household Items',
        'T-shirt': 'Apparel',
        'Notebook': 'Stationery',
        'Sneakers': 'Apparel',
        'Dress': 'Apparel',
        'Scarf': 'Apparel',
        'Pen': 'Stationery',
        'Jeans': 'Apparel',
        'Desk Lamp': 'Household Items',
        'Umbrella': 'Accessories',
        'Sunglasses': 'Accessories',
        'Hat': 'Apparel',
        'Headphones': 'Technology',
        'Charger': 'Technology'}

df['column'] = df['product'].map(productCategoriesDict)

# Create a connection to the database
database_name = "is303"
db_user = ''
db_password = ''
db_host = "localhost" #this just means the database is stored on your own computer
db_port = "5432" # default setting

engine = sqlalchemy.create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{database_name}')

df.to_sql('retail_sales', engine, if_exists='replace', index=False)
print('you have imported your dataframe into the postgres database')
# check pgadmin4 to see what happened:

conn = engine.connect()

# Part II
# step 1
print()
print("The following are all the categories that have been sold:") 

# steop 2
query = "SELECT DISTINCT category FROM retail_sales"

df_category = pd.read_sql_query(query, engine)

for i, category in enumerate(df_category['category'], start = 1):
    print(f"{i}. {category}") 

# step 3
category_dictionary = {"Electronics" : "1", "Accessories" : "2", "Groceries" : "3", "Stationery" : "4", "Clothing" : "5"}
input_number = int((input("Please enter the number of the category you want to see summarized: ")))

# part 4
if input_number == 1:
#     total_sales_query = "SELECT SUM(sales) AS total_sales FROM retail_sales WHERE category = 'Electronics'"
#     result = conn.execute(total_sales_query)
        total_sales_query = "SELECT SUM(sales) AS total_sales FROM retail_sales WHERE category = 'Electronics'"
        result = conn.execute(total_sales_query)

        for row in result:
                print(row)
    
