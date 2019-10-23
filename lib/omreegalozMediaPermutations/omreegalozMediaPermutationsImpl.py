# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
from biokbase.workspace.client import Workspace
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.fba_toolsClient import fba_tools
from installed_clients.kb_uploadmethodsClient import kb_uploadmethods
from myothermodule.run_many_fba import create_sample_dict_for_run_fba, run_multiple_media_fba, test_run_fba
from myothermodule.temporary import upload_file
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
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

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
        #report_info = report.create({'report': reportObj, 'workspace_name': params['workspace_name']})

        token = os.environ.get('KB_AUTH_TOKEN', None)

        #Getting metabolic model:
        if "metabolic_model_input_ref" in params:
            mm_upa = params['metabolic_model_input_ref']
        else:
            logging.critical("the FBA Model reference number is not in the params. Cannot continue.")
            raise Exception("Passed parameters failed.")

        #Getting Base Media:
        if "base_media_ref" in params:
            media_upa = params["base_media_ref"]
        else:
            logging.critical("the base media reference number is not in the params. Cannot continue.")
            raise Exception("Passed parameters failed.")
        if "variable_media_ref" in params:
            variable_media_ref = params["variable_media_ref"]
        else:
            logging.critical("the variable media reference number is not in the params. Cannot continue.")
            raise Exception("Passed parameters failed.")

        ws = Workspace(self.ws_url, token=token)


        #Downloading and naming variable media:
        # DOWNLOAD TSV FILE OF MEDIA AND SAVE IT TO TEMP WORK DIR
        variable_media_data = ws.get_objects2({'objects':[{'ref': variable_media_ref}]})
        var_media_tsv_file_location = os.path.join(self.shared_folder, "var_med_data.txt")
        f = open(var_media_tsv_file_location)
        f.write(str(variable_media_data))
        f.close()

        

        #ws = Workspace(self.ws_url, token=token)
        mm_obj_info = ws.get_object_info3({'objects':[{'ref': mm_upa}]})
        med_obj_info = ws.get_object_info3({'objects':[{'ref': media_upa}]})
        output_dir_name = 'Multiple_FBA_Analysis'
        output_dir_path = os.path.join(self.shared_folder, output_dir_name)
        os.mkdir(output_dir_path)


        

        if "infos" in mm_obj_info:
            mm_object_name = mm_obj_info["infos"][0][1]
            mm_object_type = mm_obj_info["infos"][0][2]
            ws_name = mm_obj_info["infos"][0][7]
        else:
            logging.critical("For the metabolic model, the workspace function get_object_info3 did not work as expected.")
            raise Exception("Get Object Info failed - problem with workspace or token?")
        if "infos" in med_obj_info:
            med_object_name = med_obj_info["infos"][0][1]
            med_object_type = med_obj_info["infos"][0][2]
        else:
            logging.critical("For the media, the workspace function get_object_info_3 did not work as expected.")
            raise Exception("Get Object Info failed - problem with workspace or token?")

        if mm_object_type[:17] == 'KBaseFBA.FBAModel':
            logging.info('Succesfully recognized type as FBA Model')
            fba_t = fba_tools(self.callback_url)
            run_dict = create_sample_dict_for_run_fba()
            #CHECK THE FOLLOWING:
            logging.debug('obj name:' + mm_object_name)
            run_dict["fbamodel_id"] = mm_object_name
            logging.debug('ws_name' + ws_name)
            run_dict["workspace"] = ws_name
            run_dict["fba_output_id"] = mm_object_name + 'Output_from_app'
            logging.debug("media object name: " + med_object_name)
            run_dict["media_id"] = med_object_name


            #This is where FBA is called:
            results_refs_and_names = run_multiple_media_fba(fba_t, run_dict, var_media_tsv_file_location)

            for fba_result in results_refs_and_names:
                ref_num = fba_result[0]
                fba_name = fba_result[1]
                fba_result_dict = fba_result[2]
                logging.debug(str(fba_result_dict))
                new_obj = ws.get_objects2({'objects':[{'ref': ref_num}]})
                result_filename = fba_name + '.txt'
                f = open(os.path.join(output_dir_path, result_filename),"w")
                f.write(str(new_obj))
                f.close()
            
        else:
            logging.critical("Wrong object type!")
            raise Exception("Could not recognize type of object!")

   
        #Create various forms of media:
        



        #Download FBA Model of Organism

        output = {
            'report_name': 'Temporary',
            'report_ref': 'Unknown',
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
