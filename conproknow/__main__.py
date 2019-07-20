import argparse
from getopt import getopt, GetoptError
from sys import argv, exit
from os.path import isfile
from conproknow.identity.lattice import Lattice
from conproknow.kg.knowledge_graph import KG
from conproknow.kg.hdt_knowledge_graph import HDT
from conproknow.algo.lattice_builder import build_lattice


def usage():
    """Print help for users."""
    print("Type -h or --help to display this message.")
    print("Type -o or --output to specify the output directory. Default is /data2/hamdif/doctorants/ph/xp/")
    print("Type -r or --resource to specify the resource from which the identity context will be computed. Default is http://dbpedia.org/resource/France")
    print("Type -f or --file to specify the HDT file to process. Default is /data2/hamdif/doctorants/ph/linkeddatasets/hdt/lod-a-lot/LOD_a_lot_v1.hdt")
    print("Type -gs or --gold_standard to test the gold standard. Default is /data2/hamdif/doctorants/ph/linkeddatasets/hdt/lod-a-lot/LOD_a_lot_v1.hdt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # .add_mutually_exclusive_group(required=True)
    group1 = parser.add_mutually_exclusive_group()
    group2 = group1.add_argument_group(
        "--resource", help="The seed of the lattice.")
    group2.add_argument(
        "--output", help="Directory where the lattice will be saved as a JSON file.")
    group2.add_argument("--hdt", help="HDT file path.")
    group1.add_argument("--gold_standard",
                        help="Valid gold standard file path.")
    # group2 = parser.add_argument_group() #.add_mutually_exclusive_group(required=True)
    # group2.add_argument("lattice2")
    # group2.add_argument("gold_standard2")
    args = parser.parse_args()
    print(args)
    exit(0)
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))

    try:
        opts, args = getopt(argv[1:], "ho:r:f:", [
            "help", "output=", "resource=", "file="])
    except GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        exit(2)

    verbose = False
    hdt_file_path = "/home/ph/Téléchargements/4b3f9dd9aee2ad2cba453e23a8f4ae39an.hdt"
    resource = "http://ld.zdb-services.de/resource/1000005-7"
    output_dir = "/home/ph/Téléchargements/"
    hdt_file_path = "/data2/hamdif/doctorants/ph/linkeddatasets/hdt/dbpedia/dbpedia2016-04en.hdt"
    hdt_file_path = "/data2/hamdif/doctorants/ph/linkeddatasets/hdt/lod-a-lot/LOD_a_lot_v1.hdt"
    resource = "http://dbpedia.org/resource/Paris"
    resource = "http://dbpedia.org/resource/France"
    output_dir = "/data2/hamdif/doctorants/ph/xp/"
    gold_standard_path = "gold_standard/gold_standard.json"
    print("t1")
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            exit()
        elif o in ("-o", "--output"):
            output_dir = a
        elif o in ("-r", "--resource"):
            resource = a
        elif o in ("-f", "--file"):
            hdt_file_path = a
        elif o in ("-gs", "--gold_standard"):
            gold_standard_path = a
        else:
            assert False, "unhandled option"
    exit(0)
    kg: KG = HDT(hdt_file_path)
    lattice = build_lattice(
        "http://www.wikidata.org/entity/Q2343504", kg, None, False)

    # lattice = build_lattice(
    #     "http://www.wikidata.org/entity/Q2343504", kg, None, False)
    # # print(f"{lattice}")
    print("end!")
