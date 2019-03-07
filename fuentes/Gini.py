'''
Created on 27 feb. 2019

@author: Sergio
'''
import numpy as np

def gini(list_of_values):
    
 
    list_of_values = [ elem for elem in list_of_values if elem > 774360 ]

   
    print(min(list_of_values))
    print(len(list_of_values))
    sorted_list = sorted(list_of_values)
    height, area = 0, 0
    for value in sorted_list:
        height += value
        area += height - value / 2.
    fair_area = height * len(list_of_values) / 2.
    return (fair_area - area) / fair_area

        
def gini2(array):
    """Calculate the Gini coefficient of a numpy array."""
    array = [elem for elem in array if elem > 0]
    # based on bottom eq: http://www.statsdirect.com/help/content/image/stat0206_wmf.gif
    # from: http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    array = np.array(array, dtype='float')
    array = array.flatten() #all values are treated equally, arrays must be 1d
    
    
    if np.amin(array) < 0:
        array -= np.amin(array) #values cannot be negative
    #array += 0.0000001 #values cannot be 0
    array = np.sort(array) #values must be sorted
    index = np.arange(1,array.shape[0]+1) #index per array element
    n = array.shape[0]#number of array elements
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array))) #Gini coefficient
