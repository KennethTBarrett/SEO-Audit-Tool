import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import re

# Ensure NLTK data has been downloaded
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('average_perceptron_tagger')

def get_wordnet_pos(word):
    '''Convert NTLK POS tags to WordNet Compatible'''
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def get_synonyms(word):
    '''Gets synonyms for keyword to ensure coverage'''
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

def expand_and_lemmatize(keywords):
    lemmatizer = WordNetLemmatizer()
    expanded_keywords = set()
    for keyword in keywords:
        # Add original word
        expanded_keywords.add(keyword)
        # Add synonyms
        expanded_keywords.update(get_synonyms(keyword))
    # New set for storage of both original and lemmatized keywords
    lemmatized_keywords = set()

    for keyword in expanded_keywords:
        lemmatized_keywords.add(keyword)
        lemmatized_keywords.add(lemmatizer.lemmatize(keyword, get_wordnet_pos(keyword)))

    return lemmatized_keywords

# Currently being improved; will remove once expand_and_lemmatize() has been finished
# def lemmatize_text(text):
#     '''Lemmatizes text before sending for keyword density calculation'''
#     lemmatizer = WordNetLemmatizer()
#     words = nltk.word_tokenize(text)
#     lemmatized = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in words]
#     return ' '.join(lemmatized)

def calc_keyword_density(text, keywords):
    '''Calculates keyword density using lemmatized text'''
    lemmatized_text = lemmatize_text(text)
    vectorizer = CountVectorizer(vocabulary=keywords)
    word_count = vectorizer.fit_transform([lemmatized_text]).toarray().sum(axis=0)
    total_words = len(re.findall(r'\w+', lemmatized_text))
    keyword_density = {word: (count / total_words) * 100 for word, count in zip(keywords, word_count)}
    return keyword_density
