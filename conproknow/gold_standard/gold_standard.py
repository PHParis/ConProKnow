from json import load


class gold_standard(object):
    def __init__(self, gold_standard_file_path):
        with open(gold_standard_file_path, mode="r", encoding="utf-8") as f:
            content = load(f)
