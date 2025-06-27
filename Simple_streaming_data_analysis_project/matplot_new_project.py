import pandas as pd
import matplotlib.pyplot as mtplt
y= pd.read_csv("fictional_streaming_dataset.csv")
duplic = y.drop_duplicates()

#Checking Null Values:
print(duplic.info())

# Checking No Of Movies & Webseries 
type_count = duplic["type"].value_counts()
print(type_count) 

# Bar : Number Of Movies & Webseries

mtplt.bar(type_count.index , type_count , color = ["skyblue" , "pink"] , edgecolor = "black" , label = ["Webseries" , "Movies"])
for i , value in enumerate(type_count):
    mtplt.text(i,value,value,ha="center",va="bottom")
mtplt.legend()
mtplt.xlabel("Types")
mtplt.ylabel("No Of Released")
mtplt.title("No Of Movies/Webseries")
mtplt.tight_layout()
mtplt.savefig("Barplot1")
mtplt.show()

# Pie : Analysing Types Of Rated Movie From Dataset

rating_count = duplic["rating"].value_counts()
mtplt.pie(rating_count , labels=rating_count.index , autopct="%1.1f%%")
mtplt.title("Types Of Rating In %")
mtplt.tight_layout()
mtplt.savefig("Pieplot2")
mtplt.show()

# hist : "Analysing Duration Of No Of Movies In Dataset"

movie_type = duplic[duplic["type"]=="Movie"]
movie_dur = movie_type["duration"].str.replace("min"," ").astype("i")

mtplt.hist(movie_dur ,color="teal", edgecolor = "black")
mtplt.xlabel("Duration In Min")
mtplt.ylabel("No Of Movies")
mtplt.title("Analysing Duration Of No Of Movies In Dataset")
mtplt.tight_layout()
mtplt.savefig("histplot3")
mtplt.show()

#Scatter : Analysing No Of Movies/Webseries Released Throughtout The Yrs

release = duplic["release_year"].value_counts().sort_index()
mtplt.scatter(release.index , release.values , color = "darkgreen" , marker="o")
mtplt.grid(linestyle="--" , linewidth=1 , color="black")
mtplt.xlabel("Years")
mtplt.ylabel(("No Of Movies Release"))
mtplt.title("No Of Movies/Webseries Released Throughtout The Yrs")
mtplt.tight_layout()
mtplt.savefig("scatterplot4")
mtplt.show()

# Barh(Horizontal Bar): Top 5 Highest Movie/Webseries Released Country Wise

country_count = duplic["country"].value_counts().head()
mtplt.barh(country_count.index , country_count.values ,color=["red","purple","blue","teal","orange"] , edgecolor="black")
mtplt.title("Top 5 Highest Movie/Webseries Released Country")
mtplt.xlabel("No Of Movie Released")
mtplt.ylabel("Country")
mtplt.savefig("barh5")
mtplt.show()

# Subplots : Top 5 Highest Movies/Webseries Released Years

grp_data = duplic.groupby(["release_year" ,"type"]).size().unstack()

top_movies = grp_data["Movie"].sort_values(ascending=False).head()

top_webseries = grp_data["Web Series"].sort_values(ascending=False).head()


fig , ax = mtplt.subplots(1,2,figsize=(10,5))

ax[0].scatter(top_movies.index , top_movies.values , color="black" , marker="o" , label="Movie")
ax[0].scatter(top_webseries.index , top_webseries.values , color="blue" , marker="o" , label="Webseries")
ax[0].legend()
ax[0].set_xlabel("Released Year")
ax[0].set_ylabel("No Of Movies/Webseries Released")
ax[0].grid(linestyle="--" , linewidth = 1 , color="teal")

ax[1].bar(top_movies.index , top_movies.values , color="black" , label="Movie")
ax[1].bar(top_webseries.index , top_webseries.values , color="blue" , label="Webseries")
ax[1].legend()
ax[1].set_xlabel("Released Year")
ax[1].set_ylabel("No Of Movies/Webseries Released")
mtplt.tight_layout()
mtplt.suptitle("Top 5 Highest Movies/Webseries Released Years")
mtplt.tight_layout()
mtplt.savefig("subplot6")
mtplt.show()


