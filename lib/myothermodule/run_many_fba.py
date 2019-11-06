#This file is the entry point for myothermodule 


from myothermodule.generate_media import generate_compound_permutations
import logging

#The compounds file must be a TSV media item in the previous form.
#There is the base media, on top of which the variable media is added.
def run_multiple_media_fba(fba_tools_object, input_dict, var_media_file_name, base_media_name, run_type):
    logging.basicConfig(level=logging.DEBUG)
    logging.info("BASE_MEDIA NAME:")
    logging.info(base_media_name)

    # From the variable media, we create a list of the different permutations in tuple form.
    prepared_tuple_list_d3 = generate_compound_permutations(var_media_file_name, run_type)
    
    # First, we Generate a Metabolic Model from the Genome and gapfill it on the base media:
    # parameters for build metabolic model:
    FBA_Results_Refs = []

    media_to_compounds_str = ''
    main_workspace = input_dict["workspace"]
    for i in range(len(prepared_tuple_list_d3)):
        compounds_dicts_d2 = prepared_tuple_list_d3[i]
        logging.info("Compound Tuples:")
        logging.info(compounds_dicts_d2)
        

        #Prepare EDIT MEDIA params:
        edit_media_params = create_sample_dict_for_edit_media()
        edit_media_params["workspace"] = main_workspace
        edit_media_params["media_workspace"] = main_workspace
        edit_media_params["media_id"] = base_media_name 
        edit_media_params["compounds_to_add"] = compounds_dicts_d2
        new_media_id = base_media_name + 'output' + str(i+1)
        edit_media_params["media_output_id"] = new_media_id
        media_to_compounds_str += compound_string_from_compounds_dicts_d2(new_media_id, compounds_dicts_d2)
        #RUN EDIT MEDIA:
        edit_media_result_dict = fba_tools_object.edit_media(edit_media_params)
        logging.info(edit_media_result_dict)
        new_media_ref = edit_media_result_dict["new_media_ref"]

        """
        #BUILD METABOLIC MODEL FROM GENOME WITH NEW MEDIA:
        met_model_dict = create_sample_dict_for_build_mm()
        met_model["genome_id"] = '' #genome_id
        met_model["genome_workspace"] = input_dict["workspace"]
        met_model["media_id"] = edit_media_params["media_output_id"]
        met_model["media_workspace"] = input_dict["workspace"]
        met_model["fbamodel_output_id"] = fba_model_basic + 'gf_on_' + edit_media_params["media_output_id"]
        met_model["workspace"] = input_dict["workspace"]
        met_model["template_id"] = '?' # template id
        met_model["template_workspace"] = input_dict["workspace"]
        """

        #GAPFILL METABOLIC MODEL USING NEW MEDIA
        gapfill_params = create_dict_for_gapfill(input_dict, i, new_media_ref, new_media_id)

        gapfill_output = fba_tools_object.gapfill_metabolic_model(gapfill_params)
        
        logging.debug(gapfill_output)
        
        #Run FBA on the new media
        fba_input_dict = create_dict_for_run_fba(gapfill_params["fbamodel_output_id"], main_workspace)

        logging.debug(fba_input_dict)
        fba_input_dict["fba_output_id"] = gapfill_params["fbamodel_output_id"] + "_on_" + edit_media_params["media_output_id"]
        fba_input_dict["media_id"] = new_media_ref
        fba_input_dict["media_workspace"] = main_workspace
        logging.debug(fba_input_dict)

        
        results_from_fba = fba_tools_object.run_flux_balance_analysis(fba_input_dict)
        new_ref_id = results_from_fba['new_fba_ref']
        FBA_Results_Refs.append([new_ref_id, fba_input_dict["fba_output_id"], results_from_fba])
        

    return [FBA_Results_Refs, media_to_compounds_str]

def compound_string_from_compounds_dicts_d2(media_name, compounds_dicts_d2):
    compound_string = ''
    for compound_dict in compounds_dicts_d2:
        logging.debug(compound_dict)
        #unsure what compound is
        compound_string += compound_dict['add_id'] + ', '
    return media_name + ": " + compound_string[:-2] + '. \n'

# GF means that all these parameters matter for the gapfilling function.
# Parameters listed: https://github.com/kbaseapps/fba_tools/blob/master/fba_tools.spec
def create_dict_for_gapfill(input_dict, i, new_media_ref, new_media_id):
    ws_main = input_dict["workspace"]
    sd = dict()

    sd["fbamodel_id"] = input_dict["fbamodel_id"]
    sd["fbamodel_workspace"] = ws_main
    sd["media_id"] = new_media_id
    sd["media_workspace"] = ws_main
    sd["target_reaction"] = "bio1" #TARGET REACTION VARIABLE?
    sd["fbamodel_output_id"] = input_dict["fbamodel_id"] + "GF" + str(i)        
    sd["workspace"] = ws_main
    #sd["thermodynamic_constraints"] = False #bool - GF
    #sd["comprehensive_gapfill"] = True #bool - GF
    #sd["soure_fbamodel_id"] =  #str - GF
    #sd["source_fbamodel_workspace"] = #str - GF


    sd["custom_bound_list"] = [] #GF
    sd["media_supplement_list"] = [] #GF
    sd["feature_ko_list"] = []
    sd["reaction_ko_list"] = []

    #sd["expseries_id"] = None #GF
    #sd["expseries_workspace"] = #workspace_name
    #sd["expression_condition"] = [] #GF (string?)
    #sd["exp_threshold_percentile"] = 0.5
    #sd["exp_threshold_margin"] = 0.1
    #sd["activation_coefficient"] = 0.5
    #sd["omega"] =  #float - GF
    #sd["objective_Fraction"] = #float - GF
    sd["minimum_target_flux"] = 0.1 #float -GF
    #sd["number_of_solutions"] = #int - GF
    return sd

def create_sample_dict_for_edit_media():
    sd = dict()
    sd['compounds_to_change'] = []
    sd["compounds_to_remove"] = []
    sd["pH_data"] = None
    sd["temperature"] = None
    sd["type"] = "unknown"
    sd["isDefined"] = 1
    return sd


def create_dict_for_run_fba(gf_fba_model_id, ws_main):
    sd = dict()
    sd["fbamodel_id"] = gf_fba_model_id
    sd["fbamodel_workspace"] = ws_main
    #sd["media_id"] = media_id - This is done elsewhere
    #sd["media_workspace"] = ws_main - Done elsewhere
    sd["target_reaction"] = "bio1"
    #sd["fba_output_id"] = fba_output_id - this is done elsewhere
    sd["workspace"] = ws_main
    #sd["thermodynamic_constraints"]=
    sd["fva"] = 1 #needed
    sd["simulate_ko"] = 0 #needed
    #sd["find_min_media"] = 0 #Bool
    #sd["all_reversible"] = #Bool
    sd["feature_ko_list"] = [] #needed
    sd["reaction_ko_list"] = [] #needed
    sd["custom_bound_list"] = [] #needed
    sd["media_supplement_list"] = [] #needed
    sd["expseries_id"] = None #needed
    #sd["expseries_workspace"] = None
    sd["expression_condition"] = [] #needed
    sd["exp_threshold_percentile"] = 0.5 #needed
    sd["exp_threshold_margin"] = 0.1 #needed
    sd["activation_coefficient"] = 0.5 #needed
    #sd["omega"] = 
    #sd["objective_fraction"] = 
    sd["max_c_uptake"] = None
    sd["max_n_uptake"] = None
    sd["max_p_uptake"] = None
    sd["max_s_uptake"] = None
    sd["max_o_uptake"] = None #needed
    #sd["default_max_uptake"] = 
    sd["minimize_flux"] = 1 #needed
    #sd["notes"] = #String
    #sd["massbalance"] = #String
    return sd













def create_sample_dict_for_build_mm(genome_ws, base_media_ws, ws_main, template_ws, expseries_ws):
    sd = dict()

    #sd["template_id"] = #template_id
    if ws_main != '':
        sd["workspace"] = ws_main
    if genome_ws != '':
        sd["genome_workspace"] = genome_ws
    if base_media_ws != '':
        sd['media_workspace'] = base_media_ws
    if template_ws != '':
        sd["template_workspace"] = template_ws
    if expseries_ws != '':
        sd["expseries_workspace"] = expseries_ws
                
    #sd["coremodel"] = #bool
    sd["gapfill_model"] = True #bool
    sd["thermodynamic_constraints"] = False #bool
    sd["comprehensive_gapfill"] = True #bool - what does this mean
    sd["custom_bound_list"] = []
    sd["media_supplement_list"] = []
    sd["expseries_id"] = None
    #sd["expseries_workspace"] = #workspace_name
    sd["expression_condition"] = []
    sd["exp_threshold_percentile"] = 0.5
    sd["exp_threshold_margin"] = 0.1
    sd["activation_coefficient"] = 0.5
    #sd["omega"] =  #float
    #sd["objective_Fraction"] = #float
    #sd["minimum_target_flux"] = #float
    #sd["number_of_solutions"] = #int
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



