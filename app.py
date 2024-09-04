import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

# Function to scrape headlines from a given URL
def scrape_headlines(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract headlines; modify this based on the website structure
        headlines = soup.find_all('h3', class_='gs-c-promo-heading__title')
        
        headline_list = [headline.get_text() for headline in headlines]
        response = requests.get(url)

        # Step 3: Parse the JSON response
        data = response.json()

        # Step 4: Extract the headlines
        headlines = [article.get('title') for article in data.get('results', [])]

        return headlines
    
    except Exception as e:
        st.error(f"Error: {e}")
        return []

# Streamlit App
st.title("News Headline Scraper")

# URL input field
url = st.text_input("Enter the news website URL", "https://newsdata.io/api/1/latest?apikey=YOUR_API_KEY")

if st.button("Scrape Headlines"):
    headlines = scrape_headlines(url)
    
    if headlines:
        st.success(f"Scraped {len(headlines)} headlines from {url}")
        st.subheader('Headlines:')
        for headline in headlines:
            st.write(f'- {headline}')
        # Create a DataFrame and convert it to CSV
        df = pd.DataFrame(headlines, columns=["Headline"])
        csv = df.to_csv(index=False)
        
        # Provide a download button for the CSV file
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='headlines.csv',
            mime='text/csv',
        )
    else:
        st.warning("No headlines found or an error occurred.")

