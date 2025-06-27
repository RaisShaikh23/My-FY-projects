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
---
Bar : Number Of Movies & Webseries


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
