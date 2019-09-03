from mrex.model_selection import train_test_split
from mrex.metrics import accuracy_score
from mrex.datasets import make_classification, make_regression
import numpy as np
import pytest

# To use this experimental feature, we need to explicitly ask for it:
from mrex.experimental import enable_hist_gradient_boosting  # noqa
from mrex.ensemble import HistGradientBoostingRegressor
from mrex.ensemble import HistGradientBoostingClassifier
from mrex.ensemble._hist_gradient_boosting.binning import _BinMapper
from mrex.ensemble._hist_gradient_boosting.utils import (
    get_equivalent_estimator)


pytest.importorskip("lightgbm")


@pytest.mark.parametrize('seed', range(5))
@pytest.mark.parametrize('min_samples_leaf', (1, 20))
@pytest.mark.parametrize('n_samples, max_leaf_nodes', [
    (255, 4096),
    (1000, 8),
])
def test_same_predictions_regression(seed, min_samples_leaf, n_samples,
                                     max_leaf_nodes):
    # Make sure mrex has the same predictions as lightgbm for easy targets.
    #
    # In particular when the size of the trees are bound and the number of
    # samples is large enough, the structure of the prediction trees found by
    # LightGBM and mrex should be exactly identical.
    #
    # Notes:
    # - Several candidate splits may have equal gains when the number of
    #   samples in a node is low (and because of float errors). Therefore the
    #   predictions on the test set might differ if the structure of the tree
    #   is not exactly the same. To avoid this issue we only compare the
    #   predictions on the test set when the number of samples is large enough
    #   and max_leaf_nodes is low enough.
    # - To ignore  discrepancies caused by small differences the binning
    #   strategy, data is pre-binned if n_samples > 255.

    rng = np.random.RandomState(seed=seed)
    n_samples = n_samples
    max_iter = 1
    max_bins = 255

    X, y = make_regression(n_samples=n_samples, n_features=5,
                           n_informative=5, random_state=0)

    if n_samples > 255:
        # bin data and convert it to float32 so that the estimator doesn't
        # treat it as pre-binned
        X = _BinMapper(n_bins=max_bins + 1).fit_transform(X).astype(np.float32)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=rng)

    est_mrex = HistGradientBoostingRegressor(
        max_iter=max_iter,
        max_bins=max_bins,
        learning_rate=1,
        n_iter_no_change=None,
        min_samples_leaf=min_samples_leaf,
        max_leaf_nodes=max_leaf_nodes)
    est_lightgbm = get_equivalent_estimator(est_mrex, lib='lightgbm')

    est_lightgbm.fit(X_train, y_train)
    est_mrex.fit(X_train, y_train)

    # We need X to be treated an numerical data, not pre-binned data.
    X_train, X_test = X_train.astype(np.float32), X_test.astype(np.float32)

    pred_lightgbm = est_lightgbm.predict(X_train)
    pred_mrex = est_mrex.predict(X_train)
    # less than 1% of the predictions are different up to the 3rd decimal
    assert np.mean(abs(pred_lightgbm - pred_mrex) > 1e-3) < .011

    if max_leaf_nodes < 10 and n_samples >= 1000:
        pred_lightgbm = est_lightgbm.predict(X_test)
        pred_mrex = est_mrex.predict(X_test)
        # less than 1% of the predictions are different up to the 4th decimal
        assert np.mean(abs(pred_lightgbm - pred_mrex) > 1e-4) < .01


@pytest.mark.parametrize('seed', range(5))
@pytest.mark.parametrize('min_samples_leaf', (1, 20))
@pytest.mark.parametrize('n_samples, max_leaf_nodes', [
    (255, 4096),
    (1000, 8),
])
def test_same_predictions_classification(seed, min_samples_leaf, n_samples,
                                         max_leaf_nodes):
    # Same as test_same_predictions_regression but for classification

    rng = np.random.RandomState(seed=seed)
    n_samples = n_samples
    max_iter = 1
    max_bins = 255

    X, y = make_classification(n_samples=n_samples, n_classes=2, n_features=5,
                               n_informative=5, n_redundant=0, random_state=0)

    if n_samples > 255:
        # bin data and convert it to float32 so that the estimator doesn't
        # treat it as pre-binned
        X = _BinMapper(n_bins=max_bins + 1).fit_transform(X).astype(np.float32)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=rng)

    est_mrex = HistGradientBoostingClassifier(
        loss='binary_crossentropy',
        max_iter=max_iter,
        max_bins=max_bins,
        learning_rate=1,
        n_iter_no_change=None,
        min_samples_leaf=min_samples_leaf,
        max_leaf_nodes=max_leaf_nodes)
    est_lightgbm = get_equivalent_estimator(est_mrex, lib='lightgbm')

    est_lightgbm.fit(X_train, y_train)
    est_mrex.fit(X_train, y_train)

    # We need X to be treated an numerical data, not pre-binned data.
    X_train, X_test = X_train.astype(np.float32), X_test.astype(np.float32)

    pred_lightgbm = est_lightgbm.predict(X_train)
    pred_mrex = est_mrex.predict(X_train)
    assert np.mean(pred_mrex == pred_lightgbm) > .89

    acc_lightgbm = accuracy_score(y_train, pred_lightgbm)
    acc_mrex = accuracy_score(y_train, pred_mrex)
    np.testing.assert_almost_equal(acc_lightgbm, acc_mrex)

    if max_leaf_nodes < 10 and n_samples >= 1000:

        pred_lightgbm = est_lightgbm.predict(X_test)
        pred_mrex = est_mrex.predict(X_test)
        assert np.mean(pred_mrex == pred_lightgbm) > .89

        acc_lightgbm = accuracy_score(y_test, pred_lightgbm)
        acc_mrex = accuracy_score(y_test, pred_mrex)
        np.testing.assert_almost_equal(acc_lightgbm, acc_mrex, decimal=2)


@pytest.mark.parametrize('seed', range(5))
@pytest.mark.parametrize('min_samples_leaf', (1, 20))
@pytest.mark.parametrize('n_samples, max_leaf_nodes', [
    (255, 4096),
    (10000, 8),
])
def test_same_predictions_multiclass_classification(
        seed, min_samples_leaf, n_samples, max_leaf_nodes):
    # Same as test_same_predictions_regression but for classification

    rng = np.random.RandomState(seed=seed)
    n_samples = n_samples
    max_iter = 1
    max_bins = 255
    lr = 1

    X, y = make_classification(n_samples=n_samples, n_classes=3, n_features=5,
                               n_informative=5, n_redundant=0,
                               n_clusters_per_class=1, random_state=0)

    if n_samples > 255:
        # bin data and convert it to float32 so that the estimator doesn't
        # treat it as pre-binned
        X = _BinMapper(n_bins=max_bins + 1).fit_transform(X).astype(np.float32)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=rng)

    est_mrex = HistGradientBoostingClassifier(
        loss='categorical_crossentropy',
        max_iter=max_iter,
        max_bins=max_bins,
        learning_rate=lr,
        n_iter_no_change=None,
        min_samples_leaf=min_samples_leaf,
        max_leaf_nodes=max_leaf_nodes)
    est_lightgbm = get_equivalent_estimator(est_mrex, lib='lightgbm')

    est_lightgbm.fit(X_train, y_train)
    est_mrex.fit(X_train, y_train)

    # We need X to be treated an numerical data, not pre-binned data.
    X_train, X_test = X_train.astype(np.float32), X_test.astype(np.float32)

    pred_lightgbm = est_lightgbm.predict(X_train)
    pred_mrex = est_mrex.predict(X_train)
    assert np.mean(pred_mrex == pred_lightgbm) > .89

    proba_lightgbm = est_lightgbm.predict_proba(X_train)
    proba_mrex = est_mrex.predict_proba(X_train)
    # assert more than 75% of the predicted probabilities are the same up to
    # the second decimal
    assert np.mean(np.abs(proba_lightgbm - proba_mrex) < 1e-2) > .75

    acc_lightgbm = accuracy_score(y_train, pred_lightgbm)
    acc_mrex = accuracy_score(y_train, pred_mrex)
    np.testing.assert_almost_equal(acc_lightgbm, acc_mrex, decimal=2)

    if max_leaf_nodes < 10 and n_samples >= 1000:

        pred_lightgbm = est_lightgbm.predict(X_test)
        pred_mrex = est_mrex.predict(X_test)
        assert np.mean(pred_mrex == pred_lightgbm) > .89

        proba_lightgbm = est_lightgbm.predict_proba(X_train)
        proba_mrex = est_mrex.predict_proba(X_train)
        # assert more than 75% of the predicted probabilities are the same up
        # to the second decimal
        assert np.mean(np.abs(proba_lightgbm - proba_mrex) < 1e-2) > .75

        acc_lightgbm = accuracy_score(y_test, pred_lightgbm)
        acc_mrex = accuracy_score(y_test, pred_mrex)
        np.testing.assert_almost_equal(acc_lightgbm, acc_mrex, decimal=2)
