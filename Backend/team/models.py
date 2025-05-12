from django.db import models
from django.conf import settings

class TeamMember(models.Model):
    ROLE_CHOICES = (
        ('instructor', 'Instructor'),
        ('project_manager', 'Project Manager'),
        ('content_creator', 'Content Creator'),
        ('reviewer', 'Reviewer'),
        ('editor', 'Editor'),
        ('ceo', 'CEO'),
        ('social_media_manager', 'Social Media Manager'),
        ('hr_manager', 'HR Manager'),
        ('marketing_head', 'Marketing Head'),
        ('sales_head', 'Sales Head'),
        ('finance_head', 'Finance Head'),
    )

    WORKING_STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
        ('resigned', 'Resigned'),
    )

    WORK_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    working_status = models.CharField(max_length=50, choices=WORKING_STATUS_CHOICES, default='active')
    work_type = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='team_members/profile_images/%Y/%m/%d/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.role} - {self.work_type}"


    class Meta:
        db_table = 'team_member'
        verbose_name_plural = 'Team Members'
        ordering = ['-created_at']