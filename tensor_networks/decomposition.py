import math

import numpy as np

from tensor_networks.annotations import *
from tensor_networks.svd import truncated_svd
from tensor_networks.tensor_train import TensorTrain


def decompose(tensor: Array, d: int, svd: SVDCallable = truncated_svd,
              **svd_kwargs) -> TensorTrain:
    """
    Decompose a tensor into the tensor train format using SVD

    :param tensor: The tensor to decompose
    :param d: The dimension of the bond indices
    :param svd: The function used for singular value decomposition
    :param svd_kwargs:
        Any keyworded arguments are passed through to the svd function
        (for convenience)
    :return: The tensor in tensor train format
    """
    # Amount of elements in the tensor: $d^N$ (= tensor.size)
    # $\Leftrightarrow N = log_d(d^N)$
    n = int(math.log(tensor.size, d))
    # Add a mock index on the left for the first iteration
    t = tensor.reshape(1, tensor.size)
    cores = []
    for i in range(1, n):
        # Reshape the tensor into a matrix (to calculate the SVD)
        t.shape = (d * t.shape[0], d ** (n - i))
        # Split the tensor using Singular Value Decomposition (SVD)
        u, s, v = svd(t, **svd_kwargs)
        # Split the first index of the matrix u
        u.shape = (u.shape[0] // d, d, u.shape[1])
        # u is part of the tensor train
        cores.append(u)
        # Continue, using the contraction of s and v as the remaining tensor
        t = np.diag(s) @ v
    # The remaining matrix is the right-most tensor in the tensor train
    # and gets a mock index on the right for consistency
    t.shape = (*t.shape, 1)
    cores.append(t)
    return TensorTrain(cores)
