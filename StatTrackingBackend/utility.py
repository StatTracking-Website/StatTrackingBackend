from typing import Type

from rest_framework.schemas.openapi import AutoSchema
from rest_framework.serializers import Serializer


class SchwurbelSchema(AutoSchema):

    def __init__(self, name: str, serializer: Type[Serializer] = None):
        self.overwritten_serializer = serializer
        AutoSchema.__init__(self, operation_id_base=name)

    def get_request_serializer(self, path, method):
        if self.overwritten_serializer: return self.overwritten_serializer()
        else: return AutoSchema.get_request_serializer(self, path, method)

    method_mapping = {
        'get': '',
        'post': '',
        'put': '',
        'patch': '',
        'delete': '',
    }