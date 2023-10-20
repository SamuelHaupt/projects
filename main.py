from data_processor import DataProcessor


def main():
    data_processor = DataProcessor()
    symbol = 'TQQQ'
    start_date = '2021-01-30'
    stop_date = '2022-01-30'
    tqqq = data_processor.download_data_df_from_yf(symbol,
                                                   start_date,
                                                   stop_date)
    tqqq_preprocessed = data_processor.preprocess_data(tqqq)

    print(tqqq_preprocessed.head())


if __name__ == '__main__':
    main()
