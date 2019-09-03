from time import time
import argparse

import matplotlib.pyplot as plt
import numpy as np
from mrex.model_selection import train_test_split
# To use this experimental feature, we need to explicitly ask for it:
from mrex.experimental import enable_hist_gradient_boosting  # noqa
from mrex.ensemble import HistGradientBoostingRegressor
from mrex.ensemble import HistGradientBoostingClassifier
from mrex.datasets import make_classification
from mrex.datasets import make_regression
from mrex.ensemble._hist_gradient_boosting.utils import (
    get_equivalent_estimator)


parser = argparse.ArgumentParser()
parser.add_argument('--n-leaf-nodes', type=int, default=31)
parser.add_argument('--n-trees', type=int, default=10)
parser.add_argument('--lightgbm', action="store_true", default=False,
                    help='also plot lightgbm')
parser.add_argument('--xgboost', action="store_true", default=False,
                    help='also plot xgboost')
parser.add_argument('--catboost', action="store_true", default=False,
                    help='also plot catboost')
parser.add_argument('--learning-rate', type=float, default=.1)
parser.add_argument('--problem', type=str, default='classification',
                    choices=['classification', 'regression'])
parser.add_argument('--missing-fraction', type=float, default=0)
parser.add_argument('--n-classes', type=int, default=2)
parser.add_argument('--n-samples-max', type=int, default=int(1e6))
parser.add_argument('--n-features', type=int, default=20)
parser.add_argument('--max-bins', type=int, default=255)
args = parser.parse_args()

n_leaf_nodes = args.n_leaf_nodes
n_trees = args.n_trees
lr = args.learning_rate
max_bins = args.max_bins


def get_estimator_and_data():
    if args.problem == 'classification':
        X, y = make_classification(args.n_samples_max * 2,
                                   n_features=args.n_features,
                                   n_classes=args.n_classes,
                                   n_clusters_per_class=1,
                                   random_state=0)
        return X, y, HistGradientBoostingClassifier
    elif args.problem == 'regression':
        X, y = make_regression(args.n_samples_max * 2,
                               n_features=args.n_features, random_state=0)
        return X, y, HistGradientBoostingRegressor


X, y, Estimator = get_estimator_and_data()
if args.missing_fraction:
    mask = np.random.binomial(1, args.missing_fraction, size=X.shape).astype(
        np.bool)
    X[mask] = np.nan

X_train_, X_test_, y_train_, y_test_ = train_test_split(
    X, y, test_size=0.5, random_state=0)


def one_run(n_samples):
    X_train = X_train_[:n_samples]
    X_test = X_test_[:n_samples]
    y_train = y_train_[:n_samples]
    y_test = y_test_[:n_samples]
    assert X_train.shape[0] == n_samples
    assert X_test.shape[0] == n_samples
    print("Data size: %d samples train, %d samples test."
          % (n_samples, n_samples))
    print("Fitting a mrex model...")
    tic = time()
    est = Estimator(learning_rate=lr,
                    max_iter=n_trees,
                    max_bins=max_bins,
                    max_leaf_nodes=n_leaf_nodes,
                    n_iter_no_change=None,
                    random_state=0,
                    verbose=0)
    est.fit(X_train, y_train)
    mrex_fit_duration = time() - tic
    tic = time()
    mrex_score = est.score(X_test, y_test)
    mrex_score_duration = time() - tic
    print("score: {:.4f}".format(mrex_score))
    print("fit duration: {:.3f}s,".format(mrex_fit_duration))
    print("score duration: {:.3f}s,".format(mrex_score_duration))

    lightgbm_score = None
    lightgbm_fit_duration = None
    lightgbm_score_duration = None
    if args.lightgbm:
        print("Fitting a LightGBM model...")
        # get_lightgbm does not accept loss='auto'
        if args.problem == 'classification':
            loss = 'binary_crossentropy' if args.n_classes == 2 else \
                'categorical_crossentropy'
            est.set_params(loss=loss)
        lightgbm_est = get_equivalent_estimator(est, lib='lightgbm')

        tic = time()
        lightgbm_est.fit(X_train, y_train)
        lightgbm_fit_duration = time() - tic
        tic = time()
        lightgbm_score = lightgbm_est.score(X_test, y_test)
        lightgbm_score_duration = time() - tic
        print("score: {:.4f}".format(lightgbm_score))
        print("fit duration: {:.3f}s,".format(lightgbm_fit_duration))
        print("score duration: {:.3f}s,".format(lightgbm_score_duration))

    xgb_score = None
    xgb_fit_duration = None
    xgb_score_duration = None
    if args.xgboost:
        print("Fitting an XGBoost model...")
        # get_xgb does not accept loss='auto'
        if args.problem == 'classification':
            loss = 'binary_crossentropy' if args.n_classes == 2 else \
                'categorical_crossentropy'
            est.set_params(loss=loss)
        xgb_est = get_equivalent_estimator(est, lib='xgboost')

        tic = time()
        xgb_est.fit(X_train, y_train)
        xgb_fit_duration = time() - tic
        tic = time()
        xgb_score = xgb_est.score(X_test, y_test)
        xgb_score_duration = time() - tic
        print("score: {:.4f}".format(xgb_score))
        print("fit duration: {:.3f}s,".format(xgb_fit_duration))
        print("score duration: {:.3f}s,".format(xgb_score_duration))

    cat_score = None
    cat_fit_duration = None
    cat_score_duration = None
    if args.catboost:
        print("Fitting a CatBoost model...")
        # get_cat does not accept loss='auto'
        if args.problem == 'classification':
            loss = 'binary_crossentropy' if args.n_classes == 2 else \
                'categorical_crossentropy'
            est.set_params(loss=loss)
        cat_est = get_equivalent_estimator(est, lib='catboost')

        tic = time()
        cat_est.fit(X_train, y_train)
        cat_fit_duration = time() - tic
        tic = time()
        cat_score = cat_est.score(X_test, y_test)
        cat_score_duration = time() - tic
        print("score: {:.4f}".format(cat_score))
        print("fit duration: {:.3f}s,".format(cat_fit_duration))
        print("score duration: {:.3f}s,".format(cat_score_duration))

    return (mrex_score, mrex_fit_duration, mrex_score_duration,
            lightgbm_score, lightgbm_fit_duration, lightgbm_score_duration,
            xgb_score, xgb_fit_duration, xgb_score_duration,
            cat_score, cat_fit_duration, cat_score_duration)


n_samples_list = [1000, 10000, 100000, 500000, 1000000, 5000000, 10000000]
n_samples_list = [n_samples for n_samples in n_samples_list
                  if n_samples <= args.n_samples_max]

mrex_scores = []
mrex_fit_durations = []
mrex_score_durations = []
lightgbm_scores = []
lightgbm_fit_durations = []
lightgbm_score_durations = []
xgb_scores = []
xgb_fit_durations = []
xgb_score_durations = []
cat_scores = []
cat_fit_durations = []
cat_score_durations = []

for n_samples in n_samples_list:
    (mrex_score,
     mrex_fit_duration,
     mrex_score_duration,
     lightgbm_score,
     lightgbm_fit_duration,
     lightgbm_score_duration,
     xgb_score,
     xgb_fit_duration,
     xgb_score_duration,
     cat_score,
     cat_fit_duration,
     cat_score_duration) = one_run(n_samples)

    for scores, score in (
            (mrex_scores, mrex_score),
            (mrex_fit_durations, mrex_fit_duration),
            (mrex_score_durations, mrex_score_duration),
            (lightgbm_scores, lightgbm_score),
            (lightgbm_fit_durations, lightgbm_fit_duration),
            (lightgbm_score_durations, lightgbm_score_duration),
            (xgb_scores, xgb_score),
            (xgb_fit_durations, xgb_fit_duration),
            (xgb_score_durations, xgb_score_duration),
            (cat_scores, cat_score),
            (cat_fit_durations, cat_fit_duration),
            (cat_score_durations, cat_score_duration)):
        scores.append(score)

fig, axs = plt.subplots(3, sharex=True)

axs[0].plot(n_samples_list, mrex_scores, label='mrex')
axs[1].plot(n_samples_list, mrex_fit_durations, label='mrex')
axs[2].plot(n_samples_list, mrex_score_durations, label='mrex')

if args.lightgbm:
    axs[0].plot(n_samples_list, lightgbm_scores, label='lightgbm')
    axs[1].plot(n_samples_list, lightgbm_fit_durations, label='lightgbm')
    axs[2].plot(n_samples_list, lightgbm_score_durations, label='lightgbm')

if args.xgboost:
    axs[0].plot(n_samples_list, xgb_scores, label='XGBoost')
    axs[1].plot(n_samples_list, xgb_fit_durations, label='XGBoost')
    axs[2].plot(n_samples_list, xgb_score_durations, label='XGBoost')

if args.catboost:
    axs[0].plot(n_samples_list, cat_scores, label='CatBoost')
    axs[1].plot(n_samples_list, cat_fit_durations, label='CatBoost')
    axs[2].plot(n_samples_list, cat_score_durations, label='CatBoost')

for ax in axs:
    ax.set_xscale('log')
    ax.legend(loc='best')
    ax.set_xlabel('n_samples')

axs[0].set_title('scores')
axs[1].set_title('fit duration (s)')
axs[2].set_title('score duration (s)')

title = args.problem
if args.problem == 'classification':
    title += ' n_classes = {}'.format(args.n_classes)
fig.suptitle(title)


plt.tight_layout()
plt.show()
