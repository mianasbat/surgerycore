#  -*- coding: utf-8 -*-

# import six
import numpy as np
import pytest
import sksurgerycore.algorithms.pivot as p
from glob import glob


def test_empty_matrices():

    with pytest.raises(TypeError):
        p.pivot_calibration(None)


def test_rank_lt_six():

    with pytest.raises(ValueError):
        file_names = glob('tests/data/PivotCalibration/1378476416922755200.txt')
        arrays = [np.loadtxt(f) for f in file_names]
        matrices = np.concatenate(arrays)
        number_of_matrices = int(matrices.size/16)
        matrices = matrices.reshape(number_of_matrices, 4, 4)
        p.pivot_calibration(matrices)


def test_four_columns_matrices4x4():

    with pytest.raises(ValueError):
        p.pivot_calibration(np.arange(2, 11, dtype=float).reshape(3, 3))


def test_four_rows_matrices4x4():

    with pytest.raises(ValueError):
        p.pivot_calibration(np.arange(2, 11, dtype=float).reshape(3, 3))


def test_return_value():

    file_names = glob('tests/data/PivotCalibration/*')
    arrays = [np.loadtxt(f) for f in file_names]
    matrices = np.concatenate(arrays)
    number_of_matrices = int(matrices.size/16)
    matrices = matrices.reshape(number_of_matrices, 4, 4)
    x_values, residual_error =p.pivot_calibration(matrices)
    assert 1.838 == round(residual_error, 3)
    assert -14.476 == round(x_values[0, 0], 3)
    assert 395.143 == round(x_values[1, 0], 3)
    assert -7.558 == round(x_values[2, 0], 3)
    assert -805.285 == round(x_values[3, 0], 3)
    assert -85.448 == round(x_values[4, 0], 3)
    assert -2112.066 == round(x_values[5, 0], 3)


def test_rank_if_condition():

    # This test will be checking a specific if condition.
    # But at the moment I dont know what data I need
    # To get proper s_values to cover that if condition.
    with pytest.raises(ValueError):
        file_names = glob('tests/data/test_case_data.txt')
        arrays = [np.loadtxt(f) for f in file_names]
        matrices = np.concatenate(arrays)
        number_of_matrices = int(matrices.size/16)
        matrices = matrices.reshape(number_of_matrices, 4, 4)
        p.pivot_calibration(matrices)


def test_pivot_with_ransac():

    file_names = glob('tests/data/PivotCalibration/*')
    arrays = [np.loadtxt(f) for f in file_names]
    matrices = np.concatenate(arrays)
    number_of_matrices = int(matrices.size/16)
    matrices = matrices.reshape(number_of_matrices, 4, 4)
    model_1, residual_1 = p.pivot_calibration(matrices)
    print("Without RANSAC:" + str(model_1) + ", RMS=" + str(residual_1))
    model_2, residual_2 = p.pivot_calibration_with_ransac(matrices, 10, 4, 0.25)
    print("With RANSAC:" + str(model_2) + ", RMS=" + str(residual_2))
    assert residual_2 < residual_1
    model_3, residual_3 = p.pivot_calibration_with_ransac(matrices, 10, 4, 0.25, early_exit=True)
    print("With Early Exit RANSAC:" + str(model_3) + ", RMS=" + str(residual_3))




