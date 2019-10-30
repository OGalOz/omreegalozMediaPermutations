# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from omreegalozMediaPermutations.omreegalozMediaPermutationsImpl import omreegalozMediaPermutations
from omreegalozMediaPermutations.omreegalozMediaPermutationsServer import MethodContext
from omreegalozMediaPermutations.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class omreegalozMediaPermutationsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('omreegalozMediaPermutations'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'omreegalozMediaPermutations',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = omreegalozMediaPermutations(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    '''
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        ret = self.serviceImpl.run_omreegalozMediaPermutations(self.ctx, {'workspace_name': self.wsName,
                                                             'parameter_1': 'Hello World!'})
    '''
    def test_Ecoli_each(self):

        genome_ref = "" #E_Coli Genome Object

        mm_ref = "33008/30/1" #E_Coli_Metabolic_Model_NMS_No_Glucose

        base_media_ref = "33008/4/1" #MinimalGrowthNMS_NoGlucose

        variable_media_ref = "33008/3/1"     #This is the list of compounds that will be interchanged to see how it affects FBA

        
        run_type = "each" #Either 'all' or 'each'

        ret = self.serviceImpl.run_omreegalozMediaPermutations(self.ctx, {
            'workspace_name': self.wsName,
            'metabolic_model_ref': mm_ref,
            'genome_ref': genome_ref,
            'base_media_ref': base_media_ref,
            'variable_media_ref': variable_media_ref,
            'run_type': run_type

        })
    """
    def test_Ecoli_all(self):

        genome_ref = "" #E_Coli Genome Object

        mm_ref = "33008/30/1" #E_Coli_Metabolic_Model_NMS_No_Glucose

        base_media_ref = "33008/4/1" #MinimalGrowthNMS_NoGlucose

        variable_media_ref = "33008/3/1"     #This is the list of compounds that will be interchanged to see how it affects FBA

        
        run_type = "all" #Either 'all' or 'each'

        ret = self.serviceImpl.run_omreegalozMediaPermutations(self.ctx, {
            'workspace_name': self.wsName,
            'metabolic_model_ref': mm_ref,
            'genome_ref': genome_ref,
            'base_media_ref': base_media_ref,
            'variable_media_ref': variable_media_ref,
            'run_type' = run_type

        })

    """
    """
    def test_SHW_Metabolic_Model(self):
        
        #This is an example FBAModel called SHW_Metabolic_Model
        ref = "32176/11/1"

        ret = self.serviceImpl.run_omreegalozpathway_completeness(self.ctx, {
            'workspace_name': self.wsName,
            'metabolic_model_input_ref': ref,
        })
    """
