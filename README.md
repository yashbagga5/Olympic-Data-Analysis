# OLYMPICS DATA ANALYSIS
🏅 Olympics Data Analysis Dashboard
A Streamlit-based interactive web application to explore, analyze, and visualize data from over 120 years of Olympic history.

📌 Overview
This app provides comprehensive visual insights into the Olympic Games, including:

- 🏆 Medal tallies by year and country
- 📊 Overall statistics across editions, cities, sports, events, and athletes
- 🌍 Country-wise performance analysis
- 👥 Athlete-wise insights (age, gender, sports distribution)
- 📏 Height vs. Weight scatter plots
- 📈 Participation trends over the years


📂 Project Structure
    
    ├── app.py                   # Main Streamlit application
    ├── preprocessor.py          # Data cleaning and merging logic
    ├── helper.py                # Utility functions for analysis and visualizations
    ├── athlete_events.csv       # Main dataset
    ├── noc_regions.csv          # Country mapping dataset
    ├── requirements.txt         # Required Python packages

🚀 How to Run

1 Clone the Repository:
- git clone https://github.com/yashbagga5/olympics-analysis.git
-  cd olympics-analysis


2 Install Dependencies:
- pip install -r requirements.txt


3 Place Datasets:
Ensure the following CSV files are in the project root:
- athlete_events.csv
- noc_regions.csv


4 Run the App:
- streamlit run app.py


🛠️ Technologies Used
- Python 3
- Streamlit – Web interface
- Pandas – Data manipulation
- Plotly, Seaborn, Matplotlib – Data visualizations

🔍 Features
- Interactive sidebar navigation
- Filter medal tally by country and year
- Analyze participation trends over time
- Visualize athlete distribution by age, gender, and sport
- Compare height and weight of athletes by sport and medal

📈 Future Improvements
- Real-time Olympic data integration
- Predictive analytics using machine learning
- Support for Paralympics data
- User accounts with personalized dashboards

👨‍💻 Author
- Yash Bagga
- 📧 Email: yashbagga5@gmail.com
- 🔗 GitHub: @yashbagga5
