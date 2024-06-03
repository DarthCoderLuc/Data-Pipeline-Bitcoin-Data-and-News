import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

def get_bitcoin_news():
    # URL of the webpage to scrape
    base_url = 'https://www.ft.com/bitcoin?page='

    # Create lists to store extracted data
    headlines_list = []
    subheadlines_list = []
    dates_list = []

    # Calculate the cutoff date (300 days ago from today)
    cutoff_date = datetime.now() - timedelta(days=300)
    
    page = 1
    while True:
        # Construct the URL for the current page
        url = base_url + str(page)

        # Send an HTTP request to the webpage
        res = requests.get(url)

        # Check if the request was successful
        if res.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(res.text, 'html.parser')

            # Check for the presence of the error page title
            error_title = soup.select_one('.error-page__title')
            if error_title and 'Sorry' in error_title.text:
                print(f"Reached the error page at page {page}. Stopping the scrape.")
                break
            
            # Find all headlines related to Bitcoin
            headlines = soup.select('.o-teaser__heading')
            subheadlines = soup.select('.js-teaser-standfirst-link')
            dates = soup.select('.o-date')

            # Iterate over each headline, subheadline, and date
            for headline, subheadline, date in zip(headlines, subheadlines, dates):
                # Extract the text from the headline, subheadline, and date elements
                headline_text = headline.text.strip()
                subheadline_text = subheadline.text.strip()
                date_text = date.text.strip()

                # Parse the date string
                try:
                    date_obj = datetime.strptime(date_text, "%A, %d %B, %Y")
                except ValueError:
                    print(f"Date format not recognized for date: {date_text}")
                    continue

                # Check if the article is within the cutoff date
                if date_obj >= cutoff_date:
                    # Append the extracted data to lists
                    headlines_list.append(headline_text)
                    subheadlines_list.append(subheadline_text)
                    dates_list.append(date_obj)
        else:
            print(f"Failed to retrieve the page {page}. Status code: {res.status_code}")
            break

        # Increment the page number for the next iteration
        page += 1

    # Create DataFrame from the lists
    df = pd.DataFrame({'date': dates_list, 'headline': headlines_list, 'subheadline': subheadlines_list})

    # Sort DataFrame by 'date'
    df = df.sort_values(by='date')

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df

# Usage
bitcoin_headlines_df = get_bitcoin_news()

# Print the DataFrame
if bitcoin_headlines_df is not None:
    print(bitcoin_headlines_df)
