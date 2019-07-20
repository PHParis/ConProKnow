from typing import Set
from conproknow.kg.knowledge_graph import KG
from typing import List, Tuple
from json import load


class Context:
    def __init__(self, resource: str, id: int, parent_ids: Set[int], properties: Set[str], instances: Set[str]):
        self.properties: Set[str] = properties
        self.instances: Set[str] = instances
        self.id: int = id
        self.parent_ids: Set[int] = parent_ids
        self.resource = resource
        self.scores: List[Tuple[str, float]] = list()
        self.candidates: Set[str] = set()
        self.propagables: Set[str] = set()

    def __repr__(self):
        return str(self.__dict__)

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if isinstance(other, Context):
            return self.properties == other.properties
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def get_related_properties(self, kg: KG) -> List[str]:
        """Return properties of instances related to the context,
        ie. properties of the context's subject and properties
        of instances that are similar with respect to this context."""
        resources: Set[str] = {self.resource}
        resources.update(self.instances)
        result: Set[str] = set()
        for resource in resources:
            result.update({p for (p, o) in kg.predicate_objects(resource)})
        return list(result)

    def to_json(self):
        dict_tmp = dict()
        if self.parent_ids is None:
            parent_ids = list()
        else:
            parent_ids = list(self.parent_ids)
        return {
            "id": self.id,
            "properties": list(self.properties),
            "instances": list(self.instances),
            "parent_ids": list(parent_ids),
            "resource": self.resource,
            "scores": [list(t) for t in self.scores],
            "candidates": list(self.candidates),
            "propagables": list(self.propagables),
        }

    @staticmethod
    def load_from_file(json_file_path: str):
        with open(json_file_path, mode="r", encoding="utf-8") as json_file:
            data = load(json_file)
            c = Context(
                resource=data["resource"] if "resource" in data else "",
                properties=set(data["properties"]
                               ) if "properties" in data else set(),
                instances=set(data["instances"]
                              ) if "instances" in data else set(),
                id=int(data["id"]) if "id" in data else -1,
                parent_ids={
                    int(i) for i in data["parent_ids"]} if "parent_ids" in data else set()
            )
            if "scores" in data:
                c.scores = [t for t in data["scores"]]
            else:
                c.scores = list()
            if "candidates" in data:
                c.candidates = {t for t in data["candidates"]}
            else:
                c.candidates = set()
            if "propagables" in data:
                c.propagables = {t for t in data["propagables"]}
            else:
                c.propagables = set()
            return c
        #     for lvl in data:
        #         lattice.dict[lvl] = set()
        #         for c in data[lvl]:
        #             r = c["resource"] if "resource" in c else resource
        #             context = Context(r, int(c["id"]), set(c["parent_ids"]), set(
        #                 c["properties"]), set(c["instances"]))
        #             if len(context.parent_ids) == 0:
        #                 context.parent_ids = None
        #             lattice.dict[lvl].add(context)
        # return lattice


class ContextWGoldStand(Context):

    def __init__(self, c: Context, gold_standard: Set[str]):
        super(ContextWGoldStand, self).__init__(c.resource,
                                                c.id, c.parent_ids, c.properties, c.instances)
        self.scores = c.scores
        self.candidates = c.candidates
        self.propagables = c.propagables
        self.gold_standard: Set[str] = gold_standard
        self.precision: float = 0
        self.recall: float = 0
        self.f_measure: float = 0
