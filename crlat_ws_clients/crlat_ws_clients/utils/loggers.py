import logging
from functools import wraps

root_logger = None
loggers = {}


def get_root_logger():
    global root_logger
    if root_logger is None:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)-15s %(levelname)-8s %(name)s: %(message)s'
        )
        root_logger = logging.getLogger('[WSCLI]')
    return root_logger


def get_logger(lgr_name) -> logging.Logger:
    global loggers
    lgr = loggers.get(lgr_name, None)
    if lgr is None:
        root = get_root_logger()
        lgr = root.getChild(lgr_name)
        loggers[lgr_name] = lgr
    return lgr

def log_decorated(f):
    ml = get_logger('ML')
    @wraps(f)
    def decorated(*args, **kwargs):
        res = f(*args, **kwargs)
        ml.debug(
            'Method call: \n%s.%s(\n\t%s,\n\t%s\n)\nReturned: %s' % (
                args[0].__class__.__name__,
                f.__name__,
                ',\n\t'.join([repr(arg) for arg in args]),
                ',\n\t'.join(['%s=%s' % (k, repr(v)) for k,v in kwargs]),
                repr(res)
            )
        )
        return res
    return decorated

conn_logger = get_logger('[CONN]')
domain_logger = get_logger('[DOMAIN]')
app_logger = get_logger('[APP]')
test_logger = get_logger('[TST]')
lt_logger = get_logger('[LT]')