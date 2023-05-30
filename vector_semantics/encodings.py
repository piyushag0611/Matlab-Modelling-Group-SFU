"""
Contains various word encoders built using standard libraries (Sklearn, Tensorflow)
"""

def tf_idf(documents, choice=0):
    """
    Returns a term frequency-inverse document frequency matrix of a given collection of sentences/documents.
    Parameters:
    documents : List 
                List of strings as input. Each string is a collection of words.
    
    choice : {0, 1} default : 0
                If 0 then returns a dataframe with words as columns and documents as rows
                If 1 then returns the original sparse matrix and vocabulary from sklearn TfidfVectorizer

    ----------
    Returns a dataframe with columns being words in the vocabulary, rows as documents and values as the tf-idf representation for the word.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
    import pandas as pd
    from scipy.sparse import csr_matrix

    vectorizer = TfidfVectorizer()
    encoding = vectorizer.fit_transform(documents)
    vocab = vectorizer.get_feature_names_out()
    
    if(choice==0):
        norm_matrix = encoding.toarray()
        frame_ = pd.DataFrame(norm_matrix, columns=vocab)
        return frame_
    else:
        return encoding, vocab


