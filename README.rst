.. image:: https://img.shields.io/travis/scriptotek/otsrdflib.svg
   :target: https://travis-ci.org/scriptotek/otsrdflib
   :alt: Build status

.. image:: https://landscape.io/github/scriptotek/otsrdflib/master/landscape.svg?style=flat
   :target: https://landscape.io/github/scriptotek/otsrdflib/master
   :alt: Code health

.. image:: https://img.shields.io/pypi/v/otsrdflib.svg
   :target: https://pypi.python.org/pypi/otsrdflib
   :alt: Latest version

.. image:: https://img.shields.io/github/license/scriptotek/otsrdflib.svg
   :target: http://opensource.org/licenses/MIT
   :alt: MIT license

Ordered Turtle Serializer for rdflib
====================================

An extension to the `rdflib <https://rdflib.readthedocs.org/>`_ Turtle serializer
that adds order (at the price of speed).
Useful when you need to generate diffs between Turtle files, or just to make it
easier for human beings to inspect the files.

.. code-block:: console

    $ pip install otsrdflib

Usage:

.. code-block:: python

    from rdflib import graph
    from otsrdflib import OrderedTurtleSerializer

    my_graph = Graph()

    out = open('out.ttl', 'wb')
    serializer = OrderedTurtleSerializer(my_graph)
    serializer.serialize(out)


Class order is imposed by setting `serializer.topClasses`.
The default list is suitable for thesauri and other controlled vocabularies:

.. code-block:: python

    serializer.topClasses = [SKOS.ConceptScheme,
                           FOAF.Organization,
                           SD.Service,
                           SD.Dataset,
                           SD.Graph,
                           SD.NamedGraph,
                           ISOTHES.ThesaurusArray,
                           SKOS.Concept]

Instance order (within a class) is imposed using the Python
`cmp <https://docs.python.org/2/library/functions.html#cmp>`_ method.
By default, URIs are sorted alphabetically as-is, but with
`serializer.sorters` you can generate your own sort key based on
URI patterns. By default, if a URI ends with a number, that number is
used as a numerical sort key:

.. code-block:: python

    serializer.sorters = [
      ('.*?([0-9]+)$', lambda x: int(x[0]))
    ]

Here ``x`` refers to the match object groups. Note that index 0 refers
to the first group, not the entire match!

With this sorter, `http://…/…/99` will be arranged before `http://…/…/100`
since the sort keys are the integers 99 and 100. Note that if you have
number-ending URIs ending with different bases, these will be mangled together.
One simple way to group together URIs with the same base could be to use a
"large" number that represents the base, for instance a 8-digit hash:

.. code-block:: python

    def xhash(s):
        return int(hashlib.sha1(x[0]).hexdigest(), 16) % 10**8

    serializer.sorters = [
      ('(.*?)([0-9]+)$', lambda x: xhash(x[0]) + int(x[1]))
    ]

For a slightly more complicated example, we have a look at Dewey URIs.
For a typical URI like `http://dewey.info/class/001.433/e23/`, we would
like to use the decimal number `1.433` as the sort key. We can achieve
that by configuring a sorter like so:

.. code-block:: python

    serializer.sorters = [
      ('http://dewey.info/class/([0-9.]+)', lambda x: float(x[0]))
    ]

But then there's also table numbers like `http://dewey.info/class/T1--0901/e23/`.
We want to have the tables T1, T2, ... follow the main schedules.
Since the main schedules go from 0 to 999.99… we can map the tables T1…T6 to
some larger integers, like 1001…1006.
Noting that the table numbers like `0901` represents a fractional part,
the sort key for `T1--0901` becomes `1001.0901`. Such keys can be generated
by adding another sorter:

.. code-block:: python

    serializer.sorters = [
      ('http://dewey.info/class/([0-9.]+)', lambda x: float(x[0])),
      ('http://dewey.info/class/T([0-9])\-\-([0-9]+)', lambda x: 1000. + int(x[0]) + float('.' + x[1]))
    ]

But then there's a couple more cases.. Perhaps alphabetic sorting would work just as well? Seems like it does.

    ots.sorters = [
        ('/([0-9A-Z\-]+)\-\-([0-9.\-;:]+)/e', lambda x: 'T{}--{}'.format(x[0], x[1])),  # table numbers
        ('/([0-9.\-;:]+)/e', lambda x: 'A' + x[0]),  # standard schedule numbers
    ]

Here we've just prefixed table numbers with 'T' and normal schedule numbers with 'A'. Also, we've chosen to match the url fragment before '/e', which is the edition part of the dewey.info urls.

