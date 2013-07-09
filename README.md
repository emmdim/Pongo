Pongo
=====

POX Django Minimal integration

The initial idea and code snippets belong to Sam Russell from 
his following blog posts:
[DjangoFlow - Web UI for the POX OpenFlow controller](http://pieknywidok.blogspot.com.es/2012/08/djangoflow-web-ui-for-pox-openflow.html)
[DjangoFlow part two: Quick and simple UI](http://pieknywidok.blogspot.com.es/2012/08/djangoflow-part-two-quick-and-simple-ui.html)

The Pongo application is consisted of 3 main parts. The Django part, the poxweb Django application that integrates POX with Django
and a small library for integration with Community-Lab.

Django
------


As a tree structure, Pongo looks like a Django project. The server which leads to the Django administration
interface can be started normally by configuring the Pongo/settings.py file properly and running the following commands:


  python manage.py syncdb
  python manage.py runserver


Poxweb application
------------------

The Poxweb application is a Django application that also contains the POX functionality and is located in the poxweb folder.
We will now describe the most interesting files:


**models.py**: Contains the Django models that describe the links and the slivers.

**admin.py**: Includes the Django models in the Django administrations environment.

**ext/db.py**: A backend library for the POX application, that queries the Django database.

**ext/dbpoll.py**: A backend daemon for the POX application, that is asynchronously checking if changes concerning the links occured in the database.

**ext/l2topo.py**: The main POX application that handles the POX OpenFlow events and translates them to Django actions. At the same time it receives information from
**dbpoll.py** concerning the database changes and translates them to OpenFlow rules if necessary.


Since it is a part Django application, POX should be started after the Django server. The CLI command to start the POX application is:

  ./pox.py l2topo



Integration with Community-Lab
-------------------------------

**poxweb/ext/slice.py**: This module implements the REST communication between POX and any Community-Lab node. In case the user does not want to
use Pongo with Community-Lab but with his own set of nodes he should implement the communication overriding this module.

