from typing import Dict, List
import argparse
from getopt import getopt, GetoptError
from sys import argv, exit
from os.path import isfile
from numpy import arange
from json import dump
from datetime import datetime
from conproknow.identity.lattice import Lattice
from conproknow.kg.knowledge_graph import KG
from conproknow.kg.hdt_knowledge_graph import HDT
from conproknow.algo.lattice_builder import build_lattice
from conproknow.gold_standard.gold_standard import gold_standard
from conproknow.sentence_embedding.gensen_encoder import GenSenEncoder
from conproknow.sentence_embedding.infersent import InfersentEncoder
from conproknow.sentence_embedding.universal_sentence_encoder import UniversalSentenceEncoder
from conproknow.algo.containers import Containers


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    parser_lattice = subparsers.add_parser("lattice")
    parser_lattice.add_argument(
        "--resource", help="The seed of the lattice.")
    parser_lattice.add_argument(
        "--output", help="Directory where the lattice will be saved as a JSON file.")
    parser_lattice.add_argument("--hdt", help="HDT file path.", required=True)

    parser_gold = subparsers.add_parser("gold")
    parser_gold.add_argument("--path",
                             help="Valid gold standard file path.", default="gold_standard/gold_standard.json")
    parser_gold.add_argument("--hdt", help="HDT file path.", required=True)
    args = parser.parse_args()

    # verbose = False
    # hdt_file_path = "/home/ph/Téléchargements/4b3f9dd9aee2ad2cba453e23a8f4ae39an.hdt"
    # resource = "http://ld.zdb-services.de/resource/1000005-7"
    # output_dir = "/home/ph/Téléchargements/"
    # hdt_file_path = "/data2/hamdif/doctorants/ph/linkeddatasets/hdt/dbpedia/dbpedia2016-04en.hdt"
    # hdt_file_path = "/data2/hamdif/doctorants/ph/linkeddatasets/hdt/lod-a-lot/LOD_a_lot_v1.hdt"
    # resource = "http://dbpedia.org/resource/Paris"
    # resource = "http://dbpedia.org/resource/France"
    # output_dir = "/data2/hamdif/doctorants/ph/xp/"
    # gold_standard_path = "gold_standard/gold_standard.json"
    encoders = [
        # None,
        # GenSenEncoder,
        # InfersentEncoder,
        UniversalSentenceEncoder,
    ]
    print(f"Opening HDT file: {args.hdt}")
    kg: KG = HDT(args.hdt)
    print(f"Mode: {args.command}")

    if args.command == "lattice":
        threshold = 0.1
        encoder = InfersentEncoder
        lattice = build_lattice(threshold, encoder,
                                args.resource, kg, args.output, False)
    else:
        results: Dict[str, Dict[float, Dict[str, List[float]]]] = dict()
        for encoder in encoders:
            Containers.encoder_desc_ndarray.clear()
            results[str(encoder)] = dict()
            print(f"{datetime.now()} - Using encoder: {encoder}")
            for threshold in arange(0.25, 1.0, 0.05):
                print(f"{datetime.now()} - threshold: {threshold}")
                gs = gold_standard(args.path)
                partial_results = gs.compare_results(kg, encoder, threshold)
                results[str(encoder)][threshold] = partial_results
                print(f"Saving results in results.json...")
                with open("results.json", mode="w", encoding="utf-8") as f:
                    dump(results, f, sort_keys=True, indent=4)
    print("end!")

# V=2
# class comics character:
#     precision: 68.16%
#     recall: 83.33%
#     f-measure: 71.48%
# class country:
#     precision: 69.66%
#     recall: 85.83%
#     f-measure: 70.77%
# class film :
#     precision: 76.08%
#     recall: 76.08%
#     f-measure: 73.33%
# class literary work:
#     precision: 62.93%
#     recall: 77.73%
#     f-measure: 68.22%
# class political party:
#         precision: 61.66%
#         recall: 86.66%
#         f-measure: 66.83%
# Overall:
#         precision: 67.7%
#         recall: 81.93%
#         f-measure: 70.12%
