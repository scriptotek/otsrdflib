import unittest
from otsrdflib import OrderedTurtleSerializer
from rdflib import Graph
import hashlib
import re
from six import BytesIO


def file_contents(fp):
    fp.seek(0)
    lines = fp.read().decode('utf-8').strip().split('\n')
    lines = [x for x in lines if not x.startswith('@')]  # skip prefixes
    out = '\n'.join(lines)
    print(out)
    return out


class TestCase(unittest.TestCase):

    def xhash(self, x):
        return int(hashlib.sha1(x.encode('utf-8')).hexdigest(), 16) % 10**8

    def test_default_sorter(self):

        graph = Graph()
        graph.load('test/data/mix_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)
        out = BytesIO()
        ots.serialize(out)

        with open('test/data/mix_sorted.ttl', 'rb') as fp:
            assert file_contents(fp) == file_contents(out)

    def test_default_class_order(self):
        # Test that classes are sorted alphabetically by default

        graph = Graph()
        graph.load('test/data/classes_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)
        out = BytesIO()
        ots.serialize(out)

        with open('test/data/classes_sorted.ttl', 'rb') as fp:
            assert file_contents(fp) == file_contents(out)

    def test_custom_sorter(self):

        graph = Graph()
        graph.load('test/data/group_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)

        ots.sorters = [
            ('(.*?)([0-9]+)$', lambda x: self.xhash(x[0]) + int(x[1]))
        ]

        out = BytesIO()
        ots.serialize(out)

        with open('test/data/group_sorted.ttl', 'rb') as fp:
            assert file_contents(fp) == file_contents(out)

    def test_custom_sorter_with_fallback(self):

        graph = Graph()
        graph.load('test/data/numeric_unsorted.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)

        ots.sorters = [
            ('.*?/[A-Za-z]+([0-9.]+)$', lambda x: float(x[0])),
            ('.', lambda x: 0.0),  # default
        ]

        out = BytesIO()
        ots.serialize(out)

        with open('test/data/numeric_sorted.ttl', 'rb') as fp:
            assert file_contents(fp) == file_contents(out)

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

        with open('test/data/dewey_sorted.ttl', 'rb') as fp:
            assert file_contents(fp) == file_contents(out)

    def test_bnodes(self):
        # Just check that bnodes are included and sorted after other things.

        graph = Graph()
        graph.load('test/data/bnodes.ttl', format='turtle')
        ots = OrderedTurtleSerializer(graph)

        out = BytesIO()
        ots.serialize(out)

        with open('test/data/bnodes_sorted.ttl', 'rb') as fp:
            assert file_contents(fp) == file_contents(out)
