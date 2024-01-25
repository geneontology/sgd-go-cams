import argparse
import csv
import re

parser = argparse.ArgumentParser()
parser.add_argument('-g', '--gpad_file')
parser.add_argument('-i', '--gpi_file')


if __name__ == "__main__":
    args = parser.parse_args()

    gpi_db_xref_lkp = {}
    with open(args.gpi_file) as gpi:
        reader = csv.reader(gpi, delimiter="\t")
        for r in reader:
            if r[0].startswith("!"):
                continue
            gene_db = r[0]
            gene_id = r[1]
            gene_curie = "{}:{}".format(gene_db, gene_id)
            db_xrefs = r[8]
            # We want the first pipe-separated Curie from db_xrefs
            db_xref = db_xrefs.split("|")[0]
            if db_xref:
                gpi_db_xref_lkp[db_xref] = gene_curie
            # print(r)

    with open(args.gpad_file) as gpad:
        reader = csv.reader(gpad, delimiter="\t")
        for r in reader:
            if not r[0].startswith("!"):
                db_object_id = r[0]
                db_xref = gpi_db_xref_lkp.get(db_object_id)
                if db_xref:
                    r[0] = db_xref
                extensions = r[10]
                if extensions:
                    # Match and replace any "UniProtKB:nnnnn" value in extensions string with gpi_db_xref_lkp.get("UniProtKB:nnnnn")
                    # Get all regex matches for "UniProtKB:\w+" in extensions string
                    regex_matches = re.findall(r"UniProtKB:\w+", extensions)
                    for match in regex_matches:
                        # Replace each match with the value from gpi_db_xref_lkp
                        new_id = gpi_db_xref_lkp.get(match)
                        if new_id:
                            extensions = extensions.replace(match, new_id)
                    r[10] = extensions
                with_from = r[6]
                if with_from:
                    # Match and replace any "UniProtKB:nnnnn" value in with_from string with gpi_db_xref_lkp.get("UniProtKB:nnnnn")
                    # Get all regex matches for "UniProtKB:\w+" in with_from string
                    regex_matches = re.findall(r"UniProtKB:\w+", with_from)
                    for match in regex_matches:
                        # Replace each match with the value from gpi_db_xref_lkp
                        new_id = gpi_db_xref_lkp.get(match)
                        if new_id:
                            with_from = with_from.replace(match, new_id)
                    r[6] = with_from
            print("\t".join(r))