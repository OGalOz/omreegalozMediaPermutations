





#Note: This function doesn't work because of the 'staging_file_subdir_path' parameter which assumes the file is in the staging area.
def upload_file(filename, ws_name, kbupload_object):

        upload_params = dict()
        upload_params['staging_file_subdir_path'] = filename
        upload_params["media_name"] = "variable_media_total"
        upload_params['workspace_name'] =  ws_name

        kb_upload_object.import_tsv_as_media_from_staging(upload_params)


