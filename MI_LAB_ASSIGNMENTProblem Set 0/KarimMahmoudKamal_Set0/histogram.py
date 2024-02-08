from typing import Any, Dict, List
import utils


def histogram(values: List[Any]) -> Dict[Any, int]:
    '''
    This function takes a list of values and returns a dictionary that contains the
    list elements alongside their frequency
    For example, if the values are [3,5,3] then the result should be {3:2, 5:1} 
    since 3 appears twice while 5 appears once 
    '''
    #TODO: ADD YOUR CODE HERE
    
    result = {}
    # iterate through the list and check if the item is present in the list
    for i in values:
        # if the item is present in the list then increment the count
        if i in result:
            result[i] += 1
        # if the item is not present in the list then add the item to the list
        else:
            result[i] = 1
    return result


    #utils.NotImplemented()
