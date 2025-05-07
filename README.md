# NLP-CS4420
Contains assignments and project for the course Natural Language Processing - Theory and Applications (CS-4420) at Ashoka University in Spring 2025

## Assignment 1
POS Tagging, Named Entity Recognition, Coreference Resolution, Entity Resolution. Contains scripts for scraping Google, Bing, and MSN articles about ozempic, and performing the mentioned tasks on said articles. All tasks available in separate scripts with their respective CSV outputs. For manual annotation to measure accuracy of the NER and Coref model, I recommend using Label Studio. 

## Assignment 2
Classification of a mental health tweets dataset with LSTMs and Transformers, explanation generation with LIME and Occlusion, identification and interpretation of class signatures. Basic lstm architecture - embedding layer to convert words into dense vector representations, LSTM layer to capture textual patterns, fully connected (dense) layer to LSTM outputs to classification labels, softmax activation for producing probabilities for each mental health class. I've performed the same task with BERT for comparison, colab notebook attached here: https://colab.research.google.com/drive/12eIjTfEC0obRQ4ITrpGU5ZYrzaE8Jtto?usp=sharing

## Assignment 3
### Instructions: 
Given are a set of positive examples of sentences indicating adverse drug effects. 
Your task is to identify drug mentions in the text along with the causal relations that link a drug with an effect/symptom. 
 
Given below are two models that can help you in doing some of the tasks mentioned above - 

1. https://huggingface.co/MilosKosRad/BioNER for NER
2. https://huggingface.co/taskload/bart-cause-effect for Cause-Effect extraction

You are free to use any other model additionally or instead of them also.

Final output - 
1. A list of drugs mentioned with number of mentions of each 
2. A consolidated list of adverse symptoms associated with each drug. Please provide frequency counts, if you encounter the same pair more than once. 
3. A consolidated list of symptoms that the drug cures. Please provide frequency counts, if you encounter the same pair more than once. 
4. Discussion / observations  about your assessment of correctness.

The provided code works, but is horribly slow (about 80 minutes to run parts 2 and 3). Recommend using a GPU for these tasks.

## RAG - Retrieval-Augmented Generation

Sample code provided in class for RAG. References a knowledge base outside its training data (PDFs related to Ashoka in this case - department as well as college policy docs) to optimize the output of some given LLM (in this case I've used Gemini which offers its API for free). I've provided a link to the dataset, but the program works regardless of which pdf dataset you use. Not written by me!

## Project - Emotion Aware Speech Transcription (Multimodal)
Basically the title, uses a mix of transcription as well as audio based analyses to determine emotional context of a given audio recording. Contains a CNN trained on the CREMA-D dataset (https://www.kaggle.com/datasets/ejlok1/cremad) based on the mel-spectrograms of the the given audio files, as well as the j-hartmann/emotion-english-distilroberta-base transformer (on huggingface) for predictions based on text. First, an audio input is taken from a user, its features are extracted, a prediction is made and a probability output of some emotion is given. The text is then transcribed by using OpenAI Whisper for ASR (Automated Speech Recognition), and sentiment analysis is performed on it by the transformer, and a similar probability output is given. The fusion of the two models is a late fusion step where the probabilities are given equal weightage for making the final emotion prediction.

Important to note that the accuracy for the CNN is only about 52% (but I am yet to see a model cross 66%), and that the transformer is pretrained on a different dataset (goemotions with more than 20 different emotion classes). I do map these emotions to the 6 emotions in CREMA-D.
