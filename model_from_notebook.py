#!/usr/bin/env python
# coding: utf-8

# In[9]:


#Install necessary libraries
# get_ipython().system('pip install SpeechRecognition')
# get_ipython().system('pip install pydub')
# get_ipython().system('pip install spacy')
# get_ipython().system('pip install nltk')
# get_ipython().system('pip install SpeechRecognition pydub spacy nltk')
# get_ipython().system('python -m spacy download en_core_web_sm')
# get_ipython().system('pip install seaborn')


# In[10]:


# Import required libraries
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import speech_recognition as sr
from pydub import AudioSegment
import spacy
from matplotlib import pyplot as plt
import seaborn as sns   
import os
import tempfile


# Transcribing and analysing sample customer call.

# In[11]:


def analyze_audio(audio_path):
    import speech_recognition as sr
    from pydub import AudioSegment
    import os
    # Convert to WAV if not already
    file_ext = os.path.splitext(audio_path)[1].lower()
    if file_ext != '.wav':
        audio = AudioSegment.from_file(audio_path)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wav:
            audio.export(tmp_wav.name, format='wav')
            wav_path = tmp_wav.name
    else:
        wav_path = audio_path
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
    try:
        transcribed_text = recognizer.recognize_google(audio_data)
    except Exception as e:
        transcribed_text = f"Transcription failed: {e}"
    wav_file = AudioSegment.from_file(wav_path)
    frame_rate = wav_file.frame_rate
    number_channels = wav_file.channels
    # Clean up temp file if created
    if file_ext != '.wav' and os.path.exists(wav_path):
        os.remove(wav_path)
    return {
        'transcription': transcribed_text,
        'frame_rate': frame_rate,
        'channels': number_channels
    }


if __name__ == '__main__':
    # Transcribing and analysing sample customer call.
    recognizer = sr.Recognizer()
    sample_customer_call = sr.AudioFile(r'Analyzing-Customer-Support-Calls/sample_customer_call.wav')
    with sample_customer_call as source:
        sample_customer_call_data = recognizer.record(source)
    transcribed_text = recognizer.recognize_google(sample_customer_call_data)
    print(f"Transcription: {transcribed_text}")
    #import and analyzing audio
    wav_file = AudioSegment.from_file(r'Analyzing-Customer-Support-Calls/sample_customer_call.wav')
    frame_rate = wav_file.frame_rate
    number_channels = wav_file.channels
    print(f'Frame rate: {frame_rate}\nNumber of channels: {number_channels}')

    # Importing customer call transcriptions and analyzing them with VADER lexicon. Assigning a label based on the 'compound' score.
    df = pd.read_csv(r'Analyzing-Customer-Support-Calls/customer_call_transcriptions.csv')
    print(df.shape)
    print(df.head())
    sid = SentimentIntensityAnalyzer()
    df['polarity_score_compound'] = df['text'].apply(lambda x:sid.polarity_scores(x)['compound'])
    def classify(score):
        if score >= 0.05:
            return "positive"
        elif score <= -0.05:
            return "negative"
        else:
            return "neutral"
    df['sentiment'] = df['polarity_score_compound'].apply(classify)
    print(df.head())
    sns.kdeplot(df['polarity_score_compound'])
    plt.title('Distribution of Sentiment Compound Scores')
    plt.show()

    # Finding most frequent entities appling NER with spaCy model.
    nlp = spacy.load("en_core_web_md")
    entity_dict = {}
    for text in df['text']:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.text in entity_dict:
                entity_dict[ent.text] += 1
            else:
                entity_dict[ent.text] = 1
    #convert dictionary to dataframe and sorting
    entity_df = pd.DataFrame({"entity": entity_dict.keys(), "count": entity_dict.values()}).sort_values(by='count', ascending=False)
    print(entity_df.head())

    # Searching for most similar context to the phrase: "wrong package delivered".
    input_query = 'wrong package delivery'
    processed_query = nlp(input_query)
    df['similarity'] = df['text'].apply(lambda x: processed_query.similarity(nlp(x)))
    pd.set_option('display.max_colwidth', None)
    print(df.sort_values(by='similarity', ascending=False).head())
    # Please refer to the README file for more possible enhancements to this project
