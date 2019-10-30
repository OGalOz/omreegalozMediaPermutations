#Auxiliary functions for Media Permutations
import logging


def check_params(params):
        #Getting metabolic model:
        if "metabolic_model_ref" in params:
            metabolic_model_ref = params['metabolic_model_ref']
        else:
            logging.critical("the Genome reference number is not in the params. Cannot continue.")
            raise Exception("Passed parameters failed.")

        #Getting Base Media:
        if "base_media_ref" in params:
            base_media_ref = params["base_media_ref"]
        else:
            logging.critical("the base media reference number is not in the params. Cannot continue.")
            raise Exception("Passed parameters failed.")
        if "variable_media_ref" in params:
            variable_media_upa = params["variable_media_ref"]
        else:
            logging.critical("the variable media reference number is not in the params. Cannot continue.")
            raise Exception("Passed parameters failed.")
        return metabolic_model_ref, base_media_ref, variable_media_upa




def optional_stored():
        #Temporary upload of a media file:
        mm_obj_info = ws.get_object_info3({'objects':[{'ref': mm_upa}]})
        ws_name = mm_obj_info["infos"][0][7]
        media_creation_params = {"workspace_name" : ws_name} 
        media_creation_params['media_file'] = '/kb/module/data/tmpmedia/media4.tsv'
        media_creation_params['media_name'] = "TSTM"
        fba_t.tsv_file_to_media(media_creation_params)

