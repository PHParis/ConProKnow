from typing import Iterator, Tuple, Optional


class KG(object):

    def count(self, s: str, p: str, o: str) -> int:
        raise NotImplementedError

    def predicate_objects(self, subject: str) -> Iterator[Tuple[str, str]]:
        raise NotImplementedError

    def triples(self, subject: str, predicate: str, obj: str) -> Iterator[Tuple[str, str, str]]:
        raise NotImplementedError

    def objects(self, subject: str, predicate: str) -> Iterator[str]:
        raise NotImplementedError

    def subjects(self, predicate: str, obj: str) -> Iterator[str]:
        raise NotImplementedError

    def total_triples(self) -> int:
        raise NotImplementedError

    def nb_subjects(self) -> int:
        raise NotImplementedError

    def nb_predicates(self) -> int:
        raise NotImplementedError

    def nb_objects(self) -> int:
        raise NotImplementedError

    def nb_shared(self) -> int:
        raise NotImplementedError

    def get_schema_description(self, resource: str) -> Optional[str]:
        '''Get english description of the specified resource.
        Use the http://schema.org/description property.
        Trailing double quotes and @en are removed!'''
        raise NotImplementedError
