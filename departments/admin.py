from django.contrib import admin
from departments.models import Branch, Domain, Project, Comment, Reply
# WorkingDays, TimeSlots, SlotDomain
# Register your models here.


admin.site.register(Branch)
admin.site.register(Domain)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Reply)
#admin.site.register(WorkingDays)
#admin.site.register(TimeSlots)
#admin.site.register(SlotDomain)
