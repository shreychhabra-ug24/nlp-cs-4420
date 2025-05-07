import pandas as pd
import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Load the DataFrame (assuming it's saved after POS tagging)
df = pd.read_csv("ozempic_news_pos.csv")

# Function to extract named entities
def extract_named_entities(text):
    doc = nlp(str(text))  # Ensure text is a string
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Apply NER tagging to the "Text" column
df["Named_Entities"] = df["Text"].apply(extract_named_entities)

# Save the updated DataFrame
df.to_csv("ozempic_news_ner.csv", index=False)

print("NER tagging complete. Results saved to ozempic_news_ner.csv")
