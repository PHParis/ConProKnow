from os.path import join, isfile
from typing import Set, Dict, Optional, List
from json import load, dumps
from conproknow.utils.helpers import keep_alphanumeric_only
from conproknow.identity.lattice import Lattice
from conproknow.utils.wikidata import get_wiki_id
from conproknow.kg.hdt_knowledge_graph import KG


def build_lattice(resource: str, kg: KG, output_dir: Optional[str], saving_partial_results: bool, props_to_ignore: Set[str] = None, subjects_to_filter: Set[str] = None, desc_by_props: Dict[str, str] = None, output: bool = False) -> Optional[Lattice]:
    dump_path_context = join(
        output_dir, f"identity_context_{keep_alphanumeric_only(resource)}.json") if output_dir is not None else None
    if dump_path_context is not None and isfile(dump_path_context):
        return Lattice.load_from_file(resource, dump_path_context)
    # dictionaire de dictionaire. La première clé est la propriété et la seconde les valeurs que peut prendre cette propriété. Finalement on a un set des resources ayant meme valeur pour cette propriété que la resource en paramètre
    result: Dict[str, Dict[str, List[str]]] = dict()
    dump_path = join(
        output_dir, f"prop_obj_instances_{keep_alphanumeric_only(resource)}.json") if output_dir is not None else None
    if dump_path is not None and isfile(dump_path):
        with open(dump_path) as json_file:
            result = load(json_file)
        if output:
            print(f"result length: {len(result)}")
            print("partial results loaded")
    else:
        nb_triples = kg.count(resource, "", "")
        if output:
            print(
                f"retrieving subjects having same props and values than {resource} ({nb_triples})")
        if nb_triples == 0:
            return None
        # get all predicates and objects of the seed resource
        for p, o in kg.predicate_objects(resource):
            if props_to_ignore is not None and get_wiki_id(p) in props_to_ignore:
                continue
            # if property don't have a description, skeep it
            if desc_by_props is not None and get_wiki_id(p) not in desc_by_props:
                continue
            nb_shared_subjects = kg.count("", p, o)
            if output:
                print(f"shared subjects: {nb_shared_subjects} ")
            subjects = {s for s in kg.subjects(p, o) if s != resource}
            if subjects_to_filter is not None:  # we search only subjects that share the same type and all subject in subjects_to_filter have the same types
                subjects.intersection_update(subjects_to_filter)
            if not subjects:
                continue
            if p not in result:
                result[p] = dict()
            result[p][o] = list(subjects)
        if output:
            print(f"result length: {len(result)}")
        if saving_partial_results:
            with open(dump_path, encoding="utf-8", mode="w") as f:
                json = dumps(result)
                f.write(json)
            if output:
                print("partial results saved")
    if not result:
        return None
    lattice = Lattice(resource)
    for p in result:
        intersection = set()
        first = True
        for o in result[p]:
            if first:
                first = False
                intersection.update(set(result[p][o]))
            else:
                intersection.intersection_update(set(result[p][o]))
        if bool(intersection):
            context = lattice.build_context(None, {p}, intersection)
            lattice.add(context, 1)

    if output:
        print("building lattices")
    lattice.build_lattice()
    if dump_path_context is not None:
        lattice.save_to_file(dump_path_context)
    return lattice
