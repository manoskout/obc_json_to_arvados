import os
import sys
import ruamel.yaml as yaml


class ExecutorException(Exception):
    pass


def convert_to_yaml(wf_file):
    return yaml.dump(wf_file, sys.stdout)


class CWLExecutor():
    def __init__(self, workflow, workflow_directory=None):
        self.workflow = workflow
        self.workflow_directory = workflow_directory
        self.wf_global_envs = self.workflow.global_env_var()
        # if not os.path.exists(self.workflow):
        # os.makedir(self.workflow_directory)

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

    def build(self,):
        for index, (
                step,
                dep,
                step_type
        ) in enumerate(self.workflow.get_step_generator()):
        	
            print(index)
            # print(f"Step: {step} \tType: {step_type}\tDependencies: {dep}")
