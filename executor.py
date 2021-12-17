import argparse
import os
import json
import logging
import networkx as nx


logging.basicConfig(level=logging.DEBUG)


def log_info(message):
    '''
    '''
    logging.info(message)


def log_error(message):
    '''
    '''
    logging.error(message)


class JSON_CWLParserException(Exception):
    '''
    '''
    pass


def retrieve_workflow(workflow_file):
    '''
    Returns the JSON workflow
    '''
    try:
        wf = open(workflow_file)
        print("File exists")
        workflow = json.load(wf)
    except OSError:
        print("Could not open/read file: ", workflow_file)

    return workflow


class Workflow:
    '''
    The JSON file that contains the workflow 
    that have been created from the OpenBio platform
    '''

    def __init__(self, workflow_file=None, input_variables=None):
        workflow = retrieve_workflow(workflow_file)
        print(workflow)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='OBC Workflow parser'
    )

    parser.add_argument(
        '-W',
        '--workflow',
        dest='workflow_filename',
        help='JSON workflow file',
        required=True
    )
    # TODO : is not required for the first phase
    # This is the inputs that the cwl workflow needs
    # parser.add_argument(
    #     '-I',
    #     '--inputs',
    #     dest='input_file',
    #     help='CWL inputs file name',
    #     required=False
    # )
    parser.add_argument(
        '-O',
        '--output',
        dest='output',
        help="The output filename [Default : workflow.yaml]",
        default='workflow'
    )
    # Future work
    # parser.add_argument(
    # 	'-G',
    # 	'--graph',
    # 	dest='graph',
    # 	help="The graph of the workflow",
    # 	default='graph'
    # 	)

    args = parser.parse_args()

    print(f"The args that we get: {args}")

    workflow = Workflow(
        workflow_file=args.workflow_filename, input_variables=None)
