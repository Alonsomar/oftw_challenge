from flask_caching import Cache

from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-dir',
    "CACHE_DEFAULT_TIMEOUT": 300
})
