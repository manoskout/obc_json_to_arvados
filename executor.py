import argparse
import os
import json
import logging
# import networkx as nx
from CWLExecutor import CWLExecutor


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
        # print("File exists")
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
        self.workflow = retrieve_workflow(workflow_file)
        self.parse_workflow()

    def global_env_var(self,):
        """
        The global environment variables should be exposed at each node
        Return the global environment variables
        """
        return self.workflow["environment_variables"]
    def get_workflow_id(self,):
        return self.workflow["environment_variables"]["OBC_NICE_ID"]
        
    def get_wf_info(self,):
        log_info("Workflow steps: ")
        log_info(self.wf_steps)
        log_info("Workflow dependencies: ")
        # for index, item in enumerate(self.step_dependencies):
        # if index == 1:
        # print(item)
        # bash = self.get_bash_commands(item[0])
        #     print("\n")
        # log_info(self.step_dependencies)

    def get_steps(self,):
        '''
        Return the steps of the workflow
        '''
        return self.workflow["steps"].keys()
    def get_bash_commands(self, step):
        """
        """
        return self.workflow[step]["bash"]
    def get_step_generator(self):
        """
        Return a dict that the key is the step that depends on its value.
        Also there are two more keys (main,final) that are the first and
        the final respectively
        """
        for step in self.wf_steps:
            yield (
                step,
                self.workflow["steps"][step]["run_after"],
                self.workflow["steps"][step]["type"]
            )
    def get_first_step(self,):
        for step in self.wf_steps:
            if self.workflow["steps"][step]["type"]=="initial":
                return (step,self.workflow["steps"][step]["run_after"],self.workflow["steps"][step]["type"])
    def get_last_step(self,):
        for step in self.wf_steps:
            if self.workflow["steps"][step]["type"]=="final":
                return (step,self.workflow["steps"][step]["run_after"],self.workflow["steps"][step]["type"])

    def get_bash_commands(self, step):
        """
        Returns the bash file of the selected step
        """
        # print(self.workflow["steps"][step]["bash"])
        return self.workflow["steps"][step]["bash"]

    def parse_workflow(self):
        '''
        Parse the workflow by identifying the steps, dependencies
        environment variables etc
        '''
        if self.workflow:
            self.wf_steps = self.get_steps()
            self.step_dependencies = self.get_step_generator()
        else:
            self.wf_steps = None
            self.step_dependencies = None
            raise JSON_CWLParserException(
                "The workflow does not exist. Workflow : {}"
                .format(self.workflow)
            )
        # self.get_wf_info()


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
    #   '-G',
    #   '--graph',
    #   dest='graph',
    #   help="The graph of the workflow",
    #   default='graph'
    #   )

    args = parser.parse_args()

    # print(f"The args that we get: {args}")

    workflow = Workflow(
        workflow_file=args.workflow_filename, input_variables=None)
    e = CWLExecutor(workflow)
    e.build()

