# libraries
import re
import random
import numpy as np
import pickle
import json
from flask import Flask, render_template, request
from maths_patterns import equtionCleaner, replace_keywords
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pyttsx3 as p
from gtts import gTTS
import os

engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 120)
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

model = load_model('chatbot_model.h5')
data_file = open("intents.json").read()
intents = json.loads(data_file)
with open('words.pkl', 'rb') as words_:
    words = pickle.load(words_)

with open('classes.pkl', 'rb') as enc:
    classes = pickle.load(enc)

app = Flask(__name__)
# run_with_ngrok(app) 

@app.route("/")
def home():
    # engine.say("Hi. I'm your math bot.")
    # engine.runAndWait()
    return render_template("index.html")
    

@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    
    pattern = r"^(solve|evaluate|calculate|compute|what is|equate) [(0-9)]+"
    pattern2 = r"^([-+(]?\d+(\.\d+)?)+"
    pattern3 = r"\d+ [a-z ]+ \d+"

    
    # Chaecking if the msg sent by the user follows the first pattern
    if re.match(pattern, msg.lower()) != None:

        # Checking if the msg entered by the user follows the pattern3
        if len(re.findall(pattern3, msg.lower())) > 0:
            msg = replace_keywords(msg)
            print("54 ",msg)
        msg_ = msg.split()

        # Checking if the msg starts with "what is" and followed by a non string (numerical value)
        if msg.lower().startswith("what is") and msg_[2].isalpha() == False:
            msg_.pop(0)
            msg_[0] = "what is"

        # Passing the msg from the user to the equationCleaner class
        ec= equtionCleaner(' '.join(msg_[1:]))
        eqn_ = ec.equation
        eqn = eval(eqn_)

        # Passing the first part of the string to the prediction and replacing the placeholder with the evaluation of the equation
        ints = predict_class(msg_[0], model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",str(eqn))
        
    elif re.match(pattern2, msg.lower()) != None:
        ec= equtionCleaner(msg)
        eqn_ = ec.equation
        eqn = eval(eqn_)
        ints = predict_class("solve", model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",str(eqn))
    elif msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)

    # engine.say(res)
    # engine.runAndWait()
    comp_res(res)
    return res


# chat functionalities
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    print("Bag :", bag)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    result = ''
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result

def comp_res(response):
    #Recording voice input using microphone     
    file = "file.mp3"
    tts = gTTS(text=response,lang="en",tld="com")
    tts.save(file)
    os.system("mpg123 " + file )


if __name__ == "__main__":
    print(__name__)
    app.run()

