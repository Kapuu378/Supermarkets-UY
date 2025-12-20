class NotARequestObjectError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

def handle_recursion(fn):
    """Handle recursion error so that in case it happends it will return an empty dict and
    not crash the whole execution. This event will be logged for future analysis.
    """
    #TODO: Add logging.
    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            return result
        
        except RecursionError:
            return {}
        
    return wrapper