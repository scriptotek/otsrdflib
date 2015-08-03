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


Subjects are grouped by class membership. The order of classes
is configured through `serializer.topClasses`.
A default list is provided to have e.g. `SKOS.ConceptScheme` classes
appear before `SKOS.Concept`:

.. code-block:: python

    serializer.topClasses = [SKOS.ConceptScheme,
                           FOAF.Organization,
                           SD.Service,
                           SD.Dataset,
                           SD.Graph,
                           SD.NamedGraph,
                           ISOTHES.ThesaurusArray,
                           SKOS.Concept]
