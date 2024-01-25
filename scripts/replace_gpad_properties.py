import argparse
import csv
import re

parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gpad_file')
parser.add_argument('-n', '--from_to_tsv')


if __name__ == "__main__":
    args = parser.parse_args()

    from_to_lkp = {}
    with open(args.from_to_tsv) as ftt:
        reader = csv.reader(ftt, delimiter="\t")
        for r in reader:
            from_str = r[0]
            to_str = r[1]
            from_to_lkp[from_str] = to_str

    with open(args.gpad_file) as gpad:
        reader = csv.reader(gpad, delimiter="\t")
        for r in reader:
            if not r[0].startswith("!"):
                properties = r[11]
                if properties:
                    for f in from_to_lkp:
                        t_value = from_to_lkp[f]
                        properties = properties.replace(f, t_value)
                    r[11] = properties
            print("\t".join(r))