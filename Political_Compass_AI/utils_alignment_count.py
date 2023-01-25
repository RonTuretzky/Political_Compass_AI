# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/Db_Utils/count_alignments.ipynb.

# %% auto 0
__all__ = ['split_string', 'alignment_count']

# %% ../nbs/Db_Utils/count_alignments.ipynb 0
from fastcore.script import call_parse
from ast import literal_eval as make_tuple
def split_string(string):
    # Removing the parentheses and splitting the string by comma
    parts = string[1:-1].split(",")
    # Removing the whitespace and quotes from the parts
    parts = [part.strip().strip("'") for part in parts]
    return parts[0], parts[1]
@call_parse
def alignment_count(
            path:str # dn path to run alignment distribution

):
    db = open(path, "r",encoding='latin1')
    #TODO Add all alignments
    alignments = {
        "Libertarian Left": 0,
        "Libertarian Right": 0,
        "Authoritarian Left": 0,
        "Authoritarian Right": 0,
    }
    for line in db:
        opinion, text = split_string(line)
        alignments[opinion] += 1
    print(alignments)

