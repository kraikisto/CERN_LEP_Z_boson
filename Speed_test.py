import perfplot  
import pandas as pd
import numpy as np
from itertools import chain
abc = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
numbers = [0.1,0.22,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
abc_numbers  = abc + numbers

def normal_loop(df):
    list1 = list(df.A)
    list2 = list(df.B)
    for i in range(0,len(list1)):
        if list1[i] == list2[i]:
            df = df.drop(index = i)
    return df

    
"""
# Boolean indexing with float value comparison.
perfplot.show(
    setup=lambda n: pd.DataFrame(np.random.choice(1000, (n, 2)), columns=['A','B']),
    kernels=[
        lambda df: df[df.A != df.B],
        lambda df: df[[x != y for x, y in zip(df.A, df.B)]],
        lambda df: normal_loop(df),
    ],
    labels=['vectorised', 'list comp', "normal loop"],
    n_range=[2**k for k in range(5, 22)],
    xlabel='N', 
    logy=False, 
    logx=False
)
"""
"""
# Boolean indexing with string/int value comparison.
perfplot.show(
    setup=lambda n: pd.DataFrame({'A': random.choices(abc_numbers, k=n), 'B': random.choices(abc_numbers, k=n)}),
    kernels=[
        lambda df: df[df.A != df.B],
        lambda df: df[[x != y for x, y in zip(df.A, df.B)]],
    ],
    labels=['vectorised', 'list comp'],
    n_range=[2**k for k in range(0, 20)],
    xlabel='N',
    logx=False,
    logy=False,
    equality_check=None
)
"""

"""
#pandas vs numpy
perfplot.show(
    setup=lambda n: pd.DataFrame(np.random.choice(1000, (n, 2)), columns=['A','B']),
    kernels=[
        lambda df: df[df.A != df.B],
        lambda df: df[df.A.values != df.B.values],

    ],
    labels=['pandas', 'numpy'],
    n_range=[2**k for k in range(0, 15)],
    xlabel='N', 
    logy=False, 
    logx=False
)

"""

"""
ser2 = pd.Series([['a', 'b', 'c'], [1, 2], []])        
perfplot.show(
    setup=lambda n: pd.concat([ser2] * n, ignore_index=True),
    kernels=[
        lambda ser: ser.map(get_0th),
        lambda ser: pd.Series([x[0] if len(x) > 0 else np.nan for x in ser]),

    ],
    labels=['map', 'list comprehension'],
    n_range=[2**k for k in range(5, 22)],
    xlabel='N',
    equality_check=None,
    logy=False,
    logx=False
)
"""

# Nested list flattening.
perfplot.show(
    setup=lambda n: pd.concat([pd.Series([['a', 'b', 'c'], [1, 2], []])] * n, ignore_index=True),
    kernels=[
        lambda ser: pd.DataFrame(ser.tolist()).stack().reset_index(drop=True),
        lambda ser: pd.Series(list(chain.from_iterable(ser.tolist()))),
        lambda ser: pd.Series([y for x in ser for y in x]),
    ],
    labels=['pandas.stack', 'itertools.chain', 'nested list comp'],
    n_range=[2**k for k in range(0, 15)],
    xlabel='N',    
    equality_check=None,
    logy=False,
    logx=False    
)