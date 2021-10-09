from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Acc)
admin.site.register(models.PPU)
#admin.site.register(models.VnedPPU)
admin.site.register(models.Effect)
admin.site.register(models.Category)