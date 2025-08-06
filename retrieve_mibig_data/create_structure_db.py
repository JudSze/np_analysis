import json

from os import listdir
from os.path import isfile, join

import lwreg
import sqlite3

from rdkit import Chem

mibig_json_path = "/home/szenei/np_analysis/retrieve_mibig_data/mibig_json_4.0"
mibig_json_files = [file for file in listdir(mibig_json_path) if isfile(join(mibig_json_path, file))]

lwreg_config_path = "/home/szenei/np_analysis/retrieve_mibig_data/lwreg_db_config.json"

connection = sqlite3.connect("/home/szenei/np_analysis/mibig_structures")
cursor = connection.cursor()

cursor.execute(f"ALTER TABLE registry ADD COLUMN BGC TEXT")

# Get tables from database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
cursor.fetchall()   # regiostration_metadata, hashes, orig_data, molblocks

# Init lwreg-db
# DO NOT RUN IT, RUNNING IT RESETS THE WHOLE DB
# lwreg_cofig_handle = open(lwreg_config_path, "r")
# lwreg_config = json.load(lwreg_cofig_handle)
# lwreg.utils.initdb(lwreg_config)

# Go into MIBiG json data
for file in mibig_json_files:
    with open(f"{mibig_json_path}/{file}", "r") as jsn:
        entry = json.load(jsn)
        accession = accession

        structures = []
        numerator = 0
        # Get SMILES from the MIBiG entries
        for compound in entry["compounds"]:
            try:
                # Convert molecules into RDKit representations
                molecule = Chem.MolFromSmiles(compound)
                # Register moleculer in lwreg
                lwreg.utils.register(lwreg_config_path, mol = molecule, smiles=compound)
                cursor.execute(f"ALTER TABLE mibig_structures ADD COLUMN {accession}")
                numerator += 1
            except KeyError:
                print("no structure available")
