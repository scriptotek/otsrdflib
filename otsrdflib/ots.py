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
        self.sorters = {
            '.*?([0-9]+)$': lambda x: int(x[0])
        }

        # Order of instances:
        def compare(x1, x2):
            # Check if the instances match any special pattern:
            for pattern, func in self.sorters.items():
                m1 = re.match(pattern, x1)
                if m1:
                    x1 = func(m1.groups())
                    break
            for pattern, func in self.sorters.items():
                m2 = re.match(pattern, x2)
                if m2:
                    x2 = func(m2.groups())
                    break

            return cmp(x1, x2)

        self.sortFunction = compare

    def orderSubjects(self):
        seen = {}
        subjects = []

        for classURI in self.topClasses:
            members = list(self.store.subjects(RDF.type, classURI))
            members.sort(self.sortFunction)

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
