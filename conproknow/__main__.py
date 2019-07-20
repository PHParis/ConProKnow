import argparse
from getopt import getopt, GetoptError
from sys import argv, exit
from os.path import isfile
from conproknow.identity.lattice import Lattice
from conproknow.kg.knowledge_graph import KG
from conproknow.kg.hdt_knowledge_graph import HDT
from conproknow.algo.lattice_builder import build_lattice
from conproknow.gold_standard.gold_standard import gold_standard


def usage():
    """Print help for users."""
    print("Type -h or --help to display this message.")
    print("Type -o or --output to specify the output directory. Default is /data2/hamdif/doctorants/ph/xp/")
    print("Type -r or --resource to specify the resource from which the identity context will be computed. Default is http://dbpedia.org/resource/France")
    print("Type -f or --file to specify the HDT file to process. Default is /data2/hamdif/doctorants/ph/linkeddatasets/hdt/lod-a-lot/LOD_a_lot_v1.hdt")
    print("Type -gs or --gold_standard to test the gold standard. Default is /data2/hamdif/doctorants/ph/linkeddatasets/hdt/lod-a-lot/LOD_a_lot_v1.hdt")


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

    kg: KG = HDT(args.hdt)
    if args.command == "lattice":
        lattice = build_lattice(
            args.resource, kg, args.output, False)
    else:
        gs = gold_standard(args.path)
        gs.compare_results(kg)
    print("end!")
