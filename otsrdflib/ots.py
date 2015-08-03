from rdflib.plugins.serializers.turtle import TurtleSerializer
from rdflib.namespace import Namespace, FOAF, SKOS, RDF
from rdflib import BNode


class OrderedTurtleSerializer(TurtleSerializer):

    short_name = "ots"

    def __init__(self, store):
        super(OrderedTurtleSerializer, self).__init__(store)

        SD = Namespace('http://www.w3.org/ns/sparql-service-description#')
        ISOTHES = Namespace('http://purl.org/iso25964/skos-thes#')

        # Order of classes:
        self.topClasses = [SKOS.ConceptScheme,
                           FOAF.Organization,
                           SD.Service,
                           SD.Dataset,
                           SD.Graph,
                           SD.NamedGraph,
                           ISOTHES.ThesaurusArray,
                           SKOS.Concept]

        # Order of instances:
        def compare(x, y):
            x2 = int(re.sub(r'[^0-9]', '', x))
            y2 = int(re.sub(r'[^0-9]', '', y))
            if x2 == 0 or y2 == 0:
                return cmp(x, y)
            else:
                return cmp(x2, y2)

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
