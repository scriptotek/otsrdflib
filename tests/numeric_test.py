import unittest
from otsrdflib import OrderedTurtleSerializer
from rdflib import Graph
from cStringIO import StringIO


class TestCase(unittest.TestCase):

    def test_numeric(self):

        graph = Graph()
        graph.load('tests/data/numeric_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)
        out = StringIO()
        ots.serialize(out)
        out = '\n'.join([x for x in out.getvalue().split('\n') if x.startswith('<')])

        ref = open('tests/data/numeric_sorted.ttl').read()
        ref = '\n'.join([x for x in ref.split('\n') if x.startswith('<')])

        assert out.strip() == ref.strip()
