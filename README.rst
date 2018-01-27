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

    graph = Graph()
    serializer = OrderedTurtleSerializer(graph)
    with open('out.ttl', 'wb') as fp:
        serializer.serialize(fp)


Class order
-----------

By default, classes are ordered alphabetically by their URIS.

A custom order can be imposed by adding classes to the `class_order` attribute.
For a SKOS vocabulary, for instance, you might want to sort the concept scheme first,
followed by the other elements of the vocabulary:

.. code-block:: python

    from otsrdflib import OrderedTurtleSerializer
    from rdflib import graph
    from rdflib.namespace import Namespace, SKOS

    ISOTHES = Namespace('http://purl.org/iso25964/skos-thes#')

    graph = Graph()
    serializer = OrderedTurtleSerializer(graph)
    serializer.class_order = [
        SKOS.ConceptScheme,
        SKOS.Concept,
        ISOTHES.ThesaurusArray,
    ]
    with open('out.ttl', 'wb') as fp:
        serializer.serialize(fp)

Any class not included in the `class_order` list will be sorted alphabetically
at the end, after the classes included in the list.

Instance order
--------------

By default, instances of a class are ordered alphabetically by their URIS.

A custom order can be imposed by defining functions that generate sort keys
from the URIs. For instance, you could define a function that returns the
numeric last part of an URI to be sorted numerically:

.. code-block:: python

    serializer.sorters = [
        ('.*?/[^0-9]*([0-9.]+)$', lambda x: float(x[0])),
    ]

The first element of the tuple (`'.*?/[^0-9]*([0-9.]+)$'`) is the regexp pattern
to be matched against the URIs, while the second element (`lambda x: float(x[0])`)
is the sort key generating function. In this case, it returns the first
backreference as a float.

The patterns in `sorters` will be attempted matched against instances
of any class. You can also define patterns that will only be matched against
instances of a specific class. Let's say you only wanted to sort instances
of `SKOS.Concept` this way:

.. code-block:: python

    from rdflib.namespace import SKOS

    serializer.sorters_by_class = {
        SKOS.Concept: [
            ('.*?/[^0-9]*([0-9.]+)$', lambda x: float(x[0])),
        ]
    }

For a slightly more complicated example, let's look at Dewey. Classes
in the main schedules are describes by URIs like
`http://dewey.info/class/001.433/e23/`, and we will use the class number
(001.433) for sorting. But there's also table classes
like `http://dewey.info/class/1--0901/e23/`.
We want to sort these at the end, after the main schedules.
To achieve this, we define two sorters, one that matches the table classes
and one that matches the main schedule classes:

.. code-block:: python

    serializer.sorters = [
        ('/([0-9A-Z\-]+)\-\-([0-9.\-;:]+)/e', lambda x: 'T{}--{}'.format(x[0], x[1])),  # table numbers
        ('/([0-9.\-;:]+)/e', lambda x: 'A' + x[0]),  # main schedule numbers
    ]

By prefixing the table numbers with 'T' and the main schedule numbers with 'A',
we ensure the table numbers are sorted after the main schedule numbers.


Changes in version 0.5
----------------------

* The `topClasses` attribute was renamed to `class_order` to better reflect
  its content and comply with PEP8. It was also changed to be empty by default,
  since the previous default list was rather random.
* A `sorters_by_class` attribute was added to allow sorters to be defined per class.
