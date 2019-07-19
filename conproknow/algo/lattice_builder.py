from os.path import join, isfile
from typing import Set, Dict, Optional, List, Tuple, Iterable
from json import load, dumps
from conproknow.utils.helpers import keep_alphanumeric_only, timing, cosine_similarity
from conproknow.identity.lattice import Lattice
from conproknow.utils.wikidata import get_wiki_id
from conproknow.kg.hdt_knowledge_graph import KG
from conproknow.sentence_embedding.infersent import infersent
from statistics import mean

threshold = 0.1


@timing
def build_lattice(resource: str, kg: KG, output_dir: str, saving_partial_results: bool, props_to_ignore: Set[str] = None, subjects_to_filter: Set[str] = None, desc_by_props: Dict[str, str] = None, output: bool = False) -> Optional[Lattice]:
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
            context = lattice.build_context(set(), {p}, intersection)
            lattice.add(context, 1)

    if output:
        print("building lattices")
    lattice.build_lattice()
    if dump_path_context is not None:
        lattice.save_to_file(dump_path_context)
    return lattice


def get_descriptions(entities: Iterable[str], kg: KG) -> List[Tuple[str, str]]:
    ''' Return the list composed of entity/description couples.'''
    results: List[Tuple[str, str]] = list()
    # keep only properties with english description
    for e in entities:
        desc = kg.get_schema_description(e)
        if desc is not None:
            results.append((e, desc))
    return results


def get_propagation_set(seed: str, indiscernibles: Set[str], similars: Set[str], kg: KG) -> Set[str]:
    '''Return the set of properties that are propagable given the parameters.'''
    # get all properties that could be propagable
    candidate_properties: Set[str] = {p for r in similars.union(
        {seed}) for (_, p, _) in kg.triples(r, "", "")}
    # removes indiscernible set because they are propagable by definition
    candidate_properties.difference_update(indiscernibles)
    # get couples of candidate property/description
    candid_descs = get_descriptions(candidate_properties, kg)
    if not candid_descs:
        return set()
    # get couples of indiscernible property/description
    indi_descs = get_descriptions(indiscernibles, kg)
    if not indi_descs:
        return set()

    infersent = infersent()
    infersent.update_vocab({desc for (p, desc) in candid_descs}.union(
        {desc for (p, desc) in indi_descs}))

    # getting indiscernible set embeddings
    indi_embeds = infersent.get_embeddings([desc for (p, desc) in indi_descs])

    # getting candidate set embeddings
    candid_embeds = infersent.get_embeddings(
        [desc for (p, desc) in candid_descs])
    results: Set[str] = set()
    for i, candid_embed in enumerate(candid_embeds):
        distances: List[float] = list()
        for indi_embed in indi_embeds:
            distance = 1 - cosine_similarity(candid_embed, indi_embed)
            distances.append(distance)
        mean_distance = mean(distances)
        if mean_distance <= threshold:
            results.add(candid_descs[i][0])
    return results
