from conproknow.kg.knowledge_graph import KG
from hdt import HDTDocument
from typing import Iterator, Tuple, Optional


class HDT(KG):

    def __init__(self, hdt_file_path: str):
        self.hdt = HDTDocument(hdt_file_path)

    def predicate_objects(self, subject: str) -> Iterator[Tuple[str, str]]:
        (triples, cardinality) = self.hdt.search_triples(subject, "", "")
        for s, p, o in triples:
            yield p, o

    def subjects(self, predicate: str, obj: str) -> Iterator[str]:
        (triples, cardinality) = self.hdt.search_triples("", predicate, obj)
        for s, p, o in triples:
            yield s

    def triples(self, subject: str, predicate: str, obj: str) -> Iterator[Tuple[str, str, str]]:
        (triples, cardinality) = self.hdt.search_triples(subject, predicate, obj)
        for s, p, o in triples:
            yield (s, p, o)

    def objects(self, subject: str, predicate: str) -> Iterator[str]:
        (triples, cardinality) = self.hdt.search_triples(
            subject, predicate, "")
        for s, p, o in triples:
            yield o

    def count(self, subject: str, predicate: str, obj: str) -> int:
        (triples, cardinality) = self.hdt.search_triples(subject, predicate, obj)
        return cardinality

    def total_triples(self) -> int:
        return self.hdt.total_triples

    def nb_subjects(self) -> int:
        return self.hdt.nb_subjects

    def nb_predicates(self) -> int:
        return self.hdt.nb_predicates

    def nb_objects(self) -> int:
        return self.hdt.nb_objects

    def nb_shared(self) -> int:
        return self.hdt.nb_shared

    def get_schema_description(self, resource: str) -> Optional[str]:
        """Get english description of the specified resource.
        Use the http://schema.org/description property.
        Trailing double quotes and @en are removed!"""
        for o in self.objects(resource, "http://schema.org/description"):
            if o.endswith("@en"):
                # delete trailing @en and double quotes
                return o[1:len(o) - 4]
        return None
