from django.db import models


class Student(models.Model):

    class Sex(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    class CivilStatus(models.TextChoices):
        SINGLE = "S", "Single"
        MARRIED = "M", "Married"

    class EnrollmentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        ENROLLED = "enrolled", "Enrolled"
        DROPPED = "dropped", "Dropped"
        GRADUATED = "graduated", "Graduated"

    student_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=Sex.choices)
    civil_status = models.CharField(
        max_length=1, choices=CivilStatus.choices, default=CivilStatus.SINGLE
    )
    nationality = models.CharField(max_length=50, default="Filipino")

    # --- Contact Info ---
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    barangay = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)

    # --- Enrollment Info ---
    course = models.CharField(max_length=150)
    year_level = models.PositiveSmallIntegerField(default=1)
    section = models.CharField(max_length=20, blank=True)
    school_year = models.CharField(max_length=9, help_text="e.g. 2026-2027")
    semester = models.CharField(max_length=20, blank=True)
    status = models.CharField(
        max_length=20,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.PENDING,
    )
    date_enrolled = models.DateField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.student_number} - {self.full_name}"

    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name, self.suffix]
        return " ".join(p for p in parts if p)


class BackgroundInfo(models.Model):

    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, related_name="background"
    )

    # Father
    father_name = models.CharField(max_length=150, blank=True)
    father_occupation = models.CharField(max_length=100, blank=True)

    # Mother
    mother_name = models.CharField(max_length=150, blank=True)
    mother_maiden_name = models.CharField(max_length=150, blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Background of {self.student.full_name}"