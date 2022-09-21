from importlib.util import module_for_loader
from pypyr import pipelinerunner
import json
import omegaconf

class Action:
    def __init__(self, pipeline: omegaconf.dictconfig.DictConfig, args: dict, model: dict) -> None:
        self.__pipeline = json.dumps(omegaconf.OmegaConf.to_container(pipeline))
        self.__args = args
        self.__args['model'] = omegaconf.OmegaConf.to_container(model)

    def run(self):
        context = pipelinerunner.run(
            pipeline_name=self.__pipeline,
            dict_in=self.__args,
            loader='src.libs.pypyr_loader'
            )
        return context['response_code'], context['response_text']