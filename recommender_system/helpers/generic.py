import pandas as pd
import sqlite3 as sql


def read_data(database, query):
    # Create a Connection to the Database
    conn = sql.connect(database)

    # Load the data from the database
    dataframe = pd.read_sql_query(query, con=conn)
    dataframe = dataframe.reset_index()
    dataframe = dataframe.drop('index', axis=1)

    # Close the Connection
    conn.close()
    return dataframe


def update_data(database, query):
    """

    :param database:
    :param query:
    :return:
    """

    conn = sql.connect(database)

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

    conn.close()


def df_to_html(dataframe):
    with pd.option_context('display.max_colwidth', -1):
        output_html = dataframe.to_html(na_rep="")

    output_html = output_html.replace('<table border="1" class="dataframe">',
                                      '<table class = "table table-bordered" id = "anime_df">')
    output_html = output_html.replace('<thead>', '<thead class = "thead-dark">')
    output_html = output_html.replace('<tr style="text-align: right;">', '<tr>')
    output_html = output_html.replace('<th></th>', '<th>#</th>')

    return output_html
