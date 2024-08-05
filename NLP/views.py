import textwrap
import google.generativeai as genai
from IPython.display import display, Markdown
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import json
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import matplotlib.pyplot as plt
import numpy as np

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')



genai.configure(api_key=GOOGLE_API_KEY)
tokenizer = AutoTokenizer.from_pretrained("avichr/heBERT_sentiment_analysis")
model_hebret = AutoModelForSequenceClassification.from_pretrained("avichr/heBERT_sentiment_analysis")

model = genai.GenerativeModel('gemini-1.5-pro')
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



def call_geminie(prompt,text):
    max_attempts = 5
    attempts = 0
    try:
        formatted_prompt = f"{prompt}\n\n{text}"
        
        while attempts < max_attempts:
            response = model.generate_content(formatted_prompt)
            attempts += 1
            
            # Process the response
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts') and candidate.content.parts:
                    text_content = candidate.content.parts[0].text
                    return jsonify({'generated_content': text_content}), 200
        
        return jsonify({'error': 'No valid content parts available in the response after multiple attempts.'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500




def improve():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'No text field provided in JSON'}), 400
    
    text = data['text']
    prompt = "זה התמלול הראשוני בבקשה תשפר את זה, תשמור על סדר?"
    response1, status1 = call_geminie(prompt, text)
    if status1 != 200:
        return jsonify({'error': 'Error processing first request'}), status1
    summary = response1.get_json().get('generated_content', 'No content')
    result = {
        'summary': summary,
    }
    
    return jsonify(result)



def subject_extract():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'No text field provided in JSON'}), 400
    
    text = data['text']
    prompt = "מה הנושא המרכזי בטקסט? תסכם לי את הטקסט במשפט אחד,תן לי תשובה ב json?"
    response3, status3 = call_geminie(prompt, text)
    if status3 != 200:
        return jsonify({'error': 'Error processing third request'}), status3
    subject_content = response3.get_json().get('generated_content', 'No content')
    
    try:
        start_index = subject_content.find('{')
        end_index = subject_content.rfind('}') + 1
        json_text = subject_content[start_index:end_index]
        subject = json.loads(json_text).get('נושא_מרכזי', 'No content')
    except (json.JSONDecodeError, ValueError) as e:
        return jsonify({'error': f'JSON parsing error: {e}'}), 500
    
    result = {
        'subject': subject
    }
    
    return jsonify(result)


def summary_text():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'No text field provided in JSON'}), 400
    
    text = data['text']
    
    prompt = "בבקשה תסכם"
    response1, status1 = call_geminie(prompt, text)
    if status1 != 200:
        return jsonify({'error': 'Error processing first request'}), status1
    summary = response1.get_json().get('generated_content', 'No content')
    
    result = {
        'summary': summary
    }
    
    return jsonify(result)
    
    

def sentiment_analysis():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'No text field provided in JSON'}), 400
    
    text = data['text']
    sentences = re.split(r'(?<=\.)|(?<=\?)|(?<=!)', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    print(f"Sentences: {sentences}") 
    
    sentiment_analysis_pipeline = pipeline(
        "sentiment-analysis",
        model=model_hebret,
        tokenizer=tokenizer,
        return_all_scores=True
    )
    
    results = [{'sentence': sentence, 'analysis': sentiment_analysis_pipeline(sentence)} for sentence in sentences]
    return jsonify(results)
        
        