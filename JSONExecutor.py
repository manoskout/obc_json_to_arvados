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
    def __init__(self,)
        pass

    def yaml_workflow_builder(self, workflow_name, step_type):
        if step_type == "initial":
            return {
                "class": "CommandLineTool",
                "cwlVersion": "v1.0",
                "baseCommand": ["bash", "OBC_CWL_INIT.sh"]
                "requirements": {
                    "InitialWorkDirRequirement": {
                        "InlineJavascriptRequirement": {}
                        "EnvVarRequirements": {
                            "envDef": {
                                self.global_env_vars,
                            }
                        }
                    }
                },
                "inputs": self.inputs,
                "outputs": self.outputs

            }
  
