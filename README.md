# AI Resume Analyser

**Overview**

"Resume Analyzer AI" is an innovative Streamlit application powered by LLM and OpenAI, designed for in-depth resume analysis. It offers features such as summarization, strength evaluation, weakness identification, improvement suggestions, and job title recommendations. Additionally, it seamlessly integrates Selenium to extract valuable LinkedIn data, including company names, job titles, locations, URLs, and detailed job descriptions. This tool aims to simplify the job search process by providing users with comprehensive insights to enhance their career prospects.

**Table of Contents**

1. Key Technologies and Skills
2. Installation Guide
3. How to Use
4. Features Overview
5. Contribution Guidelines
6. Licensing Information
7. Contact Details

**Key Technologies and Skills**
- Python Programming Language
- Numpy for Numerical Computations
- Pandas for Data Manipulation
- Streamlit for Web Application Development
- LLM (Large Language Model)
- LangChain for Text Analysis
- OpenAI for Advanced AI Capabilities
- Selenium for Web Scraping

**Installation Guide**

To run this application, you need to install the following packages:

```python
pip install numpy
pip install pandas
pip install streamlit
pip install streamlit_option_menu
pip install streamlit_extras
pip install PyPDF2
pip install langchain
pip install openai
pip install tiktoken
pip install faiss-cpu
pip install selenium
```

**How to Use**

To utilize this tool, follow these steps:
1. Install the required packages using `pip install -r requirements.txt`.
2. Run the Streamlit application by executing `streamlit run app.py`.
3. Access the application in your web browser at `http://localhost:8501`.

**Features Overview**

**User-Friendly Experience:**
- Resume Analyzer AI offers a user-friendly interface for easy resume analysis. Users can upload their resumes and enter their OpenAI API key seamlessly.
- The tool employs PyPDF2 to swiftly extract text from resumes, streamlining the analysis process.

**Smart Text Analysis with Langchain:**
- Utilizing Langchain, the tool intelligently breaks down lengthy resume sections into smaller, meaningful chunks, enhancing analysis accuracy and providing practical insights for career improvement.

**Enhanced OpenAI Integration with FAISS:**
- The application integrates seamlessly with OpenAI services using the user's API key, enabling advanced analysis and efficient data retrieval.
- Leveraging FAISS, it converts text chunks and query data into numerical vectors, simplifying analysis and information retrieval.

**Intelligent Chunk Selection and LLM:**
- Through similarity search, Resume Analyzer AI selects the top 'K' most similar chunks based on similarity scores between the query and text chunks.
- It utilizes an LLM (Large Language Model), specifically ChatGPT 3.5 Turbo, and the user's OpenAI API key for robust analysis.

**Robust Question-Answering Pipeline:**
- The tool employs a robust question-answering pipeline, utilizing multiple components, including the language model, to efficiently handle input documents and questions, providing comprehensive responses.

**Comprehensive Resume Analysis:**
- **Summary:** Provides a comprehensive overview of resumes, highlighting qualifications, experience, skills, projects, and achievements, enhancing review efficiency.
- **Strength:** Conducts a thorough review of qualifications, experience, and accomplishments, highlighting strengths for job seekers.
- **Weakness:** Pinpoints weaknesses and offers tailored solutions for improvement, empowering job seekers.
- **Suggestion:** Provides personalized job title recommendations aligned with the user's qualifications and resume content, optimizing the job search experience.
