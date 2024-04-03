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
db_user = "is303user"
db_password = "12345classpassword"
db_host = "localhost" #this just means the database is stored on your own computer
db_port = "5432" # default setting

engine = sqlalchemy.create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{database_name}')

df.to_sql('retail_sales', engine, if_exists='replace', index=False)
print('you have imported your dataframe into the postgres database')
# check pgadmin4 to see what happened: