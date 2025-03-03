from django.contrib import admin
from .models import Candidate, Skill, Experience, Education


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "user", "user__email")
    search_fields = ("first_name", "last_name", "user__email")
    list_filter = ("skills",)
    inlines = [ExperienceInline, EducationInline]
    filter_horizontal = ("skills",)


admin.site.register(Experience)
admin.site.register(Education)
