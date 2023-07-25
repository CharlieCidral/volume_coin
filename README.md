# Crypto Volume Bar Chart

Crypto Volume Bar Chart is a web application that allows users to scrape cryptocurrency data from a specified website and visualize the trading volumes as a bar chart. The app is built with Python, Flask, Socket.IO, and Chart.js.

## Features

- Real-time data scraping using WebSockets: The app updates the bar chart dynamically as new volume data becomes available.

- Interactive web interface: Users can input the website URL from which they want to scrape data and view the bar chart with volume data.

- Customizable starting index: Users can choose the starting index for the displayed data in the chart.

- Export data: Users can export the scraped data in JSON format.

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/CharlieCidral/crypto-volume-bar-chart.git
```

2. Install the required libraries:

```bash
pip install Flask Flask-SocketIO requests selenium beautifulsoup4 matplotlib pandas
```

2. Run the app:

```
python app.py
```

3. Access the app in your web browser at `http://127.0.0.1:5000/`.


### Usage

1. Enter the URL(`https://coinmarketcap.com/`) of the website you want to scrape in the provided input field.
2. (Optional) Choose the starting index for the displayed data in the chart. The default is 0.
3. Click the "Scrape Data" button. The app will scrape the data and update the bar chart in real-time.

## Screenshot

![image](https://user-images.githubusercontent.com/69029099/211183900-2dbe7169-f8c9-494f-9e14-71825eb3ef30.png)

### Dependecies

- Flask: Web framework for building the application.
- Flask-SocketIO: Provides WebSocket support for real-time communication.
- requests: HTTP library for making web requests.
- selenium: Web browser automation library for web scraping.
- beautifulsoup4: Library for parsing HTML and XML documents.
- matplotlib: Library for creating visualizations, including the bar chart.
- pandas: Data analysis library for handling data structures and manipulation.

### Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request with any improvements or bug fixes.
