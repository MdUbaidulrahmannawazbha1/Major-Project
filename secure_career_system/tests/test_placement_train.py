"""Tests for the placement training module."""
from secure_career_system import placement_train
import numpy as np


def test_generate_placement_data_shape():
    X, y = placement_train.generate_placement_data(n=100)
    assert X.shape == (100, 5)
    assert y.shape == (100,)


def test_placement_labels_binary():
    X, y = placement_train.generate_placement_data(n=200)
    assert set(np.unique(y)).issubset({0, 1})
