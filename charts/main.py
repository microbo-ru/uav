import streamlit as st
import requests
import time

st.set_page_config(
    page_title="Charts",
    page_icon="📈",
    layout="wide"
)

base_url ='http://app-a:8000/task'

def get_status(job_id):
    url = f"{base_url}/{job_id}/status"
    response = requests.get(url)
    return response.json()

def submit_job(filename):
    response = requests.post(base_url)

    headers = {
        'accept': 'application/json',
    }

    files = {
        'xslx_file': (filename, open(f'tmp/{filename}', 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
    }

    response = requests.post(base_url, headers=headers, files=files)
    
    st.write(response.json(), response.status_code)
    return response.json()

xlsx_file = st.sidebar.file_uploader("Загрузите .xlsx файл")
if xlsx_file is not None:
    filename = xlsx_file.name
    file_path = f"tmp/{filename}"

    if st.button("Построить график"):
        st.write("Нормализация данных...")

        with st.spinner("Ожидаем ответка от API..."):
            try:
                with open(file_path, "wb") as f:
                    f.write(xlsx_file.getbuffer())

                response = submit_job(filename)
                job_id = response["id"]
                job_status = response["status"]

                st.write(job_id)

                while (job_status != "SUCCESS"):
                    response = get_status(job_id)
                    job_status = response["status"]
                    st.json(response)
                    time.sleep(1)

                st.success("Data fetched successfully!")
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching data: {e}")
