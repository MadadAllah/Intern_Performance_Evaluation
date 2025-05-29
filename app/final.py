# ----------------------------------------------
# 📦 Imports
# ----------------------------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud 
import time
import io
import os
import json
import pandas as pd
import datetime
from streamlit_plotly_events import plotly_events


# 🔄 Load existing notes if available
NOTES_CSV = "intern_notes.csv"
NOTES_JSON = "intern_notes.json"

if os.path.exists(NOTES_CSV):
    notes_df = pd.read_csv(NOTES_CSV)
else:
    notes_df = pd.DataFrame(columns=["Intern ID", "Note"])

if os.path.exists(NOTES_JSON):
    with open(NOTES_JSON, "r") as f:
        notes_json = json.load(f)
else:
    notes_json = {}

# ----------------------------------------------
# ⚙️ Streamlit Page Config & Logo
# ----------------------------------------------
st.set_page_config(page_title="Intern Performance Dashboard", layout="wide")
st.markdown("""
    <style>
        .stDataFrame th {
            background-color: #f0f0f0;
            color: #333;
            font-weight: bold;
            text-align: center;
        }

        .stDataFrame td {
            padding: 10px;
        }

        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }

        .stTabs [role="tablist"] {
            border-bottom: 2px solid #e0e0e0;
            margin-bottom: 20px;
        }

        .stTabs [role="tab"] {
            font-size: 16px;
            padding: 8px 12px;
            font-weight: 600;
            border: 1px solid transparent;
            border-radius: 6px 6px 0 0;
        }

        .stTabs [aria-selected="true"] {
            border: 1px solid #ccc;
            border-bottom: none;
            background-color: #f5f5f5;
        }

        .stMetric {
            text-align: center !important;
            background-color: #f2f2f2 !important;
            border-radius: 12px;
            padding: 1em !important;
            color: #222 !important;
        }

        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            font-size: 15px;
        }

        .stButton>button {
            border-radius: 10px;
            background-color: #4CAF50;
            color: white;
            padding: 0.5em 1em;
        }
        /* Hover row highlight in tables */
        tbody tr:hover {
            background-color: #e8f0fe !important;
            color: #000000 !important;
        }

        }
    </style>
""", unsafe_allow_html=True)



logo_path = "img/interneepk_logo.png"
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo_path, width=280)
with col2:
    st.markdown(
        """
        <h1 style='font-size: 28px; margin-bottom: 0;'>Intern Performance Evaluation Dashboard</h1>
        <p style='color: gray; font-size: 16px;'>Built during Data Analyst Internship @ Internee.pk</p>
        """,
        unsafe_allow_html=True
    )


# ----------------------------------------------
# 🧾 Load & Clean Data
# ----------------------------------------------

df = pd.read_csv("Cleaned_Intern_Performance_Data.csv", parse_dates=["Date of Assignment", "Date of Completion"])

# ----------------------------------------------
# 🔍 Sidebar Filters (with Tooltips)
# ----------------------------------------------
st.sidebar.header("🧰 Filter Data")
# Count interns per department/status dynamically
dept_counts = df["Department"].value_counts().to_dict()
status_counts = df["Completion_Status"].value_counts().to_dict()

selected_depts = st.sidebar.multiselect(
    "🏢 Department",
    options=[f"{dept} ({dept_counts[dept]})" for dept in dept_counts],
    default=[f"{dept} ({dept_counts[dept]})" for dept in dept_counts],
    key="multiselect_1",
    help="Filter interns based on their department"
)

selected_status = st.sidebar.multiselect(
    "✅ Completion Status",
    options=[f"{stat} ({status_counts[stat]})" for stat in status_counts],
    default=[f"{stat} ({status_counts[stat]})" for stat in status_counts],
    key="multiselect_2",
    help="Filter by completion status"
)

# Extract only the names from formatted values like "Marketing (12)"
selected_depts = [x.split(" (")[0] for x in selected_depts]
selected_status = [x.split(" (")[0] for x in selected_status]


quality_range = st.sidebar.slider(
    "🎚️ Filter by Quality Score", 0.0, 10.0, (0.0, 10.0),
    key="slider_1"
)

theme = st.sidebar.radio(
    "🖌️ Choose Theme", ["Light", "Dark"],
    key="radio_1"
)

# 🎨 Apply Dark/Light mode styling
if theme == "Dark":
    st.markdown("""
        <style>
            html, body, [class*="css"] {
                background-color: #0e1117 !important;
                color: #e0e0e0 !important;
            }
            .stDataFrame {
                background-color: #1e1e1e !important;
            }
            .stButton>button {
                background-color: #1f77b4 !important;
                color: white !important;
            }
            .stMetric {
                background-color: #1e1e1e !important;
                border-radius: 10px;
                padding: 0.8em;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            html, body, [class*="css"] {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            .stDataFrame {
                background-color: #f9f9f9 !important;
            }
            .stButton>button {
                background-color: #4CAF50 !important;
                color: white !important;
            }
            .stMetric {
                background-color: #f2f2f2 !important;
                border-radius: 10px;
                padding: 0.8em;
            }
        </style>
    """, unsafe_allow_html=True)



# Calculate min and max dates for date filter (move this earlier!)
df["Date of Assignment"] = pd.to_datetime(df["Date of Assignment"])
min_date = df["Date of Assignment"].min()
max_date = df["Date of Assignment"].max()


# 🔄 Reset Filters Button
if st.sidebar.button("🔁 Reset All Filters"):
    st.session_state["multiselect_1"] = list(df["Department"].unique())
    st.session_state["multiselect_2"] = list(df["Completion_Status"].unique())
    st.session_state["slider_1"] = (0.0, 10.0)
    st.session_state["radio_1"] = "Light"
    st.session_state["date_input_1"] = min_date
    st.session_state["date_input_2"] = max_date
    st.session_state["text_input_1"] = ""
    st.experimental_rerun()

# selected_depts = st.sidebar.multiselect("🏢 Department", df["Department"].unique(), default=df["Department"].unique(), help="Filter interns based on their department", key="depts_slider")
# selected_status = st.sidebar.multiselect("✅ Completion Status", df["Completion_Status"].unique(), default=df["Completion_Status"].unique(), help="Filter by completion status", key="status_slider")
# quality_range = st.sidebar.slider("🎚️ Filter by Quality Score", 0.0, 10.0, (0.0, 10.0), key="quality_slider")
# theme = st.sidebar.radio("🖌️ Choose Theme", ["Light", "Dark"], key="theme_slider")

# if theme == "Dark":
#     st.markdown("<style>body { background-color: #111; color: #eee; }</style>", unsafe_allow_html=True)

# # Apply sidebar filters
# df = df[(df["Department"].isin(selected_depts)) & (df["Completion_Status"].isin(selected_status))]
# df = df[(df["Project_Quality_Score"] >= quality_range[0]) & (df["Project_Quality_Score"] <= quality_range[1])]

# ----------------------------------------------
# 🔄 Spinner
# ----------------------------------------------
with st.spinner("🔄 Processing data..."):
    time.sleep(1)

# ----------------------------------------------
# 📆 Date Range Filter & Search Box
# ----------------------------------------------
# Convert to datetime if not already
df["Date of Assignment"] = pd.to_datetime(df["Date of Assignment"])

# Calculate min and max dates
min_date = df["Date of Assignment"].min()
max_date = df["Date of Assignment"].max()

# Date input fields for filtering
start_date = st.sidebar.date_input(
    "📅 Start Date", value=min_date, min_value=min_date, max_value=max_date,
    key="date_input_1"
)

end_date = st.sidebar.date_input(
    "📅 End Date", value=max_date, min_value=min_date, max_value=max_date,
    key="date_input_2"
)

# Validate the date range
if start_date > end_date:
    st.sidebar.warning("⚠️ Start date should be before end date.")
else:
    df = df[(df["Date of Assignment"] >= pd.to_datetime(start_date)) & (df["Date of Assignment"] <= pd.to_datetime(end_date))]

search_term = st.text_input(
    "🔍 Search Intern by Name or ID",
    help="Type part of an intern's name or ID to filter",
    key="text_input_1"
)


# search_term = st.text_input("🔍 Search Intern by Name or ID", help="Type part of an intern's name or ID to filter")
# if search_term:
#     df = df[df["Intern Name"].str.contains(search_term, case=False) | df["Intern ID"].astype(str).str.contains(search_term)]

# ----------------------------------------------
# 🧮 Monthly Summary Aggregation
# ----------------------------------------------
monthly_summary = df.groupby("Month").agg({
    'Task_Completion_Days': 'mean',
    'Project_Quality_Score': 'mean',
    'Mentor_Feedback_Score': 'mean'
}).reset_index()

month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
monthly_summary['Month'] = pd.Categorical(monthly_summary['Month'], categories=month_order, ordered=True)
monthly_summary = monthly_summary.sort_values('Month')

# ----------------------------------------------
# ✨ Styling Functions
# ----------------------------------------------
def style_main_df(df):
    def feedback_color(val):
        return 'background-color: red' if val < 3 else ''
    
    def quality_color(val):
        return 'background-color: orange' if val < 6 else ''
    
    def task_days_gradient(val):
        from matplotlib import cm
        norm = (val - df['Task_Completion_Days'].min()) / (df['Task_Completion_Days'].max() - df['Task_Completion_Days'].min())
        rgba = cm.get_cmap('Blues')(norm)
        r, g, b, _ = [int(255 * x) for x in rgba]
        return f'background-color: rgb({r},{g},{b})'
    
    return df.style\
        .applymap(feedback_color, subset=['Mentor_Feedback_Score'])\
        .applymap(quality_color, subset=['Project_Quality_Score'])\
        .applymap(task_days_gradient, subset=['Task_Completion_Days'])\
        .format({
            'Task_Completion_Days': '{:.1f}',
            'Project_Quality_Score': '{:.1f}',
            'Mentor_Feedback_Score': '{:.1f}'
        })

# ----------------------------------------------
# 📊 Main Tabs Layout
# ----------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard", 
    "📅 Monthly Summary", 
    "📁 Full Intern Data", 
    "🏆 Intern Report",
    "📷 Code Snapshots"
    
])

# ----------------------------------------------
# 📊 Tab 1: Dashboard
# ----------------------------------------------
with tab1:
    st.subheader("📊 Main Dashboard Charts")
    
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3 = st.columns(3)

    metric_card_style = """
    <style>
    .metric-box {
        background-color: #1e1e1e;
        color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-top: 5px;
    }
    .metric-label {
        font-size: 14px;
        color: #ccc;
        text-align: center;
        margin-bottom: 0;
    }
    </style>
    """

    st.markdown(metric_card_style, unsafe_allow_html=True)

    with col1:
        st.markdown("<div class='metric-label'>Average Completion Days</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'>{df['Task_Completion_Days'].mean():.1f}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-label'>Average Quality Score</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'>{df['Project_Quality_Score'].mean():.1f}</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='metric-label'>Average Feedback Score</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'>{df['Mentor_Feedback_Score'].mean():.1f}</div>", unsafe_allow_html=True)


    st.subheader("📌 Quality Score by Department")
    fig = px.bar(
    df,
    x='Department',
    y='Project_Quality_Score',
    color='Department',
    title='Quality by Department',
    hover_data=['Intern Name', 'Project_Quality_Score'])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Task Duration by Assignment Date")
    fig = px.bar(df, x="Date of Assignment", y="Task_Completion_Days", title="Task Completion Duration per Assignment", color="Department")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 Top 5 Interns by Project Quality Score")
    top_interns = df.sort_values(by='Project_Quality_Score', ascending=False).head(5)
    st.table(top_interns[['Intern Name', 'Project_Quality_Score']])

    # Simulate textual feedback from numerical score
    def map_score_to_feedback(score):
        if score == 5:
            return "Excellent support and communication"
        elif score == 4:
            return "Very helpful mentor and clear instructions"
        elif score == 3:
            return "Satisfactory performance with room to improve"
        elif score == 2:
            return "Needs better guidance and structure"
        else:
            return "Poor mentoring experience"

    # Create feedback column
    df["Mentor Feedback"] = df["Mentor_Feedback_Score"].apply(map_score_to_feedback)

    # Count feedback frequencies
    feedback_counts = df["Mentor Feedback"].value_counts().reset_index()
    feedback_counts.columns = ["Feedback", "Count"]

    st.subheader("🥧 Mentor Feedback Distribution")
    fig = px.pie(feedback_counts, names="Feedback", values="Count", title="Mentor Feedback Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("📊 Main Dashboard Loaded Successfully!")


    # ----------------------------------------------
    # 🗒️ Activity Notes 
    # ----------------------------------------------
    st.subheader("🗒️ Activity Notes ")

    selected_intern = st.selectbox("Select Intern ID to add/view notes", df["Intern ID"].unique(), key='selectbox_1')
    existing_note = notes_json.get(str(selected_intern), "")  
    note = st.text_area("Write your reflection for this intern:", value=existing_note, key="text_area_1")

    if st.button("💾 Save Note", key='button_1'):
        # Update dictionary & DataFrame
        notes_json[str(selected_intern)] = note
        updated_row = {"Intern ID": selected_intern, "Note": note}

        # Remove old entry if exists
        notes_df = notes_df[notes_df["Intern ID"] != selected_intern]
        # Append updated note
        notes_df = pd.concat([notes_df, pd.DataFrame([updated_row])], ignore_index=True)

        # Save to both CSV and JSON
        notes_df.to_csv(NOTES_CSV, index=False)
        with open(NOTES_JSON, "w") as f:
            json.dump(notes_json, f, indent=4)

        st.success("✅ Note saved successfully!")
            
    st.download_button("📥 Download Cleaned Dataset as CSV", data=df.to_csv(index=False), file_name="Cleaned_Intern_Performance.csv", mime="text/csv")
    st.download_button("📥 Download Filtered Data", data=df.to_csv(index=False), file_name="filtered_intern_data.csv", mime="text/csv")

    st.markdown("""<hr style='margin-top: 40px; margin-bottom: 5px;'>""", unsafe_allow_html=True)
    st.markdown("<center>Made by <b>MadadAllah Bhatti</b> during internship @ <a href='https://internee.pk'>Internee.pk</a></center>", unsafe_allow_html=True)

# ----------------------------------------------
# 📅 Tab 2: Monthly Summary
# ----------------------------------------------
with tab2:
    st.subheader("📅 Monthly Summary")
    st.markdown("### 📈 Average Metrics by Month")

    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_summary.set_index('Month')[['Task_Completion_Days', 'Project_Quality_Score', 'Mentor_Feedback_Score']].plot(kind='bar', ax=ax)
    plt.ylabel("Average Score")
    plt.title("Monthly Averages")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    st.pyplot(fig)

    def highlight_low_feedback(val): return 'background-color: red' if val < 3 else ''
    def highlight_low_quality(val): return 'background-color: orange' if val < 6 else ''
    def blue_to_green(val):
        from matplotlib import cm
        norm_val = (val - df["Task_Completion_Days"].min()) / (df["Task_Completion_Days"].max() - df["Task_Completion_Days"].min())
        rgba = cm.get_cmap('BuGn')(norm_val)
        r, g, b, _ = [int(255*x) for x in rgba]
        return f'background-color: rgb({r},{g},{b})'

    styled_summary = monthly_summary.style\
        .applymap(highlight_low_feedback, subset=["Mentor_Feedback_Score"])\
        .applymap(highlight_low_quality, subset=["Project_Quality_Score"])\
        .applymap(blue_to_green, subset=["Task_Completion_Days"])\
        .format({
            'Task_Completion_Days': '{:.1f}',
            'Project_Quality_Score': '{:.1f}',
            'Mentor_Feedback_Score': '{:.1f}'
        })

    st.markdown("### 📋 Monthly Performance Summary Table (With Highlights)")
    st.dataframe(styled_summary, use_container_width=True)
    
    st.subheader("⏳ Task Completion Time Distribution")
    fig1, ax1 = plt.subplots()
    sns.histplot(df['Task_Completion_Days'].dropna(), bins=30, ax=ax1, color='skyblue')
    st.pyplot(fig1)

    st.subheader("📋 Avg Project Quality by Department")
    fig2, ax2 = plt.subplots()
    df.groupby("Department")["Project_Quality_Score"].mean().plot(kind='barh', ax=ax2, color='mediumseagreen')
    st.pyplot(fig2)

    st.subheader("💬 Avg Mentor Feedback by Department")
    fig3, ax3 = plt.subplots()
    df.groupby("Department")["Mentor_Feedback_Score"].mean().plot(kind='barh', ax=ax3, color='salmon')
    st.pyplot(fig3)

# ----------------------------------------------
# 📁 Tab 3: Full Intern Data
# ----------------------------------------------
with tab3:
    st.subheader("📁 Full Intern Data")
    styled_full = style_main_df(df)
    st.dataframe(styled_full, use_container_width=True)

    # Export HTML
    html_buffer = io.StringIO()
    styled_full.to_html(buf=html_buffer)
    html_content = html_buffer.getvalue()
    with open("styled_table.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # Export Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Intern Data')
    excel_data = excel_buffer.getvalue()

    st.markdown("### 📤 Export Styled Data")
    st.download_button("⬇️ Download Styled Table (HTML)", data=html_content, file_name="styled_table.html", mime="text/html")
    st.download_button("⬇️ Download Intern Data (Excel)", data=excel_data, file_name="intern_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.markdown("### 📂 Download Data by Department")
    for dept in df["Department"].unique():
        dept_df = df[df["Department"] == dept]
        st.download_button(f"⬇️ Download {dept} Data", data=dept_df.to_csv(index=False), file_name=f"{dept}_data.csv", mime="text/csv")

# ----------------------------------------------
# 📷 Tab 4: Intern Report
# ----------------------------------------------
with tab4:
    # 📋 Individual Intern Report Card
    st.subheader("📋 Individual Intern Report Card")
    selected_intern = st.selectbox("🔍 Choose Intern", df['Intern Name'].unique(), key='selectbox_2')
    data = df[df['Intern Name'] == selected_intern]
    st.write("📊 Average Scores:")
    st.dataframe(data[['Task_Completion_Days', 'Project_Quality_Score', 'Mentor_Feedback_Score']].mean().round(2))

    # 🏆 Top Performing Interns Leaderboard
    st.subheader("🏅 Intern Leaderboard with Avatars")

    top_n = 5
    top_interns = df.sort_values("Project_Quality_Score", ascending=False).head(top_n).reset_index(drop=True)

    # Add avatars
    import random
    avatar_links = [
        "https://avatars.dicebear.com/api/identicon/a.svg",
        "https://avatars.dicebear.com/api/identicon/b.svg",
        "https://avatars.dicebear.com/api/identicon/c.svg",
        "https://avatars.dicebear.com/api/identicon/d.svg",
        "https://avatars.dicebear.com/api/identicon/e.svg"
    ]
    top_interns["Avatar"] = [random.choice(avatar_links) for _ in range(len(top_interns))]

    medals = ["🥇", "🥈", "🥉", "🎖️", "🏅"]
    top_interns["Rank"] = [f"{medals[i]} {i+1}" for i in range(len(top_interns))]

    # Show leaderboard
    for i, row in top_interns.iterrows():
        # Improved Leaderboard Card with Dark Mode Support
        st.markdown(f"""
            <div style='
                display: flex; 
                align-items: center; 
                justify-content: flex-start;
                background-color: #f9f9f9;
                padding: 10px 15px;
                border-radius: 8px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                color: #111;
                font-size: 14px;
                transition: all 0.2s ease;
            '
            onmouseover="this.style.backgroundColor='#e6f7ff';"
            onmouseout="this.style.backgroundColor='#f9f9f9';">
                <img src='{row["Avatar"]}' style='width: 36px; height: 36px; border-radius: 50%; margin-right: 12px;'>
                <div>
                    <strong style="font-size: 15px;">{row['Rank']} - {row['Intern Name']}</strong><br>
                    <span>Dept: {row['Department']} | ⭐ {row['Project_Quality_Score']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)




    st.markdown("### 🗒️ Summary Table")
    st.table(top_interns[["Rank", "Intern ID", "Intern Name", "Department", "Project_Quality_Score"]])
    
    st.markdown("### 🕒 Timeline Summary (Sample)")
    st.markdown("""
    - ✅ **2025-05-01**: Task Assigned  
    - 📌 **2025-05-05**: Mid Project Review  
    - 📝 **2025-05-10**: Final Feedback Logged  
    """)

    
    # 🗒️ Intern Progress Notes
    st.subheader("🗒️ Intern Progress Notes")

    # Load notes if not loaded already
    NOTES_CSV = "intern_notes.csv"
    NOTES_JSON = "intern_notes.json"

    if os.path.exists(NOTES_CSV):
        notes_df = pd.read_csv(NOTES_CSV)
    else:
        notes_df = pd.DataFrame(columns=["Intern ID", "Note"])

    if os.path.exists(NOTES_JSON):
        with open(NOTES_JSON, "r") as f:
            notes_json = json.load(f)
    else:
        notes_json = {}

    # Get Intern ID from selected name
    intern_id = int(df[df["Intern Name"] == selected_intern]["Intern ID"].values[0])
    existing_note = notes_json.get(str(intern_id), "")

    new_note = st.text_area("🗒️ Enter Note for this Intern", value=existing_note, height=150, key="text_area_2")

    if st.button("💾 Save Note", key='button_2'):
        # Save note to JSON and CSV
        notes_json[str(intern_id)] = new_note

        notes_df = pd.DataFrame.from_dict(notes_json, orient="index", columns=["Note"]).reset_index()
        notes_df.rename(columns={"index": "Intern ID"}, inplace=True)
        notes_df.to_csv(NOTES_CSV, index=False)

        with open(NOTES_JSON, "w") as f:
            json.dump(notes_json, f, indent=4)

        # Get intern name and timestamp
        intern_name = selected_intern
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Display confirmation messages
        st.success("✅ Note saved successfully!")
        st.success(f"🧑‍💼 Intern: **{intern_name}**")
        st.success(f"🕒 Saved on: {timestamp}")
        st.success("📘 Intern report updated successfully!")

    # 📥 Download buttons
    st.download_button("📤 Download Notes as CSV", data=notes_df.to_csv(index=False), file_name="intern_notes.csv", mime="text/csv")
    st.download_button("📤 Download Notes as JSON", data=json.dumps(notes_json, indent=2), file_name="intern_notes.json", mime="application/json")

    # ✅ Final Success message scoped to this tab
    st.success("📊 Intern Report Loaded Successfully!")

# ----------------------------------------------
# 📷 Tab 5: Code Snapshots
# ----------------------------------------------
import zipfile
import os

# 📷 Tab 5: Code Snapshots with Styling & Single ZIP Download
with tab5:
    st.subheader("📷 Code Snapshots")

    # 💅 Inject CSS
    st.markdown("""
        <style>
            .img-card {
                background-color: #f8f8f8;
                padding: 12px;
                border-radius: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                margin-bottom: 20px;
                transition: transform 0.2s ease;
            }

            .zoom-img {
                border-radius: 6px;
                transition: transform 0.3s ease-in-out;
            }

            .zoom-img:hover {
                transform: scale(1.03);
            }

            .stDownloadButton > button {
                background-color: #007BFF;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # 🖼️ Show images in styled cards (no buttons)
    for i in range(1, 9):
        st.markdown("<div class='img-card'>", unsafe_allow_html=True)
        st.image(f"img/JN{i}.jpg", caption=f"JN{i}", use_column_width=True, output_format="JPEG")
        st.markdown("</div>", unsafe_allow_html=True)

    # 📦 Download All as ZIP
    st.markdown("### 📦 Download All Snapshots")
    zip_filename = "all_snapshots.zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for i in range(1, 9):
            zipf.write(f"img/JN{i}.jpg", arcname=f"JN{i}.jpg")

    with open(zip_filename, "rb") as zip_file:
        st.download_button(
            label="📥 Download All as ZIP",
            data=zip_file,
            file_name="all_snapshots.zip",
            mime="application/zip",
            key="download_all"
        )

# ----------------------------------------------
# ----------------------------------------------

st.markdown("""
    <style>
        .scroll-top {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background-color: #4CAF50;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            z-index: 9999;
        }
    </style>
    <div class="scroll-top" onclick="window.scrollTo({top: 0, behavior: 'smooth'});">
        ⬆️ Back to Top
    </div>
""", unsafe_allow_html=True)
