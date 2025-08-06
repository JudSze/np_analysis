import json

from os import listdir
from os.path import isfile, join

import lwreg
import sqlite3

from rdkit import Chem

# Paths and files
mibig_json_path = "/home/szenei/np_analysis/retrieve_mibig_data/mibig_json_4.0"
mibig_json_files = [file for file in listdir(mibig_json_path) if isfile(join(mibig_json_path, file))]

# Init lwreg-db
# DO NOT RUN IT, RUNNING IT RESETS THE WHOLE DB
# lwreg_cofig_handle = open(lwreg_config_path, "r")
# lwreg_config = json.load(lwreg_cofig_handle)
# lwreg.utils.initdb(lwreg_config)

lwreg_config_path = "/home/szenei/np_analysis/retrieve_mibig_data/lwreg_db_config.json"

# DB manipulation
connection = sqlite3.connect("/home/szenei/np_analysis/mibig_structures")
cursor = connection.cursor()

try:
    cursor.execute(f"ALTER TABLE orig_data ADD COLUMN BGC TEXT")
except Warning:
    print("Column already exists")


# Go into MIBiG json data
for file in mibig_json_files:
    with open(f"{mibig_json_path}/{file}", "r") as jsn:
        entry = json.load(jsn)
        accession = accession

        structures = []
        id = 1
        # Get SMILES from the MIBiG entries
        for compound in entry["compounds"]:
            try:
                # Convert molecules into RDKit representations
                molecule = Chem.MolFromSmiles(compound)
                # Register moleculer in lwreg
                lwreg.utils.register(lwreg_config_path, mol = molecule, smiles=compound)
                cursor.execute(f'UPDATE orig_data SET BGC={accession} WHERE molregno={id}')
                id += 1
            except KeyError:
                print("no structure available")
