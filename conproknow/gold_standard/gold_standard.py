from json import load
from typing import List, Tuple
from statistics import mean
from conproknow.identity.context import ContextWGoldStand, Context
from conproknow.algo.lattice_builder import get_propagation_set


class gold_standard(object):
    class gold_standard_class(object):
        def __init__(self, class_label: str, precision: float, recall: float, f_measure: float, contexts: List[ContextWGoldStand]):
            self.class_label = class_label
            self.precision = precision
            self.recall = recall
            self.f_measure = f_measure
            self.contexts = contexts

    def __init__(self, gold_standard_file_path):
        self.contexts_by_class: List[gold_standard_class] = list()
        with open(gold_standard_file_path, mode="r", encoding="utf-8") as f:
            content = load(f)
            for class_label in content:
                class_label: str = class_label
                precision: float = content[class_label]["p"]
                recall: float = content[class_label]["r"]
                f_measure: float = content[class_label]["f1"]
                contexts: List[ContextWGoldStand] = list()
                for c in content[class_label]["contexts"]:
                    context: Context = Context(str(c["resource"]), int(c["id"]),
                                               set(c["parent_ids"]), set(c["properties"]), set(c["instances"]))
                    cgs: ContextWGoldStand = ContextWGoldStand(
                        context, set(c["gold_standard"]))
                    contexts.append(cgs)
                gsc: gold_standard_class = gold_standard_class(
                    class_label, precision, recall, f_measure, contexts)
                self.contexts_by_class.append(gsc)
        prf: List[Tuple[float, float, float]] = [
            (c.precision, c.recall, c. f_measure) for gsc in self.contexts_by_class for c in gsc.contexts]
        self.precision: float = mean([e[0] for e in prf])
        self.recall: float = mean([e[1] for e in prf])
        self.f_measure: float = mean([e[2] for e in prf])

    def compare
