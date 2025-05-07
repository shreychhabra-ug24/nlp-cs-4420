import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")
df = pd.read_csv("ozempic_news_150.csv")

#extract POS tags
def pos_tag_text(text):
    doc = nlp(str(text))  
    pos_tags = [(token.text, token.pos_) for token in doc]
    return pos_tags

df["POS_Tags"] = df["Text"].apply(pos_tag_text)
df.to_csv("ozempic_news_pos.csv", index=False)

print("POS tagging complete. Results saved to ozempic_news_pos.csv")
