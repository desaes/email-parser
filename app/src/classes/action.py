from importlib.util import module_for_loader
from pypyr import pipelinerunner
import json

class Action:
    def __init__(self, pipeline: dict, args: dict, model: dict) -> None:
        self.__pipeline = json.dumps(pipeline)
        self.__args = args
        self.__args['model'] = model

    def run(self):
        context = pipelinerunner.run(
            pipeline_name=self.__pipeline,
            dict_in=self.__args,
            loader='src.libs.pypyr_loader'
            )
        return context['response_code'], context['response_text']