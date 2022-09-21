from pypyr.errors import PipelineNotFoundError
import pypyr.yaml
from typing import Any
import yaml
import json
import pypyr.pipelinerunner

"""
This is custom loader to pypyr. Note that pipeline_name receives the pipeline from the caller, not the path to the yaml file.
"""


def get_pipeline_definition(pipeline_name: str, parent: Any):
    return pypyr.yaml.get_pipeline_yaml(yaml.dump(json.loads(pipeline_name), allow_unicode=True, default_flow_style=False))