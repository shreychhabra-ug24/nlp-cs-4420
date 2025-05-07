import pandas as pd
import json

#utility script for converting csv to json for labeling input on label studio

df = pd.read_csv("ozempic_news_150.csv")
subset_df = df.head(50)

articles = [{"text": row["Text"]} for _, row in subset_df.iterrows()]

output_file = "articles_for_label_studio.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=4, ensure_ascii=False)

print(f"Saved {len(articles)} articles to {output_file}")
