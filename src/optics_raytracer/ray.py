import numpy as np
from .primitives import vector_dtype

ray_dtype = np.dtype([
    ('origin', *vector_dtype),
    ('direction', *vector_dtype),
])
