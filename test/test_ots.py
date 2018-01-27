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
        graph.load('test/data/group_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)

        ots.sorters = [
            ('(.*?)([0-9]+)$', lambda x: self.xhash(x[0]) + int(x[1]))
        ]

        out = BytesIO()
        ots.serialize(out)
        out = '\n'.join([x for x in out.getvalue().decode('utf-8').split('\n') if x.startswith('<')])

        ref = open('test/data/group_sorted.ttl').read()
        ref = '\n'.join([x for x in ref.split('\n') if x.startswith('<')])

        assert ref.strip() == out.strip()

    def test_dewey_sorter(self):

        graph = Graph()
        graph.load('test/data/dewey_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)

        ots.sorters = [
            ('/([0-9A-Z\-]+)\-\-([0-9.\-;:]+)/e', lambda x: 'T{0}--{0}'.format(x[0], x[1])),  # table numbers
            ('/([0-9.\-;:]+)/e', lambda x: 'A' + x[0]),  # standard schedule numbers
        ]

        out = BytesIO()
        ots.serialize(out)
        out = '\n'.join([x for x in out.getvalue().decode('utf-8').split('\n') if x.startswith('<')])

        ref = open('test/data/dewey_sorted.ttl').read()
        ref = '\n'.join([x for x in ref.split('\n') if x.startswith('<')])

        assert ref.strip() == out.strip()

    def test_numeric(self):

        graph = Graph()
        graph.load('test/data/numeric_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)

        ots.sorters = [
            ('.*?/[A-Za-z]+([0-9.]+)$', lambda x: float(x[0])),
            ('.', lambda x: 0.0),  # default
        ]

        out = BytesIO()
        ots.serialize(out)
        out = '\n'.join([x for x in out.getvalue().decode('utf-8').split('\n') if x.startswith('<')])

        ref = open('test/data/numeric_sorted.ttl').read()
        ref = '\n'.join([x for x in ref.split('\n') if x.startswith('<')])

        assert ref.strip() == out.strip()

    def test_mixed(self):

        graph = Graph()
        graph.load('test/data/mix_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)
        out = BytesIO()
        ots.serialize(out)
        out = '\n'.join([x for x in out.getvalue().decode('utf-8').split('\n') if x.startswith('<')])

        ref = open('test/data/mix_sorted.ttl').read()
        ref = '\n'.join([x for x in ref.split('\n') if x.startswith('<')])

        assert ref.strip() == out.strip()

    def test_bnodes_sort(self):

        graph = Graph()
        graph.load('test/data/bnodes.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)

        out = BytesIO()
        ots.serialize(out)

        # TODO: And then...
