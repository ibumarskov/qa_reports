import copy
import xml.etree.ElementTree as ET
import yaml

from lib.reportparser import ReportParser


class TempestXMLParser(ReportParser):

    def __init__(self, xmlfile, tr_case_attrs='etc/tr_case_attrs.yaml',
                 tr_result_attrs='etc/tr_result_attrs.yaml',
                 tr_case_map='etc/maps/tempest/tr_case.yaml',
                 tr_result_map='etc/maps/tempest/tr_result.yaml',
                 sections_map='etc/maps/tempest/sections.yaml'):
        super(TempestXMLParser, self).__init__(tr_case_attrs=tr_case_attrs,
                                               tr_result_attrs=tr_result_attrs)
        with open(tr_case_map, 'r') as stream:
            self.tr_case_map = yaml.safe_load(stream)
        with open(tr_result_map, 'r') as stream:
            self.tr_result_map = yaml.safe_load(stream)
        with open(sections_map, 'r') as stream:
            self.sections_map = yaml.safe_load(stream)

        tree = ET.parse(xmlfile)
        root = tree.getroot()

        for child in root:
            if child.tag != 'testcase':
                continue
            tc_res = self.parse_tc_results_attr(child)
            if 'setUpClass' in tc_res['title']:
                self.set_test_group(tc_res)
                self.result_list_setUpClass.append(tc_res)
                continue
            elif 'tearDownClass' in tc_res['title']:
                # TO DO: add action for failed tearDownClass
                continue
            else:
                self.result_list.append(tc_res)
            tc = self.parse_tc_attr(child.attrib)
            section = self.choose_section_by_test_name(tc['title'])
            pos = self.get_section_position(section)
            self.suite_list[pos]['test_cases'].append(tc)

    @staticmethod
    def set_test_group(tc_res):
        gr = tc_res['title']
        remove_str = ['setUpClass', ' ', '(', ')']
        for s in remove_str:
            gr = gr.replace(s, '', 1)
        tc_res['group'] = gr

    def get_section_position(self, name):
        for i, suite in enumerate(self.suite_list):
            if name == self.suite_list[i]['section_name']:
                return i
        self.suite_list.append({'section_name': name, 'test_cases': []})
        return self.get_section_position(name)

    def choose_section_by_test_name(self, tc_name):
        for section, key_words in self.sections_map.items():
            for key_word in key_words:
                if key_word in tc_name:
                    return section
        return 'None'

    def parse_tc_attr(self, attributes):
        tc = copy.copy(self.tr_case_attrs)
        for tr_attr, xml_map_tags in self.tr_case_map.iteritems():
            for xml_attr, xml_attr_val in attributes.iteritems():
                if xml_attr in xml_map_tags:
                    if tc[tr_attr] != "":
                        tc[tr_attr] = tc[tr_attr] + '.' + xml_attr_val
                    else:
                        if tr_attr == 'estimate':
                            # TO DO - fix bug TestRail API returned HTTP 400
                            # ("Field :estimate is not in a valid time span
                            # format.")
                            continue
                            tc[tr_attr] = xml_attr_val+'s'
                        else:
                            tc[tr_attr] = xml_attr_val
        return tc

    def parse_tc_results_attr(self, child):
        result_attr_map = {
            'classname': ['title'],
            'name': ['title']
        }

        res = {
            "title": '',
            "status": 'passed',
            "comment": ''
        }

        for key, value in child.attrib.iteritems():
            if key in result_attr_map.keys():
                item = result_attr_map[key]
                for attr in item:
                    if res[attr] != "":
                        res[attr] = res[attr] + '.' + value
                    else:
                        res[attr] = value
        for obj in child:
            if obj.tag:
                res['status'] = obj.tag
                res['comment'] = obj.text
        return res
