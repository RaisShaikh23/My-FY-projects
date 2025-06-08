# 📊 iPhone Sales Analysis

This project focuses on analyzing and visualizing sales data for iPhone products using Python and Plotly. It provides insights into product ratings, pricing trends, discounts, and correlations using interactive visualizations.

## 🚀 Key Features

- ✅ Cleaned and explored real-world sales data stored in CSV format.
- 📌 Used `pandas` for efficient data manipulation and cleaning.
- 📌 Visualized trends using interactive plots with `plotly.express` and `plotly.graph_objects`.
- 🔁 Converted non-numeric RAM data (e.g., "4GB") to integer format for better visualization in size-based scatter plots.

## 🧰 Tools & Libraries Used

- **Python**
- **pandas** – for data wrangling and preprocessing
- **plotly** – for building interactive and informative visualizations

## 📁 Dataset

- Format: CSV file
- Includes fields such as: `Product Name`, `Star Rating`, `Number Of Ratings`, `Sale Price`, `Mrp`, `Discount Percentage`, `Ram`, etc.

## 📈 Visualizations & Insights

1. **Top 10 Highest Star-Rated iPhone Products**
   - 📊 **Type:** Bar Chart
   - Shows top 10 iPhones based on star ratings and their corresponding number of ratings.
   - Helps identify the most well-reviewed iPhones by users.

2. **Relationship Between Ratings, Price & Discount**
   - 📉 **Type:** Scatter Plot with Trendline
   - Compares `Number Of Ratings`, `Sale Price`, and `Discount Percentage`.
   - Observation: As the number of ratings increases, sale price tends to decrease, and discounts increase — indicating a **negative correlation**.

3. **Top 10 Lowest Priced iPhones with RAM**
   - 💸 **Type:** Scatter Plot (bubble size = RAM)
   - Highlights the cheapest iPhones, along with RAM size and price.
   - RAM values were preprocessed by removing `"GB"` and converting to integers.

4. **Correlation Between Sale Price, MRP & Discount**
   - 📈 **Type:** Scatter Plot with Trendline
   - Shows how `Sale Price` and `MRP` rise together, with discounts increasing as well — indicating a **positive correlation**.

## 📌 Conclusion

This project offers a compact yet insightful analysis of iPhone product data. With interactive visualizations and clear trends, it’s a handy tool for understanding product popularity, pricing behavior, and customer interest.

---

Feel free to ⭐ the repo if you find it useful!
