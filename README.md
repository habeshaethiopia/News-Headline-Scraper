# News Headline Scraper

This project is a web application that scrapes news headlines from a given URL and allows users to download the headlines as a CSV file. The application is built using Streamlit, BeautifulSoup, and Pandas.

## Features

- Input a news website URL to scrape headlines.
- Display the scraped headlines.
- Download the headlines as a CSV file.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/news-headline-scraper.git
    cd news-headline-scraper
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Enter the news website URL in the input field and click the "Scrape Headlines" button.

4. View the scraped headlines and download them as a CSV file.

## Project Structure
 ``` 
    ├── app.py 
    ├── requirements.txt 
  ```


## Dependencies

- Streamlit
- Requests
- BeautifulSoup
- Pandas

## License

This project is licensed under the MIT License.