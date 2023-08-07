# Q&A App for Drugs & Medication in English - Developed with OpenAI APIs
# by Inuri Muthukumarana
# Last Update: 2022-08-07

import openai
import streamlit as st
import configparser
import os

config = configparser.ConfigParser()
config.read('F:\QnA_App/config.ini')

openai_api_key = config['SECRETS']['openai_api_key']

st.title("💊 Medication and Drugs Q&A App")
st.write("_This app is designed to provide informational answers about medications and drugs. Please remember that the information presented here is for general purposes only. Consult a qualified healthcare professional for professional advice and guidance_")


def answer_generate(user_prompt):    
    prompt = F"You have to answer question about medications and drugs based on the context given. Always mention 'Remember, this app is not a substitute for consulting a qualified healthcare professional' at the end of the answer. If the question is nonsense or no clear answer is found, respond 'Sorry I could not find the answer. Please reach out to your healthcare provider for clarification and guidance!' \n\n{user_prompt}\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return prompt, response

with st.form("my_form"):
    user_prompt = st.text_area("Type your question here", "")
    submitted = st.form_submit_button("Submit")
    if submitted:
        openai.api_key = openai_api_key
        prompt, response = answer_generate(user_prompt)
        st.info(response["choices"][0]["text"])

        with st.expander("Response"):
            st.write(response)