import pandas as pd
import plotly.express as plx
data = pd.read_csv("apple_products.csv")

# checking dataset Missing value:
print(data.isnull().sum()) # No Null Value
print(data.info())

# Top 10 Product Name On Basis Of Star Rating
sort_rating = data.sort_values(by=["Star Rating"] , ascending=[False]).head(10)


high_model_sale = sort_rating["Product Name"].value_counts()
prod_name = high_model_sale.index

Rating = sort_rating["Number Of Ratings"]

# figure 1 Bar Chart
fig1 = plx.bar(sort_rating , x=prod_name , y=Rating , title="Top 10 highest star rating iphone product & its No of rating")
fig1.show()

# figure 2 Relation Ship between two points using scatter diagram

fig2 = plx.scatter(data_frame=data , x="Number Of Ratings" , y="Sale Price" , size="Discount Percentage" , trendline="ols" , title="Realtionships between sales price and number of rating of iphone")
fig2.show()

# # figure 3 Top 10 lowest Price Iphone with Price & Ram 
mrp_sort = data.sort_values(by=["Sale Price"], ascending=[True]).head(10)

int_ram = mrp_sort["Ram"].str.replace("GB","").astype("int") # Change Ram into int datatype by replacing GB into " "(empty space).

fig3 = plx.scatter(mrp_sort , x="Product Name" , y="Sale Price" , size= int_ram , labels={"size":"RAM(GB)"} , title="Top 10 lowest Price Iphone with Price & Ram")
fig3.show()

# # figure 4 Sale Price increase silmationusly mrp increase inversly discount pct decrease 

fig4 = plx.scatter(data_frame=data , x="Sale Price" , y="Mrp" , size="Discount Percentage" , trendline="ols" , title="Relation between sale price , mrp and discount percentage")
fig4.show()