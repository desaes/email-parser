from pypyr import pipelinerunner
import os

class Action:
    def __init__(self, id: str, parameters: dict ) -> None:
        self.id = id
        self.parameters = parameters

    def run(self):
        context = pipelinerunner.run(pipeline_name=f'configs/action/{self.id}',dict_in=self.parameters[0])
        print(context)