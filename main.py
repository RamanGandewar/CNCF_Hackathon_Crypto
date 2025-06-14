import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time # To simulate collecting data over time
import random # For simulating price data (now only for fallback)
import os # To create directories for output
import requests # For making API calls

# This DataFrame will store multiple data points over time
all_collected_data_df = pd.DataFrame()

# --- Functions for data ingestion and processing ---
def get_crypto_price_data(coin_ids, vs_currencies):
    """
    Fetches live cryptocurrency price data from CoinGecko API.
    Uses placeholder random data as a fallback if API call fails.
    """
    print(f"  -> Attempting to fetch live data for coins: {coin_ids} against currencies: {vs_currencies}")
    api_url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': coin_ids,
        'vs_currencies': vs_currencies
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if not data:
            print("  -> API returned empty data. Using simulated data as fallback.")
            return _simulate_crypto_price_data(coin_ids, vs_currencies)
        print("  -> Live data fetched successfully.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"  -> Error fetching data from CoinGecko API: {e}. Using simulated data as fallback.")
        return _simulate_crypto_price_data(coin_ids, vs_currencies)

def _simulate_crypto_price_data(coin_ids, vs_currencies):
    """
    Helper function to simulate cryptocurrency price data. Used as a fallback.
    """
    simulated_data = {}
    coins = [coin.strip() for coin in coin_ids.split(',')]
    currencies = [currency.strip() for currency in vs_currencies.split(',')]

    for coin in coins:
        simulated_data[coin] = {}
        for currency in currencies:
            if coin == 'bitcoin':
                simulated_data[coin][currency] = random.uniform(25000, 70000)
            elif coin == 'ethereum':
                simulated_data[coin][currency] = random.uniform(1500, 4000)
            else:
                simulated_data[coin][currency] = random.uniform(1, 100)
    return simulated_data


def process_crypto_data(raw_data):
    """
    Processes raw cryptocurrency data into a pandas DataFrame.
    """
    print("  -> Processing raw data...")
    if not raw_data:
        print("  -> No raw data to process.")
        return None

    processed_records = []
    timestamp = datetime.now() # Use current time for when data was processed

    for coin, currencies_data in raw_data.items():
        for currency, price in currencies_data.items():
            processed_records.append({
                'timestamp': timestamp,
                'coin': coin,
                'currency': currency,
                'price': price,
                # Assume CoinGecko API returns USD price directly for 'usd'
                # For 'inr', CoinGecko provides it, so no manual conversion needed
                'price_usd': price if currency == 'usd' else (price / 83.0 if currency == 'inr' else None)
                # Note: CoinGecko provides direct conversion, but keeping a fallback if structure changes
            })

    df = pd.DataFrame(processed_records)
    df['price_usd'] = pd.to_numeric(df['price_usd'], errors='coerce')

    # Filter to only USD for visualization as per original visualize function expectation
    return df[df['currency'] == 'usd'].dropna(subset=['price_usd'])


def collect_and_process_multiple_times(num_iterations, delay_seconds, coin_ids, vs_currencies):
    """
    Collects and processes data multiple times to simulate a time-series.
    Appends data from each iteration to a global DataFrame.

    Args:
        num_iterations (int): How many times to collect data.
        delay_seconds (int): Delay between each collection.
        coin_ids (str): Comma-separated string of coin IDs (e.g., "bitcoin,ethereum").
        vs_currencies (str): Comma-separated string of target currencies (e.g., "usd,inr").

    Returns:
        pd.DataFrame: A combined DataFrame of all collected and processed data.
    """
    global all_collected_data_df # Declare intent to modify the global DataFrame
    all_collected_data_df = pd.DataFrame() # Reset for each run

    print(f"\n--- Pipeline Stage: Data Collection Loop ({num_iterations} iterations) ---")
    for i in range(num_iterations):
        print(f"  Iteration {i+1}/{num_iterations}...")
        try:
            raw_data = get_crypto_price_data(coin_ids, vs_currencies)
            if raw_data:
                processed_df_single = process_crypto_data(raw_data)
                if processed_df_single is not None and not processed_df_single.empty:
                    all_collected_data_df = pd.concat([all_collected_data_df, processed_df_single], ignore_index=True)
                    print(f"  -> Data point collected at {processed_df_single['timestamp'].iloc[0]} for {processed_df_single['coin'].tolist()} (USD price: {processed_df_single['price_usd'].tolist()})")
                else:
                    print(f"  -> Warning: No valid data processed for iteration {i+1}.")
            else:
                print(f"  -> Warning: No raw data ingested for iteration {i+1}.")
        except Exception as e:
            print(f"  -> Error during data collection for iteration {i+1}: {e}")
            # In a real pipeline, you might log this error to a file or monitoring system

        if i < num_iterations - 1:
            print(f"  Waiting for {delay_seconds} seconds before next collection...")
            time.sleep(delay_seconds) # Pause for a few seconds

    print(f"\n--- Pipeline Stage: Data Aggregation Complete ---")
    print(f"Total records collected: {len(all_collected_data_df)}")
    return all_collected_data_df

def visualize_crypto_prices(df_to_plot, output_path="output/crypto_price_trend.png"):
    """
    Creates a simple line plot of cryptocurrency prices over time and saves it to a file.

    Args:
        df_to_plot (pd.DataFrame): DataFrame containing 'timestamp', 'coin', and 'price_usd' columns.
        output_path (str): The file path where the plot will be saved.
    """
    if df_to_plot.empty:
        print("No data to visualize.")
        return

    print(f"\n--- Pipeline Stage: Generating Visualization and Saving ---")
    plt.figure(figsize=(12, 6)) # Set the figure size for better readability

    df_to_plot['timestamp'] = pd.to_datetime(df_to_plot['timestamp'])

    for coin in df_to_plot['coin'].unique():
        coin_df = df_to_plot[df_to_plot['coin'] == coin].sort_values(by='timestamp')
        plt.plot(coin_df['timestamp'], coin_df['price_usd'], marker='o', linestyle='-', label=coin.capitalize())

    plt.title('Cryptocurrency Price Trend Over Time (USD)')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        plt.savefig(output_path) # Save the plot to a file
        print(f"  -> Plot successfully saved to {output_path}")
    except Exception as e:
        print(f"  -> Error saving plot to {output_path}: {e}")
    finally:
        plt.close() # Close the plot to free up memory


def main_pipeline_run():
    """
    Orchestrates the entire cryptocurrency data collection and visualization pipeline.
    """
    print("===================================================")
    print("           Starting Cryptocurrency Data Pipeline         ")
    print("===================================================")

    # --- Pipeline Stage: Configuration ---
    print("\n--- Pipeline Stage: Configuration ---")
    num_iterations = 3 # Collect data 3 times
    delay_seconds = 5  # Increased delay to avoid CoinGecko API rate limits
    coin_ids_to_track = "bitcoin,ethereum"
    currencies_to_track = "usd,inr"
    output_plot_path = "output/crypto_price_trend.png"
    print(f"  Configured to collect data for: {coin_ids_to_track}")
    print(f"  Against currencies: {currencies_to_track}")
    print(f"  Plot will be saved to: {output_plot_path}")
    print(f"  Note: Using CoinGecko API for real-time prices with {delay_seconds}s delay.")


    # --- Pipeline Stage: Execute Data Collection and Processing ---
    final_aggregated_df = collect_and_process_multiple_times(
        num_iterations,
        delay_seconds,
        coin_ids_to_track,
        currencies_to_track
    )

    # --- Pipeline Stage: Visualization and Reporting ---
    if not final_aggregated_df.empty:
        visualize_crypto_prices(final_aggregated_df, output_plot_path)
    else:
        print("\n--- Pipeline Stage: Visualization Skipped (No Data) ---")
        print("  No data was collected to generate a visualization.")

    print("\n===================================================")
    print("           Cryptocurrency Data Pipeline Complete         ")
    print("===================================================")

# --- Main execution block for Colab ---
if __name__ == "__main__":
    main_pipeline_run()
