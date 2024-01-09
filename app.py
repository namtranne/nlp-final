import time
import streamlit as st
import SessionState
import numpy as np
from predictor import Predictor
from dataset.add_noise import SynthesizeData
import requests
from closest_predictor import ClosestPredictor
# openai.
# client = OpenAI()
state = SessionState.get(text_correct="", input="", noise="")

def replace_missing_words(sentence, word_dict, predictor):
    words = sentence.split()

    for i in range(len(words)):
        word = words[i]

        if word.lower() not in word_dict:
            # Use the predictor to predict the missing word
            predicted_word = predictor.predict(word)

            # Replace the missing word in the sentence
            words[i] = predicted_word

    # Join the words back into a sentence
    replaced_sentence = ' '.join(words)
    state.text_correct2 = replaced_sentence

def predict_long_word(sentence, word_dict, predictor):
    words = sentence.split()

    for i in range(len(words)):
        word = words[i]

        if word.lower() not in word_dict and len(word)>=7:
            # Use the predictor to predict the missing word
            predicted_word = predictor.predict_long_word(word)

            # Replace the missing word in the sentence
            words[i] = predicted_word

    # Join the words back into a sentence
    replaced_sentence = ' '.join(words)
    return replaced_sentence

def main(word_dict, predictor):
    model = load_model()
    synther = SynthesizeData()
    st.title("Vietnamese spelling correction website")
    # Load model
    state.input = ""
    state.noise = ""
    text_input = st.text_area("Input:", value=state.input)
    text_input = text_input.strip()
    if st.button("Correct spelling"):
        state.noise = text_input

        url = "http://localhost:3000/complete"
        body = {"content": text_input}

        # Making the POST request
        response = requests.post(url, json=body)

        # Checking the response
        if response.status_code == 200:
            print("Request successful!")
            response = response.json()
            response = response['response']
            state.text_correct = response
        else:
            print(f"Request failed with status code {response.status_code}")
            print("Response text:", response.text)
        
        text_correct = predict_long_word(state.noise, word_dict, predictor)
        text_correct = model.spelling_correct(text_correct)
        replace_missing_words(text_correct, word_dict, predictor)
        st.text("Input: ")
        st.success(state.noise)
        st.text("OpenAI's result:")
        st.success(state.text_correct)
        st.text("Model's result:")
        st.success(state.text_correct2)
    
    if st.button("Add noise and Correct"):
        state.noise = synther.add_noise(text_input, percent_err=0.3)
        # state.output = noise_text
        state.text_correct = model.spelling_correct(state.noise)
        url = "http://localhost:3000/complete"
        body = {"content": text_input}

        # Making the POST request
        response = requests.post(url, json=body)

        # Checking the response
        if response.status_code == 200:
            print("Request successful!")
            response = response.json()
            response = response['response']
            state.text_correct = response
        else:
            print(f"Request failed with status code {response.status_code}")
            print("Response text:", response.text)
        
        text_correct = predict_long_word(state.noise, word_dict, predictor)
        text_correct = model.spelling_correct(text_correct)
        replace_missing_words(text_correct, word_dict, predictor)
        st.text("Input: ")
        st.success(state.noise)
        st.text("OpenAI's result:")
        st.success(state.text_correct)
        st.text("Model's result:")
        st.success(state.text_correct2)


@st.cache(allow_output_mutation=True)  # hash_func
def load_model():
    print("Loading model ...")
    # model1 = Predictor(weight_path='weights/seq2seq.pth', have_att=True)
    model2 = Predictor(weight_path='weights/seq2seq_luong.pth', have_att=True)
    return model2


if __name__ == "__main__":
    word_dict = set()
    with open('frequency_generate/index.dic', 'r', encoding='utf-8') as dic_file:
        for line in dic_file:
            # Remove leading and trailing whitespaces, and convert to lowercase
            dictionary_word = line.strip().lower()
            
            # Add the lowercase word to the set
            word_dict.add(dictionary_word)
    predictor = ClosestPredictor()
    main(word_dict, predictor)