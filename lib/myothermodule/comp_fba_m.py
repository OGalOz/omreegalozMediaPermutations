#!/bin/python3
import pandas as pd
from optparse import OptionParser
import sys
import numpy as np
import logging
import os

def compare_two_files(filename1, filename2, output_dir_name, rxns_dir):
    f1_fullpath = os.path.join(rxns_dir, filename1)
    f2_fullpath = os.path.join(rxns_dir, filename2)
    try:
      data1 = pd.read_csv(f1_fullpath,sep="\t");
      data2 = pd.read_csv(f2_fullpath,sep="\t");
    except IOError:
        logging.critical("files not found")
        sys.exit(2)
    data = data1.append(data2)
    grouped = data.groupby(['id'])
    # for the reactions that appear in both FBA solutions
    flux1 = []
    flux2 = []
    comi = []
    com_name = []
    diffi = []
    for i in grouped:
        content = i[1]
        fluxes = content['flux'].values
        if( len(fluxes) == 2 ):
            comi.append(i[0])
            com_name.append(content['name'].values[0])
            flux1.append(fluxes[0])
            flux2.append(fluxes[1])
        elif ( len(fluxes) == 1):
            diffi.append(i[0])
        else:
            logging.critical("Could not recognize length of flux")
    logging.info(np.corrcoef(flux1,flux2))
    df = pd.DataFrame(list(zip(comi,com_name,flux1,flux2,np.abs(np.subtract(flux1,flux2)))),columns=['id','name','flux1','flux2','diff'])
    df = df.sort_values(by=['diff'],ascending=False)
    df.to_csv(os.path.join(output_dir_name,filename1[:-4] + "VS" + filename2[:-4] + "COMPARED.csv"))
    logging.info(diffi)




# The original functions:
def main():
    parser = OptionParser()
    parser.add_option("-m","--file1",dest="filename1",help="FBA input file 1 in tsv format",metavar="FILE")
    parser.add_option("-n","--file2",dest="filename2",help="FBA input file 2 in tsv format",metavar="FILE")
    (options, args) = parser.parse_args()
    try:
      data1 = pd.read_csv(options.filename1,sep="\t");
      data2 = pd.read_csv(options.filename2,sep="\t");
    except IOError:
        print("files not found")
        sys.exit(2)
    data = data1.append(data2)
    grouped = data.groupby(['id'])
    # for the reactions that appear in both FBA solutions
    flux1 = []
    flux2 = []
    comi = []
    com_name = []
    diffi = []
    for i in grouped:
        content = i[1]
        fluxes = content['flux'].values
        if( len(fluxes) == 2 ):
            comi.append(i[0])
            com_name.append(content['name'].values[0])
            flux1.append(fluxes[0])
            flux2.append(fluxes[1])
        elif ( len(fluxes) == 1):
            diffi.append(i[0])
        else:
            logging.critical("Could not recognize length of flux - comp_fba_m.py")
    print(np.corrcoef(flux1,flux2))
    df = pd.DataFrame(list(zip(comi,com_name,flux1,flux2,np.abs(np.subtract(flux1,flux2)))),columns=['id','name','flux1','flux2','diff'])
    df = df.sort_values(by=['diff'],ascending=False)
    df.to_csv('output.csv')
    print(diffi)

#if __name__ == "__main__":
#    main()
