import traceback


def func_name():
    """
    Method that gives the name of the current function
    Returns:
        str: current function name
    """
    return traceback.extract_stack(None, 2)[0][2]
