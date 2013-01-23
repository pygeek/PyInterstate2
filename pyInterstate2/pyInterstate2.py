#! /usr/bin/env python
import requests


class PyInterstateError(Exception):
    """Base class for Interstate App Exceptions."""
    generic_error_message = "Please see InterstateApp API documentation for more details."

class AuthError(PyInterstateError):
    """Exception raised upon authentication errors."""

class RequestError(PyInterstateError):
    """Exception raised upon violating standard request format."""
    pass

class RequestHasParamsError(RequestError):
    pass

class RequestRequiresParamsError(RequestError):
    pass

class IdError(PyInterstateError):
    """Raised when an operation attempts to query's an Interstate \
        Road or Roadmap that does not exist."""
    pass


class MetaBase(object):
    _rest_methods = ('get', 'put', 'post', 'delete')
    _is_rest_method = lambda inst, name: bool(name.lower() in getattr(inst, '_rest_methods'))

    def __init__(self, oauth_token):
        self._metanames = []
        self._rest_method = None
        self.oauth_token = oauth_token 
        self.params = {}
    
    def __call__(self, object_id=None, params=None):
        resource = self._resource(object_id)

        if params:
            self.params.update(params)

        if not self._rest_method:
            return self
        else:
            return self._validate_request(resource)
    
    def __getattr__(self, metaname):
        setattr(self, metaname, self._meta)

        if not self._is_rest_method(metaname):
            self._metanames.append(metaname)
        else:
            self._rest_method = metaname.lower()

        return getattr(self, metaname)

    @property
    def _meta(self):
        return self

    def _resource(self, object_id):
        if object_id != None:
            self._metanames.append(object_id)

        resource = '/'.join(self._metanames)
    
        return resource

    def _validate_request(self, resource):
        try:
            if self._rest_method in ('get', 'delete') and self.params:
                raise RequestHasParamsError("method does not support parameters.")
            elif self._rest_method in ('post', 'put') and not self.params:
                raise RequestRequiresParamsError("method must include parameter.")
        except RequestHasParamsError as e:
            print("{0}: {1} {2} {3}".format(e.__class__.__name__,
                                            self._rest_method.upper(),
                                            e.args[0],
                                            e.generic_error_message))

        except RequestRequiresParamsError as e:
            print("{0}: {1} {2} {3}".format(e.__class__.__name__,
                                            self._rest_method.upper(),
                                            e.args[0],
                                            e.generic_error_message))
        else:
            return self._request(resource=resource, method=self._rest_method, params=self.params)

    def _request(self):
        raise NotImplementedError


class PyInterstate2(MetaBase):
    protocol = "https"
    base_url = "api.interstateapp.com"
    api_version = 2
    format_type = "json"
    request_timeout = 2.000 

    @property
    def _base_url(self):
        base_url_kwargs = {'protocol' : self.protocol,
                           'base_url' : self.base_url,
                           'api_version' : self.api_version}

        base_url = "{protocol}://{base_url}/v{api_version}".format(**base_url_kwargs)

        return base_url

    def _resource_url(self, resource):
        base_resource_url_kwargs = {'base_url' : self._base_url,
                                    'resource' : resource}

        resource_url = "{base_url}/{resource}".format(**base_resource_url_kwargs)

        return resource_url

    def _request(self, resource, method='get', params={}):
        resource_url = self._resource_url(resource)
        request_url_kwargs = {'resource_url' : resource_url,
                              'oauth_token' : self.oauth_token,
                              'format_type' : self.format_type}
        
        request_url = "{resource_url}.{format_type}?oauth_token={oauth_token}".format(**request_url_kwargs)

        try:
            response = getattr(requests, method)(request_url, verify=False, data=params, timeout=self.timeout) #probably need to verify eventually
        except requests.exceptions.Timeout:
            print(RequestError('RequestError: Request has exceeded specified timeout limit of {0} seconds'.format(self.request_timeout)))
        else:
            return response.content


interstate_app = PyInterstate2(oauth_token='')

#print(interstate_app.project(object_id='4c2d3b5f8ead0ec070010000').get())
