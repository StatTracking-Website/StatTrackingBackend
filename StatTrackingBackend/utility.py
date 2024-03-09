import os
import re
from io import BytesIO
from typing import Type
from uuid import uuid4

from PIL import Image, ImageSequence
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import ImageFieldFile
from django_resized.forms import ResizedImageFieldFile, ResizedImageField
from rest_framework import serializers, validators
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
import random
import string

from StatTrackingBackend import settings


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


def generate_random_string(length: int, url_encodable: bool = True) -> str:
    pool = string.ascii_letters + string.digits if url_encodable else string.printable
    return ''.join(random.choice(pool) for _ in range(length))


class MissingKeyException(Exception):
    pass


def check_required_keys(data: dict, required_keys: list[str]) -> bool:
    for key in required_keys:
        if key not in data: raise serializers.ValidationError(f"\"{key}\" is required")
    return


class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        new_name = self.unique_name(name)
        self.delete_matching_files(name)
        return super(OverwriteStorage, self)._save(new_name, content)

    def unique_name(self, name: string):
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        unique_suffix = uuid4().hex[:8]  # Generate a random 8-character hex string
        return os.path.join(dir_name, f"{file_root}_{unique_suffix}{file_ext}")

    def delete_matching_files(self, name):
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        pattern = re.compile(f"^{re.escape(file_root)}_[a-f0-9]{{8}}{re.escape(file_ext)}$")

        if self.exists(dir_name):
            for file in self.listdir(dir_name)[1]:  # [1] refers to the list of files in the directory
                if pattern.match(file):
                    self.delete(os.path.join(dir_name, file))

    def get_available_name(self, name, max_length=None):
        return name
