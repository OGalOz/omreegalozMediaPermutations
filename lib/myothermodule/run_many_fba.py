#This file is the central piece for myothermodule 


from myothermodule.generate_media import generate_compound_permutations


#The compounds file must be a TSV media item in the previous form.
def run_multiple_media_fba(fba_tools_object, input_dict, media_file_name):


    compounds_ids_d2 = generate_compound_permutations(media_file_name)
    FBA_Results_Refs = []
    for i in range(len(compounds_ids_d2)):
        compounds_ids_d1 = compounds_ids_d2[i]
        #Run FBA on the new compounds
        new_input_dict = input_dict.copy()
        new_input_dict["fba_output_id"] = new_input_dict["fba_output_id"] + str(i+1)
        new_input_dict["media_supplement_list"] = compounds_ids_d1
        results_from_fba = fba_tools_object.run_flux_balance_analysis(new_input_dict)
        new_ref_id = results_from_fba['new_fba_ref']
        FBA_Results_Refs.append([new_ref_id, new_input_dict["fba_output_id"], results_from_fba])

    return FBA_Results_Refs





def create_sample_dict_for_run_fba():
    sd = dict()
    sd["fva"] = 1
    sd["simulate_ko"] = 0 
    sd["feature_ko_list"] = []
    sd["target_reaction"] = "bio1"
    sd["reaction_ko_list"] = []
    sd["custom_bound_list"] = []
    sd["media_supplement_list"] = []
    sd["expseries_id"] = None
    sd["expression_condition"] = []
    sd["exp_threshold_percentile"] = 0.5
    sd["exp_threshold_margin"] = 0.1
    sd["activation_coefficient"] = 0.5
    sd["max_c_uptake"] = None
    sd["max_n_uptake"] = None
    sd["max_p_uptake"] = None
    sd["max_s_uptake"] = None
    sd["max_o_uptake"] = None
    sd["minimize_flux"] = 1
    return sd


# Previously decided parameters: fbamodel_id, fbamodel_workspace, media_id, media_workspace, target_reaction, fba_output_id, workspace,
def test_run_fba(fba_tools_object, input_dict):

    sample_compounds_ids = ['cpd00221','cpd00013','cpd00009','cpd00001','cpd12857','cpd00007']
    params_dict = input_dict
    params_dict['media_supplement_list'] = sample_compounds_ids

    '''
    #parameters already completed: "fbamodel_id","media_id", "target_reaction", "fba_output_id"
    # "target_reaction", "fba_output_id", "workspace", "thermodynamic_constraints",
    # 
    #params_dict = dict()
    params_dict["fbamodel_id"] = input_dict["fbamodel_id"] #type fbamodel_id
    params_dict["fbamodel_workspace"] = input_dict["fbamodel_workspace"] #type workspace_name - optional
    params_dict["media_id"] = '' #type media_id
    #params_dict["media_workspace"] = '' #type workspace_name - optional
    params_dict["target_reaction"] = input_dict["target_reaction"] #type list of reaction_id
    params_dict["fba_output_id"] = 'Test_Output_FBA' #type fba_id
    params_dict["workspace"] = input_dict["workspace"] #workspace_name
    params_dict["thermodynamic_constraints"] = False #bool
    params_dict["fva"] = False #bool
    params_dict["minimize_flux"] = False #bool
    params_dict["simulate_ko"] = False #bool
    params_dict["find_min_media"] = False #bool
    params_dict["all_reversible"] = False #bool
    params_dict["feature_ko_list"] = [''] #list_o_feature_ko
    params_dict["reaction_ko_list"] = [''] #list_o_rxn_ids
    params_dict["custom_bound_list"] = [''] #list_o_strings
    params_dict["media_supplement_list"] = sample_compound_ids #list_o_cmpnd_ids_strings
    params_dict["expseries_id"] = '' #type expseries_id
    params_dict["expression_condition"] = '' #string
    params_dict["exp_threshold_percentile"] = #float
    params_dict["exp_threshold_margin"] = #float
    params_dict["activation_coefficient"] = #float
    params_dict["omega"] = #float
    params_dict["objective_fraction"] = #float
    params_dict["max_c_uptake"] = #float
    params_dict["max_n_uptake"] = #float
    params_dict["max_p_uptake"] = #float
    params_dict["max_s_uptake"] = #float
    params_dict["max_o_uptake"] = #float
    params_dict["default_max_uptake"] = #float
    params_dict["notes"] = #string
    params_dict["massbalance"] = #string
    '''

    fba_result = fba_tools_object.run_flux_balance_analysis(params_dict)

    '''
    Results Structure:
        typedef structure {
        ws_fba_id new_fba_ref;
        int objective;
        string report_name;
		ws_report_id report_ref;
    } RunFluxBalanceAnalysisResults;
    '''


    return fba_result



