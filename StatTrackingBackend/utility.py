from typing import Type

from rest_framework import serializers, validators
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
import random
import string


class SussySerializerBypass(serializers.ModelSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        # Horrible hack - In order to reuse all other validation logic in the model field, we need to
        # remove the Uniqueness validation.
        for field in self.fields.values():
            new_validators = filter(
                lambda validator: not isinstance(validator, (validators.UniqueValidator, validators.UniqueTogetherValidator)),
                field.validators
            )
            field.validators = new_validators


class LateThrottleAPIView(APIView):
    class Meta:
        abstract = True

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        self.perform_authentication(request)
        self.check_permissions(request)
        # self.check_throttles(request)


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


def generate_random_string(length: int, url_encodable: bool = False) -> str:
    pool = string.printable if url_encodable else string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for _ in range(length))


class MissingKeyException(Exception):
    pass


def check_required_keys(data: dict, required_keys: list[str]) -> bool:
    for key in required_keys:
        if key not in data: raise serializers.ValidationError(f"\"{key}\" is required")
    return