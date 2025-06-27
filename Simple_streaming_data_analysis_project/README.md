## 📊 Streaming Content Analysis using Matplotlib

This simple data analysis project uses Python and Matplotlib to visualize trends and patterns in a fictional streaming dataset. 
The dataset includes over **8,000+ entries** of movies and web series released across various countries, years, and content ratings.

---

### 📁 Project Files

* `matplot_new_project.py` – The main Python script that reads, processes, and visualizes the dataset.
* `fictional_streaming_dataset.csv` – Dataset containing over 8000+ rows of streaming content information like title, type, rating, duration, country, and release year.

---

### 🔍 Key Features

* **Data Cleaning:**

  * Removes duplicate entries
  * Checks for null values

* **Visualizations:**

  1. **Bar Chart** – Number of Movies vs Web Series
  2. **Pie Chart** – Distribution of Content Ratings
  3. **Histogram** – Duration distribution of Movies
  4. **Scatter Plot** – Number of releases per year
  5. **Horizontal Bar Chart** – Top 5 countries by total releases
  6. **Subplots (Scatter & Bar)** – Top 5 years with most Movie/Web Series releases

---

### 📈 Sample Insights

* Most of the content is either **Movies** or **Web Series**, with a significant rating spread.
* Duration varies widely among movies, typically clustering between short and medium-length films.
* Some countries contribute far more to content production.
* There are peak years in terms of content release frequency.

---
### Analysis Examles :

Bar Plot: Number Of Movies & Webseries

![image alt](https://github.com/RaisShaikh23/My-FY-projects/blob/98be409587b0773c3ce4b15e2630e1aa27d14f99/Simple_streaming_data_analysis_project/Barplot1.png)

Pie Plot: Analysing Types Of Rated Movie/Webseries From Dataset

![image alt](https://github.com/RaisShaikh23/My-FY-projects/blob/335f312fbdf7d5b1c50f4e900052fe35388ed0df/Simple_streaming_data_analysis_project/Pieplot2.png)

Hist Plot: Analysing Duration Of No Of Movies From Dataset

![image alt](https://github.com/RaisShaikh23/My-FY-projects/blob/58603307b34d79534c58089ba65cf0376e8b5e05/Simple_streaming_data_analysis_project/histplot3.png)

Scatter Plot: Analysing No Of Movies/Webseries Released Throughtout The Yrs

![image alt](https://github.com/RaisShaikh23/My-FY-projects/blob/478cd9675cfb7f17bd132053d42f31153b5c93bb/Simple_streaming_data_analysis_project/scatterplot4.png)

Barh(vertical bar)plot: Top 5 Highest Movies/Webseries Released Country Wise

![iamge alt](https://github.com/RaisShaikh23/My-FY-projects/blob/478cd9675cfb7f17bd132053d42f31153b5c93bb/Simple_streaming_data_analysis_project/barh5.png)

Subplots: Top 5 Highest Movies/Webseries Released Years

![image alt](https://github.com/RaisShaikh23/My-FY-projects/blob/817bc4a597f847471057cbda42e0629394487746/subplot6.png)

---
### 🧪 How to Run

1. Install dependencies (if not already):

   ```bash
   pip install pandas matplotlib
   ```

2. Run the script:

   ```bash
   python matplot_new_project.py
   ```

3. View the generated visualizations in separate windows.

---

### 💡 Future Improvements

* Add interactivity using `plotly` or `seaborn`
* Save visualizations to image files
* Add filtering options (by country, year, rating)

---
Feel free to ⭐ the repo if you find it useful!
---
### 🏷️ Tags

`#Python` `#Matplotlib` `#DataVisualization` `#Pandas` `#StreamingAnalysis` `#SimpleProject`
