from datetime import datetime
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.backend
import pandas_datareader as web
from sklearn.preprocessing import MinMaxScaler
#import fix_yahoo_finance
from pandas_datareader import data as pdr
import yfinance

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# cover image used and streamlit function call to display image
image_path = ('image.jpeg')
st.image(image_path, use_column_width=True)

# basic title and markdown
st.title("Stock Prediction including Sentiment analysis 📈")
st.header("Welcome !")
st.markdown(
    "In this Machine Learning application, we have used the historical stock price data for Alphabet (GOOGL) and Apple Inc. (AAPL) to forecast their price in a specified future window.")
st.markdown(
    "We have used the Tensorflow and Keras APIs to build a stacked LSTM model with a convolutional as well as a lambda layer. We trained our model on a roughly four-month period from May 14, 2021 through May 13, 2022.")

path_googl = ('data_googl.csv')
path_aapl = ('data_aapl.csv')


# function to load separate models on the basis of user choice

def load_model(forecast_window):
    if forecast_window == '1 week':
        model = keras.models.load_model('Experiments NB/Model1_pred_7days.h5')
    elif forecast_window == '2 weeks':
        model = keras.models.load_model('Experiments NB/Model2_pred_14days.h5')
    elif forecast_window == '3 weeks':
        model = keras.models.load_model('Experiments NB/Model_3_Pred21_Days.h5')
    elif forecast_window == '4 weeks':
        model = keras.models.load_model('Experiments NB/Model_4_Pred28_Days.h5')
    elif forecast_window == '5 weeks':
        model = keras.models.load_model('Experiments NB/Model5_Pred_35Days.h5')

    # model._make_predict_function()
    model.summary()
    return model


def load_model_app(forecast_window):
    if forecast_window == '1 week':
        model = keras.models.load_model('Experiments NB/Apple-Model-TransferLearning/apple-7.h5')
    elif forecast_window == '2 weeks':
        model = keras.models.load_model('Experiments NB/Apple-Model-TransferLearning/apple-14.h5')
    elif forecast_window == '3 weeks':
        model = keras.models.load_model('Experiments NB/Apple-Model-TransferLearning/apple-21.h5')
    elif forecast_window == '4 weeks':
        model = keras.models.load_model('Experiments NB/Apple-Model-TransferLearning/apple-28.h5')
    elif forecast_window == '5 weeks':
        model = keras.models.load_model('Experiments NB/Apple-Model-TransferLearning/apple-35.h5')

    # model._make_predict_function()
    model.summary()
    return model


# function to load data from dataset
@st.cache(persist=True)
def load_data(path, nrows):
    data = pd.read_csv(filepath_or_buffer=path, nrows=nrows)
    return data


# simple mapping function to map forecast input strings to relevant integers
def mapper(forecast_window):
    if forecast_window == '1 week':
        return 7
    elif forecast_window == '2 weeks':
        return 14
    elif forecast_window == '3 weeks':
        return 21
    elif forecast_window == '4 weeks':
        return 28
    elif forecast_window == '5 weeks':
        return 35


# windowing functions

def windowed_dataset(series, window_size=31, predday=7, batch_size=32, shuffle_buffer=1000):
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + predday, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + predday))
    ds = ds.shuffle(shuffle_buffer)
    ds = ds.map(lambda w: (w[:-7], tf.squeeze(w[-7:])))
    return ds.batch(batch_size).prefetch(3)


def windowed_dataset1(series, window_size=62, predday=14, batch_size=32, shuffle_buffer=1000):
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + predday, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + predday))
    ds = ds.shuffle(shuffle_buffer)
    ds = ds.map(lambda w: (w[:-14], tf.squeeze(w[-14:])))
    return ds.batch(batch_size).prefetch(3)


def windowed_dataset2(series, window_size=90, predday=21, batch_size=32, shuffle_buffer=1000):
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + predday, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + predday))
    ds = ds.shuffle(shuffle_buffer)
    ds = ds.map(lambda w: (w[:-21], tf.squeeze(w[-21:])))
    return ds.batch(batch_size).prefetch(3)


def windowed_dataset3(series, window_size=120, predday=28, batch_size=32, shuffle_buffer=1000):
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + predday, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + predday))
    ds = ds.shuffle(shuffle_buffer)
    ds = ds.map(lambda w: (w[:-28], tf.squeeze(w[-28:])))
    return ds.batch(batch_size).prefetch(3)


def windowed_dataset4(series, window_size=150, predday=35, batch_size=32, shuffle_buffer=1000):
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + predday, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + predday))
    ds = ds.shuffle(shuffle_buffer)
    ds = ds.map(lambda w: (w[:-35], tf.squeeze(w[-35:])))
    return ds.batch(batch_size).prefetch(3)


# plotting function to plot the final forecast line graph

def plot_graph(forecast, forecast_window_int, a):

    if forecast_window_int == 7:
        plt.plot(np.arange(0, 31), scaler1.inverse_transform(a[0]))
        plt.plot(np.arange(31, 38), scaler1.inverse_transform(forecast)[0], "-")

    elif forecast_window_int == 14:
        plt.plot(np.arange(1, 63),scaler1.inverse_transform(a[0]))
        plt.plot(np.arange(63, 77), scaler1.inverse_transform(forecast)[0], "-")

    elif forecast_window_int == 21:
        plt.plot(np.arange(1, 91), scaler1.inverse_transform(a[0]))
        plt.plot(np.arange(91, 112), scaler1.inverse_transform(forecast)[0], "-")

    elif forecast_window_int == 28:
        plt.plot(np.arange(1, 121), scaler1.inverse_transform(a[0]))
        plt.plot(np.arange(121, 149), scaler1.inverse_transform(forecast)[0], "-")

    elif forecast_window_int == 35:
        plt.plot(np.arange(1, 151), scaler1.inverse_transform(a[0]))
        plt.plot(np.arange(151, 186), scaler1.inverse_transform(forecast)[0], "-")

    plt.legend(["Actual Days", "Prediction"])
    plt.title('Prediction for next {} Days'.format(forecast_window_int))
    st.pyplot()


def future_predicted(testbatches, window_size, predday):
    x, y = next(iter(testbatches))
    output = model.predict(x)

    time = list(range(1, window_size + 1))
    time2 = list(range(window_size + 1, window_size + predday + 1))
    plt.plot(time, x[0])
    plt.plot(time2, output[0])
    plt.legend(['Actual Values', 'Predicted Values'])
    plt.title('Prediction for {} Days'.format(predday))

    st.pyplot()


# main function
if __name__ == "__main__":
    st.markdown(
        "You may go over the raw data for Alphabet or Apple. Just go to the sidebar and select your stock of choice. We have used the closing price as the generic price. ")
    
    st.subheader("Choose from Apple Inc. (AAPL) and Alphabet Inc. (GOOGL) for lastest values")
    choice = st.selectbox("Show Raw Data", ['Alphabet (GOOGL)', 'Apple (APPL)'])
    if choice == 'Alphabet (GOOGL)':
        data = load_data('GOOGL.csv', 4000)
        st.write(data)
    elif choice == 'Apple (APPL)':
        data = load_data('AAPL.csv', 4000)
        st.write(data)

    # Dropdown Menu to Choose Company Stock
    st.subheader("Choose from Apple Inc. (AAPL) and Alphabet Inc. (GOOGL) to predict their future stock prices.")
    stock_choice = st.selectbox("Choice of Company Stock", ['Alphabet (GOOGL)', 'Apple (AAPL)'])

    # st.subheader("Select the period (1-5 weeks) into the future for when you would like to see the forecast: ")
    # forecast_window = st.selectbox("Choice of Future Forecast Period", ['1 week','2 weeks','3 weeks','4 weeks','5 weeks'])

    if stock_choice == 'Alphabet (GOOGL)':
        # Reading the data
        #start_date = '2010-01-01'
        #end_date = '2016-12-31'
        start_date = '2021-05-01'
        end_date = '2022-05-01'
        df_test =  pdr.DataReader('GOOGL', 'yahoo', start_date, end_date)
        df_test = pd.DataFrame(df_test)
        df_test.reset_index(level=0, inplace=True)
        #df_test =load_data(path_googl, 4000)
        # Displaying historical data for Alphabet
        st.subheader("Graph of Alphabet Inc.'s Historical Stock Prices")
        st.line_chart(df_test['Close'])

        # Inputting forecast window
        st.subheader(
            "Select the period (1-5 weeks) into the future for when you would like to see %s's forecast: " % stock_choice)
        forecast_window = st.selectbox("Choice of Future Forecast Period",
                                       ['1 week', '2 weeks', '3 weeks', '4 weeks', '5 weeks'])
        forecast_window_int = mapper(forecast_window)

        # Choosing the closing data and reshaping into input shape
        x_test = df_test['Close']
        x_test = np.array(x_test).reshape(-1, 1)

        # Scaling and windowing the input
        scaler1 = MinMaxScaler(feature_range=(0, 0.75))
        xt1 = scaler1.fit_transform(x_test)

        if forecast_window_int == 7:

            xt = windowed_dataset(xt1, predday=7)



        elif forecast_window_int == 14:

            xt = windowed_dataset1(xt1, predday=14)

        elif forecast_window_int == 21:
            xt = windowed_dataset2(xt1, predday=21)

        elif forecast_window_int == 28:
            xt = windowed_dataset3(xt1, predday=28)

        else:
            xt = windowed_dataset4(xt1, predday=35)

        a, b = next(iter(xt))

        # load that model which is asked by the user and predict based on given timestep
        model = load_model(forecast_window)
        forecast = model.predict(a)

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

        st.subheader("Latest News for %s " % (stock_choice))
        #st.dataframe(df[['date', 'time', 'title']], width=2000, height=500)
        st.table(df[['date', 'time', 'title']].head())
        #plot_graph(mean_df, forecast_window_int, a)
        #st.pyplot(df['compound'])


        new_df = df[['date', 'compound']].copy()

        #st.bar_chart(new_df['compound'])
        
        st.subheader("Sentiment Analysis of %s as per latest News" % (stock_choice))

        st.area_chart(new_df['compound'])


        #new_df = new_df.rename(columns={'date':'index'}).set_index('index')

        #st.line_chart(new_df)

    elif stock_choice == 'Apple (AAPL)':

        # Reading the data
        #df_test = web.DataReader('AAPL', data_source='yahoo', start='10-01-2019', end='07-20-2020')
        
        #df_test = web.DataReader('AAPL', data_source='yahoo', start=datetime(2019,1,10), end=datetime(2020,7,20))

        # Displaying historical data for Alphabet
        start_date = '2021-05-01'
        end_date = '2022-05-01'
        df_test =  pdr.DataReader('GOOGL', 'yahoo', start_date, end_date)
        df_test = pd.DataFrame(df_test)
        df_test.reset_index(level=0, inplace=True)
        st.subheader("Graph of Apple Inc.'s Historical Stock Prices")
        st.line_chart(df_test['Close'])

        # Inputting forecast window
        st.subheader(
            "Select the period (1-5 weeks) into the future for when you would like to see %s's forecast: " % stock_choice)
        forecast_window = st.selectbox("Choice of Future Forecast Period",
                                       ['1 week', '2 weeks', '3 weeks', '4 weeks', '5 weeks'])
        forecast_window_int = mapper(forecast_window)

        # Choosing the closing data and reshaping into input shape
        x_test = df_test['Close']
        x_test = np.array(x_test).reshape(-1, 1)

        # Scaling and windowing the input
        scaler1 = MinMaxScaler(feature_range=(0, 0.75))
        xt1 = scaler1.fit_transform(x_test)

        if forecast_window_int == 7:
            xt = windowed_dataset(xt1, predday=7)

        elif forecast_window_int == 14:

            xt = windowed_dataset1(xt1, predday=14)

        elif forecast_window_int == 21:
            xt = windowed_dataset2(xt1, predday=21)

        elif forecast_window_int == 28:
            xt = windowed_dataset3(xt1, predday=28)

        else:
            xt = windowed_dataset4(xt1, predday=35)

        a, b = next(iter(xt))

        # load that model which is asked by the user and predict based on given timestep

        model = load_model_app(forecast_window)
        forecast = model.predict(a) 

        finviz_url = 'https://finviz.com/quote.ashx?t='
        tickers = ['AAPL']

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

        st.subheader("Latest News for %s " % (stock_choice))
        st.table(df[['date', 'time', 'title']].head())
        #plot_graph(mean_df, forecast_window_int, a)
        #st.pyplot(df['compound'])


        new_df = df[['date', 'compound']].copy()

        #st.bar_chart(new_df['compound'])

        st.subheader("Sentiment Analysis of %s as per latest News" % (stock_choice))
       
        st.area_chart(new_df['compound'])


        #new_df = new_df.rename(columns={'date':'index'}).set_index('index')

        #st.line_chart(new_df)

    # Plotting of future forecast graph
    st.subheader("Future forecast for %s for a period of %s after 20th July, 2020:" % (stock_choice, forecast_window))

    plot_graph(forecast, forecast_window_int, a)

   
   #####################################################################################
   #SENTIMENT ANALYSIS
   ###################################################################################

    
