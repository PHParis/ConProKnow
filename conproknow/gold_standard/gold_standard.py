from json import load
from typing import List, Tuple, Set, Dict
from statistics import mean
from math import floor
from conproknow.identity.context import ContextWGoldStand, Context
from conproknow.algo.lattice_builder import get_propagation_set
from conproknow.kg.knowledge_graph import KG


class gold_standard_class(object):
    def __init__(self, class_label: str, precision: float, recall: float, f_measure: float, contexts: List[ContextWGoldStand]):
        self.class_label = class_label
        self.precision = precision
        self.recall = recall
        self.f_measure = f_measure
        self.contexts = contexts


class gold_standard(object):

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
                    cgs.precision = float(c["p"])
                    cgs.recall = float(c["r"])
                    cgs.f_measure = float(c["f1"])
                    contexts.append(cgs)
                gsc: gold_standard_class = gold_standard_class(
                    class_label, precision, recall, f_measure, contexts)
                self.contexts_by_class.append(gsc)
        prf: List[Tuple[float, float, float]] = [
            (c.precision, c.recall, c. f_measure) for gsc in self.contexts_by_class for c in gsc.contexts]
        self.precision: float = mean([e[0] for e in prf])
        self.recall: float = mean([e[1] for e in prf])
        self.f_measure: float = mean([e[2] for e in prf])

    # def get_descriptions(self, kg: KG):
    #     '''Get alls property descriptions needed for this Gold Standard in order to feed the encoder vocabulary.'''
    #     raise NotImplementedError
    #     for gsc in self.contexts_by_class:
    #         for c in gsc.contexts:
    #             seed: str = c.resource
    #             indiscernibles: Set[str] = c.properties
    #             similars: Set[str] = c.instances
    #             # get all properties that could be propagable
    #             candidate_properties: Set[str] = {p for r in similars.union(
    #                 {seed}) for (_, p, _) in kg.triples(r, "", "")}
    #             candidate_properties = {get_wiki_id(
    #                 p) for p in candidate_properties if "wikidata" in p}
    #             # get couples of candidate property/description
    #             candid_descs = get_descriptions(
    #                 [wd + p for p in candidate_properties], kg)
    #             if not candid_descs:
    #                 return set()
    #             # get couples of indiscernible property/description
    #             indi_descs = get_descriptions(
    #                 [wd + p for p in indiscernibles], kg)
    #             if not indi_descs:
    #                 return set()
    #             vocab = {desc for (p, desc) in candid_descs}.union(
    #                 {desc for (p, desc) in indi_descs})

    def compare_results(self, kg: KG, encoder_type: type, threshold: float) -> Dict[str, List[float]]:
        '''Compute propagable set for the given indiscernible sets and then, print precison, recall and f-measure.'''
        overall_precisions: List[float] = list()
        overall_recalls: List[float] = list()
        overall_f_measures: List[float] = list()
        results: Dict[str, List[float]] = dict()
        for gsc in self.contexts_by_class:
            class_label = gsc.class_label
            print(f"Processing class: {class_label}")
            precisions: List[float] = list()
            recalls: List[float] = list()
            f_measures: List[float] = list()
            for c in gsc.contexts:
                seed: str = c.resource
                indiscernibles: Set[str] = c.properties
                similars: Set[str] = c.instances
                selected_candidates = get_propagation_set(
                    seed, indiscernibles, similars, kg, encoder_type, threshold)
                gold_standard_selection: Set[str] = c.gold_standard
                tp = gold_standard_selection.intersection(selected_candidates)
                fp = selected_candidates.difference(tp)
                fn = gold_standard_selection.difference(selected_candidates)
                precision = len(tp) / (len(tp) + len(fp)
                                       ) if len(tp) + len(fp) > 0 else 0
                recall = len(tp) / (len(tp) + len(fn)
                                    ) if len(tp) + len(fn) > 0 else 0
                f_measure = 2 * precision * recall / \
                    (precision + recall) if precision + recall > 0 else 0
                precisions.append(precision)
                recalls.append(recall)
                f_measures.append(f_measure)
            precision = mean(precisions)
            recall = mean(recalls)
            f_measure = mean(f_measures)
            overall_precisions.append(precision)
            overall_recalls.append(recall)
            overall_f_measures.append(f_measure)
            print(f"class {class_label}:")
            print(f"\tprecision: {floor(precision * 10000) / 100}%")
            print(f"\trecall: {floor(recall * 10000) / 100}%")
            print(f"\tf-measure: {floor(f_measure * 10000) / 100}%")
            results[class_label] = [precision, recall, f_measure]

        print(f"Overall:")
        print(f"\tprecision: {floor(mean(overall_precisions) * 10000) / 100}%")
        print(f"\trecall: {floor(mean(overall_recalls) * 10000) / 100}%")
        print(f"\tf-measure: {floor(mean(overall_f_measures) * 10000) / 100}%")
        results["overall"] = [mean(overall_precisions),
                              mean(overall_recalls), mean(overall_f_measures)]
        return results
