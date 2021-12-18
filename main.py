import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

st.title('US Consumer Finance Complaints')


@st.cache
def load_data():
    print("Loading csv.")
    data = pd.read_csv('consumer_complaints.zip')
    data['date_received'] = data['date_received'].apply(lambda v: datetime.strptime(v, '%m/%d/%Y'))
    data['date_sent_to_company'] = data['date_sent_to_company'].apply(lambda v: datetime.strptime(v, '%m/%d/%Y'))
    data['Processing Time (Days)'] = data.apply(lambda row: (row['date_sent_to_company'] - row['date_received']).days,
                                                axis=1)
    return data


data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show Column Names'):
    st.subheader('Data Columns')
    st.write(data.columns)

date, col = st.columns(2)
time = str(datetime.now().strftime('%Y-%m-%d'))
date.metric("The DATE now is ", time)

st.subheader('Complaint Frequency')
fig, ax = plt.subplots()
plt.xticks(rotation=90)
data['date_received'].hist(bins=100)
st.pyplot(fig)

st.subheader('Top Ten')

with st.form("my_form"):
    report_type = st.radio('Which Report?', ('Top 10 issues', 'Top 10 companies that received complaints'))

    submit = st.form_submit_button("Submit")

    if report_type == 'Top 10 issues':
        chart_data = data['issue'].value_counts().head(10)

        st.bar_chart(chart_data)

    if report_type == 'Top 10 companies that received complaints':
        chart_data = data['company'].value_counts().head(10)

        st.bar_chart(chart_data)

    st.info('Remarks: Size and business targets of the companies affects the data')

st.subheader('Main Submission Methods')

submission_method_ratio = data['submitted_via'].value_counts().to_dict()
method = [key for key in submission_method_ratio.keys()]
method_data = [int(value) for value in submission_method_ratio.values()]

labels = method
sizes = method_data

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
ax1.axis('equal')

st.pyplot(fig1)

st.subheader('Processing Time (Days)')

ten_companies = data['company'].value_counts().head(10).index
ten_companies.to_list()

frequent_state = data['state'].value_counts().head(10).index
frequent_state.to_list()

option = st.selectbox('Select dimension:', ['company', 'state', 'submitted_via'])
st.write('You selected:', option)

fig2, ax2 = plt.subplots(figsize=(18, 10))

plt.xticks(fontsize=18, rotation='vertical')

sns.barplot(option, 'Processing Time (Days)', data=data[
    data['company'].isin(ten_companies) &
    data['state'].isin(frequent_state)
    ])
st.pyplot(fig2)

st.info('Remarks: Top Ten Companies & Frequent States are chosen for demonstration')


@st.cache
def convert_df(data):
    return data.to_csv().encode('utf-8')


csv = convert_df(data)
st.subheader('Download Link')

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='consumer_complaints.csv',
    mime='text/csv',
)
