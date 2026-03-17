from common_code.config import get_settings
from common_code.logger.logger import get_logger, Logger
from common_code.service.models import Service
from common_code.service.enums import ServiceStatus
from common_code.common.enums import FieldDescriptionType, ExecutionUnitTagName, ExecutionUnitTagAcronym
from common_code.common.models import FieldDescription, ExecutionUnitTag
from common_code.tasks.models import TaskData
# Imports required by the service's model
import io
from PIL import Image

api_description = """
This service converts an image to greyscale.
"""
api_summary = """
Converts an image to greyscale.
"""

api_title = "Image Greyscale API."
version = "1.0.0"

settings = get_settings()


class MyService(Service):
    """
    Image greyscale model
    """

    # Any additional fields must be excluded for Pydantic to work
    _model: object
    _logger: Logger

    def __init__(self):
        super().__init__(
            name="Image Greyscale",
            slug="image-greyscale",
            url=settings.service_url,
            summary=api_summary,
            description=api_description,
            status=ServiceStatus.AVAILABLE,
            data_in_fields=[
                FieldDescription(name="image", type=[FieldDescriptionType.IMAGE_PNG, FieldDescriptionType.IMAGE_JPEG]),
            ],
            data_out_fields=[
                FieldDescription(name="result", type=[FieldDescriptionType.IMAGE_PNG, FieldDescriptionType.IMAGE_JPEG]),
            ],
            tags=[
                ExecutionUnitTag(
                    name=ExecutionUnitTagName.IMAGE_PROCESSING,
                    acronym=ExecutionUnitTagAcronym.IMAGE_PROCESSING
                ),
            ],
            has_ai=False,
            docs_url="https://docs.swiss-ai-center.ch/reference/services/image-greyscale/",
        )
        self._logger = get_logger(settings)

    def process(self, data):
        raw = data["image"].data
        input_type = data["image"].type
        stream = io.BytesIO(raw)
        img = Image.open(stream)

        img = img.convert("L")
        out_buff = io.BytesIO()
        img.save(out_buff, format=input_type.split("/")[1], quality=95)
        out_buff.seek(0)
        return {
            "result": TaskData(
                data=out_buff.read(),
                type=input_type
            )
        }
