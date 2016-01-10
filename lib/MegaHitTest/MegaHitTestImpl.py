#BEGIN_HEADER
import os
import sys
import uuid

from biokbase.workspace.client import Workspace as workspaceService
#END_HEADER


class MegaHitTest:
    '''
    Module Name:
    MegaHitTest

    Module Description:
    A KBase module: MegaHitTest
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    #BEGIN_CLASS_HEADER
    workspaceURL = None
    MEGAHIT = '/kb/module/megahit/megahit'

    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        #END_CONSTRUCTOR
        pass

    def run_megahit(self, ctx, params):
        # ctx is the context object
        # return variables are: output
        #BEGIN run_megahit


        ws = workspaceService(self.workspaceURL, token=ctx['token'])
        objects = ws.get_objects([{'ref': params['workspace_name']+'/'+params['read_library_name']}])

        data = objects[0]['data']
        info = objects[0]['info']
        type_name = info[2].split('.')[1].split('-')[0]

        report = 'report will go here'
        report += 'input data type: '+type_name
        reportObj = {
            # 'objects_created':[{'ref':params['workspace_name']+'/'+params['output_contigset_name'], 'description':'Assembled contigs'}],
            'objects_created':[],
            'text_message':report
        }

        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects']=[params['workspace_name']+'/'+params['read_library_name']]

        reportName = 'megahit_report_'+str(hex(uuid.getnode()))
        report_obj_info = ws.save_objects({
                'id':info[6],
                'objects':[
                    {
                        'type':'KBaseReport.Report',
                        'data':reportObj,
                        'name':reportName,
                        'meta':{},
                        'hidden':1,
                        'provenance':provenance
                    }
                ]
            })[0]

        output = { 'report_name': reportName, 'report_ref': str(report_obj_info[6]) + '/' + str(report_obj_info[0]) + '/' + str(report_obj_info[4]) }

        #END run_megahit

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_megahit return value ' +
                             'output is not type dict as required.')


        # return the results
        return [output]
