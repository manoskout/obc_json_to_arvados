import os
import sys
import ruamel.yaml as yaml



class ExecutorException(Exception):
    pass


class BaseExecutor():
    def __init__(self, workflow, global_env_vars, inputs, outputs):
        self.workflow = workflow
        self.global_env_vars = global_env_vars
        self.inputs = inputs
        self.outputs = outputs


def convert_to_yaml(workflow):
    return yaml.dump(workflow, sys.stdout)


class CWLExecutor(BaseExecutor):
    def __init__(self, workflow_directory):
        self.workflow_directory = workflow_directory
        if not os.path.exists(workflow):
            os.makedir(self.workflow_directory)

    def wf_template(self, obc_inputs, obc_outputs, outputs_path, wf_steps):
        return {
            "cwlVersion": "v1.0",
            "class": "Workflow",
            "inputs": {
                {obc_inputs}
            },
            "outputs": {
                f"{obc_outputs}": {
                    "type": "File",
                    "outputSource": f"{obc_outputs_path}"
                },
            },
            "steps": {
                wf_steps
            }
        }
    # def cwl_workflow_builder(self,):
    #     workflow =

    def best_step_creator():
        pass

    def step_template(self, workflow_name, step_type, step_name):
        if step_type == "initial":
            return {
                "class": "CommandLineTool",
                "cwlVersion": "v1.0",
                "baseCommand": ["bash", step_name],
                "requirements": {
                    "InitialWorkDirRequirement": {
                        "InlineJavascriptRequirement": {},
                        "EnvVarRequirements": {
                            "envDef": {
                                self.global_env_vars,
                                },
                        },
                    },
                },
                "inputs": self.inputs,
                "outputs": self.outputs

            }
        elif step_type == "tool_installation":
            return {
                "class": "CommandLineTool",
                "cwlVersion": "v1.0",
                "baseCommand": ["bash", step_name],
                "requirements": {
                    "InitialWorkDirRequirement": {
                        "InlineJavascriptRequirement": {},
                        "EnvVarRequirements": {
                            "envDef": {
                                self.global_env_vars,
                            },
                        },
                    },
                },
                "inputs": self.inputs,
                "outputs": self.outputs

            }
