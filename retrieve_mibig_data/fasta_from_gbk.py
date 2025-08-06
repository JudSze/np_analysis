from os import listdir
from os.path import isfile, join

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

# Define path to MIBiG folder with gbk files
path = "/home/szenei/np_analysis/retrieve_mibig_data/mibig_gbk_4.0"

# Get the gbk file names from the defined MIBiG folder
gbk_files = [file for file in listdir(path) if isfile(join(path, file))]

# Create a fasta file with the protein sequences for each gbk file
for file in gbk_files:
    bgc_accession = file.strip('.gbk')
    file_path = f"{path}/{file}"
    output_handle = open(f"{path}/{bgc_accession}.fasta", "w")
    translations = []
    try:
        for record in SeqIO.parse(file_path, "genbank"):
            for seq_feature in record.features:
                if "translation" in seq_feature.qualifiers.keys():
                    # SeqIO stores the translations in list, which needs to be unwrapped
                    translations.append(*seq_feature.qualifiers["translation"])
    except Exception:
        print(f"File not found: {bgc_accession}")

    numerator = 0
    for sequence in translations:
        try:
            seqio_record = SeqRecord(Seq(sequence), id = f"{bgc_accession}_{numerator}")
            numerator += 1
            SeqIO.write(seqio_record, output_handle, "fasta")
        except Exception:
            print(file, "Error in the sequence")
    output_handle.close()
