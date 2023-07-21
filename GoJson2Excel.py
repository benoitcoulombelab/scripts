import argparse
import pathlib
import os
import json


def is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


parser = argparse.ArgumentParser(description='Convert GO Enrichment Analysis JSON output to a tab delimited file.')
parser.add_argument('json', type=lambda x: is_valid_file(parser, x),
                    help='GO Enrichment Analysis JSON file')
parser.add_argument('tsv', type=pathlib.Path, default='go.tsv',
                    help='Tab delimited output file')

args = parser.parse_args()

with open(args.json) as go_json_in, open(args.tsv, 'w') as tsv_out:
    go_json = json.load(go_json_in)
    overrepresentation = go_json['overrepresentation']

    tsv_out.write('Analysis type:\tPANTHER Overrepresentation Test (Released {})\n'.format(overrepresentation['tool_release_date']))
    tsv_out.write('Annotation Version and Release Date:\t{}\n'.format(overrepresentation['data_version_release_date']))
    upload_lists = overrepresentation['upload_lists']['input_list']
    tsv_out.write('Analyzed List:\t{}\n'.format(upload_lists['list_name']))
    tsv_out.write('Reference List:\t{}\n'.format(upload_lists['organism']))
    tsv_out.write('Test Type:\t{}\n'.format(overrepresentation['test_type']))
    tsv_out.write('Correction:\t{}\n'.format(overrepresentation['correction']))
    tsv_out.write('\n')
    groups = overrepresentation['group']
    tsv_out.write('GO molecular function complete\tLevel\tNumber in reference\tNumber in list\tExpected\tOver/Under\tFold enrichment\tRaw pValue\tFDR\tGenes\n')

    if type(groups) is not list:
        groups = [groups]
    group_index = -1
    for group in groups:
        group_index = group_index + 1
        results = group['result']
        if type(results) is not list:
            results = [results]
        result_index = -1
        for result in results:
            result_index = result_index + 1
            error = False
            if 'term' not in result:
                print('term element not in group {}, result {}'.format(group_index, result_index))
                error = True
            if 'input_list' not in result:
                print('input_list element not in group {}, result {}'.format(group_index, result_index))
                error = True
            if error:
                continue
            term = result['term']
            input_list = result['input_list']
            number_in_list = input_list['number_in_list']
            tsv_out.write('{} ({})'.format(term['label'], term['id']))
            tsv_out.write('\t')
            tsv_out.write('{}'.format(term['level']))
            tsv_out.write('\t')
            tsv_out.write('{}'.format(result['number_in_reference']))
            tsv_out.write('\t')
            tsv_out.write('{}'.format(number_in_list))
            tsv_out.write('\t')
            tsv_out.write('{}'.format(input_list['expected']))
            tsv_out.write('\t')
            tsv_out.write('{}'.format(input_list['plus_minus']))
            tsv_out.write('\t')
            tsv_out.write('{}'.format(input_list['fold_enrichment']))
            tsv_out.write('\t')
            tsv_out.write('{}'.format(input_list['pValue']))
            tsv_out.write('\t')
            tsv_out.write('{}'.format(input_list['fdr']))
            tsv_out.write('\t')
            tsv_out.write(';'.join(input_list['mapped_id_list']['mapped_id']) if number_in_list > 0 else '')
            tsv_out.write('\n')
