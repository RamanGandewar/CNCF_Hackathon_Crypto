# 📈 Real-Time Cryptocurrency Price Monitoring Pipeline

A **Python-based solution** for fetching, processing, and visualizing live crypto prices.

---

## ✨ Overview

This project showcases a streamlined data pipeline designed to **track and visualize cryptocurrency prices in near real-time**. Primarily built for use in **Google Colab**, it offers a hands-on example of constructing a robust data flow — from raw data ingestion to actionable insights and dynamic visualizations.

It continuously fetches live price data for selected cryptocurrencies (like **Bitcoin** and **Ethereum**) against specified fiat currencies (USD, INR) using a public API. This raw data is then processed, aggregated over time, and finally rendered into an insightful **time-series plot**.

---

## 🚀 Features at a Glance

- 🔄 **Live Data Ingestion**: Seamlessly pulls current market data directly from the **CoinGecko API**.
- 🧠 **Efficient Data Processing**: Leverages `pandas` for robust data manipulation, cleaning, and structuring.
- ⏱ **Time-Series Data Collection**: Simulates continuous monitoring by collecting data points at regular intervals.
- 📦 **Unified Data Aggregation**: Combines all collected data into a single dataset for holistic analysis.
- 📊 **Dynamic Visualization**: Utilizes `matplotlib` to generate clear and insightful line plots.
- 🧩 **Modular Pipeline Design**: Code is structured into distinct, reusable functions.
- 🛡 **Basic Error Handling**: Includes `try-except` blocks to handle API failures gracefully.

---

## 📂 Project Structure

.
├── main.py # The core Python script containing the data pipeline
└── output/
└── crypto_price_trend.png # The generated cryptocurrency price trend plot


---

## ▶️ How to Run in Google Colab

### 🔧 Prerequisites
- A Google Account to access Google Colab.

### 🪜 Step-by-Step Instructions

1. **Open Google Colab**  
   Navigate to [Google Colab](https://colab.research.google.com).

2. **Create a New Notebook**  
   Go to `File > New notebook`.

3. **Paste the Code**  
   Copy the content of `main.py` and paste it into the first cell of the Colab notebook.

4. **Run the Cell**  
   Click ▶️ or press `Shift + Enter` to execute.

5. **Access the Results**  
   - Once complete, a plot named `crypto_price_trend.png` will be generated.
   - Click the 📁 **Files** icon in the left sidebar.
   - Navigate to the `output/` folder to preview or download the plot.

---

## 👨‍💻 Core Pipeline Stages

### 1. ⚙️ Configuration
Defines parameters like:
- Number of iterations
- Delay between API calls
- Cryptocurrency IDs (e.g., `bitcoin,ethereum`)
- Fiat currencies (e.g., `usd,inr`)

### 2. 📊 Data Collection & Processing Loop
Function: `collect_and_process_multiple_times()`

- **Ingestion** (`get_crypto_price_data`)  
  Fetches real-time data from CoinGecko API.

- **Processing** (`process_crypto_data`)  
  Converts raw JSON to structured `pandas` DataFrame.

- **Aggregation**  
  Appends each cleaned record to a global dataset.

- **Delay**  
  Introduces `time.sleep()` between each poll.

### 3. 📉 Visualization & Output
Function: `visualize_crypto_prices()`

- Generates a time-series plot using `matplotlib`.
- Saves the image as `crypto_price_trend.png` under `output/`.

---

## 🛠️ Technologies Used

- **Python 3**
- `pandas` — data analysis and manipulation
- `matplotlib` — data visualization
- `requests` — for API integration
- **CoinGecko API** — real-time cryptocurrency price feed

---

## 💡 Future Enhancements

- 🔧 Move configuration to external `config.json` or `.ini` file.
- ☁️ Add persistent storage with **Google Cloud**, **BigQuery**, or **Firestore**.
- 📈 Build a **real-time dashboard** using Streamlit or Plotly Dash.
- 🤖 Add predictive analytics or anomaly detection features.
- 🔔 Integrate alerts for significant price movements.
- 📋 Implement advanced logging and monitoring.

---

## 📬 Contact

For suggestions or improvements, feel free to open an issue or submit a PR!

---

> Made with ❤️ using Python and APIs.
