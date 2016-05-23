import unittest
from otsrdflib import OrderedTurtleSerializer
from rdflib import Graph
import hashlib
from six import BytesIO


class TestCase(unittest.TestCase):

    def xhash(self, x):
        return int(hashlib.sha1(x.encode('utf-8')).hexdigest(), 16) % 10**8

    def test_custom_sorter(self):

        graph = Graph()
        graph.load('tests/data/group_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)

        ots.sorters = {
            '(.*?)([0-9]+)$': lambda x: self.xhash(x[0]) + int(x[1])
        }

        out = BytesIO()
        ots.serialize(out)
        out = '\n'.join([x for x in out.getvalue().decode('utf-8').split('\n') if x.startswith('<')])

        ref = open('tests/data/group_sorted.ttl').read()
        ref = '\n'.join([x for x in ref.split('\n') if x.startswith('<')])

        assert out.strip() == ref.strip()

    def test_dewey_sorter(self):

        graph = Graph()
        graph.load('tests/data/dewey_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)

        ots.sorters = {
            'http://dewey.info/class/([0-9]{1})/': lambda x: float(x[0] + '00') - 2.e-7,   # a smaller number
            'http://dewey.info/class/([0-9]{2})/': lambda x: float(x[0] + '0') - 1.e-7,  # a small number (so we don't collide with the last .999... number)
            'http://dewey.info/class/([0-9.]{3,})/': lambda x: float(x[0]),
            'http://dewey.info/class/([0-9])\-\-([0-9]+)/': lambda x: 1000. + int(x[0]) + float('.' + x[1])
        }

        out = BytesIO()
        ots.serialize(out)
        out = '\n'.join([x for x in out.getvalue().decode('utf-8').split('\n') if x.startswith('<')])

        ref = open('tests/data/dewey_sorted.ttl').read()
        ref = '\n'.join([x for x in ref.split('\n') if x.startswith('<')])

        assert out.strip() == ref.strip()

    def test_numeric(self):

        graph = Graph()
        graph.load('tests/data/numeric_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)
        out = BytesIO()
        ots.serialize(out)
        out = '\n'.join([x for x in out.getvalue().decode('utf-8').split('\n') if x.startswith('<')])

        ref = open('tests/data/numeric_sorted.ttl').read()
        ref = '\n'.join([x for x in ref.split('\n') if x.startswith('<')])

        assert out.strip() == ref.strip()

    def test_bnodes_sort(self):

        graph = Graph()
        graph.load('tests/data/bnodes.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)

        out = BytesIO()
        ots.serialize(out)

        # TODO: And then...
