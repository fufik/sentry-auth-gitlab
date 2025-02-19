from requests.exceptions import RequestException

from sentry import http
from sentry.utils import json

from .constants import API_BASE_URL

class GitLabApiError(Exception):
    def __init__(self, message='', status=None):
        super().__init__(message)
        self.status = status


class GitLabClient(object):
    def __init__(self, access_token):
        self.http = http.build_session()
        self.access_token = access_token

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.http.close()


    def _request(self, path):
        headers = {'Authorization': f"Bearer {self.access_token}"}
        url = '{0}/{1}'.format(API_BASE_URL, path.lstrip('/'))

        try:
            req = self.http.get(url, headers=headers)
        except RequestException as e:
            raise GitLabApiError(unicode(e), status=getattr(e, "status_code", 0))
        if req.status_code < 200 or req.status_code >= 300:
            raise GitLabApiError(req.content, status=req.status_code)
        return json.loads(req.content)

    def get_user(self):
        return self._request('user')
