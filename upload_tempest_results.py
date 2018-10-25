import argparse
import logging
import os

from lib.testrailproject import TestRailProject
from lib.tempestparser import TempestXMLParser
from lib.testrailreporter import TestRailReporter

LOGS_DIR = os.environ.get('LOGS_DIR', os.getcwd())
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    filename=os.path.join(LOGS_DIR, 'log/upload_test_plan.log')
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
console.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Upload tests cases to TestRail.')
    parser.add_argument('report_path', metavar='Tempest report', type=str,
                        help='Path to tempest report (.xml)')
    parser.add_argument('-p', dest='project_name', default=None,
                      help='Testrail project name.')
    parser.add_argument('-s', dest='suite_name', default=None,
                      help='Testrail suite name.')
    parser.add_argument('-m', dest='milestone', default=None,
                      help='Testrail milestone.')
    parser.add_argument('-d', action="store_true", dest='dry', default=False,
                      help='Dry run mode. Only show what would be changed and'
                           ' do nothing.')

    return parser.parse_args()

def main():
    args = parse_arguments()

    url = os.environ.get('TESTRAIL_URL')
    user = os.environ.get('TESTRAIL_USER')
    password = os.environ.get('TESTRAIL_PASSWORD')

    logger.info('URL: "{0}"'.format(url))
    logger.info('User: "{0}"'.format(user))
    logger.info('Tempest report file: "{0}"'.format(args.report_path))
    logger.info('Testrail project name: "{0}"'.format(args.project_name))
    logger.info('Testrail suite name: "{0}"'.format(args.suite_name))
    logger.info('Milestone: "{0}"'.format(args.milestone))

    report_obj = TempestXMLParser(args.report_path)
    project = TestRailProject(url=url,
                              user=user,
                              password=password,
                              project_name=args.project_name)
    reporter_obj = TestRailReporter(project, report_obj)
    reporter_obj.update_test_suite(args.suite_name)
    # reporter_obj.report_test_plan('[MCP-Q3] Contrail 4.0 2018.10.12',
    #                               'Tempest 18.0.0', 'Tempest smoke',
    #                               update_existing=True)

if __name__ == "__main__":
    main()