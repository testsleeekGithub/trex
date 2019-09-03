# -*- coding: utf-8 -*-

# Author: Jan Hendrik Metzen <jhm@informatik.uni-bremen.de>
#         Vincent Dubourg <vincent.dubourg@gmail.com>
#         (mostly translation, see implementation details)
# License: BSD 3 clause

"""
The :mod:`mrex.gaussian_process` module implements Gaussian Process
based regression and classification.
"""

from .gpr import GaussianProcessRegressor
from .gpc import GaussianProcessClassifier
from . import kernels


__all__ = ['GaussianProcessRegressor', 'GaussianProcessClassifier',
           'kernels']
