from rdflib.plugins.serializers.turtle import TurtleSerializer
from rdflib.namespace import Namespace, FOAF, SKOS, RDF
from rdflib import BNode
import re

SD = Namespace('http://www.w3.org/ns/sparql-service-description#')
ISOTHES = Namespace('http://purl.org/iso25964/skos-thes#')


class OrderedTurtleSerializer(TurtleSerializer):

    short_name = "ots"

    topClasses = [SKOS.ConceptScheme,
                   FOAF.Organization,
                   SD.Service,
                   SD.Dataset,
                   SD.Graph,
                   SD.NamedGraph,
                   ISOTHES.ThesaurusArray,
                   SKOS.Concept]

    def __init__(self, store, topClasses=None):
        super(OrderedTurtleSerializer, self).__init__(store)

        # Class order:
        if topClasses is not None:
            self.topClasses = topClasses

        # Instance order:
        self.sorters = [
            ('.*?([0-9]+)$', lambda x: int(x[0]))
        ]

        # Order of instances:
        def sortKey(x):
            # Check if the instances match any special pattern:
            for pattern, func in self.sorters:
                m1 = re.search(pattern, x)
                if m1:
                    return func(m1.groups())

            return x

        self.sortFunction = sortKey

    def orderSubjects(self):
        seen = {}
        subjects = []

        for classURI in self.topClasses:
            members = list(self.store.subjects(RDF.type, classURI))
            members.sort(key=self.sortFunction)

            for member in members:
                subjects.append(member)
                self._topLevels[member] = True
                seen[member] = True

        recursable = [
            (isinstance(subject, BNode),
             self._references[subject], subject)
            for subject in self._subjects if subject not in seen]

        recursable.sort()
        subjects.extend([subject for (isbnode, refs, subject) in recursable])

        return subjects
