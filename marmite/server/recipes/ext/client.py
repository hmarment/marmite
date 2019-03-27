import requests

from marmite.server.recipes.ext.resource import Resource


class Rested:
    """
    A basic HTTP Rest client for API Integrations
    """

    def __init__(self, resources=None):

        self.resources = resources

    # def _set_headers(self, headers=None):
    #     """Update default headers to include any additionals."""
    #     default_headers = ENDPOINTS.get('Headers', {})

    #     # calls to e.g. auth API might not be authenticated
    #     if self._is_authenticated():
    #         default_headers.update({'X-AUTH-TOKEN': self.token.token})
    #     if headers:
    #         default_headers.update(headers)
    #     return default_headers

    # def _build_url(self, *parts):
    #     """Enforce the slash."""
    #     parts = [self.base_url] + list(parts)
    #     return '/'.join(str(part).strip('/') for part in parts)


class Resources:
    def __init__(self, resources=None):
        """
        :param resources: a list of Resource objects.
        """
        if resources:
            for resource in resources:
                self.register(resource)

    def register(self, resource=None):
        """
        Add a new resource, accessible via
        Resources.<resource-name>.
        """
        setattr(self, resource.name, resource)

    def list(self):
        return self.__dict__
