from getopt import getopt, GetoptError
from sys import argv, exit
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


if __name__ == "__main__":
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
        else:
            assert False, "unhandled option"
    kg: KG = HDT(hdt_file_path)
    lattice = build_lattice(
        "http://www.wikidata.org.org/entity/Q2343504", kg, None, False)
    print(f"{lattice}")
