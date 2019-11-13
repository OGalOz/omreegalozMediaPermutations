
#This file makes use of existing FBA TSVs and provides an analysis


from myothermodule.comp_fba_m import compare_two_files
#from comp_fba_m import compare_two_files
import os


# The input to this function is a path to a directory which contains the various reaction tsv files outputted from FBA.
def run_analysis_on_dir(rxns_dir, scratch_dir):

    # We create a folder to store outputs in the scratch directory
    analysis_outputs_dir = os.path.join(scratch_dir,"Comparisons")
    if os.path.exists(analysis_outputs_dir):
        for filepath in os.listdir(analysis_outputs_dir):
            os.unlink(os.path.join(analysis_outputs_dir,filepath))
    else:
        os.mkdir(analysis_outputs_dir)
    
    # We get a list of all files in the rxns dir
    all_tsv_files = os.listdir(rxns_dir)

    if len(all_tsv_files) == 0:
        logging.critical("There are no reactions tsv files in the given directory, analysis cannot be performed.")
    else:
        for i in range(len(all_tsv_files)):
            for j in range(i+1, len(all_tsv_files)):
                #Compare_two_files writes a file to the analysis outputs directory
                compare_two_files(all_tsv_files[i],all_tsv_files[j],analysis_outputs_dir, rxns_dir)
    





