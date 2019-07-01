import numpy as np

def gini(list_of_values):
    """
    Versión 1: Curva de Lorenz para calcular el índice Gini
    """
 
    list_of_values = [ elem for elem in list_of_values if elem > 0 ]

    sol = 0
    if(len(list_of_values)>0):
        sorted_list = sorted(list_of_values)
        height, area = 0, 0
        for value in sorted_list:
            height += value
            area += height - value / 2.
        fair_area = height * len(list_of_values) / 2.
        sol = (fair_area - area) / fair_area
    return sol

        
def gini2(array):
    """
    Versión 2: Fórmula de Brown:
    """
    
    array = [elem for elem in array if elem > 0]
    
    # de: http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    array = np.array(array, dtype='float')
    array = array.flatten() 
    
    if np.amin(array) < 0:
        array -= np.amin(array) 
    array = np.sort(array) 
    index = np.arange(1,array.shape[0]+1) 
    n = array.shape[0]
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array))) 
