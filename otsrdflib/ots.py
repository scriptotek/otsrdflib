from rdflib.plugins.serializers.turtle import TurtleSerializer
from rdflib.namespace import Namespace, FOAF, SKOS, RDF
from rdflib import BNode
import logging
import re

SD = Namespace('http://www.w3.org/ns/sparql-service-description#')
ISOTHES = Namespace('http://purl.org/iso25964/skos-thes#')

logger = logging.getLogger(__name__)


class OrderedTurtleSerializer(TurtleSerializer):

    short_name = "ots"

    def __init__(self, store):
        super(OrderedTurtleSerializer, self).__init__(store)

        # Class order:
        self.class_order = []

        # Sort key generators for specific classes :
        self.sorters_by_class = {}

        # Default sort key generators
        self.sorters = [
            ('^(.+)$', lambda x: str(x[0])),
        ]

    def getSorters(self, class_uri):
        return self.sorters_by_class.get(class_uri, self.sorters)

    def getSortKeyFunction(self, class_uri):
        sorters = self.getSorters(class_uri)

        # Order of instances:
        def sortKeyFn(x):
            # Check if the instances match any special pattern:
            for pattern, func in sorters:
                m1 = re.search(pattern, x)
                if m1:
                    return func(m1.groups())
            logging.warning('%s did not match any sorters', x)

        return sortKeyFn

    def orderSubjects(self):
        seen = {}
        subjects = []

        # Find classes not included in self.class_order and sort them alphabetically
        other_classes = [x for x in set(self.store.objects(predicate=RDF.type)) if x not in self.class_order]
        other_classes = sorted(other_classes)

        # Loop over all classes
        for class_uri in self.class_order + other_classes:

            # Sort the members of each class
            members = sorted(self.store.subjects(RDF.type, class_uri),
                             key=self.getSortKeyFunction(class_uri))

            for member in members:
                subjects.append(member)
                self._topLevels[member] = True
                seen[member] = True

        # Include anything not seen yet
        recursable = [
            (isinstance(subject, BNode),
            self._references[subject], subject)
            for subject in self._subjects
            if subject not in seen
        ]

        recursable.sort()
        subjects.extend([subject for (isbnode, refs, subject) in recursable])

        return subjects
