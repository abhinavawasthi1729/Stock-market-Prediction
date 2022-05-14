from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

finviz_url = 'https://finviz.com/quote.ashx?t='
#tickers = ['AMZN', 'GOOG', 'FB']
tickers = ['GOOG']

news_tables = {}
for ticker in tickers:
    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response, features='html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

parsed_data = []

for ticker, news_table in news_tables.items():

    for row in news_table.findAll('tr'):

        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

vader = SentimentIntensityAnalyzer()

f = lambda title: vader.polarity_scores(title)['compound']
df['compound'] = df['title'].apply(f)
df['date'] = pd.to_datetime(df.date).dt.date

print(df)

plt.figure(figsize=(10,8))
mean_df = df.groupby(['ticker', 'date']).mean().unstack()
print(mean_df)
mean_df = mean_df.xs('compound', axis="columns")
#mean_df.plot(kind='bar')
print(mean_df.columns)
print(mean_df)
#plt.show()


"""
    finviz_url = 'https://finviz.com/quote.ashx?t='
    tickers = ['GOOG']

    news_tables = {}
    for ticker in tickers:
        url = finviz_url + ticker

        req = Request(url=url, headers={'user-agent': 'my-app'})
        response = urlopen(req)

        html = BeautifulSoup(response, features='html.parser')
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table

    parsed_data = []

    for ticker, news_table in news_tables.items():

        for row in news_table.findAll('tr'):

            title = row.a.text
            date_data = row.td.text.split(' ')

            if len(date_data) == 1:
                time = date_data[0]
            else:
                date = date_data[0]
                time = date_data[1]

            parsed_data.append([ticker, date, time, title])

    df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

    vader = SentimentIntensityAnalyzer()

    f = lambda title: vader.polarity_scores(title)['compound']
    df['compound'] = df['title'].apply(f)
    df['date'] = pd.to_datetime(df.date).dt.date

    #plt.figure(figsize=(10,8))
    #mean_df = df.groupby(['ticker', 'date']).mean().unstack()
    #mean_df = mean_df.xs('compound', axis="columns")
    #mean_df.plot(kind='bar')
    #plt.show()

    st.subheader("Sentiment analyis for %s as per latest news" % (stock_choice))
    st.dataframe(df[['date', 'time', 'title']], width=2000, height=500)
    #plot_graph(mean_df, forecast_window_int, a)
    #st.pyplot(df['compound'])


    new_df = df[['date', 'compound']].copy()

    #st.bar_chart(new_df['compound'])

    st.area_chart(new_df['compound'])


    #new_df = new_df.rename(columns={'date':'index'}).set_index('index')

    #st.line_chart(new_df)

    
    
    
"""