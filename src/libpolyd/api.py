import logging
import time
import os

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from . import exceptions
from . import const
from . import http
from . import resources
from . import request

logger = logging.getLogger(__name__)


class PolydAPI(object):
    def __init__(self, key, uri=None, timeout=None, wallet=None):
        logger.info('Creating PolydAPI instance: api_key: %s, api_uri: %s', key, uri)
        self.uri = uri or const.DEFAULT_API_URI
        self.timeout = timeout or const.DEFAULT_HTTP_TIMEOUT
        self.session = http.PolyswarmHTTP(key, retries=const.DEFAULT_RETRIES)
        self.generator = request.PolydRequestGenerator(self, self.uri)

    def get_bounty(self, bounty_guid):
        logger.info('Looking up bounty %s', bounty_guid)
        return self.generator.get_bounty_results(bounty_guid).execute().result

    def get_assertion(self, bounty_guid, assertion_id):
        logger.info('Looking up assertion %s for bounty %s', assertion_id, bounty_guid)
        return self.generator.get_assertion(bounty_guid, assertion_id).execute().result

    def get_vote(self, bounty_guid, vote_id):
        logger.info('Looking up vote %s for bounty %s', vote_id, bounty_guid)
        return self.generator.get_vote(bounty_guid, vote_id).execute().result

    def get_wallet(self, address):
        logger.info('Getting balance for %s', address)
        return self.generator.get_wallet(address).execute().result

    def post_assertion(self, signed_assertion):
        logger.info('Posting tx: %s', signed_assertion)
        return self.generator.post_assertion(signed_assertion)