# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import shutil
from biokbase.workspace.client import Workspace
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.fba_toolsClient import fba_tools
from installed_clients.kb_uploadmethodsClient import kb_uploadmethods
#from installed_clients.DataFileUtilClient import DataFileUtil
from myothermodule.run_many_fba import run_multiple_media_fba, test_run_fba, create_sample_dict_for_build_mm
from myothermodule.aux_functions import check_params
from myothermodule.temporary import upload_file
from myothermodule.analyze_many_fba import run_analysis_on_dir

#from random import randint
#END_HEADER


class omreegalozMediaPermutations:
    '''
    Module Name:
    omreegalozMediaPermutations

    Module Description:
    A KBase module: omreegalozMediaPermutations
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.2"
    GIT_URL = "https://github.com/OGalOz/omreegalozMediaPermutations.git"
    GIT_COMMIT_HASH = "a2e3f761df5f28c9461894be36a04818e973a463"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.ws_url = config['workspace-url']
        #END_CONSTRUCTOR
        pass


    def run_omreegalozMediaPermutations(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_omreegalozMediaPermutations
        report = KBaseReport(self.callback_url)

        create_ext_report_params = dict()
        create_ext_report_params["workspace_name"] = params['workspace_name']
        


        token = os.environ.get('KB_AUTH_TOKEN', None)

        ws = Workspace(self.ws_url, token=token)

        fba_t = fba_tools(self.callback_url)

        #Check parameters here: Input should be a genome object instead of metabolic model
        metabolic_model_ref, base_media_ref, variable_media_ref, run_type, output_name = check_params(params)
        logging.debug("RUN TYPE: " + run_type)

                

        #Downloading and naming variable media:
        # DOWNLOAD TSV FILE OF MEDIA AND SAVE IT TO TEMP WORK DIR
        variable_media_obj = fba_t.export_media_as_tsv_file({'input_ref': variable_media_ref})
        var_med_info = ws.get_object_info3({'objects':[{'ref': variable_media_ref}]})

        if "infos" in var_med_info:
            #The way the variable media file is stored is in this location in the scratch directory:
            var_med_filename = os.path.join(var_med_info['infos'][0][1], var_med_info['infos'][0][1] + '.tsv')
            var_media_tsv_file_location = os.path.join(self.shared_folder, var_med_filename)

            #Main workspace is defined by location of the variable media item.
            ws_main = var_med_info["infos"][0][7]
            logging.debug(var_med_filename)
            logging.debug(variable_media_obj)
        else:
            raise Exception("The variable media object info was not retrieved correctly- try a different Media Object.")
        
        # Getting information about other objects in use:
        metabolic_model_info = ws.get_object_info3({'objects':[{'ref': metabolic_model_ref}]})
        base_med_obj_info = ws.get_object_info3({'objects':[{'ref': base_media_ref}]})


        #Making output information:
        output_dir_name = 'Multiple_FBA_Analysis'
        output_dir_path = os.path.join(self.shared_folder, output_dir_name)
        os.mkdir(output_dir_path)

        if "infos" in metabolic_model_info:
            metabolic_model_object_name = metabolic_model_info["infos"][0][1]
            metabolic_model_object_type = metabolic_model_info["infos"][0][2]
            metabolic_model_ws = metabolic_model_info["infos"][0][7]
        else:
            logging.critical("For the metabolic model, the workspace function get_object_info3 did not work as expected.")
            raise Exception("Get Object Info failed - problem with workspace or token?")
        if "infos" in base_med_obj_info:
            base_med_object_name = base_med_obj_info["infos"][0][1]
            base_med_object_type = base_med_obj_info["infos"][0][2]
            base_media_ws = base_med_obj_info["infos"][0][7]
        else:
            logging.critical("For the media, the workspace function get_object_info_3 did not work as expected.")
            raise Exception("Get Object Info failed - problem with workspace or token?")

        #CHECK IF FBA MODEL OBJECT:
        if metabolic_model_object_type[:17] == "KBaseFBA.FBAModel":
            logging.info('Succesfully recognized type as FBA Model')

            run_dict = dict() 
            run_dict["fbamodel_id"] = metabolic_model_object_name
            run_dict["fbamodel_workspace"] = ws_main
            run_dict["workspace"] = ws_main
            run_dict["fba_output_id"] = "FBA_Output_Test"
            
            #This is where FBA is called:
            RESULTS = run_multiple_media_fba(fba_t, run_dict, var_media_tsv_file_location, base_med_object_name, run_type, base_media_ref)
            results_refs_and_names = RESULTS[0]
            media_to_compounds_str = RESULTS[1]
            fba_refs_list = []

            #Make a directory to store the reactions tsv files
            all_rxn_tsvs_dir = os.path.join(self.shared_folder,"FBA_TSVs") 
            os.mkdir(all_rxn_tsvs_dir)
            for fba_result in results_refs_and_names:
                ref_num = fba_result[0]
                fba_refs_list.append(ref_num)
                #We download the model as a tsv list- it is downloaded into a folder of its name
                fba_t.export_model_as_tsv_file({"input_ref": ref_num})
                fba_tsv_name = fba_result[1] + "-reactions.tsv"
                reactions_tsv_file = os.path.join(self.shared_folder,os.path.join(fba_result[1],fba_tsv_name))
                # We move the downloaded file to our directory called FBA_TSVs
                shutil.move(reactions_tsv_file,os.path.join(all_rxn_tsvs_dir,fba_tsv_name))
            
            #Analyze the reactions tsvs:
            run_analysis_on_dir(all_rxn_tsvs_dir, self.shared_folder)
            comparisons_folder = os.path.join(self.shared_folder, "Comparisons")
            

               
           
            #Here, given the fba ids, we download the TSVs
            #The fba models will be downloaded into their names:


            #new_obj = ws.get_objects2({'objects':[{'ref': ref_num}]})
            #result_filename = fba_name + '.txt'
            #f = open(os.path.join(output_dir_path, result_filename),"w")
            #f.write(str(new_obj))
            #f.close()
            

            #HERE WE RUN COMPARE FBA:
            """
            comp_fba_params = {"fba_id_list": fba_ids_list, "fbacomparison_output_id": output_name}
            comp_fba_params['workspace'] = ws_main
            comp_fba_ref_dict = fba_t.compare_fba_solutions(comp_fba_params)
            logging.info("COMPARE FBA RESULTS:")
            logging.info(comp_fba_ref_dict)
            new_comp_fba_ref = comp_fba_ref_dict['new_fbacomparison_ref']
            #new_obj = ws.get_objects2({'objects':[{'ref': new_comp_fba_ref}]})
            #result_filename =  'Compared_FBA_Results.txt'
            #f = open(os.path.join(self.shared_folder, result_filename),"w")
            #f.write(str(new_obj))
            #f.close()
            create_ext_report_params['objects_created'] = [{'ref': new_comp_fba_ref, 'description': "The fba comparison output"}]
            """


        #Did not recognize type as FBA Model:
        else:
            logging.critical("Wrong object type!")
            raise Exception("Could not recognize type of object!")
        create_ext_report_params['message'] = media_to_compounds_str
        file_links_list = []
        for f in os.listdir(comparisons_folder):
            file_links_list.append({"path": os.path.join(comparisons_folder,f), "name": f, "label": f})

        create_ext_report_params['file_links'] = file_links_list
        report_info = report.create_extended_report(create_ext_report_params)


        logging.debug(report_info)


        
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],

        }
        #END run_omreegalozMediaPermutations

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_omreegalozMediaPermutations return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
