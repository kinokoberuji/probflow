"""
The core.utils.casting module contains functions for casting back and forth
betweeen Tensors and numpy arrays.

* :func:`.to_numpy`
* :func:`.to_tensor`
* :func:`.make_input_tensor`

----------

"""



__all__ = [
    'to_numpy',
    'to_tensor',
    'make_input_tensor',
]



import numpy as np
import pandas as pd

from probflow.core.settings import get_backend



def to_numpy(x):
    """Convert tensor to numpy array"""
    if isinstance(x, list):
        return [to_numpy(e) for e in x]
    elif isinstance(x, np.ndarray):
        return x
    elif isinstance(x, (pd.DataFrame, pd.Series)):
        return x.values
    elif get_backend() == 'pytorch':
        return x.detach().numpy()
    else:
        return x.numpy()



def to_tensor(x):
    """Make x a tensor if not already"""
    if get_backend() == 'pytorch':
        import torch
        if not isinstance(x, torch.Tensor):
            return torch.tensor(x)
    return x



def make_input_tensor(fn):

    def tensor_fn(*args, **kwargs):
        return fn(to_tensor(args[0]), *args[1:], **kwargs)

    return tensor_fn