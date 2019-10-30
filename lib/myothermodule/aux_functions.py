#Auxiliary functions for Media Permutations
import logging


def check_params(params):
        #Getting metabolic model:
        if "metabolic_model_ref" in params:
            metabolic_model_ref = params['metabolic_model_ref']
        else:
            logging.critical("the metabolic model reference number is not in the params. Cannot continue.")
            raise Exception("Passed parameters failed. Error CP1")

        #Getting Base Media:
        if "base_media_ref" in params:
            base_media_ref = params["base_media_ref"]
        else:
            logging.critical("the base media reference number is not in the params. Cannot continue.")
            raise Exception("Passed parameters failed. Error CP2")
        if "variable_media_ref" in params:
            variable_media_upa = params["variable_media_ref"]
        else:
            logging.critical("the variable media reference number is not in the params. Cannot continue.")
            raise Exception("Passed parameters failed. Error CP3")
        if "run_type" in params:
            run_type = params["run_type"]
        else:
            logging.critical("run type not included in parameters")
            raise Exception("Passed parameters failed. Error CP4")
        return metabolic_model_ref, base_media_ref, variable_media_upa, run_type
        





def optional_stored():
        #Temporary upload of a media file:
        mm_obj_info = ws.get_object_info3({'objects':[{'ref': mm_upa}]})
        ws_name = mm_obj_info["infos"][0][7]
        media_creation_params = {"workspace_name" : ws_name} 
        media_creation_params['media_file'] = '/kb/module/data/tmpmedia/media4.tsv'
        media_creation_params['media_name'] = "TSTM"
        fba_t.tsv_file_to_media(media_creation_params)

