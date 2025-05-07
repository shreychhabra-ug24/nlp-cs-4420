import pandas as pd
from stanza.server import CoreNLPClient
import json  

#stanza neural coref with corenlp
client = CoreNLPClient(annotators=["tokenize", "ssplit", "pos", "lemma", "ner", "parse", "coref"], 
                       properties={'coref.algorithm': 'neural'}, 
                       timeout=600000, memory="8G")

def resolve_coreferences(text):
    if not isinstance(text, str) or text.strip() == "":
        return text  #skips empty or non-string values

    ann = client.annotate(text)
    
    #extracts coref chains
    coref_chains = {}
    for chain in ann.corefChain:
        representative = chain.mention[0]
        rep_text = " ".join(text.split()[representative.beginIndex:representative.endIndex])

        for mention in chain.mention[1:]:  #skip the representative
            mention_text = " ".join(text.split()[mention.beginIndex:mention.endIndex])
            coref_chains[mention_text] = rep_text

    #replaces mentions with representative names
    resolved_text = text
    for mention, rep in coref_chains.items():
        resolved_text = resolved_text.replace(mention, rep)

    return resolved_text, json.dumps(coref_chains)  # Return both resolved text & coref chains

df = pd.read_csv("ozempic_news_150.csv")  

#coref
df[["resolved_text", "coref_chains"]] = df["Text"].apply(lambda text: pd.Series(resolve_coreferences(text)))
df.to_csv("ozempic_neural_coref_with_chains.csv", index=False)

print("Coreference resolution completed and stored in 'resolved_text' and 'coref_chains' columns.")
