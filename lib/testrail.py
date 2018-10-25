#
# TestRail API binding for Python 2.x (API v2, available since 
# TestRail 3.0)
#
# Learn more:
#
# http://docs.gurock.com/testrail-api2/start
# http://docs.gurock.com/testrail-api2/accessing
#
# Copyright Gurock Software GmbH. See license.md for details.
#

import base64
import json
import urllib2


class APIClient:
    def __init__(self, base_url):
        self.user = ''
        self.password = ''
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'

    #
    # Send Get
    #
    # Issues a GET request (read) against the API and returns the result
    # (as Python dict).
    #
    # Arguments:
    #
    # uri                 The API method to call including parameters
    #                     (e.g. get_case/1)
    #
    def send_get(self, uri):
        return self.__send_request('GET', uri, None)

    #
    # Send POST
    #
    # Issues a POST request (write) against the API and returns the result
    # (as Python dict).
    #
    # Arguments:
    #
    # uri                 The API method to call including parameters
    #                     (e.g. add_case/1)
    # data                The data to submit as part of the request (as
    #                     Python dict, strings must be UTF-8 encoded)
    #
    def send_post(self, uri, data):
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri
        request = urllib2.Request(url)
        if method == 'POST':
            request.add_data(json.dumps(data))
        auth = base64.b64encode('%s:%s' % (self.user, self.password))
        request.add_header('Authorization', 'Basic %s' % auth)
        request.add_header('Content-Type', 'application/json')

        e = None
        try:
            response = urllib2.urlopen(request).read()
        except urllib2.HTTPError as e:
            response = e.read()

        if response:
            result = json.loads(response)
        else:
            result = {}

        if e != None:
            if result and 'error' in result:
                error = '"' + result['error'] + '"'
            else:
                error = 'No additional error message received'
            raise APIError('TestRail API returned HTTP %s (%s)' %
                           (e.code, error))

        return result


class APIError(Exception):
    pass


class TestRailAPICalls(object):
    def __init__(self, url, user, password):
        self.client = APIClient(base_url=url)
        self.client.user = user
        self.client.password = password

    # API: Cases

    def get_case(self, case_id):
        uri = 'get_case/{case_id}'.format(case_id=case_id)
        return self.client.send_get(uri)

    def get_cases(self, project_id, suite_id=None, section_id=None):
        uri = 'get_cases/{project_id}'.format(project_id=project_id)
        if suite_id:
            uri += '&suite_id={suite_id}'.format(suite_id=suite_id)
        if section_id:
            uri += '&section_id={section_id}'.format(section_id=section_id)
        return self.client.send_get(uri)

    def add_case(self, section_id, data):
        uri = 'add_case/{section_id}'.format(section_id=section_id)
        return self.client.send_post(uri, data)

    def update_case(self, case_id, data):
        uri = 'update_case/{case_id}'.format(case_id=case_id)
        return self.client.send_post(uri, data)

    def delete_case(self, case_id):
        uri = 'delete_case/{case_id}'.format(case_id=case_id)
        return self.client.send_post(uri, None)

    # API: Case Fields

    def get_case_fields(self):
        uri = 'get_case_fields'
        return self.client.send_get(uri)

    # API: Case Types

    def get_case_types(self):
        uri = 'get_case_types'
        return self.client.send_get(uri)

    # API: Configurations

    def get_configs(self, project_id):
        uri = 'get_configs/{project_id}'.format(project_id=project_id)
        return self.client.send_get(uri)

    def add_config_group(self, project_id, data):
        uri = 'add_config_group/{project_id}'.format(project_id=project_id)
        return self.client.send_post(uri, data)

    def add_config(self, config_group_id, data):
        uri = 'add_config/{config_group_id}'.format(
            config_group_id=config_group_id)
        return self.client.send_post(uri, data)

    def update_config_group(self, config_group_id, data):
        uri = 'update_config_group/{config_group_id}'.format(
            config_group_id=config_group_id)
        return self.client.send_post(uri, data)

    def update_config(self, config_id, data):
        uri = 'update_config/{config_id}'.format(config_id=config_id)
        return self.client.send_post(uri, data)

    def delete_config_group(self, config_group_id):
        uri = 'delete_config_group/{config_group_id}'.format(
            config_group_id=config_group_id)
        return self.client.send_post(uri, None)

    def delete_config(self, config_id):
        uri = 'delete_config/{config_id}'.format(config_id=config_id)
        return self.client.send_post(uri, None)

    # API: Milestones

    def get_milestone(self, milestone_id):
        uri = 'get_milestone/{milestone_id}'.format(milestone_id=milestone_id)
        return self.client.send_get(uri)

    def get_milestones(self, project_id, filter=None):
        uri = 'get_milestones/{project_id}'.format(project_id=project_id)
        if filter is not None:
            uri += '{}'.format(filter)
        return self.client.send_get(uri)

    def add_milestone(self, project_id, data):
        uri = 'add_milestone/{project_id}'.format(project_id=project_id)
        return self.client.send_post(uri, data)

    def update_milestone(self, milestone_id, data):
        uri = 'update_milestone/{milestone_id}'.format(
            milestone_id=milestone_id)
        return self.client.send_post(uri, data)

    def delete_milestone(self, milestone_id):
        uri = 'delete_milestone/{milestone_id}'.format(
            milestone_id=milestone_id)
        return self.client.send_post(uri, None)

    # API: Plans

    def get_plan(self, plan_id):
        uri = 'get_plan/{plan_id}'.format(plan_id=plan_id)
        return self.client.send_get(uri)

    def get_plans(self, project_id, filter=None):
        uri = 'get_plans/{project_id}'.format(project_id=project_id)
        if filter is not None:
            uri += '{}'.format(filter)
        return self.client.send_get(uri)

    def add_plan(self, project_id, data):
        uri = 'add_plan/{project_id}'.format(project_id=project_id)
        return self.client.send_post(uri, data)

    def add_plan_entry(self, plan_id, data):
        uri = 'add_plan_entry/{plan_id}'.format(plan_id=plan_id)
        return self.client.send_post(uri, data)

    def update_plan(self, plan_id, data):
        uri = 'update_plan/{plan_id}'.format(plan_id=plan_id)
        return self.client.send_post(uri, data)

    def update_plan_entry(self, plan_id, entry_id, data):
        uri = 'update_plan_entry/{plan_id}/{entry_id}'.format(
            plan_id=plan_id, entry_id=entry_id)
        return self.client.send_post(uri, data)

    def close_plan(self, plan_id):
        uri = 'close_plan/{plan_id}'.format(plan_id=plan_id)
        return self.client.send_post(uri, None)

    def delete_plan(self, plan_id):
        uri = 'delete_plan/{plan_id}'.format(plan_id=plan_id)
        return self.client.send_post(uri, None)

    def delete_plan_entry(self, plan_id, entry_id):
        uri = 'delete_plan_entry/{plan_id}/{entry_id}'.format(
            plan_id=plan_id, entry_id=entry_id)
        return self.client.send_post(uri, None)

    # API: Priorities

    def get_priorities(self):
        uri = 'get_priorities'
        return self.client.send_get(uri)

    # API: Projects

    def get_project(self, project_id):
        uri = 'get_project/{project_id}'.format(project_id=project_id)
        return self.client.send_get(uri)

    def get_projects(self):
        uri = 'get_projects'
        return self.client.send_get(uri)

    def add_project(self, data):
        uri = 'add_project'
        return self.client.send_post(uri, data)

    def update_project(self, project_id, data):
        uri = 'update_project/{project_id}'.format(project_id=project_id)
        return self.client.send_post(uri, data)

    def delete_project(self, project_id):
        uri = 'delete_project/{project_id}'.format(project_id=project_id)
        return self.client.send_post(uri, None)

    # API: Results

    def get_results(self, test_id, filter=None):
        uri = 'get_results/{test_id}'.format(test_id=test_id)
        if filter is not None:
            uri += '{}'.format(filter)
        return self.client.send_get(uri)

    def get_results_for_case(self, run_id, case_id, filter=None):
        uri = 'get_results_for_case/{run_id}/{case_id}'.format(run_id=run_id,
                                                               case_id=case_id)
        if filter is not None:
            uri += '{}'.format(filter)
        return self.client.send_get(uri)

    def get_results_for_run(self, run_id, filter=None):
        uri = 'get_results_for_run/{run_id}'.format(run_id=run_id)
        if filter is not None:
            uri += '{}'.format(filter)
        return self.client.send_get(uri)

    def add_result(self, test_id, data):
        uri = 'add_result/{test_id}'.format(test_id=test_id)
        return self.client.send_post(uri, data)

    def add_result_for_case(self, run_id, case_id, data):
        uri = 'add_result_for_case/{run_id}/{case_id}'.format(run_id=run_id,
                                                              case_id=case_id)
        return self.client.send_post(uri, data)

    def add_results(self, run_id, data):
        uri = 'add_results/{run_id}'.format(run_id=run_id)
        return self.client.send_post(uri, data)

    def add_results_for_cases(self, run_id, data):
        uri = 'add_results_for_cases/{run_id}'.format(run_id=run_id)
        return self.client.send_post(uri, data)

    # API: Result Fields

    def get_result_fields(self):
        uri = 'get_result_fields'
        return self.client.send_get(uri)

    # API: Runs

    def get_run(self, run_id):
        uri = 'get_run/{run_id}'.format(run_id=run_id)
        return self.client.send_get(uri)

    def get_runs(self, project_id, filter=None):
        uri = 'get_runs/{project_id}'.format(project_id=project_id)
        if filter is not None:
            uri += '{}'.format(filter)
        return self.client.send_get(uri)

    def add_run(self, project_id, data):
        uri = 'add_run/{project_id}'.format(project_id=project_id)
        return self.client.send_post(uri, data)

    def update_run(self, run_id, data):
        uri = 'update_run/{run_id}'.format(run_id=run_id)
        return self.client.send_post(uri, data)

    def close_run(self, run_id):
        uri = 'close_run/{run_id}'.format(run_id=run_id)
        return self.client.send_post(uri, None)

    def delete_run(self, run_id):
        uri = 'delete_run/{run_id}'.format(run_id=run_id)
        return self.client.send_post(uri, None)

    # API: Sections

    def get_section(self, section_id):
        uri = 'get_section/{section_id}'.format(section_id=section_id)
        return self.client.send_get(uri)

    def get_sections(self, project_id, suite_id):
        uri = 'get_sections/{project_id}&suite_id={suite_id}'.format(
            project_id=project_id, suite_id=suite_id)
        return self.client.send_get(uri)

    def add_section(self, project_id, data):
        uri = 'add_section/{project_id}'.format(project_id=project_id)
        return self.client.send_post(uri, data)

    def update_section(self, section_id, data):
        uri = 'update_section/{section_id}'.format(section_id=section_id)
        return self.client.send_post(uri, data)

    def delete_section(self, section_id):
        uri = 'delete_section/{section_id}'.format(section_id=section_id)
        return self.client.send_post(uri, None)

    # API: Statuses

    def get_statuses(self):
        uri = 'get_statuses'
        return self.client.send_get(uri)

    # API: Suites

    def get_suite(self, suite_id):
        uri = 'get_suite/{suite_id}'.format(suite_id=suite_id)
        return self.client.send_get(uri)

    def get_suites(self, project_id):
        uri = 'get_suites/{project_id}'.format(project_id=project_id)
        return self.client.send_get(uri)

    def add_suite(self, project_id, data):
        uri = 'add_suite/{project_id}'.format(project_id=project_id)
        return self.client.send_post(uri, data)

    def update_suite(self, suite_id, data):
        uri = 'update_suite/{suite_id}'.format(suite_id=suite_id)
        return self.client.send_post(uri, data)

    def delete_suite(self, suite_id):
        uri = 'delete_section/{suite_id}'.format(suite_id=suite_id)
        return self.client.send_post(uri, None)

    # API: Template

    def get_templates(self, project_id):
        uri = 'get_templates/{project_id}'.format(project_id=project_id)
        return self.client.send_get(uri)

    # API: Tests

    def get_test(self, test_id):
        uri = 'get_test/{test_id}'.format(test_id=test_id)
        return self.client.send_get(uri)

    def get_tests(self, run_id, filter=None):
        uri = 'get_tests/{run_id}'.format(run_id=run_id)
        if filter is not None:
            uri += '{}'.format(filter)
        return self.client.send_get(uri)

    # API: Users

    def get_user(self, user_id):
        uri = 'get_user/{user_id}'.format(user_id=user_id)
        return self.client.send_get(uri)

    def get_user_by_email(self, email):
        uri = 'get_user_by_email&email={email}'.format(email=email)
        return self.client.send_get(uri)

    def get_users(self):
        uri = 'get_users'
        return self.client.send_get(uri)
