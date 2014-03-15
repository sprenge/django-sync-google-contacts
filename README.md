django-group-user-mngt
======================

Manage groups and users using jquery jtable

settings.py
-----------

Add to INSTALLED_APPS : 'group_user_mngt',

GROUP_MANAGEMENT_TEMPLATE = 'manage_groups.html'

Replace the template with a customized template (See below how to create)

urls.py
-------

url(r'^groupmanagement/', include('group_user_mngt.urls', namespace="gm_space")),

copy following files
--------------------

The dist-packages subdirectory in the examples below is just an example.  It all depends on
how this package was installed (with or without env, ubuntu/windows, ...)

Under static root :

mkdir group_user_mngt
cd group_user_mngt
cp -r /usr/local/lib/python2.7/dist-packages/group_user_mngt/static/group_user_mngt/* .


Group view
----------

http://<FQDN>/groupmanagement/group/update/

Template creation
-----------------

.. code-block:: html

    {% extends "group_user_base.html" %}

    <!DOCTYPE html>
    <html>
        <head>
            {% block head_group %}
            {{ block.super }}
            {% endblock %}
        </head>

        <body>


        <article>
            {% block group_user %}
            {{block.super}}
            <div id="GroupMngt" class="grid_16">{% csrf_token %}</div>
            {% endblock %}
            {% block user_group %}
            {{block.super}}
            <div id="UserMngt" class="grid_16">{% csrf_token %}</div>
            {% endblock %}
        </article>

        </body>
    </html>


Future work
-----------

- CSRF support
- Edit permissions
- Improve portability of app
- ...

