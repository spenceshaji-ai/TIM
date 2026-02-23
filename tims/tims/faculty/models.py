from django.db import models
from tims.users.models import User
from adminapp.models import Course, Batch


class FacultyCourseMaterial(models.Model):
    MATERIAL_TYPE = (
        ("pdf", "PDF"),
        ("image", "Image"),
        ("video", "Video"),
    )

    faculty = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role__role_name": "faculty"},
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    material_type = models.CharField(
        max_length=10,
        choices=MATERIAL_TYPE
    )

    pdf_file = models.FileField(
        upload_to="faculty/materials/pdfs/",
        blank=True,
        null=True
    )
    image_file = models.ImageField(
        upload_to="faculty/materials/images/",
        blank=True,
        null=True
    )
    video_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course} ({self.batch})"
