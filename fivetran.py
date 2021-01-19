
# -*- coding: utf-8 -*-
import json
import requests
import time

class FivetranApi(object):
    """
    Class for interacting with the Fivetran API
    * :py:meth:`list_jobs` - list all Jobs for the specified Account ID
    * :py:meth:`get_run` - Get information about a specified Run ID
    * :py:meth:`trigger_job_run` - Trigger a Run for a specified Job ID
    * :py:meth: `try_get_run` - Attempts to get information about a specific Run ID for up to max_tries
    * :py:meth: `run_job` - Triggers a run for a job using the job name
    """

    def __init__(self, api_token):
        self.api_token = api_token
        self.api_base = 'https://api.fivetran.com/v1/'

    def _get(self, url_suffix):
        url = self.api_base + url_suffix
        headers = {'Authorization': 'Token %s' % self.api_token}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise RuntimeError(response.content)

    def _post(self, url_suffix, data=None):
        url = self.api_base + url_suffix
        print('request url: ', url)
        print('showing request body: ', json.dumps(data))
        headers = {'Content-Type': 'application/json', 'Authorization': 'token %s' % self.api_token}

        response = requests.post(url, data=json.dumps(data), headers=headers)
        
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise RuntimeError(response.text)
    
    def get_groups(self):
        """Returns group information from the fivetran account"""
        return self._get(url_suffix='groups/').get('data')

    def get_group_connectors(self, group_id):
        """Returns information about connectors attached to a group"""
        return self._get(url_suffix=f'groups/{group_id}/connectors').get('data')
    
    def get_connector(self, connector_id):
        """Returns information about the connector under connector_id"""
        return self._get(url_suffix=f'connectors/{connector_id}').get('data')
    
    def force_connector_sync(self, request_body={}, **kwargs):
        """Triggers a run of the target connector under connector_id"""
        connector_id = kwargs['dag_run'].conf['connector_id']
        return self._post(url_suffix=f'connectors/{connector_id}/force', data=request_body).get('data')

    # def list_jobs(self):
    #     return self._get('/accounts/%s/jobs/' % self.account_id).get('data')

    # def get_run(self, run_id):
    #     return self._get('/accounts/%s/runs/%s/' % (self.account_id, run_id)).get('data')

    # def trigger_job_run(self, job_id, data=None):

    #     return self._post(url_suffix='/accounts/%s/jobs/%s/run/' % (self.account_id, job_id), data=data).get('data')

    # def try_get_run(self, run_id, max_tries=3):
    #     for i in range(max_tries):
    #         try:
    #             run = self.get_run(run_id)
    #             return run
    #         except RuntimeError as e:
    #             print("Encountered a runtime error while fetching status for {}".format(run_id))
    #             time.sleep(10)

    #     raise RuntimeError("Too many failures ({}) while querying for run status".format(run_id))

    # def create_job(self, data=None):
    #     return self._post(url_suffix='/accounts/%s/jobs/' % (self.account_id), data=data)

    # def update_job(self, job_id, data=None):
    #     return self._post(url_suffix='/accounts/%s/jobs/%s/' % (self.account_id, job_id), data=data)
