import platform

from . import _version

DEFAULT_API_URI = 'https://nu.k.polyswarm.network/v1'
DEFAULT_HTTP_TIMEOUT = 30
DEFAULT_RETRIES = 0
DEFAULT_BACKOFF = 1
DEFAULT_RETRY_CODES = (502, 504)
DEFAULT_USER_AGENT = 'libpolyd/{} ({}-{}-{}-{})'.format(
    _version.__version__, platform.machine(), platform.system(),
    platform.python_implementation(), platform.python_version(),
)
