import time
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from selenium import webdriver
from selenium.webdriver.common.by import By
import warnings

warnings.filterwarnings("ignore")


def streamlit_config():
    st.set_page_config(page_title="Resume Analyzer AI", layout="wide")
    page_background_color = """
    <style>
    [data-testid="stHeader"] 
    {
    background: rgba(0,0,0,0);
    }
    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)
    st.markdown(
        f'<h1 style="text-align: center;">AI Resume Analyser</h1>',
        unsafe_allow_html=True,
    )


class resume_analyzer:

    @staticmethod
    def pdf_to_chunks(pdf):
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700, chunk_overlap=200, length_function=len
        )
        chunks = text_splitter.split_text(text=text)
        return chunks

    @staticmethod
    def resume_summary(query_with_chunks):
        query = f''' need to detailed summarization of below resume and finally conclude them
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    {query_with_chunks}
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    '''
        return query

    @staticmethod
    def resume_strength(query_with_chunks):
        query = f'''need to detailed analysis and explain of the strength of below resume and finally conclude them
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    {query_with_chunks}
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    '''
        return query

    @staticmethod
    def resume_weakness(query_with_chunks):
        query = f'''need to detailed analysis and explain of the weakness of below resume and how to improve make a better resume.
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    {query_with_chunks}
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    '''
        return query

    @staticmethod
    def job_title_suggestion(query_with_chunks):
        query = f''' what are the job roles i apply to likedin based on below?
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    {query_with_chunks}
                    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    '''
        return query

    @staticmethod
    def openai(openai_api_key, chunks, analyze):
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectorstores = FAISS.from_texts(chunks, embedding=embeddings)
        docs = vectorstores.similarity_search(query=analyze, k=3)
        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=analyze)
        return response


class linkedin_scrap:

    @staticmethod
    def linkedin_open_scrolldown(driver, user_job_title):
        b = []
        for i in user_job_title:
            x = i.split()
            y = "%20".join(x)
            b.append(y)
        job_title = "%2C%20".join(b)
        link = f"https://www.linkedin.com/jobs/search/?currentJobId=3910773395&f_TPR=r604800&keywords={job_title}&location=United%20Kingdom&originalSubdomain=uk"
        driver.get(link)
        driver.implicitly_wait(10)
        for i in range(0, 3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            try:
                x = driver.find_element(
                    by=By.CSS_SELECTOR, value="button[aria-label='See more jobs']"
                ).click()
                time.sleep(3)
            except:
                pass

    @staticmethod
    def company_name(driver):
        company = driver.find_elements(
            by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]'
        )
        company_name = []
        for i in company:
            company_name.append(i.text)
        return company_name

    @staticmethod
    def company_location(driver):
        location = driver.find_elements(
            by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]'
        )
        company_location = []
        for i in location:
            company_location.append(i.text)
        return company_location

    @staticmethod
    def job_title(driver):
        title = driver.find_elements(
            by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]'
        )
        job_title = []
        for i in title:
            job_title.append(i.text)
        return job_title

    @staticmethod
    def job_url(driver):
        url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
        url_list = [i.get_attribute("href") for i in url]
        job_url = []
        for url in url_list:
            job_url.append(url)
        return job_url

    @staticmethod
    def job_title_filter(x, user_job_title):
        s = [i.lower() for i in user_job_title]
        suggestion = []
        for i in s:
            suggestion.extend(i.split())
        s = x.split()
        a = [i.lower() for i in s]
        intersection = list(set(suggestion).intersection(set(a)))
        return x if len(intersection) > 1 else np.nan

    @staticmethod
    def get_description(driver, link):
        driver.get(link)
        time.sleep(3)
        driver.find_element(
            by=By.CSS_SELECTOR,
            value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]',
        ).click()
        time.sleep(2)
        description = driver.find_elements(
            by=By.CSS_SELECTOR,
            value='div[class="show-more-less-html__markup relative overflow-hidden"]',
        )
        driver.implicitly_wait(4)
        for j in description:
            return j.text

    @staticmethod
    def data_scrap(driver, user_job_title):
        df = pd.DataFrame(linkedin_scrap.company_name(driver), columns=["Company Name"])
        df["Job Title"] = pd.DataFrame(linkedin_scrap.job_title(driver))
        df["Location"] = pd.DataFrame(linkedin_scrap.company_location(driver))
        df["Website URL"] = pd.DataFrame(linkedin_scrap.job_url(driver))
        df["Job Title"] = df["Job Title"].apply(
            lambda x: linkedin_scrap.job_title_filter(x, user_job_title)
        )
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)
        df = df.iloc[:10, :]
        website_url = df["Website URL"].tolist()
        job_description = []
        for i in range(0, len(website_url)):
            link = website_url[i]
            data = linkedin_scrap.get_description(driver, link)
            if data is not None and len(data.strip()) > 0:
                job_description.append(data)
            else:
                job_description.append("Description Not Available")
        df["Job Description"] = pd.DataFrame(job_description, columns=["Description"])
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)
        return df

    @staticmethod
    def main(user_job_title):
        driver = webdriver.Chrome()
        driver.maximize_window()
        linkedin_scrap.linkedin_open_scrolldown(driver, user_job_title)
        final_df = linkedin_scrap.data_scrap(driver, user_job_title)
        driver.quit()
        return final_df


streamlit_config()
add_vertical_space(1)

with st.sidebar:
    add_vertical_space(3)
    option = option_menu(
        menu_title="",
        options=[
            "Summary",
            "Strength",
            "Weakness",
            "Job Titles",
            "Linkedin Jobs",
            "Exit",
        ],
        icons=[
            "house-fill",
            "database-fill",
            "pass-fill",
            "list-ul",
            "linkedin",
            "sign-turn-right-fill",
        ],
    )

if option == "Summary":
    pdf = st.file_uploader(label="", type="pdf")
    openai_api_key = st.text_input(label="OpenAI API Key", type="password")
    try:
        if pdf is not None and openai_api_key is not None:
            pdf_chunks = resume_analyzer.pdf_to_chunks(pdf)
            summary = resume_analyzer.resume_summary(query_with_chunks=pdf_chunks)
            result_summary = resume_analyzer.openai(
                openai_api_key=openai_api_key, chunks=pdf_chunks, analyze=summary
            )
            st.subheader("Summary:")
            st.write(result_summary)
    except Exception as e:
        col1, col2 = st.columns(2)
        with col1:
            st.warning(e)

elif option == "Strength":
    pdf = st.file_uploader(label="", type="pdf")
    openai_api_key = st.text_input(label="OpenAI API Key", type="password")
    try:
        if pdf is not None and openai_api_key is not None:
            pdf_chunks = resume_analyzer.pdf_to_chunks(pdf)
            summary = resume_analyzer.resume_summary(query_with_chunks=pdf_chunks)
            result_summary = resume_analyzer.openai(
                openai_api_key=openai_api_key, chunks=pdf_chunks, analyze=summary
            )
            strength = resume_analyzer.resume_strength(query_with_chunks=result_summary)
            result_strength = resume_analyzer.openai(
                openai_api_key=openai_api_key, chunks=pdf_chunks, analyze=strength
            )
            st.subheader("Strength:")
            st.write(result_strength)
    except Exception as e:
        col1, col2 = st.columns(2)
        with col1:
            st.warning(e)


elif option == "Weakness":
    pdf = st.file_uploader(label="", type="pdf")
    openai_api_key = st.text_input(label="OpenAI API Key", type="password")
    try:
        if pdf is not None and openai_api_key is not None:
            pdf_chunks = resume_analyzer.pdf_to_chunks(pdf)
            summary = resume_analyzer.resume_summary(query_with_chunks=pdf_chunks)
            result_summary = resume_analyzer.openai(
                openai_api_key=openai_api_key, chunks=pdf_chunks, analyze=summary
            )
            weakness = resume_analyzer.resume_weakness(query_with_chunks=result_summary)
            result_weakness = resume_analyzer.openai(
                openai_api_key=openai_api_key, chunks=pdf_chunks, analyze=weakness
            )
            st.subheader("Weakness:")
            st.write(result_weakness)
    except Exception as e:
        col1, col2 = st.columns(2)
        with col1:
            st.warning(e)

elif option == "Job Titles":
    pdf = st.file_uploader(label="", type="pdf")
    openai_api_key = st.text_input(label="OpenAI API Key", type="password")
    try:
        if pdf is not None and openai_api_key is not None:
            pdf_chunks = resume_analyzer.pdf_to_chunks(pdf)
            summary = resume_analyzer.resume_summary(query_with_chunks=pdf_chunks)
            result_summary = resume_analyzer.openai(
                openai_api_key=openai_api_key, chunks=pdf_chunks, analyze=summary
            )
            job_suggestion = resume_analyzer.job_title_suggestion(
                query_with_chunks=result_summary
            )
            result_suggestion = resume_analyzer.openai(
                openai_api_key=openai_api_key, chunks=pdf_chunks, analyze=job_suggestion
            )
            st.subheader("Suggestion: ")
            st.write(result_suggestion)
    except Exception as e:
        col1, col2 = st.columns(2)
        with col1:
            st.warning(e)

elif option == "Linkedin Jobs":
    try:
        user_input_job_title = st.text_input(
            label="Enter Job Titles (with comma separated):"
        )
        submit = st.button("Submit")
        if submit and len(user_input_job_title) > 0:
            user_job_title = user_input_job_title.split(",")
            df = linkedin_scrap.main(user_job_title)
            l = len(df["Company Name"])
            for i in range(0, l):
                st.write(f"Company Name : {df.iloc[i,0]}")
                st.write(f"Job Title    : {df.iloc[i,1]}")
                st.write(f"Location     : {df.iloc[i,2]}")
                st.write(f"Website URL  : {df.iloc[i,3]}")
                with st.expander(label="Job Desription"):
                    st.write(df.iloc[i, 4])
                st.write("")
                st.write("")
        elif submit and len(user_input_job_title) == 0:
            col1, col2 = st.columns(2)
            with col1:
                st.info("Please Enter the Job Titles")
    except:
        st.write("")
        st.info(
            "This feature is currently not working in the deployed Streamlit application due to a 'selenium.common.exceptions.WebDriverException' error."
        )
        st.write("")
        st.write(
            "Please use the local Streamlit application for a smooth experience: [http://localhost:8501](http://localhost:8501)"
        )

elif option == "Exit":
    add_vertical_space(3)
    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])
    with col2:
        st.success("Thank you for your time. Exiting the application")
        st.snow()
