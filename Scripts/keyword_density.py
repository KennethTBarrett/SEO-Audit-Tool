import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import re

# Ensure NLTK data has been downloaded
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')


def get_wordnet_pos(word):
    """Convert NTLK POS tags to WordNet Compatible"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


# def get_synonyms(word):
#     """Gets synonyms for keyword to ensure coverage"""
#     synonyms = set()
#     for syn in wordnet.synsets(word):
#         for lemma in syn.lemmas():
#             synonyms.add(lemma.name())
#     return synonyms


# def lemmatize_text(text):
#     """Lemmatizes text before sending for keyword density calculation"""
#     lemmatizer = WordNetLemmatizer()
#     words = nltk.word_tokenize(text)
#     lemmatized = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in words]
#     return ' '.join(lemmatized)

def calc_keyword_density(text, keywords):
    """Calculates keyword density"""
    vectorizer = CountVectorizer(vocabulary=keywords)
    word_count = vectorizer.fit_transform([text]).toarray().sum(axis=0)
    total_words = len(re.findall(r'\w+', text))
    keyword_density = {word: (count / total_words) * 100 for word,
                       count in zip(keywords, word_count)}
    return keyword_density


text = "This is a sample text to analyze keyword density. The text is simple and contains several repeated words like text to analyze."
keywords = ["run", "simple", "analyze"]

density = calc_keyword_density(text, keywords)
print(density)