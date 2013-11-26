__author__ = 'dan'

import requests
import json
import config


class WorkflowClient(object):

    def __init__(self):
        self.workflow_service_base_uri = config.instance().workflow_service_base_uri

    def execute_workflow(self, workflow, plan):
        response = requests.post('{0}/workflows'.format(self.workflow_service_base_uri),
                                 json.dumps({
                                     'radial': workflow,
                                     'fields': {'plan': plan}
                                 }))
        # TODO: handle error code
        return response.json()

    def validate_workflows(self, plan):
        prepare_plan_participant_workflow = '''define validate
    prepare_plan plan: $plan
        '''
        execution_response = self.execute_workflow(prepare_plan_participant_workflow, plan)
        response = {'state': 'pending'}
        while response['state'] is not 'terminated' or response['state'] is not 'failed':
            response = self.get_workflow_status(execution_response['id'])
        # This is good
        if response['state'] is 'terminated':
            return {'status': 'valid'}
        else:
            return {'status': 'invalid'}

    def get_workflow_status(self, workflow_id):
        response = requests.get('{0}/workflows/{1}'.format(self.workflow_service_base_uri, workflow_id))
        # TODO: handle error code
        return response.json()


def workflow_client():
    if config.instance().test_mode:
        from test.mocks import MockWorkflowClient
        return MockWorkflowClient()
    else:
        return WorkflowClient()
