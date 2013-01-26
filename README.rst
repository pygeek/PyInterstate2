PyInterstate2: A Python wrapper for InterstateApp's v2 API
==========================================================

Support for all resources in InterstateApp v2 REST API as `documented <http://developers-v2.interstateapp.com/docs/rest>`_.

v2.0.0.0 alpha 2
**see TODO for information on future releases**

Requirements
------------
- Requires Python2.6+

Dependancies
------------
- `requests <https://github.com/kennethreitz/requests>`_

Quick Guide
-----------

To authenticate, initialize InterstateApp with the provided oauth_token.

.. code-block:: python

    interstate_app = PyInterstate2(oauth_token='<oauth_token>')

Example Requests:
-----------------

.. code-block:: python

    #resource GET /account
    interstate_app.account.get() 

    #resource GET /app/:app_id
    interstate_app.app(object_id='<app_id>').get()

    #resource GET /project/:project_id/roads
    interstate_app.project(object_id='<project_id>').roads.get()

    #resource POST /app/:app_id
    params = {}
    interstate_app.app(object_id='<app_id>', params).post() #this works
    interstate_app.app(object_id='<app_id>').post(params) #this works too

    #resource PUT /project/:project_id
    params = {}
    interstate_app.project(object_id='<project_id>', params).put() #this works
    interstate_app.project(object_id='<project_id>').put(params) #this works too

    #resource DELETE /project/:project_id
    interstate_app.project(object_id='<project_id>').delete()


`More info <http://developers-v2.interstateapp.com/docs/rest>`_ on InterstateApp's v2 REST API
