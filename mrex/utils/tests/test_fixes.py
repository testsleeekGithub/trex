# Authors: Gael Varoquaux <gael.varoquaux@normalesup.org>
#          Justin Vincent
#          Lars Buitinck
# License: BSD 3 clause

import pickle

import numpy as np
import pytest

from mrex.utils.testing import assert_array_equal

from mrex.utils.fixes import MaskedArray
from mrex.utils.fixes import _joblib_parallel_args
from mrex.utils.fixes import _object_dtype_isnan


def test_masked_array_obj_dtype_pickleable():
    marr = MaskedArray([1, None, 'a'], dtype=object)

    for mask in (True, False, [0, 1, 0]):
        marr.mask = mask
        marr_pickled = pickle.loads(pickle.dumps(marr))
        assert_array_equal(marr.data, marr_pickled.data)
        assert_array_equal(marr.mask, marr_pickled.mask)


@pytest.mark.parametrize('joblib_version', ('0.11', '0.12.0'))
def test_joblib_parallel_args(monkeypatch, joblib_version):
    import joblib
    monkeypatch.setattr(joblib, '__version__', joblib_version)

    if joblib_version == '0.12.0':
        # arguments are simply passed through
        assert _joblib_parallel_args(prefer='threads') == {'prefer': 'threads'}
        assert _joblib_parallel_args(prefer='processes', require=None) == {
                    'prefer': 'processes', 'require': None}
        assert _joblib_parallel_args(non_existing=1) == {'non_existing': 1}
    elif joblib_version == '0.11':
        # arguments are mapped to the corresponding backend
        assert _joblib_parallel_args(prefer='threads') == {
                    'backend': 'threading'}
        assert _joblib_parallel_args(prefer='processes') == {
                    'backend': 'multiprocessing'}
        with pytest.raises(ValueError):
            _joblib_parallel_args(prefer='invalid')
        assert _joblib_parallel_args(
                prefer='processes', require='sharedmem') == {
                    'backend': 'threading'}
        with pytest.raises(ValueError):
            _joblib_parallel_args(require='invalid')
        with pytest.raises(NotImplementedError):
            _joblib_parallel_args(verbose=True)
    else:
        raise ValueError


@pytest.mark.parametrize("dtype, val", ([object, 1],
                                        [object, "a"],
                                        [float, 1]))
def test_object_dtype_isnan(dtype, val):
    X = np.array([[val, np.nan],
                  [np.nan, val]], dtype=dtype)

    expected_mask = np.array([[False, True],
                              [True, False]])

    mask = _object_dtype_isnan(X)

    assert_array_equal(mask, expected_mask)
