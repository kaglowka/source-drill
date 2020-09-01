import pandas as pd
import spacy
spacy_stopwords = spacy.load('en_core_web_sm').Defaults.stop_words


def embedding_score(link, metrics, embedding_name, embedding):
    all_sim = {}

    s = link.citing_context_part
    s.tokens = [token for token in s if token.text not in spacy_stopwords]

    embedding.embed(s)
    citation_embedding = s.embedding.detach().numpy()

    sentences = link.cited_text_parts
    for sentence in sentences:
        embedding.embed(sentence)
        all_sim[sentence.to_plain_string()] = {}
        for name, metric in metrics.items():
            sim = metric(sentence.embedding.detach().numpy(), citation_embedding)
            full_name = '_'.join([embedding_name, name])
            all_sim[sentence.to_plain_string()][full_name] = sim
        sentence.clear_embeddings()
    s.clear_embeddings()

    return pd.DataFrame(all_sim).T
