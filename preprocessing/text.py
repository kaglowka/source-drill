import regex
from syntok.segmenter import split
from syntok.tokenizer import Tokenizer
from flair.data import Sentence

token_filter_re = r'^\p{L}(\p{L}|\.|[0-9])+$'

def filter_tokens(tokens):
    # Filter out non-common-word/non-real-world-entity tokens
    return [
        token for token in tokens if
            regex.match(token_filter_re, token.text)
    ]


author_re = r'(((de|De|van|Van|von|Von)\s+(\p{Ll}+\s+)?)?\p{Lu}(\p{Ll}|-)+)'


citation_re = (
               r'([(;,]|\s)'
            + author_re +
               r'(\s?((([&,]|and|\s)+\s?' + author_re + r')|(et al\.?)))?'  # alternative second author
               r'('
                 r'([;,]|\s)+'
                 r'\s*[0-9]{4}\p{Ll}?\s*'  # year
               r')+'
               r'([);,]|\s)'
              )

in_text_citation_re = (
    author_re + r'\s*\((\s*[0-9]{4}\p{Ll}?\s*,?)\)'
)


def remove_citations(text):
    n_subs_made = 1
    while n_subs_made > 0:
        text, n_subs_made = regex.subn(citation_re, ';', text)
        text, n_subs_made2 = regex.subn(citation_re, ';', text)
        n_subs_made += n_subs_made2
    return text


def text_to_chunks(text):
    chunksize = 1
    tokenized_sents = list(split(Tokenizer().tokenize(text)))
    sents = [' '.join(str(token) for token in sent) for sent in tokenized_sents]
    sents = [' '.join(sents[i:i+chunksize]) for i in range(len(sents)-chunksize)]
    sentences = []
    for sent in sents:
        sent = text_to_sentence(sent)
        if sent is not None:
            sentences.append(sent)
    return sentences


def text_to_sentence(text):
    text = remove_citations(text)
    s = Sentence(text, use_tokenizer=True)
    s.tokens = filter_tokens(s.tokens)
    if len(s.tokens) > 0:
        return s
    else:
        return None

