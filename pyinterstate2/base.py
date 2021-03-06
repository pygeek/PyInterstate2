class MetaBase(object):
    rest_methods = ('get', 'put', 'post', 'delete')
    is_rest_method = lambda inst, name: bool(name.lower() in getattr(inst, 'rest_methods'))
    metanames = []
    rest_method = None
    params = {}
    
    def __call__(self, object_id=None, params=None):
        resource = self.resource(object_id)

        if params:
            self.params.update(params)

        if not self.rest_method:
            return self
        else:
            return self.validate_request(resource)
    
    def __getattr__(self, metaname):
        return_value = None

        if not self.is_rest_method(metaname):
            self.metanames.append(metaname)
            return_value = self
        else:
            self.rest_method = metaname.lower()

        return return_value

    def resource(self, object_id):
        if object_id != None:
            self.metanames.append(object_id)

        resource = '/'.join(self.metanames)
    
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
            return self.request(resource=resource, method=self.rest_method, params=self.params)

    def request(self):
        raise NotImplementedError

