import json
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from collections import defaultdict
import ast  # For parsing string tuples from CSV

#manual annotations
manual_ner_path = "annotated-ner-manual.json"
with open(manual_ner_path, "r", encoding="utf-8") as f:
    manual_annotations = json.load(f)

#extract ground truth entities (only manually labeled ones)
true_entities = defaultdict(list)
text_data = {}

for annotation in manual_annotations:
    article_id = annotation["id"]
    text_data[article_id] = annotation["data"]["text"]  # Store article text
    
    for result in annotation["annotations"][0]["result"]:
        entity_text = result["value"]["text"]
        entity_label = result["value"]["labels"][0]
        true_entities[article_id].append((entity_text, entity_label))

#spacy ner predictions
ner_csv_path = "ozempic_news_ner.csv"
df_ner = pd.read_csv(ner_csv_path)
predicted_entities = {}

for index, row in df_ner.iterrows():
    article_id = index 
    if isinstance(row["Named_Entities"], str):
        try:
            pred_ents = ast.literal_eval(row["Named_Entities"])  # Convert string tuple to list of tuples
            predicted_entities[article_id] = pred_ents if isinstance(pred_ents, list) else [pred_ents]
        except (SyntaxError, ValueError):
            predicted_entities[article_id] = []
    else:
        predicted_entities[article_id] = []

#only evaluates words that were manually labeled (ignores null entries)
true_labels = []
pred_labels = []

for article_id in true_entities:
    true_set = set(true_entities[article_id])
    pred_set = set(predicted_entities.get(article_id, []))
    
    for entity in true_set:  
        true_labels.append(entity[1])  # True label from manual annotation
        pred_label = next((pred[1] for pred in pred_set if pred[0] == entity[0]), "O")  # Match predicted entity
        pred_labels.append(pred_label)

# Compute Precision, Recall, and F1-score
precision = precision_score(true_labels, pred_labels, average="weighted", zero_division=0)
recall = recall_score(true_labels, pred_labels, average="weighted", zero_division=0)
f1 = f1_score(true_labels, pred_labels, average="weighted", zero_division=0)


print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-score: {f1:.4f}")

#bad results expected?