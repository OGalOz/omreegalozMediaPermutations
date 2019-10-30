





#Note: This function doesn't work because of the 'staging_file_subdir_path' parameter which assumes the file is in the staging area.
def upload_file(filename, ws_name, kbupload_object):

        upload_params = dict()
        upload_params['staging_file_subdir_path'] = filename
        upload_params["media_name"] = "variable_media_total"
        upload_params['workspace_name'] =  ws_name

        kb_upload_object.import_tsv_as_media_from_staging(upload_params)


def build_metabolic_model_from_genome():
            # Last two input items here are template workspace and expseries workspace:
            fba_input_dict = create_sample_dict_for_build_mm(metabolic_model_ws, base_media_ws, ws_main, '', '')
            #The following may need to be updated in order to not rename the fbamodel over and over:
            fbamodel_output_id = 'Test_Output_Name'
            fba_input_dict['fbamodel_output_id'] = fbamodel_output_id 
            fba_input_dict['genome_id'] = metabolic_model_object_name
            fba_input_dict['media_id'] = base_med_object_name

            #Here we generate an fba model from the build metabolic model function
            #new_fba_model_results = fba_t.build_metabolic_model(mm_input_dict) 
            #logging.debug(new_fba_model_results)
            #new_fbamodel_ref = new_fba_model_results["new_fbamodel_ref"]


