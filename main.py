import streamlit as st
import requests
import selectorlib
import plotly.express as px
from datetime import datetime

URL = "https://programmer100.pythonanywhere.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

st.title("Temperature Graph")



def scrape(url):
    """Scrape the page source from the URL"""
    response =  requests.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["temp"]
    return value

def timestamp():
    now = datetime.now()
    #current_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    year = now.strftime("%Y")
    current_time = now.strftime("-%m-%d-%H-%M-%S")
    time_format = year[2:] + current_time
    return time_format

def store(extracted, time):
    with open("data.txt", "a") as file:
        file.write(time + ", " + extracted + "\n")

def read():
    with open("data.txt", "r") as file:
        return file.read()

def sort_data():
    with open("data.txt", "r") as file:
      lines = file.readlines()

    dates = []
    temperature = []

    for line in lines[1:]:
        date, temp = line.strip().split(", ")
        dates.append(date)
        temperature.append(int(temp))

    return dates, temperature

scraped_info = scrape(URL)
extracted = extract(scraped_info)
content = read()

if extracted not in content:
    time = timestamp()
    store(extracted, time)

dates, temperatures = sort_data()
figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (C)"})
st.plotly_chart(figure)

#if __name__ == "__main__":
    #scraped_info = scrape(URL)
    #extracted = extract(scraped_info)
    #content = read()
    #if extracted not in content:
        #time = timestamp()
        #store(extracted, time)
    #print(timestamp() + " " + extracted)
