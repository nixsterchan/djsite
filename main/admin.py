from django.contrib import admin
# import your tutorial model
from .models import Tutorial, TutorialSeries, TutorialCategory
from tinymce.widgets import TinyMCE
from django.db import models
# Register your models here.

# When we register, we register tutorial with tutorial admin:
# And we can override and add fields under
class TutorialAdmin(admin.ModelAdmin):
  # fields = ["tutorial_title",
  #           "tutorial_published",
  #           "tutorial_content"]
  fieldsets = [
    ("Title/date", {"fields": ["tutorial_title", "tutorial_published"]}),
    ("URL", {"fields": ["tutorial_slug"]}),
    ("Series", {"fields": ["tutorial_series"]}),
    ("Content", {"fields": ["tutorial_content"]})
  ]

  # overrides the specific text field just for tutorial admin
  formfield_overrides = {
    models.TextField: {'widget': TinyMCE()}
  }

admin.site.register(TutorialSeries)
admin.site.register(TutorialCategory)
admin.site.register(Tutorial, TutorialAdmin)