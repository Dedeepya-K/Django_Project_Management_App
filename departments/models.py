from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
import os

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

def save_domain_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.domain_id:
        filename = 'Domain_Pictures/{}.{}'.format(instance.domain_id, ext)
    return os.path.join(upload_to, filename)

class Domain(models.Model):
    domain_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='domains')
    image = models.ImageField(upload_to=save_domain_image, blank=True, verbose_name='Domain Image')
    description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.domain_id)
        super().save(*args, **kwargs)


def save_project_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.project_id:
        filename = 'project_files/{}/{}.{}'.format(instance.project_id,instance.project_id, ext)
        if os.path.exists(filename):
            new_name = str(instance.project_id) + str('1')
            filename =  'project_images/{}/{}.{}'.format(instance.project_id,new_name, ext)
    return os.path.join(upload_to, filename)

class Project(models.Model):
    project_id = models.CharField(max_length=100, unique=True)
    Branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE,related_name='projects')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Batch no.")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=save_project_files,verbose_name="Video", blank=True, null=True)
    ppt = models.FileField(upload_to=save_project_files,verbose_name="Presentations", blank=True)
    Other_Details = models.FileField(upload_to=save_project_files,verbose_name="Other_Details", blank=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('departments:project_list', kwargs={'slug':self.domain.slug, 'branch':self.Branch.slug})
"""
class WorkingDays(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,related_name='branch_days')
    day = models.CharField(max_length=100)
    def __str__(self):
        return self.day

class TimeSlots(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,related_name='branch_time_slots')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.start_time) + ' - ' + str(self.end_time) 

class SlotDomain(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,related_name='branch_slots')
    day = models.ForeignKey(WorkingDays, on_delete=models.CASCADE,related_name='branch_slots_days')
    slot = models.ForeignKey(TimeSlots, on_delete=models.CASCADE,related_name='branch_slots_time')
    slot_domain = models.ForeignKey(Domain, on_delete=models.CASCADE,related_name='branch_slots_domain')

    def __str__(self):
        return str(self.branch)+ ' - ' + str(self.day) + ' - ' + str(self.slot) + ' - ' + str(self.slot_domain)
"""
class Comment(models.Model):
    project_name = models.ForeignKey(Project,null=True, on_delete=models.CASCADE,related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)
    # reply = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)
