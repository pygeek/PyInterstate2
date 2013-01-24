class MetaBase(object):
    rest_methods = ('get', 'put', 'post', 'delete')
    is_rest_method = lambda inst, name: bool(name.lower() in getattr(inst, '_rest_methods'))

    def __init__(self, oauth_token):
        self.metanames = []
        self.rest_method = None
        self.oauth_token = oauth_token 
        self.params = {}
    
    def __call__(self, object_id=None, params=None):
        resource = self.resource(object_id)

        if params:
            self.params.update(params)

        if not self.rest_method:
            return self
        else:
            return self.validate_request(resource)
    
    def __getattr__(self, metaname):
        _metaname = 'meta_{0}'.format(metaname)

        setattr(self, metaname, self._meta)

        if not self.is_rest_method(metaname):
            self.metanames.append(metaname)
        else:
            self.rest_method = metaname.lower()

        return getattr(self, _metaname)

    @property
    def _meta(self):
        return self

    def resource(self, object_id):
        if object_id != None:
            self.metanames.append(object_id)

        resource = '/'.join(self._metanames)
    
        return resource

    def validate_request(self, resource):
        try:
            if self.rest_method in ('get', 'delete') and self.params:
                raise RequestHasParamsError("method does not support parameters.")
            elif self.rest_method in ('post', 'put') and not self.params:
                raise RequestRequiresParamsError("method must include parameter.")
        except RequestHasParamsError as e:
            print("{0}: {1} {2} {3}".format(e.__class__.__name__,
                                            self.rest_method.upper(),
                                            e.args[0],
                                            e.generic_error_message))

        except RequestRequiresParamsError as e:
            print("{0}: {1} {2} {3}".format(e.__class__.__name__,
                                            self.rest_method.upper(),
                                            e.args[0],
                                            e.generic_error_message))
        else:
            return self.request(resource=resource, method=self._rest_method, params=self.params)

    def request(self):
        raise NotImplementedError

