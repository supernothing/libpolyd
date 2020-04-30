import logging
import os

logger = logging.getLogger(__name__)


class BasePolydType(object):
    def __init__(self, api=None):
        self.api = api


class BasePolydResourceType(BasePolydType):
   @classmethod
   def parse_result(cls, result, api, **kwargs):
       logger.debug('Parsing resource %s', cls.__name__)
       return cls(result, api=api, **kwargs)


class BasePolydJSONType(BasePolydResourceType):
    def __init__(self, json=None, api=None):
        super().__init__(api)
        self.json = json
        # TODO be safer and less lazy
        self.__dict__.update(self.json)


class BountyResult(BasePolydJSONType):
    def resolve_assertions(self):
        self.resolved_assertions = []
        for assertion_url in self.assertions:
            assertion_id = os.path.basename(assertion_url)
            self.resolved_assertions.append(self.api.get_assertion(self.guid, assertion_id))

    def resolve_votes(self):
        self.resolved_votes = []
        for vote_url in self.votes:
            vote_id = os.path.basename(vote_url)
            self.resolved_votes.append(self.api.get_vote(self.guid, vote_id))


class Assertion(BasePolydJSONType):
    pass


class Vote(BasePolydJSONType):
    pass
