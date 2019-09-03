"""Enables histogram-based gradient boosting estimators.

The API and results of these estimators might change without any deprecation
cycle.

Importing this file dynamically sets the
:class:`mrex.ensemble.HistGradientBoostingClassifier` and
:class:`mrex.ensemble.HistGradientBoostingRegressor` as attributes of the
ensemble module::

    >>> # explicitly require this experimental feature
    >>> from mrex.experimental import enable_hist_gradient_boosting  # noqa
    >>> # now you can import normally from ensemble
    >>> from mrex.ensemble import HistGradientBoostingClassifier
    >>> from mrex.ensemble import HistGradientBoostingRegressor


The ``# noqa`` comment comment can be removed: it just tells linters like
flake8 to ignore the import, which appears as unused.
"""

from ..ensemble._hist_gradient_boosting.gradient_boosting import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor
)

from .. import ensemble

ensemble.HistGradientBoostingClassifier = HistGradientBoostingClassifier
ensemble.HistGradientBoostingRegressor = HistGradientBoostingRegressor
ensemble.__all__ += ['HistGradientBoostingClassifier',
                     'HistGradientBoostingRegressor']
