# 📊 Intern Performance Evaluation Dashboard

This repository contains a comprehensive performance evaluation system built with **Streamlit**, designed during a **Data Analytics Internship at Internee.pk**. The project evaluates interns' performance based on multiple factors such as task completion speed, project quality, and mentor feedback.

The dashboard provides a clean, interactive interface where managers or mentors can analyze, filter, visualize, and export intern-related data efficiently.

---

## 🚀 Overview

The Intern Performance Evaluation Dashboard was created with the objective of simplifying performance analysis for internship programs. It leverages **data visualization, interactive filters, and scoring metrics** to offer an insightful view into each intern's journey.

From evaluating task duration and project quality to leaderboards, departmental statistics, and personalized mentor notes — this dashboard serves as a full-stack analytics and reporting tool.

---

## 🧠 Key Features

- 📁 Load and preprocess intern data from CSV
- 🎯 Filter interns based on department, status, quality score, and date
- 📊 Interactive visualizations using Plotly and Seaborn
- 🏆 Intern leaderboard highlighting top performers with avatars
- 📝 Notes system to track individual intern feedback
- 📅 Monthly summary of performance trends
- 💡 Search functionality by Intern Name or ID
- 📤 Export data to CSV, Excel, and styled HTML tables
- 🖼️ Code snapshot gallery and downloadable assets
- 🌗 Light and Dark themes supported dynamically

---

## 🖼🎥 Dashboard Demo Video

<video controls width="700" style="max-width: 100%;">
  <source src="videos/Dashboard_Demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

## 🛠️ Tech Stack

| Layer        | Technologies                             |
|--------------|-------------------------------------------|
| Interface    | Streamlit                                |
| Data Analysis| Pandas, NumPy                            |
| Visualization| Plotly, Matplotlib, Seaborn, WordCloud   |
| Storage      | CSV, JSON                                |
| Utilities    | I/O, Styling, datetime, zipfile          |

---

## 📂 Folder Structure

```
intern-performance-evaluation/
│
├── app/
│   └── final.py                      # Main Streamlit app
│
├── data/
│   ├── intern_performance_dataset.csv        # Raw dataset
│   ├── Cleaned_Intern_Performance_Data.csv   # Cleaned dataset used in app
│   ├── intern_notes.csv                      # Notes saved as CSV
│   └── intern_notes.json                     # Notes saved as JSON
│
├── notebooks/
│   └── Intern_Performance_Evaluation_AtoZ.ipynb  # Full exploratory notebook
│
├── img/
│   ├── interneepk_logo.png            # Logo used in app
│   ├── JN1.jpg - JN8.jpg              # Code snapshots
│   └── sample_dashboard.png           # Screenshot for README
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE (optional)
```

---

## ⚙️ Installation Guide

To run the project locally on your system:

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/intern-performance-evaluation.git
cd intern-performance-evaluation
```

### 2. Create Virtual Environment (optional but recommended)
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

### 4. Launch Streamlit App
```bash
cd app
streamlit run final.py
```

---

## 📦 Required Python Packages

Here's a sample of what to include in `requirements.txt`:

```txt
streamlit
pandas
matplotlib
seaborn
plotly
wordcloud
streamlit_plotly_events
```

You can generate this file with:
```bash
pip freeze > requirements.txt
```
(Then edit out unnecessary packages)

---

## 📊 How the Dashboard Works

### 📋 Tab 1: Main Dashboard
- View key metrics (avg quality, feedback, completion days)
- Bar and pie charts per department
- Filter by department, date, score, or status
- Add mentor notes per intern
- Download full or filtered data

### 📅 Tab 2: Monthly Summary
- Average scores by month
- Performance distribution histograms
- Quality and feedback by department

### 📁 Tab 3: Full Intern Data
- Styled and color-coded intern table
- Export to HTML, Excel, or department-wise CSV

### 🏆 Tab 4: Intern Report
- Select intern and view their scores
- Top performers with avatars
- Timeline summary and notes section
- Download notes in CSV or JSON

### 📷 Tab 5: Code Snapshots
- Images of key code blocks
- Option to download all as ZIP

---

## 📥 Downloads Available

- Filtered datasets
- Full cleaned dataset
- Intern notes (CSV and JSON)
- Styled tables (HTML)
- Excel sheets
- ZIP of all code snapshots

---

## 👨‍💻 About the Author

**MadadAllah Bhatti**  
Data Analytics Intern @ [Internee.pk](https://internee.pk)  
🔗 [LinkedIn](https://www.linkedin.com) – Update with your actual profile URL

This project was built to explore real-world data analysis, dashboard development, and full-cycle reporting workflows.

---

## 📃 License

MIT License (optional)

---

## 🙌 Acknowledgments

Thanks to **Internee.pk** for the opportunity and mentoring provided during the internship. This project is part of a learning journey in building full-stack data-driven applications.
