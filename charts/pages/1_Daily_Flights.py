import streamlit as st
import plost
import pandas as pd

st.subheader('Daily Flights Stats')
st.write(
    """
    **Дневная интенсивность** полетов отображает кол-во записе в табеле в разерезе месяцев и дней недели.
    """
)

csv_file = st.sidebar.file_uploader("Upload .csv file")
if csv_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(csv_file)
    # df['tc'] = pd.to_datetime(df['tc'])

    st.write(
        """
        Выбереите вид представления информации:
        """
    )

    tab1, tab2 = st.tabs(["По дням", "По дням недели"])

    with tab1:
        plost.time_hist(
            data=df,
            date='Дата',
            x_unit='date',
            y_unit='month',
            # color='call_volume',
            aggregate='count',
        )

    with tab2:
        plost.time_hist(
            data=df,
            date='Дата',
            x_unit='days',
            y_unit='month',
            # color='call_volume',
            aggregate='count',
        )

    df

