import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
import re
import requests

# Ensure NLTK data has been downloaded
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def fetch_text(url):
    doc = url
    res = requests.get(doc)
    soup = BeautifulSoup(res.content, 'html.parser').get_text()
    return soup


def get_wordnet_pos(word):
    """Convert NLTK POS tags to WordNet Compatible"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def calc_keyword_density(text, keywords):
    """Calculates keywod density"""
    vectorizer = CountVectorizer(vocabulary=keywords)
    word_count = vectorizer.fit_transform([text]).toarray().sum(axis=0)
    total_words = len(re.findall(r'\w+', text))
    keyword_density = {word: (count / total_words) * 100 for word,
                       count in zip(keywords, word_count)}
    
    return keyword_density

# Example usage
# text = fetch_text('https://www.arthritis.org/health-wellness/healthy-living/managing-pain/pain-relief-solutions/cbd-for-arthritis-pain')
# keywords = ['cbd', 'cannabidiol']
# print(calc_keyword_density(text, keywords))

##### MVP #####

# Below here are future improvements and these will be integrated later.
# def get_synonyms(word):
#     """Gets synonyms for keyword to ensure coverage"""
#     synonyms = set()
#     for syn in wordnet.synsets(word):
#         for lemma in syn.lemmas():
#             synonyms.add(lemma.name())
#     return synonyms

# def get_filtered_synsets(word, pos=None, min_definition_length=1):
#     """Filters synonym sets to improve on accuracy of terminology"""
#     synsets = wordnet.synsets(word)
#     text = set()
#     if pos:
#         synsets = [synset for synset in synsets if synset.pos() == pos]
#     if min_definition_length:
#         synsets = [synset for synset in synsets if len(synset.definition()) >= min_definition_length]
    
#     synonyms = set()
#     for syn in synsets:
#         for lemma in syn.lemmas():
#             synonyms.add(lemma.name())
#     return synonyms

# def calc_keyword_density(text, keywords):
#     """Calculates keyword density including synonyms"""
#     # Get the synonyms for each keyword
#     expanded_keywords = set()
#     for keyword in keywords:
#         expanded_keywords.add(keyword)
#         expanded_keywords.update(get_filtered_synsets(keyword))
    
#     # Convert expanded keywords into a list for vectorization
#     expanded_keywords_list = list(expanded_keywords)
    
#     # Use CountVectorizer to count the words
#     vectorizer = CountVectorizer(vocabulary=expanded_keywords_list)
#     word_count = vectorizer.fit_transform([text]).toarray().sum(axis=0)
    
#     total_words = len(re.findall(r'\w+', text))
#     keyword_density = {word: (count / total_words) * 100 for word,
#                        count in zip(expanded_keywords_list, word_count)}
#     return keyword_density