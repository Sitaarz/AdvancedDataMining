import string

import nltk
import pandas as pd

nltk.download('punkt_tab')

from bs4 import BeautifulSoup

def clean_text(text: str) -> str:
    text = BeautifulSoup(text, 'html.parser').get_text()
    text = text.lower()
    # text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('','', string.punctuation))
    # text = re.sub(r'\W', '', text)

    return text

if __name__ == "__main__":
    df = pd.read_csv("../../data/filtered_data_10000_rows_per_genre.csv")
    print(df.columns)

    print(df.head())
    df = df.map(clean_text)
    print(df.head())




