# Istanbul-Price-Prediction
This project uses data scraped from [Hepsiemlak](https://www.hepsiemlak.com/) to analyze and forecast Istanbul real estate prices.
It has a complete pipeline: data scraping, cleaning, EDA, model training, and deployment through Streamlit.

---

## 📦 Project Structure
├── Scrapper_House.py         # Selenium-based scraper (Hepsiemlak listings)
├── scraped_data3.csv         # Raw dataset from scraping
├── Price_Prediction.ipynb    # Jupyter notebook for EDA & model building
├── streamlit_hosue.py        # Interactive app using Streamlit
├── real_estate_price_model.pkl  # Trained regression model (saved with joblib)
├── requirements.txt          # Dependencies for deployment
└── README.md

## 🚀 Features

- 🧠 Predict real estate prices based on user inputs (size, rooms, age, etc.)
- 📊 Visualize average price per m² across Istanbul districts
- 🗺️ Interactive Folium map for geographical price overview
- 🔍 Includes Jupyter notebook with  EDA and feature engineering

---

## 📉 Data Source

Data is scraped from  [Hepsiemlak](https://www.hepsiemlak.com/istanbul-satilik) using a custom Selenium-based scraper.

---

## 🛠️ Installation

```bash
git clone https://github.com/paoins/Istanbul-Price-Prediction.git
cd Istanbul-Price-Prediction
pip install -r requirements.txt
