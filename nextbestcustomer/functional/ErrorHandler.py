import sys
import azure.functions as func



def own_except_hook(exc_type, exc_value, exc_traceback):
    
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    return func.HttpResponse(exc_value.args[0])

sys.excepthook = own_except_hook
