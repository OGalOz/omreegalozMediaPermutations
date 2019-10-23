

import csv
import logging
#from jinja2 import Environment, PackageLoader, select_autoescape

def tsv_to_d2_list(file_name):
        d2_list = []
        with open(file_name) as list_values:
                list_reader = csv.reader(list_values, delimiter='\t')
                for list_object in list_reader:
                        d2_list.append(list_object)
        return d2_list


def csv_to_d2_list(file_name):
        d2_list = []
        with open(file_name) as list_values:
                list_reader = csv.reader(list_values, delimiter=',')
                for list_object in list_reader:
                        d2_list.append(list_object)
        return d2_list


def tsv_to_csv(file_name, output_file_name):
    with open(file_name,'r') as tsvin, open(output_file_name, 'w') as csvout:
        tsvin = csv.reader(tsvin, delimiter='\t')
        csvout = csv.writer(csvout, delimiter=',')

        for row in tsvin:
            csvout.writerow(row)



def csv_to_tsv(file_name, output_file_name):
    with open(file_name,'r') as csvin, open(output_file_name, 'w') as tsvout:
        csvin = csv.reader(csvin)
        tsvout = csv.writer(tsvout, delimiter='\t')

        for row in csvin:
            tsvout.writerow(row)




#This function takes a list of lists and prints it out to a file with a given name.
def print_d2_list_out_to_tsv_file(input_list, output_filename):
                with open(output_filename, 'w') as f:
                        for item in input_list:
                                my_string = ''
                                for part in item:
                                        my_string += str(part) + '\t'
                                f.write("%s\n" % my_string)

def print_d2_list_out_to_csv_file(input_list, output_filename):
                with open(output_filename, 'w') as f:
                        for item in input_list:
                                my_string = ''
                                for part in item:
                                        my_string += str(part) + ','
                                f.write("%s\n" % my_string)


#This function converts a d2_list (table) to an HTML table
def d2_list_to_html_table(list_d2):
    
    html_string = '<head><meta charset="UTF-8"><!-- Below are imports for the font and datatables--><link href="https://fonts.googleapis.com/css?family=Oxygen:400,700" rel="stylesheet"><link rel="stylesheet" href="https://cdn.datatables.net/v/bs4-4.1.1/jq-3.3.1/dt-1.10.18/b-1.5.4/b-colvis-1.5.4/b-html5-1.5.4/b-print-1.5.4/datatables.min.css"/><!----><style type="text/css">*{font-family: "Oxygen", Helvetica, sans-serif;}</style></head><body><div id="stats" class="tabcontent">'


    html_string += '<table id="stats_table" style="width:98%;" class="table table-striped table-bordered">'



    for row in list_d2:
        html_string += '<tr>'
        for item in row:
            html_string += '<td>' + str(item) + '</td>'
        html_string += '</tr>'

    html_string += '</table></div></body>'  

    return html_string


def d2_list_to_html_table_file(list_d2, output_filename):
    
    html_table = d2_list_to_html_table(list_d2)
    with open(output_filename, 'w') as f:
        f.write(html_table)

def string_to_html_file(html_string, output_filename):
        with open(output_filename, 'w') as f:
            f.write(html_string)



def check_if_tsv_or_csv(filename):
    if filename[-3:] == 'tsv':
        return 'tsv'
    elif filename[-3:] == 'csv':
        return 'csv'
    else:
        return 'Unknown'


# Following function used in main_functions
#For the following func, the input dictionary comes after getting the object using ws.get_objects2,
#    then taking "Y = obj['data'][0]['data']['data']", so you only have the contigs and related Features.
def get_TIGRFAM_IDs_from_KBaseGeneFamilies_DomainAnnotation_2(input_dict):

    #For each 'key' (keys are contigs) in the dictionary, you get a list (a) of lists (b).
    # list (a) contains all the features which are packaged into list (b)
    # list (b) represents one feature, indeces are 0 = feature name, 1 = feature start in contig
    # 2 = feature end in contig, 3 = feature direction in contig (1 positive, -1 negative) 
    # 4 = a dict with the TIGR ID as the key.

    #Initialize the TIGRFAM ID LIST TO RETURN
    TIGR_ID_List = []
 
    for k in input_dict.keys():
        list_of_features = input_dict[k]
        for feat in list_of_features:
            tfam_dict = feat[4]
            tfam_dict_keys_list = list(tfam_dict.keys())
            if len(tfam_dict_keys_list) == 1:
                TFAM_ID = tfam_dict_keys_list[0]
                TIGR_ID_List.append(TFAM_ID)
            elif len(tfam_dict_keys_list) > 1:
                logging.info('multiple TIGRFAM IDs')
                
    return TIGR_ID_List
    





    


