from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


class Media(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image",
        VIDEO = "video",
        AUDIO = "audio",
        FILE = "file",
        MUSIC = "music",

    type = models.CharField("type", max_length=50, choices=MediaType.choices)
    file = models.FileField(
        "file",
        upload_to="media_files",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["png", "jpg", "jpeg", "gif", "mp4", "mp3"]
            )
        ],
    )

    def clean(self):
        if self.type not in self.MediaType.values:
            raise ValidationError("Invalid File Type")
        elif self.type == self.MediaType.IMAGE:
            if self.file.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
                raise ValidationError("Invalid Image File")

    def __str__(self) -> str:
        return str(self.file)

    def __str__(self):
        return f"{self.get_type_display()}: {self.file.name}"

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"


