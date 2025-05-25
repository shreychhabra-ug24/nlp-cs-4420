## Project - Emotion Aware Speech Transcription (Multimodal)
Basically the title, uses a mix of transcription as well as audio based analyses to determine emotional context of a given audio recording. Contains a CNN trained on the CREMA-D dataset (https://www.kaggle.com/datasets/ejlok1/cremad) based on the mel-spectrograms of the the given audio files, as well as the j-hartmann/emotion-english-distilroberta-base transformer (on huggingface) for predictions based on text. First, an audio input is taken from a user, its features are extracted, a prediction is made and a probability output of some emotion is given. The text is then transcribed by using OpenAI Whisper for ASR (Automated Speech Recognition), and sentiment analysis is performed on it by the transformer, and a similar probability output is given. The fusion of the two models is a late fusion step where the probabilities are given equal weightage for making the final emotion prediction.

Important to note that the accuracy for the CNN is only about 52% (but I am yet to see a model cross 66%), and that the transformer is pretrained on a different dataset (goemotions with more than 20 different emotion classes). I do map these emotions to the 6 emotions in CREMA-D.

## Instructions

# Setup a Virtual Environment
In the project directory, run the following commands in the terminal (you might have to use either python -m venv .venv or python3 as shown below)
1. python3 -m venv .venv 
2. .venv\Scripts\activate (On Windows)
3. source .venv/bin/activate (On MacOS/Linux)
4. pip install -r requirements.txt (Installs the required packages in your venv)

# Run the Model

Download the training dataset from  - 
Unzip and move the dataset to the main project directory
Open audio-cnn-with-multimodal-fusion.ipynb and run all cells
It should take about 5 minutes to train and generate the model weights, you can record audio in the last cell and use your own inputs. 