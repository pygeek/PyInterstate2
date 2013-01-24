#! /usr/bin/env python
import requests
from base import MetaBase
from exceptions import *

class PyInterstate2(MetaBase):
    protocol = "https"
    base_url = "api.interstateapp.com"
    api_version = 2
    format_type = "json"
    request_timeout = 2.000 

    @property
    def base_url(self):
        base_url_kwargs = {'protocol' : self.protocol,
                           'base_url' : self.base_url,
                           'api_version' : self.api_version}

        base_url = "{protocol}://{base_url}/v{api_version}".format(**base_url_kwargs)

        return base_url

    def resource_url(self, resource):
        base_resource_url_kwargs = {'base_url' : self._base_url,
                                    'resource' : resource}

        resource_url = "{base_url}/{resource}".format(**base_resource_url_kwargs)

        return resource_url

    def request(self, resource, method='get', params={}):
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

#print(interstate_app.project(object_id='').get())
