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

Instance order (within a class) is imposed by adding URI patterns
to `serializer.sorters`:

.. code-block:: python

    serializer.sorters = {
      'http://dewey.info/class/(T?([0-9]+)\-\-)?([0-9.]+)': lambda x: (0 if x[1] is None else int(x[1])*1000) + float(x[2])
    }

URIs that doesn't match any of the specialized sorters are sorted
alphabetically using the Python
`cmp <https://docs.python.org/2/library/functions.html#cmp>`_ method.

