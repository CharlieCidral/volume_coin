from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import base64
from selenium import webdriver
import time
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generates a 16-byte (32-character) random hexadecimal secret key

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def scrape():
    url = request.form['url']
    data = scrape_data(url)
    return jsonify(data)


def scrape_data(url, start_index):
    # Step 1: Set up the Selenium webdriver (ensure you have the appropriate driver installed)
    driver = webdriver.Chrome()  # You can use other browsers as well

    # Step 1: Make an HTTP request to the website
    driver.get(url)

    # Step 3: Define a function to scroll down the page
    def scroll_to_percentage(percentage):
        # Calculate the scroll position based on the page height and the desired percentage
        scroll_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
        scroll_position = int(scroll_height * (percentage / 100))

        # Scroll to the calculated position
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")

        # Wait for some time to let the content load
        time.sleep(2)

    # Step 4: Scroll to different percentages to load content in parts
    scroll_to_percentage(13)

    # Step 5: Parse the HTML content after loading all items
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    data_list = []
    p_elements = soup.find_all('p', class_='coin-item-symbol')
    symbols = []
    for p_element in p_elements:
        symbol = p_element.text.strip()
        symbols.append(symbol)

    # Step 1: Find the <label> tag with class="gFMJer"
    label_element = soup.find('label', class_='gFMJer')

    # Step 2: Check if the label element exists
    if label_element:
        # Exclude the first three items from the 'symbols' list
        symbols = symbols[3:]

    # Step 6: Find all div elements with the specified class
    div_elements = soup.find_all('div', class_='sc-bc83b59-0')

    # Step 7: Iterate through each div element and extract the prices
    prices = []
    for div_element in div_elements:
        # Find the <a> tag inside the div
        a_tag = div_element.find('a')
        if a_tag:
            # Find the <span> tag inside the <a> tag to get the price
            price_span = a_tag.find('span')
            if price_span:
                # Extract the price text and append to the prices list
                price = price_span.text.strip()
                prices.append(price)

    div_elementts = soup.find_all('div', class_='bpHLqp')

    volumes = []
    for div_elementt in div_elementts:
        # Find the <a> tag inside the div
        a_tag = div_elementt.find('a')
        if a_tag:
            # Find the <a> tag inside the <a> tag to get the price
            volume_p = a_tag.find('p')
            if volume_p:
                # Extract the price text and append to the prices list
                volume = volume_p.text.strip()
                volumes.append(volume)

    volumes = [float(volume.replace('$', '').replace(',', '')) for volume in volumes]

    for symbol, price, volume in zip(symbols, prices, volumes):
        # Create a dictionary for each symbol, its corresponding price, and volume
        data = {'Symbol': symbol, 'Price': price, 'Volume': volume}
        # Append the data to the 'data_list'
        data_list.append(data)

    # Step 8: Close the webdriver
    driver.quit()

    data_list.sort(key=lambda x: x['Volume'], reverse=True)
    data_list = data_list[start_index:]

    return data_list

@socketio.on('scrape_request')
def handle_scrape_request(message):
    url = message['url']
    start_index = int(message.get('start_index', 0))
    data = scrape_data(url, start_index)
    emit('scrape_response', data)

if __name__ == '__main__':
    socketio.run(app, debug=True)