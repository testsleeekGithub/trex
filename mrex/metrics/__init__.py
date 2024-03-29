"""
The :mod:`mrex.metrics` module includes score functions, performance metrics
and pairwise metrics and distance computations.
"""


from .ranking import auc
from .ranking import average_precision_score
from .ranking import coverage_error
from .ranking import dcg_score
from .ranking import label_ranking_average_precision_score
from .ranking import label_ranking_loss
from .ranking import ndcg_score
from .ranking import precision_recall_curve
from .ranking import roc_auc_score
from .ranking import roc_curve

from .classification import accuracy_score
from .classification import balanced_accuracy_score
from .classification import classification_report
from .classification import cohen_kappa_score
from .classification import confusion_matrix
from .classification import f1_score
from .classification import fbeta_score
from .classification import hamming_loss
from .classification import hinge_loss
from .classification import jaccard_similarity_score
from .classification import jaccard_score
from .classification import log_loss
from .classification import matthews_corrcoef
from .classification import precision_recall_fscore_support
from .classification import precision_score
from .classification import recall_score
from .classification import zero_one_loss
from .classification import brier_score_loss
from .classification import multilabel_confusion_matrix

from . import cluster
from .cluster import adjusted_mutual_info_score
from .cluster import adjusted_rand_score
from .cluster import completeness_score
from .cluster import consensus_score
from .cluster import homogeneity_completeness_v_measure
from .cluster import homogeneity_score
from .cluster import mutual_info_score
from .cluster import normalized_mutual_info_score
from .cluster import fowlkes_mallows_score
from .cluster import silhouette_samples
from .cluster import silhouette_score
from .cluster import calinski_harabasz_score
from .cluster import calinski_harabaz_score
from .cluster import v_measure_score
from .cluster import davies_bouldin_score

from .pairwise import euclidean_distances
from .pairwise import pairwise_distances
from .pairwise import pairwise_distances_argmin
from .pairwise import pairwise_distances_argmin_min
from .pairwise import pairwise_kernels
from .pairwise import pairwise_distances_chunked

from .regression import explained_variance_score
from .regression import max_error
from .regression import mean_absolute_error
from .regression import mean_squared_error
from .regression import mean_squared_log_error
from .regression import median_absolute_error
from .regression import r2_score
from .regression import mean_tweedie_deviance
from .regression import mean_poisson_deviance
from .regression import mean_gamma_deviance


from .scorer import check_scoring
from .scorer import make_scorer
from .scorer import SCORERS
from .scorer import get_scorer

from ._plot.roc_curve import plot_roc_curve
from ._plot.roc_curve import RocCurveDisplay


__all__ = [
    'accuracy_score',
    'adjusted_mutual_info_score',
    'adjusted_rand_score',
    'auc',
    'average_precision_score',
    'balanced_accuracy_score',
    'calinski_harabaz_score',
    'calinski_harabasz_score',
    'check_scoring',
    'classification_report',
    'cluster',
    'cohen_kappa_score',
    'completeness_score',
    'confusion_matrix',
    'consensus_score',
    'coverage_error',
    'dcg_score',
    'davies_bouldin_score',
    'euclidean_distances',
    'explained_variance_score',
    'f1_score',
    'fbeta_score',
    'fowlkes_mallows_score',
    'get_scorer',
    'hamming_loss',
    'hinge_loss',
    'homogeneity_completeness_v_measure',
    'homogeneity_score',
    'jaccard_score',
    'jaccard_similarity_score',
    'label_ranking_average_precision_score',
    'label_ranking_loss',
    'log_loss',
    'make_scorer',
    'matthews_corrcoef',
    'max_error',
    'mean_absolute_error',
    'mean_squared_error',
    'mean_squared_log_error',
    'mean_poisson_deviance',
    'mean_gamma_deviance',
    'mean_tweedie_deviance',
    'median_absolute_error',
    'multilabel_confusion_matrix',
    'mutual_info_score',
    'ndcg_score',
    'normalized_mutual_info_score',
    'pairwise_distances',
    'pairwise_distances_argmin',
    'pairwise_distances_argmin_min',
    'pairwise_distances_chunked',
    'pairwise_kernels',
    'plot_roc_curve',
    'precision_recall_curve',
    'precision_recall_fscore_support',
    'precision_score',
    'r2_score',
    'recall_score',
    'RocCurveDisplay',
    'roc_auc_score',
    'roc_curve',
    'SCORERS',
    'silhouette_samples',
    'silhouette_score',
    'v_measure_score',
    'zero_one_loss',
    'brier_score_loss',
]
