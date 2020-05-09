from . import const, exceptions, resources

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


class PolydRequest(object):
    def __init__(self, api, request_parameters, timeout=const.DEFAULT_HTTP_TIMEOUT, result_parser=None,
                 **kwargs):
        self.api = api
        self.session = self.api.session
        self.request_parameters = request_parameters
        self.timeout = timeout
        self.result_parser = result_parser
        self.parser_kwargs = kwargs
        self.status_code = None
        self.result = None
        self.raw_result = None

    def execute(self):
        self.request_parameters.setdefault('timeout', self.timeout)
        self.raw_result = self.session.request(**self.request_parameters)
        if self.result_parser is not None:
            self.parse_result(self.raw_result)
        return self

    def parse_result(self, result):
        # TODO better exception handling
        try:
            self.status_code = result.status_code
            if self.status_code // 100 != 2:
                raise exceptions.PolydException(f'Status: {result.status_code}, {result.json()}')
            json = result.json()
            if json['status'] != 'OK':
                raise exceptions.PolydException(f'Failed request: {json}')

            self.result = self.result_parser.parse_result(json['result'], self.api, **self.parser_kwargs)
        except JSONDecodeError as e:
            raise


class PolydRequestGenerator(object):
    def __init__(self, api, base_uri):
        self.api = api
        self.base_uri = base_uri

    def get_bounty_results(self, bounty_guid):
        return PolydRequest(self.api, {
            'method': 'GET',
            'url': f'{self.base_uri}/bounties/{bounty_guid}'
        }, result_parser=resources.BountyResult)

    def get_assertion(self, bounty_guid, assertion_id):
        return PolydRequest(self.api, {
            'method': 'GET',
            'url': f'{self.base_uri}/bounties/{bounty_guid}/assertions/{assertion_id}'
        }, result_parser=resources.Assertion)

    def get_vote(self, bounty_guid, vote_id):
        return PolydRequest(self.api, {
            'method': 'GET',
            'url': f'{self.base_uri}/bounties/{bounty_guid}/votes/{vote_id}'
        }, result_parser=resources.Vote)

    def get_wallet(self, wallet):
        return PolydRequest(self.api, {
            'method': 'GET',
            'url': f'{self.base_uri}/wallets/{wallet}/'
        }, result_parser=resources.Wallet)

    def post_bounty(self, bounty):
        raise NotImplemented()

    def post_assertion(self, signed_assertion):
        pass

    def post_vote(self, assertion):
        raise NotImplemented()


class PolydFastRequestGenerator(PolydRequestGenerator):
    BASE = '/v1'
