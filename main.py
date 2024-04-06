import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plot

# Create a connection to the database
database_name = "is303"
db_user = "is303user"
db_password = "12345classpassword"
db_host = "localhost" #this just means the database is stored on your own computer
db_port = "5432" # default setting

engine = sqlalchemy.create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{database_name}')

# read the excel file into a df
df = pd.read_excel("Retail_Sales_Data.xlsx")
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

df['category'] = df['product'].map(productCategoriesDict)

user_input = int(input("If you want to import data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: ").strip())

if user_input == 1:
    df.to_sql('sale', engine, if_exists='replace', index=False)
    print('you have imported your dataframe into the postgres database')
    # check pgadmin4 to see what happened:

# Part II
elif user_input == 2:
    # step 1
    print()
    print("The following are all the categories that have been sold:") 

    # step 2
    query = "SELECT DISTINCT category FROM sale"

    df_category = pd.read_sql_query(query, engine)

    for i, category in enumerate(df_category['category'], start = 1):
        print(f"{i}. {category}") 

    # step 3
    category_dictionary = {"Electronics" : "1", "Accessories" : "2", "Groceries" : "3", "Stationery" : "4", "Clothing" : "5"}
    category_number = int((input("Please enter the number of the category you want to see summarized: ")))

    # step 4
    category_selected = list(category_dictionary.keys())[list(category_dictionary.values()).index(str(category_number))]

    query = f"SELECT * FROM sale WHERE category = '{category_selected}'"
    df_selected_category = pd.read_sql_query(query, engine)

    # filter the dataframe for the selected category
    df_filtered = df_selected_category.query(f"category == '{category_selected}'")

    # calculate the sum of total sales, the average sale amount, and the total units sold
    total_sales_sum = df_filtered["total_price"].sum()
    average_sale_amount = df_filtered["total_price"].mean()
    total_units_sold = df_filtered["quantity_sold"].sum()

    # display the calculated values
    print(f"\nSummary for {category_selected} category:")
    print(f"Total Sales: {total_sales_sum}")
    print(f"Average Sale Amount: {average_sale_amount}")
    print(f"Total Units Sold: {total_units_sold}")

    # step 5
    # grouping one row per product
    df_productSales = df_filtered.groupby("product")["total_price"].sum()

    # creating the chart
    df_productSales.plot(kind = 'bar') # creates the chart
    plot.title(f"Total Sales in {category_selected}") # adds title to the top
    plot.xlabel("Product") # label x-axis
    plot.ylabel("Total Sales") # label y-axis
    plot.show() # makes the chart pop up on the screen

else:
    print("Exiting Program")
    
