#! /usr/bin/env python
import requests


class PyInterstate2Base(object):
    _rest_methods = ['get', 'put', 'post', 'delete']
    _is_rest_method = lambda inst, name: bool(name.lower() in getattr(inst, '_rest_methods'))

    def __init__(self, oauth_token):
        self._metanames = []
        self._metamethod = None
        self.oauth_token = oauth_token 
    
    def __call__(self, params=None,*args):
        #add error handling - params for put or post only
        #get/post/put/delete methods do not take any arguments
        resource = self._resource(*args)        

        if not self._metamethod:
            return self
        else:
            return self._request(resource, self._metamethod)
    
    def __getattr__(self, name):
        setattr(self, name, self._meta)

        if not self._is_rest_method(name):
            self._metanames.append(name)
        else:
            self._metamethod = name.lower()

        return getattr(self, name)

    @property
    def _meta(self):
        return self

    def _resource(self, *args):
        if args:
            self._metanames.append(*args)

        resource = '/'.join(self._metanames)
    
        return resource

    def _request(self):
        raise NotImplementedError


class PyInterstate2(PyInterstate2Base):
    protocol = "https"
    base_url = "api.interstateapp.com"
    api_version = 2
    format_type = "json"

    @property
    def _base_uri(self):
        base_uri_kwargs = {'protocol' : self.protocol,
                           'base_url' : self.base_url,
                           'api_version' : self.api_version}

        base_uri = "{protocol}://{base_url}/v{api_version}".format(**base_uri_kwargs)

        return base_uri

    def _resource_uri(self, resource):
        base_resource_uri_kwargs = {'base_uri' : self._base_uri,
                                    'resource' : resource}

        resource_uri = "{base_uri}/{resource}".format(**base_resource_uri_kwargs)

        return resource_uri

    def _request(self, resource, params=None, method='get'):
        #add error handling - unable to contact server
        resource_uri = self._resource_uri(resource)
        request_uri_kwargs = {'resource_uri' : resource_uri,
                              'oauth_token' : self.oauth_token,
                              'format_type' : self.format_type}
        
        request_uri = "{resource_uri}.{format_type}/?oauth_token={oauth_token}".format(**request_uri_kwargs)

        #different request if it's post/put to allow params
        response = getattr(requests, method)(request_uri, verify=False) #probably need to verify eventually

        return response.content


#interstate_app = PyInterstate2(oauth_token="")
#print(interstate_app.account.get())
