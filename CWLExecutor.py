import os
import sys
import ruamel.yaml as yaml
# Inline list
from ruamel.yaml.comments import CommentedSeq, CommentedMap
# For the quotes in inline list
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as dq


class ExecutorException(Exception):
    pass


def convert_to_yaml(wf_file):
    return yaml.dump(wf_file, sys.stdout)


class CWLExecutor():
    def __init__(self, workflow, workflow_directory=None):
        self.workflow = workflow
        self.workflow_directory = workflow_directory
        self.wf_global_envs = self.workflow.global_env_var()

    def wf_template(self,):
        template= {}
        template["cwlVersion"]="v1.0"
        template["class"]="Workflow"
        template["inputs"]={
            "OBC_TOOL_PATH": ("string"),
            "OBC_DATA_PATH": ("string"),
            "OBC_WORK_PATH": ("string"),
        }
        # print(self.workflow.get_last_step())
        # Check about the final step... Should I add the word report ?
        template["outputs"]={
            "OBC_OUTPUT":{
                "type":"File",
                "outputSource": "{}/{}".format(self.workflow.get_last_step()[0],self.workflow.get_last_step()[0])
            }
        }
        # print(wf_steps)
        template["steps"]:{}
        
        # for step,dep,type in self.get_step_generator():
        # template["outputs"]
        
        return template
    # def cwl_workflow_builder(self,):
    #     workflow =

    def bash_step_creator():
        pass
    
    # def cs(*elements):
    #     res = CommentedSeq(*elements)
    #     res.fa.set_flow_style()
    #     return res

    def step_template(self, step_type, step_name):
        """
        I had a problem with the inline list. 
        Following the StackOverflow thread I partially solved it
        https://stackoverflow.com/questions/23716531/python-yaml-dump-format-list-in-other-yaml-format
        Another problem was the double quotes after the inline list creation
        https://stackoverflow.com/questions/60132660/how-to-set-list-with-strings-as-a-yaml-value-while-preserving-quotes
        """
        template = CommentedMap()
        template["class"]="CommandLineTool"
        template["cwlVersion"]="v1.0"
        template["baseCommand"]=cl =CommentedSeq([dq("bash"), dq(f"{step_name}.bash")])
        template["requirements"]={}
        template["requirements"]["InitialWorkDirRequirements"]={}
        template["requirements"]["EnvVarRequirements"]= {}
        if self.wf_global_envs:
            template["requirements"]["EnvVarRequirements"]["EnvDef"]= self.wf_global_envs
        else:
            template["requirements"]["EnvVarRequirements"]["EnvDef"]= {}

        
        template["requirements"]["inputs"] = {
            "OBC_TOOL_PATH":("string"),
            "OBC_DATA_PATH":("string"),
            "OBC_WORK_PATH":("string")
        }
        template["requirements"]["outputs"]={
            f"{step_name}":{
                "type":("stdout")
            }
        }
        # print(self.wf_global_envs)
        cl.fa.set_flow_style()
        return template
          
    def build(self,):
        if self.workflow.get_workflow_id():
            output_dir = os.getcwd()+f"/{self.workflow.get_workflow_id()}"
            try:
                os.mkdir(output_dir)
            except:
                print(f"The folder exists : {output_dir}")
        # print("Global Environment Variables: {}".format(self.workflow.global_env_var()))
        for index, (
                step,
                dep,
                step_type
        ) in enumerate(self.workflow.get_step_generator()):
            # print(f"Step: {step} \tType: {step_type}\tDependencies: {dep}")
            # if step == "INIT_STEP":
            # print(f"Step: {step} \tType: {step_type}\tDependencies: {dep}")
            # print("INIT STEP template: {}".format(self.step_template(step_type, step)))

            with open(f"{output_dir}/{step}.cwl", "w") as file:
                bashfile = yaml.dump(self.step_template(step_type, step), file,Dumper=yaml.RoundTripDumper)
            with open(f"{output_dir}/{step}.bash", "w") as bash:
                bash.write(self.workflow.get_bash_commands(step))
                # print(self.workflow.get_bash_commands(step))
        print(self.wf_template())