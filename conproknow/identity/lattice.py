from context import Context
from typing import Iterator, Set
from json import dumps, load


class Lattice(object):
    def __init__(self, resource: str):
        self.dict = dict()
        self.counter = 0
        self.resource = resource

    def __repr__(self):
        return str(self.__dict__)

    def to_json(self):
        dict_tmp = dict()
        for lvl in self.dict:
            dict_tmp[lvl] = list()
            for c in self.dict[lvl]:
                dict_tmp[lvl].append(c.to_json())
                # if c.parent_ids is None:
                #     parent_ids = list()
                # else:
                #     parent_ids = list(c.parent_ids)
                # {
                #     "id": c.id,
                #     "properties": list(c.properties),
                #     "instances": list(c.instances),
                #     "parent_ids": list(parent_ids)
                # })
        return dict_tmp

    @staticmethod
    def load_from_file(resource: str, json_file_path: str):
        lattice = Lattice(resource)
        with open(json_file_path, mode="r", encoding="utf-8") as json_file:
            data = load(json_file)
            for lvl in data:
                lattice.dict[lvl] = set()
                for c in data[lvl]:
                    r = c["resource"] if "resource" in c else resource
                    context = Context(r, int(c["id"]), set(c["parent_ids"]), set(
                        c["properties"]), set(c["instances"]))
                    if len(context.parent_ids) == 0:
                        context.parent_ids = None
                    lattice.dict[lvl].add(context)
        return lattice

    def get_max_lvl(self) -> int:
        if not bool(self.dict):
            return 0
        return max([int(k) for k in self.dict.keys()])

    def add(self, context: Context, level: int) -> None:
        key = str(level)
        if key in self.dict:
            self.dict[key].add(context)
        else:
            self.dict[key] = {context}

    def get_contexts(self, level: int) -> Iterator[Context]:
        if str(level) in self.dict:
            for context in self.dict[str(level)]:
                yield context

    def get_all_contexts(self) -> Iterator[Context]:
        for level in self.dict:
            for context in self.dict[level]:
                yield context

    def count_contexts(self, level: int = None) -> int:
        if level is None:
            return sum(1 for _ in self.get_all_contexts())
        return sum(1 for _ in self.get_contexts(level))

    def build_context(self, parent_ids: Set[int], properties: Set[str], instances: Set[str]) -> Context:
        context = Context(self.resource, self.counter,
                          parent_ids, properties, instances)
        self.counter += 1
        return context

    def build_lattice(self, level: int = 2, output: bool = False):
        if output:
            print(f"level {level}")
        if level <= 1:  # this case should never happend, since by default level=2, then it is recursively called and increased
            return self
        nb_elements_at_level_1 = self.count_contexts(1)
        if nb_elements_at_level_1 <= 1:  # There is only one element at level one, thus the lattice is composed of only one node
            return self
        super_contexts = list(self.get_contexts(level - 1))
        visited_nodes = set()
        for i in range(len(super_contexts)):
            c_1: Context = super_contexts[i]
            for j in range(i + 1, len(super_contexts)):
                c_2: Context = super_contexts[j]
                props_union = c_1.properties.union(c_2.properties)
                key = tuple(sorted(list(props_union)))
                if len(props_union) == level and key not in visited_nodes:
                    visited_nodes.add(key)
                    intersection = c_1.instances.intersection(c_2.instances)
                    if bool(intersection):
                        context = self.build_context(
                            {c_1.id, c_2.id}, props_union, intersection)
                        self.add(context, level)
        if self.get_max_lvl() == level:
            return self.build_lattice(level + 1)
        else:
            return self

    def save_to_file(self, output_json_file_path: str) -> None:
        print("saving lattice")
        with open(output_json_file_path, encoding="utf-8", mode="w") as f:
            json = dumps(self.to_json(), sort_keys=True, indent=4)
            f.write(json)
        print(f"lattice saved in {output_json_file_path}")
