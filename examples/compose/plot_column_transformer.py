"""
==================================================
Column Transformer with Heterogeneous Data Sources
==================================================

Datasets can often contain components of that require different feature
extraction and processing pipelines.  This scenario might occur when:

1. Your dataset consists of heterogeneous data types (e.g. raster images and
   text captions)
2. Your dataset is stored in a Pandas DataFrame and different columns
   require different processing pipelines.

This example demonstrates how to use
:class:`mrex.compose.ColumnTransformer` on a dataset containing
different types of features.  We use the 20-newsgroups dataset and compute
standard bag-of-words features for the subject line and body in separate
pipelines as well as ad hoc features on the body. We combine them (with
weights) using a ColumnTransformer and finally train a classifier on the
combined set of features.

The choice of features is not particularly helpful, but serves to illustrate
the technique.
"""

# Author: Matt Terry <matt.terry@gmail.com>
#
# License: BSD 3 clause

import numpy as np

from mrex.base import BaseEstimator, TransformerMixin
from mrex.datasets import fetch_20newsgroups
from mrex.datasets.twenty_newsgroups import strip_newsgroup_footer
from mrex.datasets.twenty_newsgroups import strip_newsgroup_quoting
from mrex.decomposition import TruncatedSVD
from mrex.feature_extraction import DictVectorizer
from mrex.feature_extraction.text import TfidfVectorizer
from mrex.metrics import classification_report
from mrex.pipeline import Pipeline
from mrex.compose import ColumnTransformer
from mrex.svm import LinearSVC


class TextStats(BaseEstimator, TransformerMixin):
    """Extract features from each document for DictVectorizer"""

    def fit(self, x, y=None):
        return self

    def transform(self, posts):
        return [{'length': len(text),
                 'num_sentences': text.count('.')}
                for text in posts]


class SubjectBodyExtractor(BaseEstimator, TransformerMixin):
    """Extract the subject & body from a usenet post in a single pass.

    Takes a sequence of strings and produces a dict of sequences.  Keys are
    `subject` and `body`.
    """
    def fit(self, x, y=None):
        return self

    def transform(self, posts):
        # construct object dtype array with two columns
        # first column = 'subject' and second column = 'body'
        features = np.empty(shape=(len(posts), 2), dtype=object)
        for i, text in enumerate(posts):
            headers, _, bod = text.partition('\n\n')
            bod = strip_newsgroup_footer(bod)
            bod = strip_newsgroup_quoting(bod)
            features[i, 1] = bod

            prefix = 'Subject:'
            sub = ''
            for line in headers.split('\n'):
                if line.startswith(prefix):
                    sub = line[len(prefix):]
                    break
            features[i, 0] = sub

        return features


pipeline = Pipeline([
    # Extract the subject & body
    ('subjectbody', SubjectBodyExtractor()),

    # Use ColumnTransformer to combine the features from subject and body
    ('union', ColumnTransformer(
        [
            # Pulling features from the post's subject line (first column)
            ('subject', TfidfVectorizer(min_df=50), 0),

            # Pipeline for standard bag-of-words model for body (second column)
            ('body_bow', Pipeline([
                ('tfidf', TfidfVectorizer()),
                ('best', TruncatedSVD(n_components=50)),
            ]), 1),

            # Pipeline for pulling ad hoc features from post's body
            ('body_stats', Pipeline([
                ('stats', TextStats()),  # returns a list of dicts
                ('vect', DictVectorizer()),  # list of dicts -> feature matrix
            ]), 1),
        ],

        # weight components in ColumnTransformer
        transformer_weights={
            'subject': 0.8,
            'body_bow': 0.5,
            'body_stats': 1.0,
        }
    )),

    # Use a SVC classifier on the combined features
    ('svc', LinearSVC(dual=False)),
], verbose=True)

# limit the list of categories to make running this example faster.
categories = ['alt.atheism', 'talk.religion.misc']
X_train, y_train = fetch_20newsgroups(random_state=1,
                                      subset='train',
                                      categories=categories,
                                      return_X_y=True)
X_test, y_test = fetch_20newsgroups(random_state=1,
                                    subset='test',
                                    categories=categories,
                                    return_X_y=True)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
print(classification_report(y_pred, y_test))
