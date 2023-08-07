# Q&A App for Drugs & Medication in Sinhala - Developed with OpenAI APIs
# by Inuri Muthukumarana
# Last Update: 2022-08-07

import requests
import json
import openai
import streamlit as st
import configparser
import os

config = configparser.ConfigParser()
config.read('F:\QnA_App/config.ini')
openai_api_key = config['SECRETS']['openai_api_key']
lingvanex_api_key = config['SECRETS']['lingvanex_api_key']


st.title("💊 ඖෂධ සඳහා ප්‍රශ්න සහ පිළිතුරු යෙදුම - සිංහල")
st.write("_මෙම යෙදුම ඖෂධ පිළිබඳ තොරතුරු සැපයීම සඳහා නිර්මාණය කර ඇත. වඩා ගුණාත්මක උපදෙස් සහ මගපෙන්වීම සඳහා සුදුසුකම් ලත් සෞඛ්‍ය සේවා වෘත්තිකයෙකුගෙන් විමසන්න_")

def answer_generate(user_prompt):    
    prompt = F"You are an Q&A application designed to provide informational answers about medication and drugs. Always limit the answer to two sentences and mention 'Remember, this app is not a substitute for consulting a qualified healthcare professional' at the end of the answer. If the question is nonsense or no clear answer is found, respond 'Sorry I could not find the answer. Please reach out to your healthcare provider for clarification and guidance!' \n\n{user_prompt}\n\n"
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


def translate(user_prompt,from_lang, to_lang): 
    url = "https://api-b2b.backenster.com/b1/api/v3/translate"
    payload = {
        "platform": "api",
        "from": from_lang,
        "to": to_lang,
        "data": user_prompt
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": lingvanex_api_key
    }
    response = requests.post(url, json=payload, headers=headers)
    parsed_data = json.loads(response.text)
    response = parsed_data.get("result", None)

    return response

with st.form("my_form"):
    user_prompt = st.text_area("ඔබේ ප්‍රශ්නය මෙහි ටයිප් කරන්න", "")
    submitted = st.form_submit_button("සබ්මිට් කරන්න")
    if submitted:
        trans_s2e_response = translate(user_prompt,"si_LK","en_GB")

        openai.api_key = openai_api_key

        ans_prompt, ans_response = answer_generate(trans_s2e_response)

        trans_e2s_response = translate(ans_response["choices"][0]["text"],"en_GB","si_LK") 
        st.info(trans_e2s_response)

        with st.expander("Response"):
            st.write(ans_response)
