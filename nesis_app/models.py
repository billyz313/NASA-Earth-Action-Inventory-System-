from django.contrib.auth.models import User
from django.db import models
from PIL import Image

class Asset(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('retired', 'Retired'),
        ('planned', 'Planned'),
    ]

    CATEGORY_CHOICES = [
        ('satellite', 'Satellite'),
        ('sensor', 'Sensor'),
        ('mission', 'Mission'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    launch_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='assets/', default='default_asset.jpg')

    def save(self, *args, **kwargs):
        """Override save method to crop image to a common aspect ratio close to 25:14."""
        super().save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            # Define target aspect ratio
            target_ratio = 25 / 14
            width, height = img.size
            current_ratio = width / height

            if current_ratio > target_ratio:
                # Crop width
                new_width = int(height * target_ratio)
                left = (width - new_width) / 2
                right = left + new_width
                img = img.crop((left, 0, right, height))
            else:
                # Crop height
                new_height = int(width / target_ratio)
                top = (height - new_height) / 2
                bottom = top + new_height
                img = img.crop((0, top, width, bottom))

            img.save(img_path)  # Save the cropped image

class CRMUser(models.Model):
    """ Represents a manually added user (for interactions not tied to system users). """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Ensure this field exists

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''} - {self.email or 'No Email'}"

class CRMInteraction(models.Model):
    """ Tracks interactions that can be manually entered by an admin. """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="interactions")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    crm_user = models.ForeignKey(CRMUser, on_delete=models.SET_NULL, null=True, blank=True)  # Manually entered user
    interaction_type = models.CharField(max_length=50, choices=[
        ('Viewed', 'Viewed'),
        ('Downloaded', 'Downloaded'),
        ('Requested Info', 'Requested Info'),
        ('Commented', 'Commented'),
        ('Phone Call', 'Phone Call'),
        ('Meeting', 'Meeting'),
    ])
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user or self.crm_user.get_full_name} - {self.interaction_type} on {self.asset}"


class Application(models.Model):
    app_id = models.CharField(max_length=100, default="", help_text="Application ID")

    def __str__(self):
        return self.app_id


class Mission(models.Model):
    mission_id = models.CharField(max_length=100, default="", help_text="Mission ID")

    def __str__(self):
        return self.mission_id

class Role(models.Model):
    role_id = models.CharField(max_length=100, default="", help_text="Role ID")

    def __str__(self):
        return self.role_id


class Partner(models.Model):
    partner_id = models.CharField(max_length=100, default="", help_text="Partner ID")

    def __str__(self):
        return self.partner_id

class CustomerOrganization(models.Model):
    CHOICES = (
        ('CoDev', 'Co-development Partner'),
        ('Sci', 'Scientific Partner'),
        ('Tech', 'Technology Partner'),
        ('User', 'End User'),
        ('Other', 'Other')
    )
    COUNTRIES = (
        ('USA', 'USA'),
        ('CAN', 'Canada'),
        ('MEX', 'Mexico'),
        ('OTH', 'Other'),
    )
    org_id = models.CharField(max_length=100, default="", help_text="Organization ID")
    name = models.TextField(default="", help_text="Organization Name")
    acronym = models.CharField(max_length=200, default="", blank=True)
    country = models.CharField(max_length=10, default="Private", help_text="Access Level", choices=COUNTRIES)
    address = models.TextField()
    url = models.CharField(max_length=200, default="", blank=True)
    last_interaction_date = models.DateField()
    stakeholder_type = models.CharField(max_length=10, default="Private", help_text="Access Level", choices=CHOICES)
    value_for_nasa = models.TextField()
    downstream_partners = models.ManyToManyField(Partner)
    missions = models.ManyToManyField(Mission)
    role_for_mission = models.ManyToManyField(Role)
    applications_used = models.ManyToManyField(Application)
    role_per_application = models.TextField()
    point_of_contact = models.ManyToManyField(User)
    organization_needs = models.TextField()

    class Meta:
        verbose_name_plural = "Customer Organizations"

    def __str__(self):
        return self.name



