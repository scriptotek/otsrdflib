import unittest
from otsrdflib import OrderedTurtleSerializer
from rdflib import Graph
import hashlib
from six import BytesIO


class TestCase(unittest.TestCase):

    def test_bnodes_sort(self):

        graph = Graph()
        graph.load('tests/data/bnodes.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)

        out = BytesIO()
        ots.serialize(out)

        # TODO: And then...
